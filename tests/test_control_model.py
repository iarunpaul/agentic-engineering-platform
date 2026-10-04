import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


class ControlModelTests(unittest.TestCase):

    def test_control_ids_are_unique(self):
        catalog = yaml.safe_load(
            (
                ROOT / "controls" / "catalog.yaml"
            ).read_text(encoding="utf-8")
        )

        ids = [
            control["id"]
            for control in catalog["controls"]
        ]

        self.assertEqual(
            len(ids),
            len(set(ids)),
            "Control IDs must be unique.",
        )

    def test_control_sources_exist(self):
        catalog = yaml.safe_load(
            (
                ROOT / "controls" / "catalog.yaml"
            ).read_text(encoding="utf-8")
        )

        for control in catalog["controls"]:
            for source in control.get("source", []):
                self.assertTrue(
                    (ROOT / source).exists(),
                    f"{control['id']} references missing {source}",
                )

    def test_evidence_schema_is_valid(self):
        schema = json.loads(
            (
                ROOT
                / "evidence"
                / "schema"
                / "control-evidence.schema.json"
            ).read_text(encoding="utf-8")
        )

        Draft202012Validator.check_schema(schema)

    def test_phase_zero_controls_exist(self):
        catalog = yaml.safe_load(
            (
                ROOT / "controls" / "catalog.yaml"
            ).read_text(encoding="utf-8")
        )

        ids = {
            control["id"]
            for control in catalog["controls"]
        }

        phase_zero = catalog["phase_0"][
            "initially_implemented_controls"
        ]

        for control_id in phase_zero:
            self.assertIn(control_id, ids)


if __name__ == "__main__":
    unittest.main()
    