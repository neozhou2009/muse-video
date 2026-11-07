"""Lossless delivery contract for reviewed performance/reaction decisions.

This validates delivery, not artistic quality. Source cues must be reviewed for
visibility, voice-over, inserts and split shots before they enter this contract.
"""
import argparse
import collections
import json
from pathlib import Path

FIELDS = (("performance", "表演"), ("reaction", "反应"))


def render_beat(beat):
    if not isinstance(beat.get("id"), str) or not beat["id"].strip():
        raise ValueError("Acting beat requires a stable visual-unit id")
    cast = set(beat.get("visible_cast", []))
    parts = []
    for key, label in FIELDS:
        decision = beat.get(key)
        if not isinstance(decision, dict):
            raise ValueError(f"{beat['id']}: missing {key} decision")
        if not str(decision.get("reason", "")).strip():
            raise ValueError(f"{beat['id']}: {key} requires an applicability reason")
        if decision.get("status") == "included":
            text = decision.get("text", "")
            if not isinstance(text, str) or not text.strip():
                raise ValueError(f"{beat['id']}: included {key} has no text")
            actors = decision.get("actors")
            if not isinstance(actors, list) or not actors:
                raise ValueError(f"{beat['id']}: included {key} requires target actors")
            if not set(actors).issubset(cast):
                raise ValueError(f"{beat['id']}: {key} targets an offscreen actor")
            parts.append(f"{label}：{text}")
        elif decision.get("status") == "not_applicable":
            if decision.get("text") or decision.get("actors"):
                raise ValueError(f"{beat['id']}: not-applicable {key} cannot carry actor instructions")
            parts.append(f"{label}：不适用（{decision['reason']}）")
        else:
            raise ValueError(f"{beat['id']}: invalid {key} disposition")
    return f"〔{beat['id']}〕" + "；".join(parts)


def render_beats(beats):
    return "\n".join(render_beat(beat) for beat in beats)


def validate_compilation(state):
    compilation = state.get("model_compilation", state)
    shots = compilation.get("shots", [])
    if not shots:
        raise ValueError("No compiled shots to validate")
    expected = compilation.get("acting_source_ids")
    if not isinstance(expected, list) or not expected:
        raise ValueError("acting_source_ids must enumerate the source visual units")
    if len(expected) != len(set(expected)):
        raise ValueError("acting_source_ids must use unique visual-unit IDs")
    delivered = []
    for shot in shots:
        beats = shot.get("acting_beats")
        if not isinstance(beats, list) or not beats:
            raise ValueError(f"{shot.get('id', shot.get('panel_id'))}: missing acting_beats")
        visual = shot.get("visual_units")
        if visual != [beat.get("id") for beat in beats]:
            raise ValueError("visual_units and acting_beats differ or are reordered")
        prompt = shot.get("compiled_prompt", "")
        for beat in beats:
            if render_beat(beat) not in prompt:
                raise ValueError(f"{beat['id']}: performance/reaction lost in final prompt")
            delivered.append(beat["id"])
    if collections.Counter(expected) != collections.Counter(delivered):
        raise ValueError("Source visual units were silently dropped or duplicated")
    return {"shots": len(shots), "visual_units": len(delivered), "status": "passed"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    result = validate_compilation(json.loads(Path(args.input).read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
