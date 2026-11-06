#!/usr/bin/env python3
"""Conservative technical QA for 3-5 16:9 thumbnails. This cannot test story originality.
Requires Pillow: pip install pillow
"""
import argparse
from itertools import combinations
from pathlib import Path
from PIL import Image


def dhash(filename):
    with Image.open(filename) as image:
        w, h = image.size
        image = image.convert('L').resize((9, 8))
        pixels = list(image.get_flattened_data() if hasattr(image, 'get_flattened_data') else image.getdata())
    bits = 0
    for row in range(8):
        for col in range(8):
            bits = (bits << 1) | int(pixels[row * 9 + col] > pixels[row * 9 + col + 1])
    return (bits, w, h)


def inspect(files):
    if not 3 <= len(files) <= 5:
        return {'status': 'BLOCK', 'reason': 'Need 3-5 images, not prompts only'}
    data = [dhash(path) for path in files]
    ratios = [{'image': Path(path).name, 'px': f'{w}x{h}', 'valid_16_9': abs((w/h) - (16/9)) < 0.03} for path, (_, w, h) in zip(files, data)]
    pairs = []
    for i, j in combinations(range(len(files)), 2):
        dist = (data[i][0] ^ data[j][0]).bit_count()
        pairs.append({'a': Path(files[i]).name, 'b': Path(files[j]).name, 'dhash_distance': dist, 'warn_near_duplicate': dist <= 6})
    status = 'REVISE' if any(not item['valid_16_9'] for item in ratios) or any(item['warn_near_duplicate'] for item in pairs) else 'TECHNICAL_PASS_ONLY'
    return {'status': status, 'ratios': ratios, 'pairs': pairs, 'manual_story_originality_required': True, 'manual_no_text_logo_watermark_review': 'PENDING_REVIEW', 'manual_truck_carries_log_review': 'PENDING_REVIEW', 'manual_reference_log_identity_review': 'PENDING_REVIEW', 'video_scene_match': 'SCENE_MATCH_PENDING'}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('images', nargs='+')
    a = p.parse_args()
    import json
    print(json.dumps(inspect(a.images), indent=2, ensure_ascii=False))
