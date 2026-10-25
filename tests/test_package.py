import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_package_excludes_private_files_and_contains_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / 'tools').mkdir()
            shutil.copyfile(ROOT / 'tools/package_skill.py', root / 'tools/package_skill.py')
            skill = root / 'skills/omni-learning-anything'
            shutil.copytree(ROOT / 'skills/omni-learning-anything', skill, ignore=shutil.ignore_patterns('__pycache__'))
            for relative in ('.env', 'config.local.json', 'scripts/credentials.json',
                             'references/token.txt', 'agents/session.json', 'course/plan.json'):
                path = skill / relative; path.parent.mkdir(exist_ok=True); path.write_text('PRIVATE_SENTINEL')
            p = subprocess.run([sys.executable, str(root / 'tools/package_skill.py')], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            archive = root / 'dist/omni-learning-anything-skill-v2.2.0.zip'
            self.assertTrue(archive.exists())
            with ZipFile(archive) as z:
                self.assertIn('omni-learning-anything/scripts/omni_delivery.py', z.namelist())
                self.assertIn('omni-learning-anything/references/commands.md', z.namelist())
                self.assertFalse(any(b'PRIVATE_SENTINEL' in z.read(n) for n in z.namelist()))
            self.assertIn(hashlib.sha256(archive.read_bytes()).hexdigest(), (root / 'dist/SHA256SUMS').read_text())
            shutil.copyfile(ROOT / 'tools/validate_v2.py', root / 'tools/validate_v2.py')
            checked = subprocess.run([sys.executable, str(root / 'tools/validate_v2.py'), '--archive', str(archive)], capture_output=True, text=True)
            self.assertEqual(checked.returncode, 0, checked.stderr)


if __name__ == '__main__': unittest.main()
