import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'skills/omni-learning-anything/scripts'))
import omni_core as c
import omni_document as doc
from test_documents import course


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def delivery(self):
        self.assertIsNotNone(importlib.util.find_spec('omni_delivery'), 'Destination delivery is missing')
        import omni_delivery
        return omni_delivery

    def ready(self, target):
        plan = course(self.root, target)
        doc.render(self.root, self.root / 'plan.json', 'plan', ['markdown', 'docx'])
        doc.review(self.root, 'plan', 'Checked plan'); c.approve(self.root)
        lesson = dict(plan, day=1, title='第一课', reading_minutes=8, practice_minutes=3)
        c.save(self.root / 'data/Day01.json', lesson)
        doc.render(self.root, self.root / 'data/Day01.json', 'Day01', ['markdown', 'docx'])
        doc.review(self.root, 'Day01', 'Checked lesson')

    def test_preflight_only_asks_for_selected_platform(self):
        d = self.delivery()
        result = d.preflight({'platform': 'notion', 'mode': 'api', 'destination': {}, 'credential_env': {}}, environ={})
        self.assertFalse(result['ready'])
        self.assertEqual(set(result['missing']), {'destination.parent_page_id', 'credential_env.token'})
        self.assertNotIn('feishu', str(result))

    def test_plain_credentials_rejected_before_initialization(self):
        self.delivery()
        with self.assertRaises(ValueError):
            course(self.root, {'platform': 'notion', 'mode': 'api', 'token': 'private-value'})
        self.assertFalse((self.root / 'state.json').exists())

    def test_unknown_mode_rejected(self):
        self.delivery()
        with self.assertRaises(ValueError):
            course(self.root, {'platform': 'notion', 'mode': 'pretend'})

    def test_cloud_cannot_advance_without_verified_receipt(self):
        self.delivery()
        self.ready({'platform': 'notion', 'mode': 'host', 'destination': {'parent_page_id': 'qa'}})
        with self.assertRaisesRegex(ValueError, 'verified'):
            c.deliver(self.root, 1)
        self.assertEqual(c.next_action(self.root)['day'], 1)
        self.assertFalse(c.read(self.root / 'state.json')['lessons'])

    def test_local_verified_delivery_can_advance_idempotently(self):
        d = self.delivery(); self.ready({'platform': 'markdown', 'mode': 'local'})
        before = c.digest(self.root / 'manifests/Day01.json')
        receipt = d.publish(self.root, 'Day01')
        self.assertEqual(receipt['status'], 'verified')
        self.assertEqual(d.publish(self.root, 'Day01')['delivery_id'], receipt['delivery_id'])
        self.assertEqual(c.digest(self.root / 'manifests/Day01.json'), before)
        self.assertEqual(c.deliver(self.root, 1)['status'], 'complete')
        self.assertEqual(c.deliver(self.root, 1)['action'], 'already_recorded')

    def test_export_for_import_is_not_cloud_delivery(self):
        d = self.delivery(); self.ready({'platform': 'tencent', 'mode': 'import', 'destination': {'folder_id': 'qa'}})
        self.assertEqual(d.publish(self.root, 'Day01')['status'], 'awaiting_import')
        with self.assertRaisesRegex(ValueError, 'verified'):
            c.deliver(self.root, 1)

    def test_notion_word_import_default_embeds_figure_and_selects_docx(self):
        d = self.delivery()
        target = {'platform': 'notion', 'mode': 'import', 'destination': {'name': 'Private QA'}}
        course(self.root, target)
        formats = d.default_formats(c.read(self.root / 'config.json'))
        doc.render(self.root, self.root / 'plan.json', 'plan', formats)
        doc.review(self.root, 'plan', 'Inspected')
        r = d.publish(self.root, 'plan')
        self.assertEqual(r['artifact'], 'sources/plan.docx')
        from zipfile import ZipFile
        with ZipFile(self.root / r['artifact']) as z:
            self.assertTrue(any(n.startswith('word/media/') for n in z.namelist()))
        self.assertEqual(d.default_formats({'delivery': dict(target, mode='api')}), ['markdown'])

    def test_existing_notion_markdown_import_can_still_resume(self):
        d = self.delivery()
        course(self.root, {'platform': 'notion', 'mode': 'import', 'destination': {'name': 'Private QA'}})
        doc.render(self.root, self.root / 'plan.json', 'plan', ['markdown'])
        doc.review(self.root, 'plan', 'Inspected')
        self.assertEqual(d.publish(self.root, 'plan')['artifact'], 'sources/plan.md')

    def test_receipt_binding_rejects_wrong_target_and_manifest(self):
        d = self.delivery(); self.ready({'platform': 'notion', 'mode': 'host', 'destination': {'parent_page_id': 'qa'}})
        r = d.publish(self.root, 'Day01')
        evidence = {'content_checked': True, 'image_checked': True, 'links_checked': True,
                    'note': 'Read back title, sections, figure and all five links'}
        wrong = dict(r, status='verified', remote_id='qa-page', url='https://www.notion.so/qa',
                     evidence=evidence, manifest_hash='wrong')
        with self.assertRaises(ValueError):
            d.record_receipt(self.root, 'Day01', wrong)
        wrong['manifest_hash'] = r['manifest_hash']; wrong['target_hash'] = 'wrong'
        with self.assertRaises(ValueError):
            d.record_receipt(self.root, 'Day01', wrong)

    def test_host_receipt_requires_image_and_link_readback(self):
        d = self.delivery(); self.ready({'platform': 'notion', 'mode': 'host', 'destination': {'parent_page_id': 'qa'}})
        r = d.publish(self.root, 'Day01')
        incomplete = dict(r, status='verified', remote_id='qa-page', url='https://www.notion.so/qa',
                          evidence={'content_checked': True, 'note': 'Only title checked'})
        with self.assertRaises(ValueError):
            d.record_receipt(self.root, 'Day01', incomplete)

    def test_mutated_receipt_blocks_archived_continuation(self):
        d = self.delivery(); self.ready({'platform': 'markdown', 'mode': 'local'})
        d.publish(self.root, 'Day01'); c.deliver(self.root, 1)
        path = self.root / 'receipts/Day01.json'; r = c.read(path)
        r['artifact'] = 'wrong.md'; c.save(path, r)
        with self.assertRaises(ValueError):
            c.next_action(self.root)

    def test_credentials_never_appear_in_preflight_output(self):
        d = self.delivery()
        value = 'private-do-not-print'
        r = d.preflight({'platform': 'notion', 'mode': 'api', 'destination': {'parent_page_id': 'qa'},
                         'credential_env': {'token': 'OMNI_QA_TOKEN'}}, environ={'OMNI_QA_TOKEN': value})
        self.assertTrue(r['ready']); self.assertNotIn(value, str(r))

    def test_reconciliation_identifies_existing_page_without_accepting_delivery(self):
        d = self.delivery()
        self.assertTrue(hasattr(d, 'reconcile'), 'Uncertain API writes need an explicit recovery command')
        self.ready({'platform': 'notion', 'mode': 'api', 'destination': {'parent_page_id': 'qa'},
                    'credential_env': {'token': 'QA_TOKEN'}})
        path = self.root / 'receipts/Day01.json'
        target = c.read(self.root / 'config.json')['delivery']
        receipt = dict(d.binding(self.root, 'Day01', c.reviewed(self.root, 'Day01'), target),
                       platform='notion', mode='api', status='needs_reconciliation')
        c.save(path, receipt)
        r = d.reconcile(self.root, 'Day01', remote_id='existing-page', url='https://www.notion.so/existing-page')
        self.assertEqual(r['status'], 'pending')
        self.assertEqual(r['remote_id'], 'existing-page')
        with self.assertRaisesRegex(ValueError, 'verified'): c.deliver(self.root, 1)

    def test_verified_adapter_result_must_identify_provider_document(self):
        d = self.delivery(); self.ready({'platform': 'notion', 'mode': 'api', 'destination': {'parent_page_id': 'qa'},
                                        'credential_env': {'token': 'QA_TOKEN'}})
        def broken_adapter(*args): return {'status': 'verified'}
        with patch.dict(os.environ, {'QA_TOKEN': 'private'}), self.assertRaises(RuntimeError):
            d.publish(self.root, 'Day01', adapter=broken_adapter)

    def test_official_notion_api_app_url_is_accepted(self):
        d=self.delivery()
        d.verify_url('notion','https://app.notion.com/p/QA-0123456789abcdef0123456789abcdef')
        for value in ['https://app.notion.com.evil.example/p/id','https://evilnotion.com/p/id','https://secret@app.notion.com/p/id','https://app.notion.com/p/id?access_token=secret']:
            with self.assertRaises(ValueError):d.verify_url('notion',value)

    def test_successful_recovery_clears_prior_error(self):
        d=self.delivery()
        self.ready({'platform':'notion','mode':'api','destination':{'parent_page_id':'qa'},'credential_env':{'token':'QA_TOKEN'}})
        def fail(*args):raise RuntimeError('private provider failure')
        success={'status':'verified','remote_id':'qa-page','url':'https://www.notion.so/qa','evidence':{'content_checked':True,'image_checked':True,'links_checked':True}}
        with patch.dict(os.environ,{'QA_TOKEN':'private'}):
            with self.assertRaises(RuntimeError):d.publish(self.root,'Day01',adapter=fail)
            self.assertIn('error',d.status(self.root,'Day01'))
            result=d.publish(self.root,'Day01',adapter=lambda *args:success)
        self.assertEqual(result['status'],'verified');self.assertNotIn('error',result)


if __name__ == '__main__':
    unittest.main()
