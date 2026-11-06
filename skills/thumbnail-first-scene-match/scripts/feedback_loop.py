#!/usr/bin/env python3
"""Local, explicit-feedback learning loop for Thumbnail First -> Scene Match.

Records user-provided feedback and suggests next-batch changes. Python stdlib only.
No background process, no autonomous model training, no modifying policy hard rules.

State is kept OUTSIDE the expiring preview vault. Configure with:
  THUMBNAIL_FEEDBACK_FILE=path/to/feedback.json
or --state path/to/feedback.json.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
import uuid

DEFAULT_STATE = Path(os.getenv('THUMBNAIL_FEEDBACK_FILE', str(Path.home() / '.thumbnail_first_scene_match' / 'feedback' / 'feedback.json'))).expanduser()
DECISIONS = ('selected', 'rejected', 'revise', 'published')
ISSUES = (
    'too_small', 'too_large', 'wrong_log', 'missing_truck', 'floating_log',
    'text_logo', 'same_concept', 'wrong_style', 'not_16_9', 'scene_mismatch', 'other'
)
HARD_RULES = (
    '3-5 independent thumbnails per batch, default 4',
    '16:9, no text/numbers/logos/watermarks on thumbnail',
    'truck carrying recognizable reference log with plausible supports',
    'meaningful concept diversity; no spam/duplicate templates',
    'thumbnail-video scene match must be evidenced, otherwise pending',
    'only locally managed preview copies eligible for 5-hour cleanup',
)


def new_state():
    return {'schema_version': 1, 'events': [], 'hard_rules': list(HARD_RULES)}


def read_state(path: Path):
    if not path.exists():
        return new_state()
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or data.get('schema_version') != 1 or not isinstance(data.get('events'), list):
        raise ValueError('Unsupported or invalid feedback state')
    return data


def save_state(path: Path, data: dict):
    path = path.expanduser().absolute()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='._feedback_', suffix='.json', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def record(path: Path, *, run_id: str, concept: str, decision: str, issues=(),
           scale_level: int = 3, story: str = '', camera: str = '', rating=None,
           notes: str = ''):
    if not 1 <= scale_level <= 5:
        raise ValueError('scale_level must be 1-5')
    if decision not in DECISIONS:
        raise ValueError(f'decision must be one of {DECISIONS}')
    if not run_id or not concept:
        raise ValueError('run_id and concept are required')
    invalid = set(issues) - set(ISSUES)
    if invalid:
        raise ValueError(f'Unknown issue codes: {sorted(invalid)}')
    if rating is not None and not (1 <= rating <= 5):
        raise ValueError('rating must be 1-5')
    if len(notes) > 1000:
        raise ValueError('notes must be <=1000 characters')
    if len(run_id) > 128 or len(concept) > 64 or len(story) > 128 or len(camera) > 128:
        raise ValueError('One of the identifiers is too long')
    data = read_state(path)
    ev = {
        'id': uuid.uuid4().hex,
        'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
        'run_id': run_id,
        'concept': concept,
        'decision': decision,
        'issues': sorted(set(issues)),
        'scale_level': scale_level,
        'story': story,
        'camera': camera,
        'rating': rating,
        'notes': notes,
    }
    data['events'].append(ev)
    save_state(path, data)
    return ev


def summarize(data: dict, current_scale=3, window=50):
    if not 1 <= current_scale <= 5:
        raise ValueError('current_scale must be 1-5')
    events = data['events'][-window:]
    issues = Counter(issue for ev in events for issue in ev.get('issues', []))
    decisions = Counter(ev.get('decision') for ev in events)
    by_story = defaultdict(lambda: {'selected': 0, 'rejected': 0, 'revise': 0, 'published': 0})
    for ev in events:
        story = ev.get('story')
        if story:
            by_story[story][ev['decision']] += 1
    # Only recommend increasing scale if there is explicit feedback, never infer it from clicks.
    desired_scale = current_scale
    if issues['too_small'] > issues['too_large'] and issues['too_small'] >= 1:
        desired_scale = min(5, current_scale + 1)
    elif issues['too_large'] > issues['too_small'] and issues['too_large'] >= 1:
        desired_scale = max(1, current_scale - 1)
    suggestions = []
    issues_to_actions = {
        'missing_truck': 'Reject images where the complete connected truck/trailer is not visibly carrying the log.',
        'floating_log': 'Make the log visibly rest on trailer saddles; do not treat a crane-suspended log as truck transport.',
        'wrong_log': 'Improve identity lock to preserve the reference cut face, bark and existing cracks.',
        'text_logo': 'Regenerate without words, numbers, logos, signs or watermarks; run visual QA.',
        'same_concept': 'Change BOTH story/action and camera/composition, not merely crop or color.',
        'too_small': 'Increase perceived log scale with camera perspective, small workers and longer plausible trailer.',
        'too_large': 'Reduce exaggeration while retaining an impressive, realistic load.',
        'not_16_9': 'Export each image independently in 16:9.',
        'scene_mismatch': 'Plan matching video footage; report pending if no verified shot exists.',
        'wrong_style': 'Use realistic industrial documentary aesthetics, not fantasy/infographic.',
    }
    for issue, n in issues.most_common():
        if issue in issues_to_actions:
            suggestions.append({'issue': issue, 'count': n, 'action': issues_to_actions[issue]})
    favored_stories = sorted(
        [{'story': story, **counts} for story, counts in by_story.items() if counts['selected'] or counts['published']],
        key=lambda d: (d['selected'] + d['published'] - d['rejected'], d['selected']), reverse=True
    )[:3]
    return {
        'feedback_events_considered': len(events),
        'decisions': dict(decisions),
        'issue_counts': dict(issues),
        'current_scale_level': current_scale,
        'suggested_scale_level': desired_scale,
        'suggestions': suggestions[:6],
        'favored_story_signals': favored_stories,
        'must_still_explore_distinct_concepts': True,
        'hard_rules_locked': list(HARD_RULES),
        'status': 'FEEDBACK_AVAILABLE' if events else 'NEEDS_USER_FEEDBACK',
        'caveat': 'Recommendations only; user requests override soft preferences. No background learning, no remote file deletion or YPP guarantee.'
    }


def main():
    parser = argparse.ArgumentParser(description='Record and learn from explicit thumbnail feedback (local only).')
    parser.add_argument('--state', default=str(DEFAULT_STATE), help='Persistent feedback JSON outside temporary preview vault')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init', help='Initialize empty feedback journal if absent')
    rec = sub.add_parser('record', help='Record a real user selection or revision request')
    rec.add_argument('--run-id', required=True)
    rec.add_argument('--concept', required=True)
    rec.add_argument('--decision', required=True, choices=DECISIONS)
    rec.add_argument('--issue', action='append', default=[], choices=ISSUES)
    rec.add_argument('--scale-level', type=int, default=3)
    rec.add_argument('--story', default='')
    rec.add_argument('--camera', default='')
    rec.add_argument('--rating', type=int)
    rec.add_argument('--notes', default='')
    summ = sub.add_parser('recommend', help='Recommend next-batch changes from recorded feedback')
    summ.add_argument('--current-scale', type=int, default=3)
    summ.add_argument('--window', type=int, default=50)
    args = parser.parse_args()
    path = Path(args.state).expanduser()
    try:
        if args.command == 'init':
            if not path.exists():
                save_state(path, new_state())
            output = {'initialized': True, 'path': str(path), 'events': len(read_state(path)['events'])}
        elif args.command == 'record':
            output = record(path, run_id=args.run_id, concept=args.concept,
                            decision=args.decision, issues=args.issue, scale_level=args.scale_level,
                            story=args.story, camera=args.camera, rating=args.rating, notes=args.notes)
        else:
            if args.window < 1:
                raise ValueError('window must be >= 1')
            output = summarize(read_state(path), current_scale=args.current_scale, window=args.window)
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f'ERROR: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
