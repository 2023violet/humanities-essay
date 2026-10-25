#!/usr/bin/env python3
"""Summarize creator-provided aggregate metrics without network access.

Ratios use views as a proxy denominator; they are not causal effects.
"""
import argparse
import csv
from pathlib import Path

METRICS = ('likes', 'comments', 'shares', 'saves', 'followers')
NEEDED = ('title', 'views') + METRICS


def positive_int(value, col, row):
    if value == '':
        return None
    if not value.isdecimal():
        raise ValueError(f'row {row}: {col} must be a nonnegative integer or blank')
    return int(value)


def report(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or any(k not in reader.fieldnames for k in NEEDED):
            raise ValueError('CSV must include ' + ', '.join(NEEDED))
        result = []
        for idx, line in enumerate(reader, 2):
            title = (line.get('title') or '').strip()
            if not title:
                raise ValueError(f'row {idx}: missing title')
            views = positive_int((line.get('views') or '').strip(), 'views', idx)
            if views is None:
                raise ValueError(f'row {idx}: missing views')
            numbers = {k: positive_int((line.get(k) or '').strip(), k, idx) for k in METRICS}
            def ratio(x):
                if views == 0 or x is None:
                    return 'NA'
                return f'{x / views * 100:.2f}%'
            result.append((title, views, {k: ratio(v) for k, v in numbers.items()}))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file', type=Path, nargs='?', help='UTF-8 CSV of aggregate metrics')
    args = parser.parse_args(argv)
    if not args.csv_file:
        parser.print_help()
        return 0
    try:
        rows = report(args.csv_file)
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        parser.error(str(exc))
    if not rows:
        print('NO_DATA: template has header only')
        return 0
    print('title\tviews\tlike%\tcomment%\tshare%\tsave%\tfollow%')
    for title, views, r in rows:
        print('\t'.join([title, str(views)] + [r[k] for k in METRICS]))
    print('NOTE: views are a proxy denominator; compare publication age and exposure before interpreting rates.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
