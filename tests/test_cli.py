"""Subprocess CLI checks exercise installation and course delivery end to end."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from test_documents import course
import omni_core as c

CLI = Path(__file__).resolve().parents[1] / 'skills/omni-learning-anything/scripts/omni_learning.py'


class CLITests(unittest.TestCase):
    def invoke(self, root, *args, success=True):
        p = subprocess.run([sys.executable, str(CLI), '--project', str(root), *args], capture_output=True, text=True)
        if success:
            self.assertEqual(p.returncode, 0, p.stderr)
            return json.loads(p.stdout)
        self.assertNotEqual(p.returncode, 0)
        return json.loads(p.stderr)

    def test_cli_reports_skill_version(self):
        p = subprocess.run([sys.executable, str(CLI), '--version'], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('2.5.0', p.stdout)

    def test_markdown_course_only_advances_after_publish(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); plan = course(root, {'platform': 'markdown', 'mode': 'local'})
            m = self.invoke(root, 'render', '--input', str(root / 'plan.json'), '--key', 'plan')
            self.assertNotIn('pdf', m['artifacts'])
            self.invoke(root, 'review', '--key', 'plan', '--note', 'Read actual text/image/links')
            self.invoke(root, 'approve')
            lesson = dict(plan, day=1, title='第一课', reading_minutes=8, practice_minutes=3)
            c.save(root / 'data/Day01.json', lesson)
            self.invoke(root, 'render', '--input', str(root / 'data/Day01.json'), '--key', 'Day01')
            self.assertEqual(self.invoke(root, 'next')['action'], 'review_existing')
            self.invoke(root, 'review', '--key', 'Day01', '--note', 'Read lesson')
            error = self.invoke(root, 'delivered', '--day', '1', success=False)
            self.assertIn('verified', error['error'])
            self.assertEqual(self.invoke(root, 'publish', '--key', 'Day01')['status'], 'verified')
            self.assertEqual(self.invoke(root, 'delivered', '--day', '1')['status'], 'complete')
            self.assertEqual(self.invoke(root, 'next')['action'], 'complete')

    def test_missing_cloud_configuration_does_not_silently_select_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); course(root, {'platform': 'notion', 'mode': 'api', 'destination': {}, 'credential_env': {}})
            r = self.invoke(root, 'delivery-check')
            self.assertFalse(r['ready']); self.assertIn('credential_env.token', r['missing'])
            m = self.invoke(root, 'render', '--input', str(root / 'plan.json'), '--key', 'plan')
            self.assertNotIn('pdf', m['artifacts'])

    def test_doctor_works_with_pdf_imports_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); course(root, {'platform': 'docx', 'mode': 'local'})
            code = '''import sys,runpy
class RejectPDF:
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in ('omni_pdf','pypdf','pypdfium2'):raise RuntimeError('PDF import forbidden')
sys.meta_path.insert(0,RejectPDF());sys.path.insert(0,sys.argv[1]);sys.argv=[sys.argv[2],'--project',sys.argv[3],'doctor'];runpy.run_path(sys.argv[0],run_name='__main__')
'''
            p = subprocess.run([sys.executable, '-c', code, str(CLI.parent), str(CLI), str(root)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(json.loads(p.stdout)['formats'], ['docx'])

    def test_missing_optional_dependency_returns_actionable_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); course(root, {'platform': 'docx', 'mode': 'local'})
            code = '''import sys,runpy
class RejectDOCX:
 def find_spec(self,fullname,path=None,target=None):
  if fullname=='docx':raise ModuleNotFoundError("missing test dependency",name='docx')
sys.meta_path.insert(0,RejectDOCX());sys.path.insert(0,sys.argv[1]);sys.argv=[sys.argv[2],'--project',sys.argv[3],'render','--input',sys.argv[4],'--key','plan'];runpy.run_path(sys.argv[0],run_name='__main__')
'''
            p = subprocess.run([sys.executable, '-c', code, str(CLI.parent), str(CLI), str(root), str(root/'plan.json')], capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0)
            self.assertTrue(p.stderr.startswith('{'), p.stderr[-200:])
            error = json.loads(p.stderr)
            self.assertEqual(error['stage'], 'dependencies')
            self.assertEqual(error['dependency'], 'python-docx')


if __name__ == '__main__': unittest.main()
