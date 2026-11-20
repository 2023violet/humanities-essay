#!/usr/bin/env python3
"""Flag disclaimer-style hedging and rhythm hints in the BODY of a Chinese essay (reader-engagement layer).

Strong = 免责式限定 that interrupt narrative (budget: <= 1 in body).
Weak   = ordinary hedges; reported as density per 1000 chars (warn above 3.0).
Text after a footnote marker line (注：/附注/来源/参考) and hashtag lines are excluded.
This is a prompt for a human editor, not a judgment of literary quality.
"""
import argparse
import re
import sys
from pathlib import Path

STRONG = [
    r'既不能[^。！？\n]*也不能', r'不能假装', r'可同样不能', r'也不能因为', r'不能因为',
    r'无从知道', r'难以彻底还原', r'难以还原', r'已无法独立证实',
    r'(史书|《史记》|史料|书中|电视剧)[^。！？\n]{0,6}没有(记载|记下|交代|说明|留下)',
    r'我们(也)?不能', r'不能把[^。！？\n]{0,20}(当成|当作|归功|归给)',
    r'并不(能)?意味着', r'不意味着', r'这不是一个[^。！？\n]{0,20}(故事|寓言)',
    r'这只是[^。！？\n]{0,12}(推测|判断|叙述)',
    r'(并)?不是一(个|件|种)[^。！？\n]{0,25}(故事|寓言)', r'轻轻带过', r'抹成',
    r'谁都不能', r'不能凭', r'来自传世史书', r'不能替[^。！？\n]{0,10}(洗清|开脱|抵消)',
]
WEAK = r'未必|恐怕|也许|或许|大概|不必|不等于|难以|当然|似乎'
FOOTNOTE = re.compile(r'^\s*(注[:：]|附注|来源[:：]|参考[:：]|【注】)')
SEPARATORS = {'…', '...', '……', '.'}


def split_body(text):
    lines = text.replace('\r\n', '\n').split('\n')
    body = []
    for line in lines:
        if FOOTNOTE.match(line):
            break
        if line.strip().startswith('#') or line.strip() in SEPARATORS or not line.strip():
            continue
        body.append(line.strip())
    return body


def analyze(body):
    text = '\n'.join(body)
    hits = []
    for i, line in enumerate(body, 1):
        found = sorted({m.group(0) for p in STRONG for m in re.finditer(p, line)})
        if found:
            hits.append((i, line, found))
    weak = len(re.findall(WEAK, text))
    return text, hits, weak


HAN = re.compile(r'[一-鿿]')
JUDGE_START = re.compile(r'^(这是|那是|这才|这就是|这便是|原来|其实|也许|或许|只是|不是|并不|真正|所以|可这|但这|这句话|这件事|这一次|他终于|我们)')
JUDGE_END = re.compile(r'(是[^，、]{1,6}|而已|罢了|不是[^，、]{1,6})$')


def rhythm(body):
    """Descriptive rhythm hints (reader-engagement §6 / rhythm-and-line-editing §0). Not a score."""
    text = ''.join(body)
    han = len(HAN.findall(text)) or 1
    periods = text.count('。')
    sents = [x for x in re.split(r'[。！？…]+', text) if HAN.search(x)]
    avg = sum(len(HAN.findall(x)) for x in sents) / max(len(sents), 1)
    judge_lines = []
    for i, line in enumerate(body, 1):
        core = line.strip('“”"')
        parts = [x for x in re.split(r'[。！？]', core) if HAN.search(x)]
        if len(parts) == 1 and len(HAN.findall(core)) <= 14:
            c = parts[0].strip('“”"')
            if JUDGE_START.search(c) or JUDGE_END.search(c):
                judge_lines.append((i, line))
    return {'per100': periods / han * 100, 'avg': avg,
            'comma_ratio': text.count('，') / max(periods, 1), 'judge': judge_lines}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('paths', type=Path, nargs='+', help='UTF-8 plain-text drafts')
    ap.add_argument('--strong-max', type=int, default=1)
    ap.add_argument('--weak-max', type=float, default=3.0, help='weak hedges per 1000 chars')
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    worst = 0
    for path in args.paths:
        try:
            raw = path.read_text(encoding='utf-8-sig')
        except (OSError, UnicodeError) as exc:
            print(f'== {path}: cannot read UTF-8 ({exc})')
            worst = 2
            continue
        body = split_body(raw)
        if not body:
            print(f'== {path}: empty body')
            continue
        text, hits, weak = analyze(body)
        density = weak / max(len(text), 1) * 1000
        strong_n = len(hits)  # count sentences/lines, not distinct phrases
        status = 'PASS'
        if strong_n > args.strong_max or density > args.weak_max:
            status = 'WARN'
            worst = max(worst, 1)
        print(f'== {path.name}  [{status}]  正文 {len(text)} 字')
        print(f'  免责式限定: {strong_n} 行 (预算 ≤{args.strong_max})')
        print(f'  一般对冲词: {density:.1f}/千字 (预算 ≤{args.weak_max})')
        for i, line, found in hits:
            snippet = line if len(line) <= 60 else line[:60] + '…'
            print(f'    L{i} [{"/".join(found)}] {snippet}')
        r = rhythm(body)
        flags = []
        if r['per100'] > 4.5: flags.append('句号偏密')
        if r['avg'] < 22: flags.append('句子偏短')
        if r['comma_ratio'] < 1.4: flags.append('逗号偏少')
        if len(r['judge']) > 5: flags.append('判词行偏多')
        if r['per100'] < 2.5 or r['avg'] > 32: flags.append('可能矫枉过正、句子过长')
        if len(HAN.findall(body[0])) > 30: flags.append('首行过长，信息流里露不全')
        print(f"  节奏提示[{'、'.join(flags) or '无'}]: 句号 {r['per100']:.1f}/百字 (≈3–4.5) · 平均句长 {r['avg']:.1f} 字 (≥22) · 逗号:句号 {r['comma_ratio']:.2f} (≥1.4) · 单独成行判断短句 {len(r['judge'])} (≤5)")
        for i, line in r['judge'][:8]:
            print(f'    判词 L{i} | {line[:40]}')
        if flags:
            print('    → 只是提示：说书体可突破句号指标；处理方法是重新说一遍（流水句），不要机械换标点。见 rhythm-and-line-editing.md §0')
        print('  前三行（检查：人／动作／反差；不以问题开头）:')
        for line in body[:3]:
            print(f'    | {line[:70]}')
        if body[0].rstrip().endswith(('？', '?')):
            print('    ! 首行是问句：考虑先放场景，再提问题')
        print(f'  末行（检查：交给读者／意象变义；不以史实收尾）:\n    | {body[-1][:70]}')
    if worst == 1:
        print('\nWARN: 把免责式限定移到文末注（以“注：”开头的行之后不计入）或置顶评论；见 references/reader-engagement.md §4')
    return worst


if __name__ == '__main__':
    raise SystemExit(main())
