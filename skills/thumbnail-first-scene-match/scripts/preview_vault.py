#!/usr/bin/env python3
"""Local-only preview retention: copies thumbnails to a managed vault and deletes
managed copies after 5h. Never modifies source images or remote media.
Python 3.9+ stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

DEFAULT_VAULT = Path(os.getenv('THUMBNAIL_VAULT_DIR', str(Path.home() / '.thumbnail_first_scene_match' / 'private_previews'))).expanduser()
TTL = timedelta(hours=5)
ALLOWED_EXT = {'.png', '.jpg', '.jpeg', '.webp'}


def utcnow():
    return datetime.now(timezone.utc)


def parse_dt(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('Timezone-aware UTC timestamp required')
    return result.astimezone(timezone.utc)


def utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def vault_paths(vault: Path):
    vault = vault.expanduser().absolute()
    return vault, vault / 'images', vault / 'manifest.json'


def initialize(vault: Path) -> None:
    root, images, _ = vault_paths(vault)
    if root.is_symlink() or images.is_symlink():
        raise ValueError('Symlinked vault directory is forbidden')
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    images.mkdir(mode=0o700, parents=True, exist_ok=True)
    for directory in (root, images):
        try: directory.chmod(0o700)
        except OSError: pass


def load_manifest(vault: Path):
    _, _, file = vault_paths(vault)
    if not file.exists():
        return {'schema': 1, 'ttl_hours': 5, 'assets': []}
    data = json.loads(file.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or not isinstance(data.get('assets'), list):
        raise ValueError('Invalid manifest structure')
    return data


def save_manifest(vault: Path, data: dict):
    root, _, file = vault_paths(vault)
    fd, temp = tempfile.mkstemp(prefix='._manifest_', suffix='.json', dir=str(root))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temp, 0o600)
        os.replace(temp, file)
    finally:
        if os.path.exists(temp): os.unlink(temp)


def safe_owned_path(vault: Path, name: str) -> Optional[Path]:
    if Path(name).name != name or name in {'.', '..'}:
        return None
    _, images, _ = vault_paths(vault)
    path = images / name
    if path.is_symlink(): return None
    # Only direct children of the internally managed folder are eligible.
    if path.parent != images: return None
    return path


def register_image(source: Path, vault: Path = DEFAULT_VAULT, *, concept: str = 'A', now: Optional[datetime] = None):
    now = now or utcnow()
    if now.tzinfo is None: raise ValueError('now must have timezone')
    source = Path(source).expanduser().absolute()
    if not source.is_file() or source.is_symlink():
        raise ValueError(f'Missing or symlinked source: {source}')
    ext = source.suffix.lower()
    if ext not in ALLOWED_EXT:
        raise ValueError(f'Unsupported thumbnail image extension: {ext}')
    initialize(vault)
    cleanup(vault, now=now)
    asset_id = uuid.uuid4().hex
    owned_name = f'{asset_id}{ext}'
    dst = safe_owned_path(vault, owned_name)
    assert dst is not None
    shutil.copyfile(source, dst)
    try: dst.chmod(0o600)
    except OSError: pass
    digest = hashlib.sha256(dst.read_bytes()).hexdigest()
    record = {
        'id': asset_id,
        'concept': concept.upper(),
        'managed_filename': owned_name,
        'sha256': digest,
        'created_utc': utc_iso(now),
        'expires_utc': utc_iso(now + TTL),
        'rights_review': 'required',
        'scene_match': 'pending',
    }
    manifest = load_manifest(vault)
    manifest['assets'].append(record)
    save_manifest(vault, manifest)
    return record


def cleanup(vault: Path = DEFAULT_VAULT, *, now: Optional[datetime] = None):
    now = now or utcnow()
    if now.tzinfo is None: raise ValueError('now must have timezone')
    initialize(vault)
    manifest = load_manifest(vault)
    kept, deleted, skipped_unsafe = [], [], []
    for record in manifest['assets']:
        try:
            expires = parse_dt(record['expires_utc'])
            name = record['managed_filename']
        except (KeyError, ValueError, TypeError):
            skipped_unsafe.append(record.get('id', 'unknown'))
            kept.append(record)
            continue
        if now < expires:
            kept.append(record)
            continue
        path = safe_owned_path(vault, name)
        if path is None:
            skipped_unsafe.append(record.get('id', name))
            kept.append(record)
            continue
        if path.exists():
            if not path.is_file():
                skipped_unsafe.append(record.get('id', name))
                kept.append(record)
                continue
            path.unlink()
        deleted.append({'id': record.get('id'), 'concept': record.get('concept'), 'name': name})
    if len(kept) != len(manifest['assets']):
        manifest['assets'] = kept
        save_manifest(vault, manifest)
    return {'deleted': deleted, 'kept': len(kept), 'skipped_unsafe': skipped_unsafe}


def status(vault: Path = DEFAULT_VAULT):
    cleanup(vault)
    return load_manifest(vault)


def main():
    parser = argparse.ArgumentParser(description='Manage thumbnail previews with a five-hour retention limit.')
    parser.add_argument('--vault', default=str(DEFAULT_VAULT), help='Private folder containing ONLY managed previews')
    sub = parser.add_subparsers(dest='cmd', required=True)
    reg = sub.add_parser('register', help='Copy a thumbnail into the expiring private vault')
    reg.add_argument('image', help='Path of thumbnail image; original will NOT be deleted')
    reg.add_argument('--concept', default='A', help='Concept label A-E')
    sub.add_parser('cleanup', help='Remove managed copies past their expiration UTC')
    sub.add_parser('status', help='List unexpired managed previews')
    args = parser.parse_args()
    vault = Path(args.vault)
    try:
        if args.cmd == 'register':
            result = register_image(Path(args.image), vault, concept=args.concept)
        elif args.cmd == 'cleanup':
            result = cleanup(vault)
        else:
            result = status(vault)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
