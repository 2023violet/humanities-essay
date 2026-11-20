"""Deterministic tests of local helper scripts; no model/network evaluation."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'humanities-essay'


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


length = load('check_length', SKILL/'scripts'/'check_length.py')
metrics = load('metrics_report', SKILL/'scripts'/'metrics_report.py')
hedges = load('check_hedges', SKILL/'scripts'/'check_hedges.py')


class LengthTests(unittest.TestCase):
    def test_chinese_punctuation_and_line_endings(self):
        self.assertEqual(length.count_text('甲。\r\n乙'), {'codepoints': 4, 'utf16_units': 4, 'newlines': 1})

    def test_emoji_more_conservative(self):
        self.assertEqual(length.count_text('A😀')['utf16_units'], 3)
        self.assertEqual(length.count_text('A😀')['codepoints'], 2)

    def test_boundary_inclusive(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'post.txt'
            p.write_text('中'*2500, encoding='utf8')
            self.assertEqual(length.main([str(p), '--min', '2500', '--max', '3000']), 0)
            p.write_text('中'*3001, encoding='utf8')
            self.assertEqual(length.main([str(p), '--min', '2500', '--max', '3000']), 1)

    def test_bom_and_crlf(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'post.txt'; p.write_bytes(b'\xef\xbb\xbfA\r\nB')
            self.assertEqual(length.main([str(p), '--max', '3']), 0)


class MetricsTests(unittest.TestCase):
    def test_empty_template(self):
        self.assertEqual(metrics.report(SKILL/'assets'/'metrics-template.csv'), [])

    def test_zero_missing_and_percentages(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'metric.csv'
            p.write_text('title,views,likes,comments,shares,saves,followers\nA,100,7,2,1,5,\nB,0,0,0,0,0,0\n',encoding='utf8')
            rows = metrics.report(p)
            self.assertEqual(rows[0][2]['likes'], '7.00%')
            self.assertEqual(rows[0][2]['followers'], 'NA')
            self.assertEqual(rows[1][2]['likes'], 'NA')

    def test_invalid_negative_or_non_numeric(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv'
            p.write_text('title,views,likes,comments,shares,saves,followers\nA,10,-1,0,0,0,0\n',encoding='utf8')
            with self.assertRaises(ValueError): metrics.report(p)
            p.write_text('title,views,likes,comments,shares,saves,followers\nA,ten,1,0,0,0,0\n',encoding='utf8')
            with self.assertRaises(ValueError): metrics.report(p)


class StructureTests(unittest.TestCase):
    def test_skill_structure_and_refs(self):
        result = subprocess.run([sys.executable, str(SKILL/'scripts'/'quick_validate.py'), str(SKILL)],capture_output=True,text=True)
        self.assertEqual(result.returncode, 0, result.stdout+'\n'+result.stderr)

    def test_frontmatter_version_and_name(self):
        text = (SKILL/'SKILL.md').read_text(encoding='utf8')
        self.assertTrue(text.startswith('---\nname: humanities-essay\n'))
        self.assertIn('version: "3.4.0"',text)
        self.assertIn('license: Apache-2.0',text)




class HedgeAndRhythmTests(unittest.TestCase):
    """check_hedges.py is a prompt for editors, not a quality score."""

    def run_on(self, text):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'draft.txt'
            p.write_text(text, encoding='utf8')
            return hedges.main([str(p)])

    def test_footnote_and_hashtags_excluded(self):
        body = hedges.split_body('他走了。\n…\n注：史书没有记载此事，既不能确定也不能否认。\n#标签')
        self.assertEqual(body, ['他走了。'])

    def test_disclaimer_lines_counted_per_line(self):
        body = ['既不能因为结局惋惜就抹去记载；也不能把叙述当成全部真相。', '《史记》没有记下他的心情。', '他转身走了。']
        _, hits, _ = hedges.analyze(body)
        self.assertEqual(len(hits), 2)

    def test_budget_warns_above_one_disclaimer(self):
        clean = '曹操亲自去接妻子回家。\n妻子坐在织布机前，听说他来了，连身子都没转一下，他只好退到门外，又问了一句。\n'
        self.assertEqual(self.run_on(clean), 0)
        heavy = clean + '史书没有记载他的想法。\n我们不能假装知道全部真相。\n'
        self.assertEqual(self.run_on(heavy), 1)

    def test_rhythm_flags_choppy_verdict_lines(self):
        body = ['这是萧何。', '这句话很重。', '这是真的。', '这才是答案。', '其实不难。', '原来如此。', '他走了。']
        r = hedges.rhythm(body)
        self.assertGreater(r['per100'], 4.5)
        self.assertLess(r['avg'], 22)
        self.assertEqual(len(r['judge']), 6)

    def test_rhythm_flowing_paragraph_is_quiet(self):
        body = ['张绣恨透了，没过多久就突然发兵偷袭，曹操仓皇往外逃，坐骑绝影又中了流矢，就在这时候，曹昂把自己的马让给了父亲。']
        r = hedges.rhythm(body)
        self.assertLessEqual(r['per100'], 4.5)
        self.assertGreaterEqual(r['avg'], 22)
        self.assertEqual(r['judge'], [])


# Documentary guardrails are static assertions; they do not substitute for model evaluation.
class EditorialContractTests(unittest.TestCase):
    def test_three_tier_language_contract(self):
        text = (SKILL/'references'/'rhythm-and-line-editing.md').read_text(encoding='utf8')
        for phrase in ('规范正确性', '语流自然性', '文学表现力', '禁止', '句号', '流水句'):
            self.assertIn(phrase, text)

    def test_reader_engagement_contract(self):
        text = (SKILL/'references'/'reader-engagement.md').read_text(encoding='utf8')
        for phrase in ('一句话测试', '前三行', '反证放置', '情绪峰值', '文末注'):
            self.assertIn(phrase, text)

    def test_provenance_and_consent_contract(self):
        text = (SKILL/'references'/'first-person-and-era-essays.md').read_text(encoding='utf8')
        for phrase in ('P｜本人亲述', 'O｜可查的外部事实', 'H｜解释', 'X｜缺失', '作者确认'):
            self.assertIn(phrase, text)

    def test_revision_stop_and_locked_ending(self):
        text = (SKILL/'references'/'revision-governance.md').read_text(encoding='utf8')
        self.assertIn('AUTHOR_READY', text)
        self.assertIn('结尾', text)
        self.assertIn('不再生成 Vn', text)

    def test_required_reference_missing_is_failure(self):
        import shutil
        with tempfile.TemporaryDirectory() as d:
            clone = Path(d)/'humanities-essay'
            shutil.copytree(SKILL, clone, ignore=shutil.ignore_patterns('__pycache__'))
            (clone/'references'/'rhythm-and-line-editing.md').unlink()
            proc = subprocess.run([sys.executable, str(SKILL/'scripts'/'quick_validate.py'), str(clone)], capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('Missing required file', proc.stdout)

if __name__ == '__main__': unittest.main()
