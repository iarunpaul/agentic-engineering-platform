#!/usr/bin/env python3

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]

TEXT_EXTENSIONS = {
    ".md",
    ".yaml",
    ".yml",
    ".json",
    ".py",
    ".txt",
}

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "evidence/generated",
}


def is_ignored(path: Path) -> bool:
    relative = path.relative_to(ROOT)

    parts = relative.parts

    if any(part in IGNORED_DIRECTORIES for part in parts):
        return True

    return str(relative).startswith("evidence/generated/")


def validate_text_file(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")

    if text and not text.endswith("\n"):
        errors.append(
            f"{path.relative_to(ROOT)}: missing final newline"
        )

    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.rstrip() != line:
            errors.append(
                f"{path.relative_to(ROOT)}:{line_number}: "
                "trailing whitespace"
            )

        if path.suffix in {".md", ".yaml", ".yml"} and "\t" in line:
            errors.append(
                f"{path.relative_to(ROOT)}:{line_number}: "
                "tab character found"
            )


def validate_structured_file(
    path: Path,
    errors: list[str],
) -> None:
    try:
        text = path.read_text(encoding="utf-8")

        if path.suffix == ".json":
            json.loads(text)

        elif path.suffix in {".yaml", ".yml"}:
            yaml.safe_load(text)

        elif path.suffix == ".py":
            compile(
                text,
                str(path),
                "exec",
            )

    except Exception as exc:
        errors.append(
            f"{path.relative_to(ROOT)}: {exc}"
        )


def main() -> int:
    errors: list[str] = []

    files = sorted(
        path
        for path in ROOT.rglob("*")
        if (
            path.is_file()
            and path.suffix in TEXT_EXTENSIONS
            and not is_ignored(path)
        )
    )

    for path in files:
        validate_text_file(path, errors)
        validate_structured_file(path, errors)

    if errors:
        print("Repository lint failed:")

        for error in errors:
            print(f" - {error}")

        return 1

    print(f"Repository lint passed ({len(files)} files checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
    