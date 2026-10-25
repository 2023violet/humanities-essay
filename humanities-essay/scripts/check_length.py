#!/usr/bin/env python3
"""Count publishable text length conservatively (UTF-16 code units).

The remote platform's counting rules may differ; its editor is authoritative.
"""
import argparse
from pathlib import Path


def count_text(text):
    normalized = text.replace('\r\n', '\n').replace('\r', '\n')
    return {'codepoints': len(normalized), 'utf16_units': len(normalized.encode('utf-16-le')) // 2,
            'newlines': normalized.count('\n')}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path, nargs='?', help='UTF-8 plain text post (not Markdown wrapper)')
    parser.add_argument('--min', dest='minimum', type=int, default=0)
    parser.add_argument('--max', dest='maximum', type=int, default=3000)
    args = parser.parse_args(argv)
    if not args.path:
        parser.print_help()
        return 0
    if args.minimum < 0 or args.maximum < args.minimum:
        parser.error('require 0 <= --min <= --max')
    try:
        data = args.path.read_text(encoding='utf-8-sig')
    except (OSError, UnicodeError) as exc:
        parser.error(f'cannot read UTF-8 text: {exc}')
    m = count_text(data)
    n = m['utf16_units']
    print(f"Unicode code points: {m['codepoints']}; UTF-16 code units: {n}; newlines: {m['newlines']}")
    print(f"Allowed inclusive range: {args.minimum}–{args.maximum}")
    if not args.minimum <= n <= args.maximum:
        print('FAIL: exceeds or falls short of this local preflight range')
        return 1
    print('PASS: local preflight only; check the platform editor before posting')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
