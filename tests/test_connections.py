"""Low-friction connect checks and metadata-only profile reuse."""
import importlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts'))

class ConnectionTests(unittest.TestCase):
    def module(self):
        try:return importlib.import_module('omni_connections')
        except ImportError:self.fail('Guided connection workflow is missing')

    def test_parse_only_selected_official_target_urls(self):
        p=self.module()
        self.assertEqual(p.location('notion','https://www.notion.so/Course-0123456789abcdef0123456789abcdef?source=copy_link'),{'parent_page_id':'0123456789abcdef0123456789abcdef'})
        self.assertEqual(p.location('feishu','https://my.feishu.cn/drive/folder/folderABC'),{'folder_token':'folderABC'})
        for url in ['https://evil.example/drive/folder/token','https://my.feishu.cn/docx/doc','https://token@my.feishu.cn/drive/folder/id','http://my.feishu.cn/drive/folder/id','https://my.feishu.cn/drive/folder/id?access_token=private']:
            with self.assertRaises(ValueError):p.location('feishu',url)

    def test_missing_connection_steps_do_not_ask_for_raw_secrets(self):
        p=self.module()
        with patch.object(p.shutil,'which',return_value=None):
            result=p.connect('feishu','https://my.feishu.cn/drive/folder/qa')
        self.assertFalse(result['ready']);self.assertEqual(result['stage'],'install')
        self.assertIn('lark-cli',str(result));self.assertNotIn('Notion',str(result))
        self.assertIn('references/onboarding.md',str(result))
        self.assertEqual(p.connect('notion')['stage'],'location')

    def test_auth_failure_is_actionable_without_exposing_provider_error(self):
        p=self.module()
        from omni_official_cli import CLIError
        class Client:
            def check_identity(self):raise CLIError('config')
        with patch.object(p.shutil,'which',return_value='/cli'):
            r=p.connect('feishu','https://my.feishu.cn/drive/folder/qa',client=Client())
        self.assertEqual(r['stage'],'authorization');self.assertIn('config init',str(r))
        self.assertFalse(r['ready'])

    def test_identity_and_target_verified_before_saving_snapshot(self):
        p=self.module();calls=[]
        class Client:
            def check_identity(self):return {'id':'account-qa','name':'Test user'}
            def json(self,method,url,**kw):calls.append((method,url,kw));return {'id':'0123456789abcdef0123456789abcdef'}
        with tempfile.TemporaryDirectory() as tmp,patch.object(p.shutil,'which',return_value='/cli'):
            r=p.connect('notion','https://notion.so/0123456789abcdef0123456789abcdef',client=Client(),save_as='course',profile_dir=Path(tmp)/'connections')
            self.assertTrue(r['ready']);self.assertEqual(r['delivery']['mode'],'cli')
            self.assertEqual(r['delivery']['account_id'],'account-qa')
            saved=p.load('course',Path(tmp)/'connections');r['delivery']['destination']['parent_page_id']='changed'
            self.assertEqual(saved['destination']['parent_page_id'],'0123456789abcdef0123456789abcdef')
        self.assertTrue(all(c[0]=='GET' for c in calls))

    def test_profiles_reject_secrets_symlinks_and_silent_replacement(self):
        p=self.module()
        target={'platform':'feishu','mode':'cli','account_id':'user','destination':{'folder_token':'qa'}}
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)/'profiles'
            p.save('course',target,base)
            self.assertEqual(p.load('course',base),target)
            if os.name=='posix':self.assertEqual((base/'course.json').stat().st_mode&0o777,0o600)
            with self.assertRaises(ValueError):p.save('course',dict(target,account_id='changed'),base)
            with self.assertRaises(ValueError):p.save('../escape',target,base)
            with self.assertRaises(ValueError):p.save('secret',dict(target,token='PRIVATE'),base)
            (base/'alias.json').symlink_to(base/'course.json')
            with self.assertRaises(ValueError):p.load('alias',base)
            self.assertEqual(p.list_connections(base)[0]['name'],'course')

    def test_destination_failure_does_not_register_a_connection(self):
        p=self.module()
        class Client:
            def check_identity(self):return {'id':'account','name':'QA'}
            def json(self,*a,**kw):raise RuntimeError('SECRET provider response')
        with tempfile.TemporaryDirectory() as tmp,patch.object(p.shutil,'which',return_value='/cli'):
            base=Path(tmp)/'profiles'
            r=p.connect('notion','https://notion.so/0123456789abcdef0123456789abcdef',client=Client(),save_as='course',profile_dir=base)
            self.assertFalse(r['ready']);self.assertEqual(r['stage'],'destination')
            self.assertNotIn('SECRET',str(r));self.assertFalse(base.exists())

    def test_corrupt_profile_is_skipped_without_breaking_other_connections(self):
        p=self.module()
        target={'platform':'feishu','mode':'cli','account_id':'user','destination':{'folder_token':'qa'}}
        with tempfile.TemporaryDirectory() as tmp:
            p.save('valid',target,tmp)
            for name,value in [('list',[]),('null',None),('delivery',{'version':1,'delivery':None})]:
                path=Path(tmp)/(name+'.json');path.write_text(json.dumps(value));path.chmod(0o600)
            self.assertEqual([item['name'] for item in p.list_connections(tmp)],['valid'])
