"""Official API transports, auth binding and checkpoint-safe CLI reuse."""
import importlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts'))
import test_providers as fixtures

class TransportTests(unittest.TestCase):
    def module(self):
        try: return importlib.import_module('omni_official_cli')
        except ImportError: self.fail('Official CLI API transports are missing')

    def test_notion_json_uses_stdin_and_pinned_official_endpoint(self):
        p=self.module(); calls=[]
        def runner(args,**kw):
            calls.append((args,kw)); return {'id':'page'}
        client=p.NotionCLI({'account_id':'user'},runner=runner)
        value=client.json('POST','https://api.notion.com/v1/pages',json={'markdown':'中文正文'})
        args,kw=calls[0]
        self.assertEqual(value['id'],'page')
        self.assertIn('2026-03-11',args)
        self.assertEqual(json.loads(kw['input'])['markdown'],'中文正文')
        self.assertNotIn('中文正文',str(args))
        self.assertEqual(kw['env']['NOTION_API_BASE_URL'],'https://api.notion.com')
        with self.assertRaises(ValueError):client.json('GET','https://evil.example/v1/users/me')

    def test_notion_multipart_uses_reviewed_local_file(self):
        p=self.module();calls=[]
        with tempfile.NamedTemporaryFile(suffix='.png') as f:
            client=p.NotionCLI({},runner=lambda args,**kw: calls.append(args) or {'status':'uploaded'})
            client.json('POST','https://api.notion.com/v1/file_uploads/upload/send',files={'file':('figure.png',f,'image/png')})
            self.assertEqual(Path(calls[0][calls[0].index('--file')+1]),Path(f.name).resolve())

    def test_cli_failure_never_returns_raw_token_or_signed_url(self):
        p=self.module()
        bad=json.dumps({'ok':False,'error':{'type':'authorization','message':'TOKEN-SECRET https://upload.test/?Signature=SECRET'}})
        with patch.object(p.subprocess,'run',return_value=subprocess.CompletedProcess([],1,'',bad)):
            with self.assertRaises(p.CLIError) as caught:p.run(['lark-cli','auth','status'])
        self.assertNotIn('SECRET',str(caught.exception))
        self.assertEqual(caught.exception.kind,'authorization')

    def test_feishu_envelope_requires_user_identity_and_uses_relative_upload(self):
        p=self.module();calls=[]
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'sources').mkdir();file=root/'sources/plan.docx';file.write_bytes(b'fixture')
            def runner(args,**kw):
                calls.append((args,kw));return {'ok':True,'identity':'user','data':{'file_token':'upload'}}
            cli=p.FeishuCLI({'cli_profile':'course'},root=root,runner=runner)
            with file.open('rb') as f:
                r=cli.json('POST','https://open.feishu.cn/open-apis/drive/v1/medias/upload_all',data={'size':'7'},files={'file':('plan.docx',f,'mime')})
            self.assertEqual(r['data']['file_token'],'upload')
            args,kw=calls[0]
            self.assertEqual(args[args.index('--as')+1],'user')
            self.assertIn('file=sources/plan.docx',args)
            self.assertEqual(kw['cwd'],root.resolve())
            bot=p.FeishuCLI({},runner=lambda *a,**kw:{'ok':True,'identity':'bot','data':{}})
            with self.assertRaises(ValueError):bot.json('GET','https://open.feishu.cn/open-apis/docx/v1/documents/doc/raw_content')

    def test_changed_account_stops_before_any_document_write(self):
        p=self.module();calls=[]
        n=p.NotionCLI({'account_id':'approved'},runner=lambda args,**kw:calls.append(args) or {'id':'different','name':'Other'})
        with self.assertRaises(ValueError):n.check_identity()
        self.assertEqual(len(calls),1)
        self.assertFalse(any('POST' in c for c in calls))

class CLIProviderTests(unittest.TestCase):
    setUp=fixtures.ProviderTests.setUp
    tearDown=fixtures.ProviderTests.tearDown
    module=fixtures.ProviderTests.module
    checkpoint=fixtures.ProviderTests.checkpoint
    markdown=fixtures.ProviderTests.markdown
    feishu_http=fixtures.ProviderTests.feishu_http
    feishu_blocks=fixtures.ProviderTests.feishu_blocks
    # Reuse real generated artifacts, but only add CLI-specific cases to this class.
    def test_feishu_cli_pending_resume_uses_same_saved_ticket(self):
        p=self.module('omni_feishu');calls=[]
        http=self.feishu_http(pending=True); original=http.json
        def record(method,url,**kw):calls.append((method,url));return original(method,url,**kw)
        http.json=record
        target={'platform':'feishu','mode':'cli','destination':{'folder_token':'folder-qa'},'account_id':'user'}
        r=p.publish(self.root,self.manifest,target,self.receipt,self.checkpoint,client=http)
        self.assertEqual(r['status'],'pending');self.assertEqual(self.receipt['task_id'],'task-qa')
        http=self.feishu_http();http.check_identity=lambda:None
        original_handler=http.handler
        http.handler=lambda method,url,kw: {'code':0,'data':{'files':[{'token':'doc-qa','name':self.plan['title']}],'has_more':False}} if url.endswith('/files') else original_handler(method,url,kw)
        p.publish(self.root,self.manifest,target,self.receipt,self.checkpoint,client=http)
        self.assertFalse(any(c[0]=='POST' for c in http.calls))

    def test_feishu_cli_wrong_destination_does_not_verify(self):
        p=self.module('omni_feishu');http=self.feishu_http();original=http.handler
        http.handler=lambda method,url,kw: {'code':0,'data':{'files':[],'has_more':False}} if url.endswith('/files') else original(method,url,kw)
        target={'platform':'feishu','mode':'cli','destination':{'folder_token':'folder-qa'},'account_id':'user'}
        with self.assertRaises(ValueError):p.publish(self.root,self.manifest,target,self.receipt,self.checkpoint,client=http)
        self.assertEqual(self.receipt['remote_id'],'doc-qa')
        self.assertNotEqual(self.receipt['status'],'verified')
