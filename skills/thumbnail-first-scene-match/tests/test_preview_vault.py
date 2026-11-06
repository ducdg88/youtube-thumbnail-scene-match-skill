"""Run: python tests/test_preview_vault.py (no third-party libraries)."""
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime, timedelta, timezone
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from preview_vault import register_image, cleanup, load_manifest, safe_owned_path


def test_ttl():
    with TemporaryDirectory() as folder:
        root = Path(folder)
        source = root / 'original.png'
        source.write_bytes(b'\x89PNG\r\n\x1a\nLOCAL_TEST_CONTENT')
        vault = root / 'vault'
        now = datetime(2026, 11, 6, 3, 0, tzinfo=timezone.utc)
        old = register_image(source, vault, concept='A', now=now - timedelta(hours=6))
        fresh = register_image(source, vault, concept='B', now=now)
        assert source.exists(), 'Never delete original'
        # The second register invokes cleanup: old copy should already have expired.
        assert len(load_manifest(vault)['assets']) == 1
        assert load_manifest(vault)['assets'][0]['id'] == fresh['id']
        path = safe_owned_path(vault, fresh['managed_filename'])
        assert path and path.exists(), 'Unexpired copy must be kept'
        report = cleanup(vault, now=now + timedelta(hours=5, minutes=1))
        assert len(report['deleted']) == 1, report
        assert not path.exists(), 'Expired copy must be removed'
        assert source.exists(), 'Original must still exist'
        assert len(load_manifest(vault)['assets']) == 0
    print('PASS: expiring copies are deleted; fresh previews and original inputs protected.')


if __name__ == '__main__':
    test_ttl()
