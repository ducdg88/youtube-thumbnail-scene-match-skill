"""Smoke test: versioned creative-brief settings and no-text hard constraints."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
conf = json.loads((root / "config" / "defaults.json").read_text(encoding="utf-8"))
profile = json.loads((root / "profile" / "creative_profile.json").read_text(encoding="utf-8"))
manifest = json.loads((root / "templates" / "manifest.example.json").read_text(encoding="utf-8"))
assert conf["skill_version"] == "2.3.0"
assert conf["thumbnail_text_mode"] == "none" and conf["allow_text_on_image"] is False
assert conf["allow_logo_or_watermark"] is False
assert conf["batch_size_default"] == 4 and conf["batch_size_min"] == 3 and conf["batch_size_max"] == 5
assert conf["aspect_ratio"] == "16:9"
assert conf["preview_ttl_hours"] == 5
assert conf["transport_scene_requires_truck_carrying_log"] is True
assert profile["thumbnail"]["all_visible_text_prohibited"] is True
assert profile["target_audience"] == "international"
assert len(manifest["concepts"]) == conf["batch_size_default"]
assert all(c["no_text_visual_qc"] == "PENDING_REVIEW" for c in manifest["concepts"])
assert conf["feedback_loop"]["enabled"] is True
assert conf["automatic_activation"]["attachment_alone_installs_skill"] is False
assert conf["size_amplification"]["allowed_levels"] == [1, 2, 3, 4, 5]
assert (root / "profile" / "AUTO_RECOGNITION_AND_FEEDBACK.md").exists()
assert (root / "scripts" / "feedback_loop.py").exists()
assert (root / "profile" / "SESSION_CREATIVE_BRIEF.md").exists()
assert (root / "templates" / "NO_TEXT_BATCH_PROMPTS.md").exists()
print("PASS: 2.3 creative profile, NO TEXT, truck-carrying, TTL, feedback loop and auto-trigger")
