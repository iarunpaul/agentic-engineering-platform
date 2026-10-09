import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ActionPinningTests(unittest.TestCase):

    def test_github_actions_are_pinned_to_full_shas(self):
        result = subprocess.run(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts"
                    / "validate_action_pinning.py"
                ),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(
            0,
            result.returncode,
            msg=(
                result.stdout
                + "\n"
                + result.stderr
            ),
        )


if __name__ == "__main__":
    unittest.main()
