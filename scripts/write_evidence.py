#!/usr/bin/env python3

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write engineering control evidence."
    )

    parser.add_argument("--control-id", required=True)
    parser.add_argument(
        "--status",
        required=True,
        choices=[
            "PASS",
            "FAIL",
            "WARN",
            "NOT_APPLICABLE",
            "NOT_EXECUTED",
        ],
    )
    parser.add_argument("--source", required=True)
    parser.add_argument("--tool", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument(
        "--subject-type",
        default="commit",
    )
    parser.add_argument(
        "--subject-value",
        default=None,
    )
    parser.add_argument(
        "--output-dir",
        default="evidence/generated",
    )

    args = parser.parse_args()

    subject_value = (
        args.subject_value
        or os.getenv("GITHUB_SHA")
        or "local"
    )

    evidence = {
        "controlId": args.control_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": args.status,
        "subject": {
            "type": args.subject_type,
            "value": subject_value,
        },
        "source": args.source,
        "tool": args.tool,
        "summary": args.summary,
    }

    optional_environment_fields = {
        "repository": "GITHUB_REPOSITORY",
        "commit": "GITHUB_SHA",
        "branch": "GITHUB_REF_NAME",
        "runId": "GITHUB_RUN_ID",
    }

    for field, environment_variable in optional_environment_fields.items():
        value = os.getenv(environment_variable)

        if value:
            evidence[field] = value

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{args.control_id}.json"

    output_file.write_text(
        json.dumps(evidence, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Evidence written to {output_file}")


if __name__ == "__main__":
    main()
