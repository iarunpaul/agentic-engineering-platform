#!/usr/bin/env python3

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"

USES_PATTERN = re.compile(
    r"^\s*uses:\s*([^@\s]+)@([^\s#]+)"
)

FULL_SHA_PATTERN = re.compile(r"^[0-9a-fA-F]{40}$")


def main() -> int:
    errors: list[str] = []

    if not WORKFLOW_DIR.exists():
        print("No GitHub workflow directory found.")
        return 0

    workflow_files = sorted(
        list(WORKFLOW_DIR.glob("*.yml"))
        + list(WORKFLOW_DIR.glob("*.yaml"))
    )

    for workflow in workflow_files:
        lines = workflow.read_text(
            encoding="utf-8"
        ).splitlines()

        for line_number, line in enumerate(
            lines,
            start=1,
        ):
            match = USES_PATTERN.match(line)

            if not match:
                continue

            action, ref = match.groups()

            if action.startswith("./"):
                continue

            if not FULL_SHA_PATTERN.fullmatch(ref):
                errors.append(
                    f"{workflow.relative_to(ROOT)}:"
                    f"{line_number}: "
                    f"{action}@{ref} is not pinned "
                    "to a full 40-character commit SHA"
                )

    if errors:
        print("GitHub Action pinning validation failed:")

        for error in errors:
            print(f" - {error}")

        return 1

    print(
        "GitHub Action pinning validation passed "
        f"({len(workflow_files)} workflows checked)."
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
