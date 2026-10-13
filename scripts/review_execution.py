#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROTOCOL_VERSION = "1"

SEQUENCE_PATTERN = re.compile(r"^(\d{4})-")


@dataclass(frozen=True)
class ReviewInput:
    review_type: str
    skill: str
    target: str
    target_sha256: str
    context: tuple[tuple[str, str], ...]
    platform_version: str
    protocol_version: str = PROTOCOL_VERSION


def fail(message: str) -> None:
    print(
        f"ERROR: {message}",
        file=sys.stderr,
    )
    raise SystemExit(1)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as source:
        while True:
            chunk = source.read(1024 * 1024)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def repository_relative(
    root: Path,
    path: Path,
) -> str:
    try:
        relative = path.resolve().relative_to(
            root.resolve()
        )
    except ValueError:
        fail(
            "Review inputs must be inside "
            f"the repository: {path}"
        )

    return relative.as_posix()


def resolve_input_file(
    root: Path,
    value: str,
) -> tuple[str, str]:
    path = root / value

    if not path.is_file():
        fail(
            f"Review input does not exist: {value}"
        )

    relative = repository_relative(
        root,
        path,
    )

    return (
        relative,
        sha256_file(path),
    )


def build_review_input(
    root: Path,
    review_type: str,
    skill: str,
    target: str,
    contexts: list[str],
    platform_version: str,
) -> ReviewInput:
    target_path, target_hash = resolve_input_file(
        root,
        target,
    )

    context_entries = {
        resolve_input_file(
            root,
            context,
        )
        for context in contexts
        if context != target
    }

    ordered_context = tuple(
        sorted(
            context_entries,
            key=lambda item: item[0],
        )
    )

    return ReviewInput(
        review_type=review_type,
        skill=skill,
        target=target_path,
        target_sha256=target_hash,
        context=ordered_context,
        platform_version=platform_version,
    )


def manifest_dict(
    review_input: ReviewInput,
) -> dict[str, Any]:
    return {
        "reviewType": review_input.review_type,
        "skill": review_input.skill,
        "target": {
            "path": review_input.target,
            "sha256": review_input.target_sha256,
        },
        "context": [
            {
                "path": path,
                "sha256": sha256,
            }
            for path, sha256
            in review_input.context
        ],
        "platformVersion": (
            review_input.platform_version
        ),
        "protocolVersion": (
            review_input.protocol_version
        ),
    }


def fingerprint(
    review_input: ReviewInput,
) -> str:
    normalized = json.dumps(
        manifest_dict(review_input),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    return hashlib.sha256(
        normalized
    ).hexdigest()


def extract_metadata_value(
    text: str,
    key: str,
) -> str | None:
    pattern = re.compile(
        rf"^{re.escape(key)}:\s*(.+?)\s*$",
        re.MULTILINE,
    )

    match = pattern.search(text)

    if not match:
        return None

    return (
        match.group(1)
        .strip()
        .strip("\"'")
    )


def find_equivalent_review(
    reviews_dir: Path,
    input_fingerprint: str,
) -> Path | None:
    if not reviews_dir.exists():
        return None

    for review in sorted(
        reviews_dir.glob("*.md")
    ):
        text = review.read_text(
            encoding="utf-8"
        )

        status = extract_metadata_value(
            text,
            "status",
        )

        recorded_fingerprint = (
            extract_metadata_value(
                text,
                "input-fingerprint",
            )
        )

        if (
            status == "completed"
            and recorded_fingerprint
            == input_fingerprint
        ):
            return review

    return None


def next_sequence(
    reviews_dir: Path,
) -> int:
    highest = 0

    if not reviews_dir.exists():
        return 1

    for path in reviews_dir.glob("*.md"):
        match = SEQUENCE_PATTERN.match(
            path.name
        )

        if not match:
            continue

        highest = max(
            highest,
            int(match.group(1)),
        )

    return highest + 1


def format_sequence(value: int) -> str:
    return f"{value:04d}"


def command_prepare(
    args: argparse.Namespace,
) -> int:
    root = args.root.resolve()
    reviews_dir = (
        root
        / args.reviews_dir
    ).resolve()

    review_input = build_review_input(
        root=root,
        review_type=args.type,
        skill=args.skill,
        target=args.target,
        contexts=args.context or [],
        platform_version=args.platform_version,
    )

    input_fingerprint = fingerprint(
        review_input
    )

    existing = find_equivalent_review(
        reviews_dir,
        input_fingerprint,
    )

    sequence = next_sequence(
        reviews_dir
    )

    result = {
        "protocolVersion": PROTOCOL_VERSION,
        "reviewType": args.type,
        "skill": args.skill,
        "inputFingerprint": (
            input_fingerprint
        ),
        "manifest": manifest_dict(
            review_input
        ),
        "equivalentReview": (
            repository_relative(
                root,
                existing,
            )
            if existing
            else None
        ),
        "nextSequence": (
            format_sequence(sequence)
        ),
        "shouldExecute": (
            existing is None
            or args.force
        ),
        "forcedRerun": (
            bool(existing)
            and args.force
        ),
    }

    if existing and not args.force:
        result["reason"] = (
            "Equivalent completed review "
            "already exists."
        )

    elif existing and args.force:
        result["rerunOf"] = (
            extract_metadata_value(
                existing.read_text(
                    encoding="utf-8"
                ),
                "id",
            )
        )

    else:
        result["reason"] = (
            "No equivalent completed "
            "review found."
        )

    output = json.dumps(
        result,
        indent=2,
        sort_keys=True,
    )

    if args.output:
        output_path = (
            root
            / args.output
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            output + "\n",
            encoding="utf-8",
        )

    print(output)

    return 0


def command_check(
    args: argparse.Namespace,
) -> int:
    root = args.root.resolve()

    review_path = (
        root
        / args.review
    )

    if not review_path.is_file():
        fail(
            f"Review does not exist: "
            f"{args.review}"
        )

    text = review_path.read_text(
        encoding="utf-8"
    )

    recorded = extract_metadata_value(
        text,
        "input-fingerprint",
    )

    if not recorded:
        fail(
            "Review does not contain "
            "input-fingerprint metadata."
        )

    review_input = build_review_input(
        root=root,
        review_type=args.type,
        skill=args.skill,
        target=args.target,
        contexts=args.context or [],
        platform_version=args.platform_version,
    )

    actual = fingerprint(
        review_input
    )

    if actual != recorded:
        print(
            "Review input fingerprint "
            "does not match current inputs."
        )

        print(
            f"Recorded: {recorded}"
        )

        print(
            f"Current:  {actual}"
        )

        return 1

    print(
        "Review input fingerprint "
        "matches current inputs."
    )

    return 0


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare and validate deterministic "
            "engineering review execution."
        )
    )

    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    prepare = subparsers.add_parser(
        "prepare"
    )

    prepare.add_argument(
        "--type",
        required=True,
    )

    prepare.add_argument(
        "--skill",
        required=True,
    )

    prepare.add_argument(
        "--target",
        required=True,
    )

    prepare.add_argument(
        "--context",
        action="append",
        default=[],
    )

    prepare.add_argument(
        "--reviews-dir",
        required=True,
    )

    prepare.add_argument(
        "--platform-version",
        required=True,
    )

    prepare.add_argument(
        "--force",
        action="store_true",
    )

    prepare.add_argument(
        "--output",
    )

    prepare.set_defaults(
        handler=command_prepare
    )

    check = subparsers.add_parser(
        "check"
    )

    check.add_argument(
        "--type",
        required=True,
    )

    check.add_argument(
        "--skill",
        required=True,
    )

    check.add_argument(
        "--target",
        required=True,
    )

    check.add_argument(
        "--context",
        action="append",
        default=[],
    )

    check.add_argument(
        "--platform-version",
        required=True,
    )

    check.add_argument(
        "--review",
        required=True,
    )

    check.set_defaults(
        handler=command_check
    )

    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(
        main()
    )