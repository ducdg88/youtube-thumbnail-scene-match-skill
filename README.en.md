# Thumbnail First, Scene Match: a no-text YouTube thumbnail skill for international channels

[Tiếng Việt](README.md) | **English**

![CI](https://github.com/ducdg88/youtube-thumbnail-scene-match-skill/actions/workflows/validate.yml/badge.svg) ![license](https://img.shields.io/badge/license-MIT-green) ![version](https://img.shields.io/badge/version-2.3.0-blue)

An Agent Skill (`SKILL.md`) that lets an AI agent create **text-free YouTube thumbnails** for channels with an international audience: 3 to 5 separate 16:9 images per run (4 by default), each with a different story and camera angle, keeping the exact subject of your reference photo, then planning the matching scene inside the video (Thumbnail First, Scene Match). A feedback loop records which images you pick or reject so the next batch improves. Works with Claude, Claude Code and any agent that reads `SKILL.md`. Built and used in production by [DUCPT](https://ducpt.com/?utm_source=github&utm_medium=readme&utm_campaign=youtube-thumbnail-scene-match-skill).

The bundled profile targets **heavy-haul trucks carrying giant tree logs**; edit the brief in `profile/` for your own niche.

## What it does

- **No text, logo or measurements on the image.** International viewers read the picture, nothing to translate. Labels A, B, C, D live only in file names.
- **3 to 5 standalone 16:9 images**, never a collage, never prompts instead of images.
- **Truly different concepts**: at least 3 real differences per image, always a different story and a different camera; recolors and recrops do not count.
- **Subject lock** on the reference (cut-end shape, cracks, bark, wood tones).
- **Size amplification 1 to 5**: say "bigger" or "scale level 4" and the skill increases perceived scale with camera angle, tiny workers and longer trailers, never fake numbers.
- **Honest Scene Match**: what the thumbnail promises must appear in the video. No video yet means `SCENE_MATCH_PENDING`, never a claimed insert.
- **Feedback loop**: records choices and issues (`too_small`, `same_concept`, `text_logo`, `missing_truck`) and suggests changes for the next batch without breaking hard rules.
- **Previews auto-delete after 5 hours**: only copies inside the skill's private vault, never your originals or approved exports.

## Install

**Claude.ai**: Customize, Skills, `+`, Create skill, Upload a skill. Zip `skills/thumbnail-first-scene-match` (the root folder in the ZIP must be named `thumbnail-first-scene-match`), upload and enable it. Attaching a ZIP to a chat does not install it.

**Claude Code**:

```bash
git clone https://github.com/ducdg88/youtube-thumbnail-scene-match-skill.git
cp -r youtube-thumbnail-scene-match-skill/skills/thumbnail-first-scene-match ~/.claude/skills/
pip install pillow   # for batch_qc.py
```

Other `SKILL.md` agents: copy that folder into the agent's skills directory. Start a new session so the skill is picked up.

## Usage

Once installed, send a photo or video and ask in plain language, no skill name needed:

> Put this tree log on a truck, make it colossal, give me 4 thumbnails.

Or call it explicitly:

> Use the `thumbnail-first-scene-match` skill. Create 4 text-free, logo-free 16:9 thumbnails of the same log from the reference photo carried on a multi-axle trailer; four different stories and camera angles. QA each image and plan the Scene Match.

Next turn, just react: "the log is still small", "B is the best", "they look the same", "there is text on it". The skill records the feedback and fixes exactly that, instead of regenerating everything.

The skill needs your agent's **AI image generator** to produce real images. Without one it says so and never pretends.

## How it works

1. Read `config/defaults.json`, the brief in `profile/` and earlier feedback.
2. Analyze source photos and video, keep an evidence ledger: real footage (`real_verified`) versus AI reconstruction (`ai_reconstruction`).
3. Pick 3 to 5 ideas with different stories and cameras (A rear close-up of the cut end, B whole convoy entering the yard, C low side view of the axles, D tractor turning into the gate, E ready to unload).
4. Generate each image with the always-on no-text prompt (`templates/NO_TEXT_BATCH_PROMPTS.md`).
5. QA every image: right subject, colossal, truly carried by the truck, 16:9, no text; check near-duplicates across the batch.
6. Deliver, explain the differences in the message (not on the image), then you pick or request edits.
7. Match the chosen image to a corresponding video scene with source and timecode.

## Bundled scripts

```bash
# 16:9 ratio and near-duplicate check (technical only, always review visually)
python skills/thumbnail-first-scene-match/scripts/batch_qc.py A.png B.png C.png D.png

# preview vault with 5-hour expiry (default ~/.thumbnail_first_scene_match/private_previews, override with THUMBNAIL_VAULT_DIR)
python skills/thumbnail-first-scene-match/scripts/preview_vault.py register A.png --concept A
python skills/thumbnail-first-scene-match/scripts/preview_vault.py status
python skills/thumbnail-first-scene-match/scripts/preview_vault.py cleanup

# feedback loop (default ~/.thumbnail_first_scene_match/feedback/feedback.json, override with THUMBNAIL_FEEDBACK_FILE)
python skills/thumbnail-first-scene-match/scripts/feedback_loop.py init
python skills/thumbnail-first-scene-match/scripts/feedback_loop.py record --run-id video-001 --concept A --decision revise --issue too_small --scale-level 3
python skills/thumbnail-first-scene-match/scripts/feedback_loop.py recommend --current-scale 3
```

On Windows, schedule the preview cleanup every 5 minutes (runs with `pythonw.exe`, so no console window flashes):

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\thumbnail-first-scene-match\scripts\install_windows_cleanup.ps1
```

Tests: `python skills/thumbnail-first-scene-match/tests/test_skill_contract.py` (plus `test_preview_vault.py`, `test_feedback_loop.py`).

## Adapt it to your niche

The bundled profile is about trucks hauling logs. For another niche, edit three files:
- `profile/SESSION_CREATIVE_BRIEF.md`: visual goal, required subject, past mistakes.
- `profile/creative_profile.json`: `required_scene`, `not_allowed`, subject traits to preserve.
- `templates/NO_TEXT_BATCH_PROMPTS.md`: the master constraint and 4 to 5 sample concepts.

The no-text, 16:9, standalone images, different story and camera, and honest Scene Match rules work for any niche.

## Limits

- `batch_qc.py` only checks ratio and pixel near-duplicates; it cannot tell whether an image has text or the right subject. Review visually.
- The skill does not guarantee avoiding claims or YouTube Partner Program approval; the video itself must add value. Realistic AI reconstructions may need a synthetic content disclosure in YouTube Studio.
- It cannot delete images already on a chat service or other devices; only the local preview vault is cleaned.
- Feedback persists across sessions only with durable file storage.

## About DUCPT

[DUCPT](https://ducpt.com/?utm_source=github&utm_medium=readme&utm_campaign=youtube-thumbnail-scene-match-skill) builds AI tools, automation workflows and training for creators, YouTube channels and small businesses in Vietnam:

- [DUCPT Skills](https://ducpt.com/skills/?utm_source=github&utm_medium=readme&utm_campaign=youtube-thumbnail-scene-match-skill): free Agent Skills for solo founders working with AI
- [YouTube Title Lab](https://ducpt.com/skills/youtube-title-lab/?utm_source=github&utm_medium=readme&utm_campaign=youtube-thumbnail-scene-match-skill): write and score YouTube titles to pair with thumbnails
- [YouTube source finder](https://ducpt.com/dich-vu/tim-nguon-youtube?utm_source=github&utm_medium=readme&utm_campaign=youtube-thumbnail-scene-match-skill): find video sources for a channel
- [Tab Cộng Đồng AI](https://ducpt.com/cong-cu-ai/tab-cong-dong-ai?utm_source=github&utm_medium=readme&utm_campaign=youtube-thumbnail-scene-match-skill): AI posts for the YouTube Community tab
- [Courses](https://ducpt.com/khoa-hoc/?utm_source=github&utm_medium=readme&utm_campaign=youtube-thumbnail-scene-match-skill): grow channels and run a business with AI

Channel identity skill (logo, avatar, banner): [youtube-channel-branding-skill](https://github.com/ducdg88/youtube-channel-branding-skill).

## License

[MIT](LICENSE).
