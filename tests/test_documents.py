"""Format-independent lessons must work without PDF packages or TeX."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/omni-learning-anything/scripts'
sys.path.insert(0, str(SCRIPTS))
import omni_core as c
from PIL import Image


def course(root, delivery=None):
    (root / 'assets').mkdir()
    Image.new('RGB', (300, 90), 'teal').save(root / 'assets/figure.png')
    config = {'timezone': 'Asia/Shanghai', 'language': 'zh', 'daily_minutes': 15,
              'sample_mode': True}
    if delivery is not None:
        config['delivery'] = delivery
    plan = {'topic': '多格式学习', 'title': '中文学习计划 / Learning plan',
            'days': [{'day': 1, 'topic': '第一课'}],
            'sections': [{'title': '目标', 'body': '保留中文、证据和图片 [S1]。'},
                         {'title': '课程安排', 'body': 'Day01：第一课，理解学习方法。'}],
            'figure': {'path': 'assets/figure.png', 'caption': '学习流程图', 'credit': 'QA fixture'},
            'sources': [{'id': f'S{i}', 'title': f'参考 {i}', 'url': f'https://example.com/{i}',
                         'publisher': 'QA', 'published_at': 'N/A', 'checked_at': 'pending',
                         'note': '用于测试链接保留'} for i in range(1, 6)]}
    c.initialize(root, config, plan)
    for source in plan['sources']:
        source['checked_at'] = c.today(root)
    c.save(root / 'plan.json', plan)
    return plan


class DocumentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.plan = course(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def documents(self):
        self.assertIsNotNone(importlib.util.find_spec('omni_document'),
                             'Independent document export is not implemented')
        import omni_document
        return omni_document

    def test_exports_preserve_chinese_image_and_five_hyperlinks(self):
        d = self.documents()
        m = d.render(self.root, self.root / 'plan.json', 'plan', ['markdown', 'docx'])
        c.manifest_ok(self.root, m)
        md = (self.root / m['artifacts']['markdown']).read_text()
        self.assertIn('中文学习计划', md)
        self.assertIn('学习流程图', md)
        for i in range(1, 6):
            self.assertIn(f'https://example.com/{i}', md)
        from docx import Document
        doc = Document(self.root / m['artifacts']['docx'])
        self.assertIn('中文学习计划', '\n'.join(p.text for p in doc.paragraphs))
        self.assertEqual(len(doc.inline_shapes), 1)
        with ZipFile(self.root / m['artifacts']['docx']) as z:
            rels = z.read('word/_rels/document.xml.rels').decode()
            for i in range(1, 6):
                self.assertIn(f'https://example.com/{i}', rels)

    def test_markdown_export_does_not_import_pdf_packages(self):
        self.documents()
        code = '''import sys
class RejectPDF:
 def find_spec(self, fullname, path=None, target=None):
  if fullname.split('.')[0] in ('omni_pdf','pypdf','pypdfium2'): raise RuntimeError('PDF imported')
sys.meta_path.insert(0,RejectPDF())
from pathlib import Path
import omni_document as d
root=Path(sys.argv[1]); d.render(root,root/'plan.json','plan',['markdown'])
'''
        proc = subprocess.run([sys.executable, '-c', code, str(self.root)],
                              cwd=SCRIPTS, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_invalid_key_cannot_write_outside_project(self):
        d = self.documents()
        with self.assertRaises(ValueError):
            d.render(self.root, self.root / 'plan.json', '../escape', ['markdown'])
        self.assertFalse((self.root / 'manifests').exists())

    def test_source_validation_applies_without_pdf(self):
        d = self.documents()
        self.plan['sources'] = self.plan['sources'][:4]
        c.save(self.root / 'plan.json', self.plan)
        with self.assertRaisesRegex(ValueError, 'five'):
            d.render(self.root, self.root / 'plan.json', 'plan', ['markdown'])

    def test_render_does_not_overwrite_reviewed_plan(self):
        d = self.documents()
        d.render(self.root, self.root / 'plan.json', 'plan', ['markdown'])
        d.review(self.root, 'plan', 'Checked text, image and all source links')
        before = c.digest(self.root / 'manifests/plan.json')
        with self.assertRaises(ValueError):
            d.render(self.root, self.root / 'plan.json', 'plan', ['markdown'])
        self.assertEqual(c.digest(self.root / 'manifests/plan.json'), before)

    def test_manifest_detects_changed_image(self):
        d = self.documents()
        m = d.render(self.root, self.root / 'plan.json', 'plan', ['markdown'])
        asset = next(name for name in m['files'] if name.startswith('assets/figure-'))
        (self.root / asset).write_bytes(b'changed')
        with self.assertRaises(ValueError):
            d.review(self.root, 'plan', 'Cannot accept changed image')

    def test_unapproved_lesson_cannot_render(self):
        d = self.documents()
        lesson = dict(self.plan, day=1, title='第一课', reading_minutes=8, practice_minutes=3)
        c.save(self.root / 'data/Day01.json', lesson)
        with self.assertRaisesRegex(ValueError, 'approved'):
            d.render(self.root, self.root / 'data/Day01.json', 'Day01', ['markdown'])

    def test_lesson_time_budget_applies_to_all_formats(self):
        d = self.documents()
        d.render(self.root, self.root / 'plan.json', 'plan', ['markdown'])
        d.review(self.root, 'plan', 'Checked plan'); c.approve(self.root)
        lesson = dict(self.plan, day=1, title='第一课', reading_minutes=13, practice_minutes=3)
        c.save(self.root / 'data/Day01.json', lesson)
        with self.assertRaisesRegex(ValueError, 'time budget'):
            d.render(self.root, self.root / 'data/Day01.json', 'Day01', ['docx'])
        self.assertFalse((self.root / 'manifests/Day01.json').exists())

    def test_docx_failure_does_not_accept_partial_export(self):
        d = self.documents()
        with patch.object(d, 'write_docx', side_effect=RuntimeError('export failed')):
            with self.assertRaises(RuntimeError):
                d.render(self.root, self.root / 'plan.json', 'plan', ['markdown', 'docx'])
        self.assertFalse((self.root / 'manifests/plan.json').exists())


if __name__ == '__main__':
    unittest.main()
