#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Execute a command and emit engineering control evidence."
    )

    parser.add_argument("--control-id", required=True)
    parser.add_argument("--tool", required=True)
    parser.add_argument("--summary-pass", required=True)
    parser.add_argument("--summary-fail", required=True)
    parser.add_argument(
        "--output-dir",
        default="evidence/generated",
    )

    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command to execute after --",
    )

    args = parser.parse_args()

    command = args.command

    if command and command[0] == "--":
        command = command[1:]

    if not command:
        print("No command supplied.", file=sys.stderr)
        return 2

    print(f"Executing control {args.control_id}")
    print(f"Command: {' '.join(command)}")

    result = subprocess.run(command, check=False)

    status = "PASS" if result.returncode == 0 else "FAIL"

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    sha = os.getenv("GITHUB_SHA", "local")
    repository = os.getenv("GITHUB_REPOSITORY")
    branch = os.getenv("GITHUB_REF_NAME")
    run_id = os.getenv("GITHUB_RUN_ID")

    evidence = {
        "controlId": args.control_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "subject": {
            "type": "commit",
            "value": sha,
        },
        "source": "ci" if os.getenv("GITHUB_ACTIONS") == "true" else "local",
        "tool": args.tool,
        "summary": (
            args.summary_pass
            if status == "PASS"
            else args.summary_fail
        ),
    }

    if repository:
        evidence["repository"] = repository

    if sha != "local":
        evidence["commit"] = sha

    if branch:
        evidence["branch"] = branch

    if run_id:
        evidence["runId"] = run_id

    output_file = output_dir / f"{args.control_id}.json"

    output_file.write_text(
        json.dumps(evidence, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Evidence written to {output_file}")
    print(f"{args.control_id}: {status}")

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())