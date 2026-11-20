#!/usr/bin/env python3
"""Verify (or rewrite) MANIFEST.sha256 against the repository files. Standard library only.

Managed files = every regular file under the repository root except: MANIFEST.sha256 itself,
the .git directory, __pycache__ directories and *.pyc / *.pyo files.
Hashes are taken over raw bytes; .gitattributes keeps text files LF in every checkout.

  python tools/verify_manifest.py           # verify; exit 1 on any missing, extra or changed file
  python tools/verify_manifest.py --write   # regenerate after an intentional change
"""
import argparse
import hashlib
import sys
from pathlib import Path

MANIFEST = 'MANIFEST.sha256'
SKIP_DIRS = {'.git', '__pycache__'}
SKIP_SUFFIX = {'.pyc', '.pyo'}


def managed_files(root):
    out = []
    for p in root.rglob('*'):
        rel = p.relative_to(root)
        if not p.is_file() or set(rel.parts) & SKIP_DIRS or p.suffix in SKIP_SUFFIX:
            continue
        if rel.as_posix() == MANIFEST:
            continue
        out.append(rel.as_posix())
    return sorted(out)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(root):
    return {rel: digest(root / rel) for rel in managed_files(root)}


def read_manifest(path):
    entries = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        h, rel = line.split(None, 1)
        entries[rel.strip().lstrip('*')] = h
    return entries


def compare(expected, actual):
    errors = []
    for rel in sorted(set(actual) - set(expected)):
        errors.append(f'not in manifest: {rel}')
    for rel in sorted(set(expected) - set(actual)):
        errors.append(f'listed but missing: {rel}')
    for rel in sorted(set(expected) & set(actual)):
        if expected[rel] != actual[rel]:
            errors.append(f'hash mismatch: {rel}')
    return errors


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument('--write', action='store_true', help='rewrite MANIFEST.sha256 from current files')
    args = ap.parse_args(argv)
    root = args.root.resolve()
    actual = build(root)
    if args.write:
        (root / MANIFEST).write_text(''.join(f'{h}  {rel}\n' for rel, h in actual.items()), encoding='utf-8', newline='\n')
        print(f'wrote {MANIFEST}: {len(actual)} files')
        return 0
    if not (root / MANIFEST).is_file():
        print(f'FAIL: {MANIFEST} not found')
        return 1
    errors = compare(read_manifest(root / MANIFEST), actual)
    if errors:
        print('FAIL:')
        for e in errors:
            print(' -', e)
        print(f'If the change is intended, run: python tools/verify_manifest.py --write')
        return 1
    print(f'PASS: {len(actual)} managed files match {MANIFEST}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
