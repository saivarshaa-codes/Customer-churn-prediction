"""
Lab_AI/install_git_hook.py — Pre-Push Git Hook Installer
Lab AI4: Configures .git/hooks/pre-push to automatically run Lab_AI/code_review.py
"""

import os
import sys

def install_hook():
    git_dir = ".git"
    if not os.path.exists(git_dir):
        print("Error: .git directory not found. Not a git repository.")
        return False

    hooks_dir = os.path.join(git_dir, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    hook_path = os.path.join(hooks_dir, "pre-push")

    hook_script = """#!/bin/sh
# Pre-push hook calling Claude AI code review
echo "Running automated pre-push code review via Lab_AI/code_review.py..."
git diff origin/main..HEAD | python Lab_AI/code_review.py
if [ $? -ne 0 ]; then
    echo "Push rejected due to defects detected by AI Code Reviewer."
    exit 1
fi
exit 0
"""
    with open(hook_path, "w", encoding="utf-8") as f:
        f.write(hook_script)

    print(f"Pre-push hook installed successfully at: {hook_path}")
    return True

if __name__ == "__main__":
    install_hook()
