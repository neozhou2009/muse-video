import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from acting_contract import render_beat, validate_compilation


def fixture():
    beat = {"id": "V001", "visible_cast": ["listener"],
            "performance": {"status": "included", "text": "Stay inside the locked room.", "actors": ["listener"], "reason": "Visible listener; speaker is outside."},
            "reaction": {"status": "included", "text": "Listen without showing the unseen gunshot.", "actors": ["listener"], "reason": "Restricted viewpoint."}}
    return {"acting_source_ids": ["V001"], "shots": [{"id": "C001", "visual_units": ["V001"], "acting_beats": [beat], "compiled_prompt": render_beat(beat)}]}


class ActingContractTests(unittest.TestCase):
    def test_complete_delivery(self):
        self.assertEqual(validate_compilation(fixture())["visual_units"], 1)

    def test_loss_is_detected_even_if_headers_remain(self):
        state = fixture()
        state["shots"][0]["compiled_prompt"] = "表演：placeholder；反应：placeholder"
        with self.assertRaises(ValueError): validate_compilation(state)

    def test_either_field_can_not_disappear(self):
        for key in ["performance", "reaction"]:
            state = fixture()
            del state["shots"][0]["acting_beats"][0][key]
            with self.subTest(key=key), self.assertRaises(ValueError): validate_compilation(state)

    def test_offscreen_actor_rejected(self):
        state = fixture()
        state["shots"][0]["acting_beats"][0]["reaction"]["actors"] = ["unseen shooter"]
        with self.assertRaises(ValueError): validate_compilation(state)

    def test_missing_target_actor_rejected(self):
        state = fixture()
        del state["shots"][0]["acting_beats"][0]["performance"]["actors"]
        with self.assertRaises(ValueError): validate_compilation(state)

    def test_environment_explicit_not_applicable(self):
        state = fixture(); beat = state["shots"][0]["acting_beats"][0]
        beat["visible_cast"] = []
        for key in ["performance", "reaction"]:
            beat[key] = {"status": "not_applicable", "reason": "Moon insert; no visible actor."}
        state["shots"][0]["compiled_prompt"] = render_beat(beat)
        validate_compilation(state)

    def test_missing_reason_rejected(self):
        state = fixture(); del state["shots"][0]["acting_beats"][0]["reaction"]["reason"]
        with self.assertRaises(ValueError): validate_compilation(state)

    def test_silent_source_omission_rejected(self):
        state = fixture(); state["acting_source_ids"].append("V002")
        with self.assertRaises(ValueError): validate_compilation(state)

    def test_duplicate_or_reordered_beats_rejected(self):
        state = fixture(); state["shots"][0]["acting_beats"].append(copy.deepcopy(state["shots"][0]["acting_beats"][0]))
        with self.assertRaises(ValueError): validate_compilation(state)

    def test_assembler_rejects_legacy_silent_loss(self):
        from prompt_assembler import assemble
        with self.assertRaises(ValueError):
            assemble({"model_compilation": {"shots": [{"compiled_prompt": "missing cues"}]}})

    def test_export_rejects_before_creating_output(self):
        import tempfile
        from export_html import export_compilation
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "preview.html"
            with self.assertRaises(ValueError):
                export_compilation({"model_compilation": {"shots": [{"compiled_prompt": "missing cues"}]}}, str(path))
            self.assertFalse(path.exists())

    def test_valid_compilation_assembles_and_exports(self):
        import tempfile
        from prompt_assembler import assemble
        from export_html import export_compilation
        state = {"model_compilation": fixture()}
        assemble(state)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "preview.html"
            export_compilation(state, str(path))
            self.assertIn("Stay inside the locked room.", path.read_text(encoding="utf-8"))


if __name__ == "__main__": unittest.main()
