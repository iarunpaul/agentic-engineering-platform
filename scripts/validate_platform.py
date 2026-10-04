#!/usr/bin/env python3

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]

CATALOG = ROOT / "controls" / "catalog.yaml"
CONTROL_MATRIX = ROOT / "controls" / "control-matrix.md"
EVIDENCE_SCHEMA = (
    ROOT
    / "evidence"
    / "schema"
    / "control-evidence.schema.json"
)


REQUIRED_FILES = [
    ROOT / "AGENTS.md",
    ROOT / "controls" / "README.md",
    CATALOG,
    CONTROL_MATRIX,
    ROOT / "evidence" / "README.md",
    ROOT / "evidence" / "evidence-contract.md",
    EVIDENCE_SCHEMA,
    ROOT / "policies" / "quality-gates.md",
    ROOT / "policies" / "human-approval.md",
    ROOT / "policies" / "secrets.md",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def validate_required_files() -> None:
    for file in REQUIRED_FILES:
        if not file.is_file():
            fail(f"Required file does not exist: {file.relative_to(ROOT)}")


def load_catalog() -> dict:
    try:
        return yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        fail(f"Invalid YAML in controls/catalog.yaml: {exc}")


def validate_catalog(catalog: dict) -> None:
    controls = catalog.get("controls")

    if not isinstance(controls, list):
        fail("controls/catalog.yaml must contain a 'controls' list.")

    seen_ids: set[str] = set()

    for control in controls:
        control_id = control.get("id")

        if not control_id:
            fail("Every control must define an id.")

        if control_id in seen_ids:
            fail(f"Duplicate control ID: {control_id}")

        seen_ids.add(control_id)

        for source in control.get("source", []):
            source_path = ROOT / source

            if not source_path.exists():
                fail(
                    f"{control_id} references missing source: {source}"
                )

    phase_zero = (
        catalog.get("phase_0", {})
        .get("initially_implemented_controls", [])
    )

    for control_id in phase_zero:
        if control_id not in seen_ids:
            fail(
                "Phase 0 references an unknown control: "
                f"{control_id}"
            )

    matrix = CONTROL_MATRIX.read_text(encoding="utf-8")

    missing_from_matrix = [
        control_id
        for control_id in seen_ids
        if control_id not in matrix
    ]

    if missing_from_matrix:
        fail(
            "Controls missing from control-matrix.md: "
            + ", ".join(missing_from_matrix)
        )


def validate_evidence_schema() -> None:
    try:
        schema = json.loads(
            EVIDENCE_SCHEMA.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        fail(f"Invalid evidence JSON Schema: {exc}")

    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        fail(f"Evidence schema validation failed: {exc}")


def main() -> int:
    validate_required_files()

    catalog = load_catalog()
    validate_catalog(catalog)

    validate_evidence_schema()

    print("Platform validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())