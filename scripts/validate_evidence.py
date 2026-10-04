#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate engineering control evidence."
    )

    parser.add_argument(
        "--directory",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--required",
        nargs="*",
        default=[],
    )

    args = parser.parse_args()

    schema = json.loads(
        (
            ROOT
            / "evidence"
            / "schema"
            / "control-evidence.schema.json"
        ).read_text(encoding="utf-8")
    )

    catalog = yaml.safe_load(
        (
            ROOT
            / "controls"
            / "catalog.yaml"
        ).read_text(encoding="utf-8")
    )

    known_controls = {
        control["id"]
        for control in catalog["controls"]
    }

    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )

    evidence_by_control: dict[str, dict] = {}
    errors: list[str] = []

    for file in sorted(args.directory.rglob("*.json")):
        try:
            evidence = json.loads(
                file.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError as exc:
            errors.append(f"{file}: invalid JSON: {exc}")
            continue

        schema_errors = sorted(
            validator.iter_errors(evidence),
            key=lambda error: list(error.path),
        )

        for error in schema_errors:
            errors.append(
                f"{file}: schema error: {error.message}"
            )

        control_id = evidence.get("controlId")

        if control_id not in known_controls:
            errors.append(
                f"{file}: unknown control ID {control_id}"
            )
            continue

        evidence_by_control[control_id] = evidence

    for control_id in args.required:
        evidence = evidence_by_control.get(control_id)

        if evidence is None:
            errors.append(
                f"Required evidence missing: {control_id}"
            )
            continue

        if evidence["status"] != "PASS":
            errors.append(
                f"{control_id} did not pass "
                f"(status={evidence['status']})"
            )

    if errors:
        print("Evidence validation failed:")

        for error in errors:
            print(f" - {error}")

        return 1

    print("Evidence validation passed.")

    for control_id in sorted(evidence_by_control):
        evidence = evidence_by_control[control_id]
        print(
            f" {control_id}: {evidence['status']}"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
    