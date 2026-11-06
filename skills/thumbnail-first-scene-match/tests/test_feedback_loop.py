"""Run: python tests/test_feedback_loop.py"""
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from feedback_loop import record, read_state, summarize, HARD_RULES


def test_feedback_loop():
    with TemporaryDirectory() as folder:
        state = Path(folder) / 'feedback.json'
        no_feedback = summarize(read_state(state))
        assert no_feedback['status'] == 'NEEDS_USER_FEEDBACK'
        record(state, run_id='demo-001', concept='A', decision='revise', issues=['too_small'],
               scale_level=3, story='log_on_truck', camera='rear_low', notes='Cây còn nhỏ')
        record(state, run_id='demo-001', concept='B', decision='rejected', issues=['same_concept'],
               scale_level=3, story='same_log_on_truck', camera='rear_low')
        record(state, run_id='demo-001', concept='C', decision='selected',
               scale_level=3, story='wide_sawmill_arrival', camera='high_wide', rating=5)
        report = summarize(read_state(state), current_scale=3)
        assert report['suggested_scale_level'] == 4, report
        assert report['issue_counts']['same_concept'] == 1
        assert report['favored_story_signals'][0]['story'] == 'wide_sawmill_arrival'
        assert report['hard_rules_locked'] == list(HARD_RULES)
        assert len(read_state(state)['events']) == 3
        assert summarize(read_state(state), current_scale=5)['suggested_scale_level'] == 5
        # The feedback journal must never delete source/preview files.
        original = Path(folder) / 'original.png'
        original.write_bytes(b'test-file')
        summarize(read_state(state))
        assert original.read_bytes() == b'test-file'
    print('PASS: feedback recorded, scale adapted, story selected, safety rules locked')


if __name__ == '__main__':
    test_feedback_loop()
