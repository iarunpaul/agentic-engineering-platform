import importlib.util
import io
import json
import sys
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

MODULE_PATH = (
    ROOT
    / "scripts"
    / "review_execution.py"
)

SPEC = importlib.util.spec_from_file_location(
    "review_execution",
    MODULE_PATH,
)

assert SPEC is not None
assert SPEC.loader is not None

review_execution = (
    importlib.util.module_from_spec(
        SPEC
    )
)

sys.modules[SPEC.name] = review_execution

SPEC.loader.exec_module(
    review_execution
)


class ReviewExecutionTests(
    unittest.TestCase
):

    def write_review(
        self,
        path: Path,
        review_id: str,
        target: str,
        fingerprint: str | None,
        protocol: str | None = "1",
    ) -> None:
        metadata = [
            "# Review",
            "",
            "## Metadata",
            "",
            "```yaml",
            f"id: {review_id}",
            "status: completed",
            f"reviewed-artifact: {target}",
        ]

        if protocol is not None:
            metadata.append(
                f'protocol-version: "{protocol}"'
            )

        if fingerprint is not None:
            metadata.append(
                f"input-fingerprint: {fingerprint}"
            )

        metadata.extend(
            [
                "```",
                "",
            ]
        )

        path.write_text(
            "\n".join(metadata),
            encoding="utf-8",
        )

    def run_prepare(
        self,
        root: Path,
        target: str,
        contexts: list[str],
        force: bool = False,
    ) -> dict:
        args = Namespace(
            root=root,
            type="architecture",
            skill="architecture-review",
            target=target,
            context=contexts,
            reviews_dir=(
                "docs/reviews/architecture"
            ),
            platform_version="v0.2.1",
            force=force,
            output=None,
        )

        output = io.StringIO()

        with redirect_stdout(output):
            result = (
                review_execution
                .command_prepare(args)
            )

        self.assertEqual(0, result)

        return json.loads(
            output.getvalue()
        )

    def test_fingerprint_is_repeatable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            (root / "target.md").write_text(
                "target\n",
                encoding="utf-8",
            )

            (root / "context.md").write_text(
                "context\n",
                encoding="utf-8",
            )

            first = review_execution.build_review_input(
                root=root,
                review_type="architecture",
                skill="architecture-review",
                target="target.md",
                contexts=["context.md"],
                platform_version="v0.2.1",
            )

            second = review_execution.build_review_input(
                root=root,
                review_type="architecture",
                skill="architecture-review",
                target="target.md",
                contexts=["context.md"],
                platform_version="v0.2.1",
            )

            self.assertEqual(
                review_execution.fingerprint(first),
                review_execution.fingerprint(second),
            )

    def test_context_order_does_not_change_fingerprint(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            (root / "target.md").write_text(
                "target\n",
                encoding="utf-8",
            )

            (root / "a.md").write_text(
                "a\n",
                encoding="utf-8",
            )

            (root / "b.md").write_text(
                "b\n",
                encoding="utf-8",
            )

            first = review_execution.build_review_input(
                root=root,
                review_type="architecture",
                skill="architecture-review",
                target="target.md",
                contexts=[
                    "a.md",
                    "b.md",
                ],
                platform_version="v0.2.1",
            )

            second = review_execution.build_review_input(
                root=root,
                review_type="architecture",
                skill="architecture-review",
                target="target.md",
                contexts=[
                    "b.md",
                    "a.md",
                ],
                platform_version="v0.2.1",
            )

            self.assertEqual(
                review_execution.fingerprint(first),
                review_execution.fingerprint(second),
            )

    def test_changed_target_changes_fingerprint(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            target = root / "target.md"

            target.write_text(
                "version one\n",
                encoding="utf-8",
            )

            first = review_execution.build_review_input(
                root=root,
                review_type="architecture",
                skill="architecture-review",
                target="target.md",
                contexts=[],
                platform_version="v0.2.1",
            )

            first_hash = (
                review_execution.fingerprint(first)
            )

            target.write_text(
                "version two\n",
                encoding="utf-8",
            )

            second = review_execution.build_review_input(
                root=root,
                review_type="architecture",
                skill="architecture-review",
                target="target.md",
                contexts=[],
                platform_version="v0.2.1",
            )

            self.assertNotEqual(
                first_hash,
                review_execution.fingerprint(second),
            )

    def test_protocol_version_must_match_for_equivalence(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            reviews = (
                root
                / "docs"
                / "reviews"
                / "architecture"
            )

            reviews.mkdir(parents=True)

            review = reviews / "0001-test.md"

            self.write_review(
                path=review,
                review_id="REVIEW-ARC-0001",
                target="target.md",
                fingerprint="abc123",
                protocol="0",
            )

            found = (
                review_execution
                .find_equivalent_review(
                    reviews,
                    "abc123",
                )
            )

            self.assertIsNone(found)

    def test_same_target_review_is_not_fingerprint_context(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            target = (
                root
                / "docs"
                / "architecture"
                / "ADRs"
                / "0001-test.md"
            )

            target.parent.mkdir(
                parents=True
            )

            target.write_text(
                "target\n",
                encoding="utf-8",
            )

            review = (
                root
                / "docs"
                / "reviews"
                / "architecture"
                / "0001-test.md"
            )

            review.parent.mkdir(
                parents=True
            )

            self.write_review(
                path=review,
                review_id="REVIEW-ARC-0001",
                target=(
                    "docs/architecture/"
                    "ADRs/0001-test.md"
                ),
                fingerprint="old",
            )

            review_input = (
                review_execution
                .build_review_input(
                    root=root,
                    review_type="architecture",
                    skill="architecture-review",
                    target=(
                        "docs/architecture/"
                        "ADRs/0001-test.md"
                    ),
                    contexts=[
                        (
                            "docs/reviews/"
                            "architecture/"
                            "0001-test.md"
                        )
                    ],
                    platform_version="v0.2.1",
                )
            )

            self.assertEqual(
                tuple(),
                review_input.context,
            )

    def test_same_fingerprint_is_idempotent(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            (root / "target.md").write_text(
                "target\n",
                encoding="utf-8",
            )

            reviews = (
                root
                / "docs"
                / "reviews"
                / "architecture"
            )

            reviews.mkdir(parents=True)

            review_input = (
                review_execution
                .build_review_input(
                    root=root,
                    review_type="architecture",
                    skill="architecture-review",
                    target="target.md",
                    contexts=[],
                    platform_version="v0.2.1",
                )
            )

            input_fingerprint = (
                review_execution
                .fingerprint(review_input)
            )

            self.write_review(
                path=reviews / "0001-test.md",
                review_id="REVIEW-ARC-0001",
                target="target.md",
                fingerprint=input_fingerprint,
            )

            result = self.run_prepare(
                root=root,
                target="target.md",
                contexts=[],
            )

            self.assertFalse(
                result["shouldExecute"]
            )

            self.assertEqual(
                (
                    "docs/reviews/architecture/"
                    "0001-test.md"
                ),
                result["equivalentReview"],
            )

    def test_forced_equivalent_review_is_rerun(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            (root / "target.md").write_text(
                "target\n",
                encoding="utf-8",
            )

            reviews = (
                root
                / "docs"
                / "reviews"
                / "architecture"
            )

            reviews.mkdir(parents=True)

            review_input = (
                review_execution
                .build_review_input(
                    root=root,
                    review_type="architecture",
                    skill="architecture-review",
                    target="target.md",
                    contexts=[],
                    platform_version="v0.2.1",
                )
            )

            input_fingerprint = (
                review_execution
                .fingerprint(review_input)
            )

            self.write_review(
                path=reviews / "0001-test.md",
                review_id="REVIEW-ARC-0001",
                target="target.md",
                fingerprint=input_fingerprint,
            )

            result = self.run_prepare(
                root=root,
                target="target.md",
                contexts=[],
                force=True,
            )

            self.assertTrue(
                result["shouldExecute"]
            )

            self.assertTrue(
                result["forcedRerun"]
            )

            self.assertEqual(
                "REVIEW-ARC-0001",
                result["rerunOf"],
            )

            self.assertNotIn(
                "supersedes",
                result,
            )

    def test_changed_inputs_supersede_current_protocol_review(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            target = root / "target.md"

            target.write_text(
                "new target\n",
                encoding="utf-8",
            )

            reviews = (
                root
                / "docs"
                / "reviews"
                / "architecture"
            )

            reviews.mkdir(parents=True)

            self.write_review(
                path=reviews / "0001-test.md",
                review_id="REVIEW-ARC-0001",
                target="target.md",
                fingerprint="old-fingerprint",
                protocol="1",
            )

            result = self.run_prepare(
                root=root,
                target="target.md",
                contexts=[],
            )

            self.assertTrue(
                result["shouldExecute"]
            )

            self.assertEqual(
                "REVIEW-ARC-0001",
                result["supersedes"],
            )

            self.assertNotIn(
                "rerunOf",
                result,
            )

    def test_legacy_review_is_not_described_as_rerun(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            (root / "target.md").write_text(
                "target\n",
                encoding="utf-8",
            )

            reviews = (
                root
                / "docs"
                / "reviews"
                / "architecture"
            )

            reviews.mkdir(parents=True)

            self.write_review(
                path=reviews / "0001-test.md",
                review_id="REVIEW-ARC-0001",
                target="target.md",
                fingerprint=None,
                protocol=None,
            )

            result = self.run_prepare(
                root=root,
                target="target.md",
                contexts=[],
            )

            self.assertTrue(
                result["shouldExecute"]
            )

            self.assertEqual(
                "REVIEW-ARC-0001",
                result["legacyPredecessor"],
            )

            self.assertNotIn(
                "rerunOf",
                result,
            )

    def test_sequence_is_category_local(self):
        with tempfile.TemporaryDirectory() as tmp:
            reviews = Path(tmp)

            (
                reviews
                / "0001-first.md"
            ).write_text(
                "one\n",
                encoding="utf-8",
            )

            (
                reviews
                / "0004-fourth.md"
            ).write_text(
                "four\n",
                encoding="utf-8",
            )

            self.assertEqual(
                5,
                review_execution.next_sequence(
                    reviews
                ),
            )


if __name__ == "__main__":
    unittest.main()
