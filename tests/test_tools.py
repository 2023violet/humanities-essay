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
        self.assertIn('version: "3.1.0"',text)
        self.assertIn('license: Apache-2.0',text)


if __name__ == '__main__': unittest.main()
