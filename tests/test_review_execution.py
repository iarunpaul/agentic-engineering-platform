import importlib.util
import tempfile
import unittest
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

SPEC.loader.exec_module(
    review_execution
)


class ReviewExecutionTests(
    unittest.TestCase
):

    def test_fingerprint_is_repeatable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            target = root / "target.md"
            context = root / "context.md"

            target.write_text(
                "target\n",
                encoding="utf-8",
            )

            context.write_text(
                "context\n",
                encoding="utf-8",
            )

            first = (
                review_execution
                .build_review_input(
                    root=root,
                    review_type="architecture",
                    skill="architecture-review",
                    target="target.md",
                    contexts=["context.md"],
                    platform_version="v0.1.4",
                )
            )

            second = (
                review_execution
                .build_review_input(
                    root=root,
                    review_type="architecture",
                    skill="architecture-review",
                    target="target.md",
                    contexts=["context.md"],
                    platform_version="v0.1.4",
                )
            )

            self.assertEqual(
                review_execution.fingerprint(
                    first
                ),
                review_execution.fingerprint(
                    second
                ),
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

            first = (
                review_execution
                .build_review_input(
                    root=root,
                    review_type="architecture",
                    skill="architecture-review",
                    target="target.md",
                    contexts=[
                        "a.md",
                        "b.md",
                    ],
                    platform_version="v0.1.4",
                )
            )

            second = (
                review_execution
                .build_review_input(
                    root=root,
                    review_type="architecture",
                    skill="architecture-review",
                    target="target.md",
                    contexts=[
                        "b.md",
                        "a.md",
                    ],
                    platform_version="v0.1.4",
                )
            )

            self.assertEqual(
                review_execution.fingerprint(
                    first
                ),
                review_execution.fingerprint(
                    second
                ),
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

            first = (
                review_execution
                .build_review_input(
                    root=root,
                    review_type="architecture",
                    skill="architecture-review",
                    target="target.md",
                    contexts=[],
                    platform_version="v0.1.4",
                )
            )

            first_hash = (
                review_execution.fingerprint(
                    first
                )
            )

            target.write_text(
                "version two\n",
                encoding="utf-8",
            )

            second = (
                review_execution
                .build_review_input(
                    root=root,
                    review_type="architecture",
                    skill="architecture-review",
                    target="target.md",
                    contexts=[],
                    platform_version="v0.1.4",
                )
            )

            self.assertNotEqual(
                first_hash,
                review_execution.fingerprint(
                    second
                ),
            )

    def test_existing_review_detected_by_fingerprint(
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

            reviews.mkdir(
                parents=True
            )

            fingerprint = "abc123"

            review = (
                reviews
                / "0001-test.md"
            )

            review.write_text(
                (
                    "## Metadata\n\n"
                    "```yaml\n"
                    "id: REVIEW-ARC-0001\n"
                    "status: completed\n"
                    f"input-fingerprint: {fingerprint}\n"
                    "```\n"
                ),
                encoding="utf-8",
            )

            found = (
                review_execution
                .find_equivalent_review(
                    reviews,
                    fingerprint,
                )
            )

            self.assertEqual(
                review,
                found,
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