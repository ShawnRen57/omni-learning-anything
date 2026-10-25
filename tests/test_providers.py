"""Official API contracts, real Vault writes and uncertain-write recovery."""
import importlib.util
import os
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'skills/omni-learning-anything/scripts'))
import omni_core as c
import omni_document as doc
import omni_delivery as delivery
from test_documents import course


class HTTP:
    def __init__(self, handler):
        self.handler = handler; self.calls = []
    def json(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs)); return self.handler(method, url, kwargs)
    def download(self, url, **kwargs):
        self.calls.append(('DOWNLOAD', url, kwargs)); return self.handler('DOWNLOAD', url, kwargs)


class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name) / 'course'; self.root.mkdir()
        self.plan = course(self.root)
        self.manifest = doc.render(self.root, self.root / 'plan.json', 'plan', ['markdown', 'docx'])
        doc.review(self.root, 'plan', 'Read all content/image/links')
        self.manifest = c.reviewed(self.root, 'plan')
        self.receipt = {'delivery_id': 'qa-stable-id', 'status': 'prepared'}
    def tearDown(self):
        self.tmp.cleanup()
    def module(self, name):
        self.assertIsNotNone(importlib.util.find_spec(name), name + ' adapter missing')
        return __import__(name)
    def checkpoint(self, **updates):
        self.receipt.update(updates)
    def markdown(self):
        return (self.root / self.manifest['artifacts']['markdown']).read_text()
    def feishu_blocks(self):
        return [{'block_type': 2, 'text': {'elements': [
            {'text_run': {'content': self.markdown(), 'text_element_style': {'link': {'url': source['url']}}}}
            for source in self.plan['sources']]}}, {'block_type': 27, 'image': {'token': 'media'}}]

    def test_obsidian_copies_assets_and_reuses_note(self):
        p = self.module('omni_obsidian')
        vault = Path(self.tmp.name) / 'vault'; vault.mkdir()
        target = {'platform': 'obsidian', 'mode': 'local', 'destination': {'vault_path': str(vault), 'subdir': 'Omni QA'}}
        r = p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint)
        self.assertEqual(r['status'], 'verified')
        note = Path(r['note_path']); text = note.read_text()
        self.assertIn('中文学习计划', text)
        self.assertNotIn('../assets/', text)
        assets = list(note.parent.glob('assets/*')); self.assertEqual(len(assets), 1)
        self.assertEqual(assets[0].read_bytes(), (self.root / self.manifest['report']['figure']).read_bytes())
        self.receipt.update(r)
        self.assertEqual(p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint)['note_path'], str(note))
        self.assertEqual(len(list(note.parent.glob('*.md'))), 1)

    def test_obsidian_does_not_overwrite_collision(self):
        p = self.module('omni_obsidian'); vault = Path(self.tmp.name) / 'vault'; vault.mkdir()
        target = {'platform': 'obsidian', 'mode': 'local', 'destination': {'vault_path': str(vault), 'subdir': 'QA'}}
        r = p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint)
        Path(r['note_path']).write_text('User edits')
        with self.assertRaises(ValueError):
            p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint)
        self.assertEqual(Path(r['note_path']).read_text(), 'User edits')

    def test_obsidian_rejects_symlink_outside_vault(self):
        p = self.module('omni_obsidian'); vault = Path(self.tmp.name) / 'vault'; vault.mkdir()
        outside = Path(self.tmp.name) / 'outside'; outside.mkdir(); (vault / 'escape').symlink_to(outside)
        target = {'platform': 'obsidian', 'mode': 'local', 'destination': {'vault_path': str(vault), 'subdir': 'escape'}}
        with self.assertRaises(ValueError):
            p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint)
        self.assertFalse(list(outside.iterdir()))

    def notion_http(self, empty=False):
        image = {'written': False}; md = self.markdown()
        def handler(method, url, kwargs):
            if url.endswith('/file_uploads'):
                return {'id': 'upload-qa'}
            if url.endswith('/send'):
                return {'id': 'upload-qa', 'status': 'uploaded'}
            if method == 'POST' and url.endswith('/pages'):
                self.assertNotIn('../assets/', kwargs['json']['markdown'])
                self.assertEqual(kwargs['json']['parent']['page_id'], 'parent-qa')
                return {'id': 'page-qa', 'url': 'https://www.notion.so/page-qa'}
            if url.endswith('/markdown'):
                return {'markdown': '' if empty else md.replace('../assets/', 'https://notion-cdn.example/'), 'truncated': False}
            if url.endswith('/children'):
                if method == 'PATCH': image['written'] = True
                return {'results': [{'type': 'image', 'image': {'type': 'file', 'file': {'url': 'https://notion-cdn.example/image'}, 'caption': [{'plain_text': '学习流程图'}]}}] if image['written'] else [], 'has_more': False}
            if '/pages/' in url:
                return {'id': 'page-qa', 'parent': {'page_id': 'parent-qa'}, 'properties': {'title': {'title': [{'plain_text': self.plan['title']}]}}}
            raise AssertionError((method, url))
        return HTTP(handler)

    def test_notion_uploads_image_and_verifies_content(self):
        p = self.module('omni_notion'); http = self.notion_http()
        target = {'platform': 'notion', 'mode': 'api', 'destination': {'parent_page_id': 'parent-qa'}, 'credential_env': {'token': 'QA_TOKEN'}}
        with patch.dict(os.environ, {'QA_TOKEN': 'private-qa-token'}):
            result = p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, client=http)
        self.assertEqual(result['status'], 'verified')
        self.assertEqual(result['remote_id'], 'page-qa')
        self.assertNotIn('private-qa-token', str(self.receipt))
        self.assertTrue(any(call[0] == 'PATCH' and call[1].endswith('/children') for call in http.calls))

    def test_notion_empty_page_is_not_verified(self):
        p = self.module('omni_notion'); http = self.notion_http(empty=True)
        target = {'platform': 'notion', 'mode': 'api', 'destination': {'parent_page_id': 'parent-qa'}, 'credential_env': {'token': 'QA_TOKEN'}}
        with patch.dict(os.environ, {'QA_TOKEN': 'private'}), self.assertRaises(ValueError):
            p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, client=http)
        self.assertEqual(self.receipt['remote_id'], 'page-qa')
        self.assertNotEqual(self.receipt['status'], 'verified')

    def test_notion_retry_with_remote_id_does_not_create_second_page(self):
        p = self.module('omni_notion'); http = self.notion_http()
        target = {'platform': 'notion', 'mode': 'api', 'destination': {'parent_page_id': 'parent-qa'}, 'credential_env': {'token': 'QA_TOKEN'}}
        self.receipt.update(remote_id='page-qa', url='https://www.notion.so/page-qa', upload_id='upload-qa', status='pending')
        with patch.dict(os.environ, {'QA_TOKEN': 'private'}):
            result = p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, client=http)
        self.assertEqual(result['status'], 'verified')
        self.assertFalse(any(call[0] == 'POST' and call[1].endswith('/pages') for call in http.calls))

    def test_notion_completed_image_upload_is_not_sent_twice(self):
        p = self.module('omni_notion'); http = self.notion_http()
        self.receipt.update(upload_id='upload-qa', upload_complete=True)
        target = {'platform': 'notion', 'mode': 'api', 'destination': {'parent_page_id': 'parent-qa'}, 'credential_env': {'token': 'QA_TOKEN'}}
        with patch.dict(os.environ, {'QA_TOKEN': 'private'}):
            p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, client=http)
        self.assertFalse(any(call[1].endswith('/send') for call in http.calls))

    def test_ambiguous_create_does_not_retry(self):
        self.module('omni_notion')
        config = c.read(self.root / 'config.json')
        config['delivery'] = {'platform': 'notion', 'mode': 'api', 'destination': {'parent_page_id': 'qa'}, 'credential_env': {'token': 'QA_TOKEN'}}
        c.save(self.root / 'config.json', config)
        # Config is hash-bound; regenerate the unapproved plan in a new directory.
        other = Path(self.tmp.name) / 'ambiguous'; other.mkdir(); course(other, config['delivery'])
        doc.render(other, other / 'plan.json', 'plan', ['markdown']); doc.review(other, 'plan', 'Checked')
        calls = []
        def ambiguous(root, manifest, target, receipt, checkpoint):
            calls.append('create'); checkpoint(status='creating'); raise TimeoutError('private-token-in-exception')
        with patch.dict(os.environ, {'QA_TOKEN': 'private'}):
            with self.assertRaises(RuntimeError) as error: delivery.publish(other, 'plan', adapter=ambiguous)
            self.assertNotIn('private-token', str(error.exception))
            with self.assertRaisesRegex(ValueError, 'uncertain'): delivery.publish(other, 'plan', adapter=ambiguous)
        self.assertEqual(calls, ['create'])

    def feishu_http(self, pending=False, missing_image=False):
        def handler(method, url, kwargs):
            if url.endswith('/upload_all'): return {'code': 0, 'data': {'file_token': 'upload-qa'}}
            if method == 'POST' and url.endswith('/import_tasks'):
                self.assertEqual(kwargs['json']['type'], 'docx'); self.assertEqual(kwargs['json']['file_extension'], 'docx')
                self.assertEqual(kwargs['json']['point']['mount_key'], 'folder-qa')
                return {'code': 0, 'data': {'ticket': 'task-qa'}}
            if '/import_tasks/' in url: return {'code': 0, 'data': {'result': {'job_status': 1 if pending else 0, 'token': 'doc-qa', 'url': 'https://qa.feishu.cn/docx/doc-qa'}}}
            if url.endswith('/raw_content'): return {'code': 0, 'data': {'content': self.markdown()}}
            if url.endswith('/blocks'): return {'code': 0, 'data': {'items': self.feishu_blocks()[:-1] if missing_image else self.feishu_blocks(), 'has_more': False}}
            raise AssertionError((method, url))
        return HTTP(handler)

    def test_feishu_import_embedded_docx_and_readback(self):
        p = self.module('omni_feishu'); http = self.feishu_http()
        target = {'platform': 'feishu', 'mode': 'api', 'destination': {'folder_token': 'folder-qa'}, 'credential_env': {'token': 'QA_TOKEN'}}
        with patch.dict(os.environ, {'QA_TOKEN': 'private'}):
            r = p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, client=http)
        self.assertEqual(r['status'], 'verified'); self.assertEqual(self.receipt['task_id'], 'task-qa')

    def test_feishu_pending_task_resumes_without_new_import(self):
        p = self.module('omni_feishu'); target = {'platform': 'feishu', 'mode': 'api', 'destination': {'folder_token': 'folder-qa'}, 'credential_env': {'token': 'QA_TOKEN'}}
        with patch.dict(os.environ, {'QA_TOKEN': 'private'}):
            r = p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, client=self.feishu_http(pending=True))
            self.receipt.update(r); http = self.feishu_http()
            r = p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, client=http)
        self.assertEqual(r['status'], 'verified')
        self.assertFalse(any(call[0] == 'POST' for call in http.calls))

    def test_feishu_missing_image_is_not_verified(self):
        p = self.module('omni_feishu'); target = {'platform': 'feishu', 'mode': 'api', 'destination': {'folder_token': 'folder-qa'}, 'credential_env': {'token': 'QA_TOKEN'}}
        with patch.dict(os.environ, {'QA_TOKEN': 'private'}), self.assertRaises(ValueError):
            p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, client=self.feishu_http(missing_image=True))

    def tencent_http(self, pending=False):
        def handler(method, url, kwargs):
            if url.endswith('/pre-import'): return {'ret': 0, 'data': {'COSFileKey': 'qa-file.docx', 'COSFileExisted': True}}
            if url.endswith('/async-import'):
                self.assertEqual(kwargs['data']['parent'], 'folder-qa')
                return {'ret': 0, 'data': {'progressQueryID': 'task-qa'}}
            if url.endswith('/import-progress'): return {'ret': 0, 'data': {'progress': 50 if pending else 100, 'ID': 'doc-qa', 'url': 'https://docs.qq.com/doc/qa', 'type': 'doc'}}
            if url.endswith('/export'): return {'ret': 0, 'data': {'url': 'https://download.docs.qq.com/qa.docx'}}
            if method == 'DOWNLOAD': return (self.root / self.manifest['artifacts']['docx']).read_bytes()
            raise AssertionError((method, url))
        return HTTP(handler)

    def test_tencent_import_and_export_readback(self):
        p = self.module('omni_tencent'); target = {'platform': 'tencent', 'mode': 'api', 'destination': {'folder_id': 'folder-qa'},
            'credential_env': {'client_id': 'QA_CLIENT', 'open_id': 'QA_OPEN', 'token': 'QA_TOKEN'}}
        with patch.dict(os.environ, {'QA_CLIENT': 'client', 'QA_OPEN': 'open', 'QA_TOKEN': 'private'}):
            r = p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, client=self.tencent_http())
        self.assertEqual(r['status'], 'verified'); self.assertEqual(r['remote_id'], 'doc-qa')

    def test_tencent_pending_task_resumes_without_upload(self):
        p = self.module('omni_tencent'); target = {'platform': 'tencent', 'mode': 'api', 'destination': {'folder_id': 'folder-qa'},
            'credential_env': {'client_id': 'QA_CLIENT', 'open_id': 'QA_OPEN', 'token': 'QA_TOKEN'}}
        with patch.dict(os.environ, {'QA_CLIENT': 'client', 'QA_OPEN': 'open', 'QA_TOKEN': 'private'}):
            r = p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, client=self.tencent_http(pending=True))
            self.receipt.update(r); http = self.tencent_http()
            r = p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, client=http)
        self.assertEqual(r['status'], 'verified'); self.assertFalse(any(call[0] == 'POST' for call in http.calls))

    def test_dingtalk_converted_false_is_not_cloud_document(self):
        p = self.module('omni_dingtalk'); target = {'platform': 'dingtalk', 'mode': 'cli', 'destination': {'folder_id': 'qa'}}
        calls = []
        def runner(args):
            calls.append(args); return {'fallback': 'upload', 'converted': False, 'nodeId': 'file-qa'}
        with self.assertRaises(ValueError):
            p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, runner=runner)
        self.assertEqual(len(calls), 1)

    def test_dingtalk_verifies_markdown_and_remote_image(self):
        p = self.module('omni_dingtalk'); target = {'platform': 'dingtalk', 'mode': 'cli', 'destination': {'folder_id': 'qa'}}
        def runner(args):
            if 'import' in args: return {'nodeId': 'doc-qa', 'documentUrl': 'https://alidocs.dingtalk.com/i/nodes/doc-qa', 'converted': True}
            if 'info' in args: return {'contentType': 'ALIDOC'}
            if 'read' in args: return {'markdown': self.markdown().replace('../assets/', 'https://alidocs-cdn.example/')}
            raise AssertionError(args)
        r = p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, runner=runner)
        self.assertEqual(r['status'], 'verified')

    def test_dingtalk_resume_keeps_original_folder_or_workspace(self):
        p = self.module('omni_dingtalk')
        for field, flag in [('folder_id', '--folder'), ('workspace_id', '--workspace')]:
            self.receipt = {'task_id': 'task-qa', 'status': 'pending'}
            calls = []
            def runner(args):
                calls.append(args)
                return {'taskId': 'task-qa', 'status': 'processing'}
            target = {'destination': {field: 'target-qa'}}
            self.assertEqual(p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, runner=runner)['status'], 'pending')
            self.assertIn(flag, calls[0])
            self.assertEqual(calls[0][calls[0].index(flag) + 1], 'target-qa')
            self.assertNotIn('--file', calls[0])

    def test_dingtalk_unverified_placement_cannot_become_delivered(self):
        p = self.module('omni_dingtalk'); calls = []
        target = {'destination': {'folder_id': 'qa'}}
        def runner(args):
            calls.append(args)
            if 'import' in args:
                return {'taskId': 'task-qa', 'nodeId': 'doc-qa', 'verified': False,
                        'documentUrl': 'https://alidocs.dingtalk.com/i/nodes/doc-qa'}
            if 'info' in args: return {'contentType': 'ALIDOC'}
            return {'markdown': self.markdown().replace('../assets/', 'https://cdn.example/')}
        for _ in range(2):
            with self.assertRaises(ValueError):
                p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, runner=runner)
        self.assertEqual(self.receipt['remote_id'], 'doc-qa')
        self.assertEqual(self.receipt['task_id'], 'task-qa')
        self.assertEqual(sum('--file' in args for args in calls), 1)
        self.assertFalse(any('read' in args for args in calls))

    def test_dingtalk_poll_timeout_preserves_recoverable_task(self):
        p = self.module('omni_dingtalk')
        response = {'success': False, 'timed_out': True, 'taskId': 'task-qa', 'status': 'processing'}
        def subprocess_result(args, **kwargs):
            if kwargs['timeout'] < 330:
                raise subprocess.TimeoutExpired(args, kwargs['timeout'])
            return subprocess.CompletedProcess(args, 0, json.dumps(response), '')
        with patch.object(p.subprocess, 'run', side_effect=subprocess_result):
            r = p.publish(self.root, self.manifest, {'destination': {'folder_id': 'qa'}}, self.receipt, self.checkpoint)
        self.assertEqual(r['status'], 'pending')
        self.assertEqual(self.receipt['task_id'], 'task-qa')

    def test_notion_compact_parent_uuid_matches_canonical_response(self):
        p = self.module('omni_notion'); http = self.notion_http(); original = http.handler
        compact = '0123456789abcdef0123456789abcdef'
        canonical = '01234567-89ab-cdef-0123-456789abcdef'
        def handler(method, url, kwargs):
            if url.endswith('/pages/page-qa'):
                return {'id': 'page-qa', 'parent': {'page_id': canonical},
                        'properties': {'title': {'title': [{'plain_text': self.plan['title']}]}}}
            return original(method, url, kwargs)
        http.handler = handler
        self.receipt.update(remote_id='page-qa', url='https://www.notion.so/page-qa', upload_id='upload-qa', status='pending')
        target = {'platform': 'notion', 'mode': 'api', 'destination': {'parent_page_id': compact}, 'credential_env': {'token': 'QA_TOKEN'}}
        with patch.dict(os.environ, {'QA_TOKEN': 'private'}):
            self.assertEqual(p.publish(self.root, self.manifest, target, self.receipt, self.checkpoint, client=http)['status'], 'verified')

    def test_tencent_verifies_xml_escaped_query_urls(self):
        p = self.module('omni_tencent'); data = dict(self.plan)
        data['sources'] = [dict(s) for s in self.plan['sources']]
        data['sources'][0]['url'] = 'https://example.com/search?q=learning&lang=zh'
        path = Path(self.tmp.name) / 'query-links.docx'
        doc.write_docx(path, data, data, c.read(self.root / 'config.json'),
                       self.root / self.manifest['report']['figure'], c.today(self.root), 'plan')
        p.check_docx(path.read_bytes(), data)

    def test_null_create_identifiers_never_enable_second_create(self):
        for platform, module, id_field, suffix in [('feishu', 'omni_feishu', 'ticket', '/import_tasks'),
                                                  ('tencent', 'omni_tencent', 'progressQueryID', '/async-import'),
                                                  ('notion', 'omni_notion', 'id', '/pages')]:
            for bad_id in (None, '', ' '):
                with self.subTest(platform=platform, bad_id=bad_id):
                    p = self.module(module)
                    if platform == 'feishu':
                        target = {'platform': platform, 'mode': 'api', 'destination': {'folder_token': 'folder-qa'}, 'credential_env': {'token': 'QA_TOKEN'}}
                        http = self.feishu_http()
                    elif platform == 'tencent':
                        target = {'platform': platform, 'mode': 'api', 'destination': {'folder_id': 'folder-qa'}, 'credential_env': {'token': 'QA_TOKEN', 'client_id': 'QA_CLIENT', 'open_id': 'QA_OPEN'}}
                        http = self.tencent_http()
                    else:
                        target = {'platform': platform, 'mode': 'api', 'destination': {'parent_page_id': 'parent-qa'}, 'credential_env': {'token': 'QA_TOKEN'}}
                        http = self.notion_http()
                    original = http.handler
                    def handler(method, url, kwargs):
                        if method == 'POST' and url.endswith(suffix):
                            if platform == 'notion': return {'id': bad_id, 'url': 'https://www.notion.so/page-qa'}
                            return {'code' if platform == 'feishu' else 'ret': 0, 'data': {id_field: bad_id}}
                        return original(method, url, kwargs)
                    http.handler = handler
                    root = Path(self.tmp.name) / (platform + '-' + str(bad_id).replace(' ', 'space')); root.mkdir()
                    course(root, target); doc.render(root, root / 'plan.json', 'plan', ['markdown', 'docx']); doc.review(root, 'plan', 'Inspected')
                    def adapter(root, manifest, target, receipt, checkpoint):
                        return p.publish(root, manifest, target, receipt, checkpoint, client=http)
                    with patch.dict(os.environ, {'QA_TOKEN': 'private', 'QA_CLIENT': 'client', 'QA_OPEN': 'open'}):
                        with self.assertRaises(RuntimeError): delivery.publish(root, 'plan', adapter=adapter)
                        with self.assertRaises(ValueError): delivery.publish(root, 'plan', adapter=adapter)
                    self.assertEqual(len([call for call in http.calls if call[0] == 'POST' and call[1].endswith(suffix)]), 1)

    def test_notion_escaped_markdown_readback_reuses_existing_page(self):
        p=self.module('omni_notion');http=self.notion_http();original=http.handler
        def handler(method,url,kwargs):
            response=original(method,url,kwargs)
            if url.endswith('/markdown'):response['markdown']=response['markdown'].replace('[S1]',r'\[S1\]').replace('|',r'\|')
            return response
        http.handler=handler
        target={'platform':'notion','mode':'api','destination':{'parent_page_id':'parent-qa'},'credential_env':{'token':'QA_TOKEN'}}
        with patch.dict(os.environ,{'QA_TOKEN':'private'}):
            result=p.publish(self.root,self.manifest,target,self.receipt,self.checkpoint,client=http)
            self.receipt.update(result)
            again=p.publish(self.root,self.manifest,target,self.receipt,self.checkpoint,client=http)
        self.assertEqual(result['status'],'verified');self.assertEqual(again['remote_id'],'page-qa')
        self.assertEqual(len([c for c in http.calls if c[0]=='POST' and c[1].endswith('/pages')]),1)

    def test_feishu_import_upload_declares_native_document_type(self):
        p=self.module('omni_feishu');http=self.feishu_http(pending=True);original=http.handler
        def handler(method,url,kwargs):
            if url.endswith('/upload_all'):
                self.assertEqual(json.loads(kwargs['data'].get('extra','{}')),{'obj_type':'docx','file_extension':'docx'})
            return original(method,url,kwargs)
        http.handler=handler
        target={'platform':'feishu','mode':'api','destination':{'folder_token':'folder-qa'},'credential_env':{'token':'QA_TOKEN'}}
        with patch.dict(os.environ,{'QA_TOKEN':'private'}):
            result=p.publish(self.root,self.manifest,target,self.receipt,self.checkpoint,client=http)
        self.assertEqual(result['status'],'pending');self.assertEqual(self.receipt['task_id'],'task-qa')

    def test_feishu_processing_and_unmaterialized_success_remain_pending(self):
        p=self.module('omni_feishu')
        target={'platform':'feishu','mode':'api','destination':{'folder_token':'folder-qa'},'credential_env':{'token':'QA_TOKEN'}}
        for status in (1,2,0):
            with self.subTest(status=status):
                http=self.feishu_http(pending=True);original=http.handler
                def handler(method,url,kwargs):
                    if '/import_tasks/' in url:return {'code':0,'data':{'result':{'job_status':status}}}
                    return original(method,url,kwargs)
                http.handler=handler;receipt={'task_id':'saved-ticket','status':'pending'}
                with patch.dict(os.environ,{'QA_TOKEN':'private'}):
                    result=p.publish(self.root,self.manifest,target,receipt,lambda **kw:receipt.update(kw),client=http)
                self.assertEqual(result['status'],'pending');self.assertEqual(receipt['task_id'],'saved-ticket')
                self.assertFalse(any(c[0]=='POST' for c in http.calls))

    def test_feishu_verifies_encoded_hrefs_and_rejects_plain_text_only_urls(self):
        from urllib.parse import quote
        p=self.module('omni_feishu')
        target={'platform':'feishu','mode':'api','destination':{'folder_token':'folder-qa'},'credential_env':{'token':'QA_TOKEN'}}
        for real_links in (True,False):
            with self.subTest(real_links=real_links):
                http=self.feishu_http();original=http.handler
                def handler(method,url,kwargs):
                    response=original(method,url,kwargs)
                    if url.endswith('/blocks'):
                        for item in response['data']['items']:
                            for element in item.get('text',{}).get('elements',[]):
                                link=element['text_run']['text_element_style']['link']
                                link['url']=quote(link['url'],safe='') if real_links else 'https://wrong.example/'
                                if real_links:
                                    for source in self.plan['sources']:element['text_run']['content']=element['text_run']['content'].replace(source['url'],'')
                    return response
                http.handler=handler;receipt={}
                with patch.dict(os.environ,{'QA_TOKEN':'private'}):
                    call=lambda:p.publish(self.root,self.manifest,target,receipt,lambda **kw:receipt.update(kw),client=http)
                    if real_links:self.assertEqual(call()['status'],'verified')
                    else:
                        with self.assertRaises(ValueError):call()


if __name__ == '__main__': unittest.main()
