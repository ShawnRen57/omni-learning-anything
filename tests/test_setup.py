"""Selected-only setup recipes and public CLI behavior."""
import json,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from test_documents import SCRIPTS

class SetupTests(unittest.TestCase):
    def engine(self):
        import omni_setup
        return omni_setup

    def test_html_markdown_and_obsidian_need_no_optional_python_packages(self):
        s=self.engine()
        for platform in ('html','markdown','obsidian'):
            with patch.object(s.importlib.util,'find_spec',return_value=None):r=s.plan(platform)
            self.assertEqual(r['packages'],[]);self.assertEqual(r['pip_argv'],[])
            self.assertEqual(r['authorization'],'not_required')
            self.assertEqual(r['native_discovery'],'unknown')

    def test_docx_pdf_and_material_pdf_only_install_relevant_packages(self):
        s=self.engine()
        with patch.object(s.importlib.util,'find_spec',return_value=None):
            doc=s.plan('docx');pdf=s.plan('pdf');book=s.plan('html',material_format='pdf')
        self.assertEqual(set(doc['modules']),{'docx','PIL'})
        self.assertEqual(set(pdf['modules']),{'pypdf','pypdfium2'})
        self.assertEqual(book['modules'],['pypdf'])
        self.assertIn('XeLaTeX',str(pdf));self.assertNotIn('xelatex',str(book).lower())

    def test_cloud_checks_only_selected_tool_and_keeps_authorization_unknown(self):
        s=self.engine()
        for platform,binary in (('notion','ntn'),('feishu','lark-cli'),('dingtalk','dws')):
            with patch.object(s.shutil,'which',return_value=None) as which:r=s.plan(platform)
            which.assert_called_once_with(binary)
            self.assertEqual(r['authorization'],'unknown')
            self.assertIn('official',r['tools'][0]['next_action'].lower())
            self.assertIn('connection',r['next_action'])
        with patch.object(s.importlib.util,'find_spec',return_value=None):r=s.plan('tencent')
        self.assertIn('keyring',r['modules']);self.assertNotIn('qcloud_cos',r['modules'])

    def test_setup_cli_before_course_and_installation_inspection(self):
        with tempfile.TemporaryDirectory() as temporary:
            cli=SCRIPTS/'omni_learning.py'
            for args in (['setup-check','--platform','html'],['installation','inspect','--path',str(SCRIPTS.parent)]):
                result=subprocess.run([sys.executable,str(cli),'--project',temporary,*args],capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr)
                data=json.loads(result.stdout)
                self.assertEqual(data['native_discovery'],'unknown')
            self.assertFalse((Path(temporary)/'config.json').exists())

    def test_missing_os_timezone_database_recommends_tzdata_even_for_html(self):
        import os
        env=dict(os.environ,PYTHONTZPATH='')
        result=subprocess.run([sys.executable,'-S',str(SCRIPTS/'omni_learning.py'),'setup-check','--platform','html'],env=env,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        data=json.loads(result.stdout);self.assertIn('tzdata',data['modules'])
        self.assertTrue(any(x.startswith('tzdata') for x in data['pip_argv']))
