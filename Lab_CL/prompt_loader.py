import os
import re
from dotenv import load_dotenv

load_dotenv()

# Shared Global Limits & Security Bounds
MAX_OUTPUT_TOKENS = 2048
MAX_HISTORY_TURNS = 8
MAX_PROMPT_CHARS = 16000

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")

class SecurityLeakageError(Exception):
    """Raised when an attempt is made to leak secrets from environment into a prompt."""
    pass

class ValidationError(Exception):
    """Raised when prompt template arguments fail validation checks."""
    pass

def _get_active_secrets() -> list[str]:
    """
    Extracts sensitive secret values from environment variables
    to prevent them from being interpolated into prompts.
    """
    sensitive_keys = [
        "API_KEY",
        "ANTHROPIC_API_KEY",
        "SECRET_KEY",
        "PASSWORD",
        "TOKEN",
        "DATABASE_URL",
    ]
    secrets = []
    for key, value in os.environ.items():
        if any(sk in key.upper() for sk in sensitive_keys):
            if value and len(value.strip()) > 3:
                secrets.append(value.strip())
    return list(set(secrets))

def sanitize_and_check_secrets(text: str, secrets: list[str]) -> None:
    """Checks whether the text contains any secret value."""
    for secret in secrets:
        if secret in text:
            raise SecurityLeakageError(
                f"SECURITY VIOLATION DETECTED: Prompt contains sensitive secret value from environment! Leakage prevented."
            )

def load_template(name: str, **kwargs) -> str:
    """
    Loads a versioned prompt template from Lab_CL/prompts/<name>.txt,
    validates arguments, enforces secret-leakage guards, and returns the filled prompt.
    """
    filename = f"{name}.txt" if not name.endswith(".txt") else name
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt template '{filename}' not found in {PROMPTS_DIR}")

    with open(filepath, "r", encoding="utf-8") as f:
        template_content = f.read()

    # 1. Argument validation: validate types and bounds
    for key, val in kwargs.items():
        if val is None:
            kwargs[key] = ""
        elif not isinstance(val, (str, int, float, bool, list, dict)):
            raise ValidationError(f"Invalid argument type for '{key}': {type(val).__name__}")
        elif isinstance(val, (list, dict)):
            kwargs[key] = str(val)

    # 2. Secret Leakage Pre-check on arguments
    secrets = _get_active_secrets()
    for key, val in kwargs.items():
        val_str = str(val)
        sanitize_and_check_secrets(val_str, secrets)

    # 3. Format Template
    try:
        rendered = template_content.format(**kwargs)
    except KeyError as e:
        raise ValidationError(f"Missing required template parameter: {e}")

    # 4. Secret Leakage Post-check on entire rendered prompt
    sanitize_and_check_secrets(rendered, secrets)

    # 5. Token / Length Budget Check
    if len(rendered) > MAX_PROMPT_CHARS:
        raise ValidationError(
            f"Rendered prompt exceeds maximum allowed character budget ({len(rendered)} > {MAX_PROMPT_CHARS})"
        )

    return rendered
