"""
Lab_AI/code_review.py — Headless Code Review Script for CI / Pre-Push Hook
Lab AI4: Reads code diff from stdin, calls Claude with forced tool_choice,
and exits non-zero if defects/regressions are detected.
"""

import os
import sys
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath("."))
load_dotenv()

REVIEW_TOOL_SCHEMA = {
    "name": "report_code_review_findings",
    "description": "Report structured findings from an automated pre-push code diff review.",
    "input_schema": {
        "type": "object",
        "properties": {
            "has_defects": {
                "type": "boolean",
                "description": "True if any defect, security risk, or hardcoded inference feature is detected."
            },
            "findings_count": {
                "type": "integer",
                "description": "Total number of defects found."
            },
            "defects": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "severity": {"type": "string", "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW"]},
                        "category": {"type": "string"},
                        "description": {"type": "string"},
                        "recommendation": {"type": "string"}
                    },
                    "required": ["severity", "category", "description", "recommendation"]
                }
            }
        },
        "required": ["has_defects", "findings_count", "defects"]
    }
}

def analyze_diff(diff_text: str) -> dict:
    if not diff_text.strip():
        return {"has_defects": False, "findings_count": 0, "defects": []}

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key and api_key != "your_claude_api_key_here":
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            prompt = f"""
You are an automated pre-push CI code auditor. Review this git diff for:
1. Secret leakage (.env, API keys, passwords)
2. Hardcoded inference feature placeholders (e.g. internet_service='Fiber optic' or auto_pay=0)
3. Unparameterized SQL or raw string formatting in queries
4. Syntax regressions

Git Diff to Review:
{diff_text}

Submit your structured report using report_code_review_findings.
"""
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                tools=[REVIEW_TOOL_SCHEMA],
                tool_choice={"type": "tool", "name": "report_code_review_findings"},
                messages=[{"role": "user", "content": prompt}]
            )
            for block in response.content:
                if block.type == "tool_use" and block.name == "report_code_review_findings":
                    return block.input
        except Exception:
            pass

    # Heuristic fallback analysis
    defects = []
    lower_diff = diff_text.lower()

    import re
    if "api_key" in lower_diff and ("=" in lower_diff or ":" in lower_diff) and "os.getenv" not in lower_diff:
        defects.append({
            "severity": "CRITICAL",
            "category": "Secret Leakage",
            "description": "Possible plaintext API_KEY assignment in diff.",
            "recommendation": "Use os.getenv() and keep secrets in .env."
        })

    if re.search(r"internet_service.*fiber\s*optic", lower_diff) or re.search(r"auto_pay_flag.*0", lower_diff):
        defects.append({
            "severity": "HIGH",
            "category": "Inference Feature Defect",
            "description": "Hardcoded feature placeholder reintroduced in inference code.",
            "recommendation": "Wire input to dynamic feature_columns.json schema."
        })

    return {
        "has_defects": len(defects) > 0,
        "findings_count": len(defects),
        "defects": defects
    }

def main():
    # Read from stdin if piped, else check recent git diff
    if not sys.stdin.isatty():
        diff_text = sys.stdin.read()
    else:
        # If run directly without pipe, check git diff
        import subprocess
        try:
            res = subprocess.run(["git", "diff", "HEAD~1"], capture_output=True, text=True)
            diff_text = res.stdout if res.returncode == 0 else ""
        except Exception:
            diff_text = ""

    print("=" * 60)
    print("RUNNING AUTOMATED PRE-PUSH CODE REVIEW")
    print("=" * 60)

    result = analyze_diff(diff_text)
    print(json.dumps(result, indent=2))

    if result.get("has_defects"):
        print("\n[REJECTED] Defects detected in code diff! Push aborted.")
        sys.exit(1)
    else:
        print("\n[APPROVED] Clean diff. Pre-push checks passed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
