"""Readiness is scoped evidence, not inferred from binary presence."""
import importlib.util
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts'))
import omni_core as c


def scheduled(root, host):
    c.save(root/'plan.json', {'topic': 'QA', 'days': [{'day': 1, 'topic': 'QA'}]})
    c.save(root/'state.json', {'status': 'active', 'approved_plan': c.digest(root/'plan.json'),
        'approved_config': c.digest(root/'config.json'), 'schedule': {'host': host, 'job_id': 'actual-job'}})


class ReadinessTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('omni_readiness'), 'Scoped readiness support missing')
        import omni_readiness
        return omni_readiness

    def test_html_has_no_pdf_or_docx_dependency_and_host_unknown(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); c.save(root/'config.json', {'delivery': {'platform': 'html', 'mode': 'local'}})
            with patch.object(module.importlib.util, 'find_spec', return_value=None), patch.object(module.shutil, 'which', return_value=None):
                r = module.diagnose(root)
            self.assertTrue(r['local_ready'])
            self.assertFalse(r['ready_to_generate'])
            self.assertFalse(r['unattended_ready'])
            self.assertEqual(r['host']['research']['status'], 'unknown')

    def test_docx_dependencies_are_actionable_but_do_not_probe_remote(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); c.save(root/'config.json', {'delivery': {'platform': 'docx', 'mode': 'local'}})
            with patch.object(module.importlib.util, 'find_spec', return_value=None):
                r = module.diagnose(root)
            self.assertFalse(r['local_ready'])
            self.assertIn('python-docx', ' '.join(x['next_action'] for x in r['checks']))
            self.assertTrue(r['delivery']['ready'])
            self.assertIn('configuration', r['delivery']['note'].lower())

    def test_fresh_scoped_foreground_report_cannot_certify_background(self):
        module = self.module(); now = datetime(2026, 10, 31, 8, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); c.save(root/'config.json', {'delivery': {'platform': 'html', 'mode': 'local'}})
            report = {'host': 'qa-host', 'project': str(root), 'config_hash': c.digest(root/'config.json'),
                      'context': 'foreground', 'checked_at': now.isoformat(),
                      'capabilities': {key: {'status': 'verified', 'evidence': 'actual-tool-run-42'}
                                       for key in ('execution', 'research', 'images', 'inspection', 'notification', 'scheduler')}}
            r = module.diagnose(root, report, host='qa-host', now=now)
            self.assertTrue(r['ready_to_generate']); self.assertFalse(r['unattended_ready'])
            r = module.diagnose(root, report, host='qa-host', background=True, now=now)
            self.assertFalse(r['ready_to_generate'])
            report['context'] = 'background'
            report['job_id'] = 'actual-job'; scheduled(root, 'qa-host')
            self.assertTrue(module.diagnose(root, report, host='qa-host', background=True, now=now)['unattended_ready'])
            self.assertFalse(module.diagnose(root, report, host='qa-host', now=now)['ready_to_generate'])
            for change in ({'project': str(root/'other')}, {'config_hash': '0'*64},
                           {'checked_at': (now-timedelta(days=2)).isoformat()},
                           {'checked_at': (now+timedelta(hours=1)).isoformat()}):
                with self.subTest(change=change):
                    r = module.diagnose(root, dict(report, **change), host='qa-host', background=True, now=now)
                    self.assertFalse(r['unattended_ready'])

    def test_verified_claim_without_evidence_stays_unknown(self):
        module = self.module(); now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); c.save(root/'config.json', {'delivery': {'platform': 'markdown', 'mode': 'local'}})
            report = {'host': 'qa', 'project': str(root), 'config_hash': c.digest(root/'config.json'),
                      'context': 'foreground', 'checked_at': now.isoformat(),
                      'capabilities': {'research': {'status': 'verified', 'evidence': ''}}}
            self.assertEqual(module.diagnose(root, report, host='qa')['host']['research']['status'], 'unknown')

    def test_cloud_background_requires_actual_credential_context_evidence(self):
        module = self.module(); now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); c.save(root/'config.json', {'delivery': {'platform': 'notion', 'mode': 'host', 'destination': {'parent_page_id': 'confirmed'}}})
            scheduled(root, 'qa')
            report = {'host': 'qa', 'job_id': 'actual-job', 'project': str(root), 'config_hash': c.digest(root/'config.json'),
                      'context': 'background', 'checked_at': now.isoformat(),
                      'capabilities': {key: {'status': 'verified', 'evidence': 'actual-tool-result'} for key in module.CAPABILITIES if key != 'credentials'}}
            self.assertFalse(module.diagnose(root, report, host='qa', background=True)['unattended_ready'])
            report['capabilities']['credentials'] = {'status': 'verified', 'evidence': 'official-background-account-check'}
            self.assertTrue(module.diagnose(root, report, host='qa', background=True)['unattended_ready'])

    def test_tencent_mcp_requires_requests_but_not_legacy_cos(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); c.save(root/'config.json', {'delivery': {'platform': 'tencent', 'mode': 'mcp',
                'destination': {'folder_id': 'root'}, 'auth_profile': 'qa', 'account_id': 'qa'}})
            with patch.object(module.importlib.util, 'find_spec', side_effect=lambda name: None if name == 'requests' else object()):
                r = module.diagnose(root)
            self.assertFalse(r['local_ready'])
            self.assertNotIn('module.qcloud_cos', [x['id'] for x in r['checks']])

    def test_report_must_match_expected_host_and_approved_registered_job(self):
        module = self.module(); now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); c.save(root/'config.json', {'delivery': {'platform': 'html', 'mode': 'local'}})
            scheduled(root, 'host-B')
            report = {'host': 'host-A', 'job_id': 'job-A', 'project': str(root), 'config_hash': c.digest(root/'config.json'),
                      'context': 'background', 'checked_at': now.isoformat(),
                      'capabilities': {key: {'status': 'verified', 'evidence': 'actual-check'} for key in module.CAPABILITIES}}
            self.assertFalse(module.diagnose(root, report, host='host-B', background=True)['unattended_ready'])
            report.update(host='host-B', job_id='actual-job')
            self.assertTrue(module.diagnose(root, report, host='host-B', background=True)['unattended_ready'])
            report['job_id'] = 'old-job'
            self.assertFalse(module.diagnose(root, report, host='host-B', background=True)['unattended_ready'])
            report['job_id'] = 'actual-job'
            c.save(root/'state.json', dict(c.read(root/'state.json'), status='paused'))
            self.assertFalse(module.diagnose(root, report, host='host-B', background=True)['unattended_ready'])


if __name__ == '__main__': unittest.main()
