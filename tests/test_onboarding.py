"""Private milestone observations survive restarts and never approve courses."""
import importlib.util
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts'))
import omni_core as c


class OnboardingTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('omni_onboarding'), 'Milestone observations missing')
        import omni_onboarding
        return omni_onboarding

    def test_restart_idempotency_and_authorization_wait(self):
        m = self.module(); start = datetime(2026, 10, 31, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            m.record(root, 'started', 'begin', now=start)
            m.record(root, 'user_action', 'choice', user_actions=1, now=start+timedelta(seconds=2))
            m.record(root, 'authorization_started', 'auth1', now=start+timedelta(seconds=10))
            m.record(root, 'authorization_finished', 'auth2', now=start+timedelta(seconds=70))
            m.record(root, 'plan_ready', 'plan', now=start+timedelta(seconds=100))
            before = (root/'onboarding/events.json').read_bytes()
            m.record(root, 'plan_ready', 'plan', now=start+timedelta(seconds=101))
            self.assertEqual(before, (root/'onboarding/events.json').read_bytes())
            r = m.status(root, now=start+timedelta(seconds=110))
            self.assertEqual(r['milestones_seconds']['plan_ready'], 100)
            self.assertEqual(r['authorization_wait_seconds'], 60)
            self.assertEqual(r['recorded_user_actions'], 1)
            self.assertIsNone(r['total_cost'])
            self.assertFalse((root/'state.json').exists())
            with self.assertRaises(ValueError):
                m.record(root, 'blocked', 'plan', stage='authorization')

    def test_rejects_secret_fields_in_usage_and_invalid_observations(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); m.record(root, 'started', 'begin')
            for usage in ({'source': 'host_meter', 'access_token': 'SECRET'},
                          {'source': 'host_meter', 'cost': float('nan'), 'currency': 'USD'},
                          {'source': 'host_meter', 'cost': -1, 'currency': 'USD'},
                          {'source': 'host_meter', 'cost': 1},
                          {'source': 'host_meter', 'input_tokens': True}):
                with self.subTest(usage=usage), self.assertRaises(ValueError):
                    m.record(root, 'plan_ready', 'bad', usage=usage)
            with self.assertRaises(ValueError): m.record(root, 'user_action', 'x', user_actions=-1)
            with self.assertRaises(ValueError): m.record(root, 'authorization_finished', 'end')
            self.assertNotIn('SECRET', (root/'onboarding/events.json').read_text())

    def test_records_only_explicit_metered_usage_without_mutating_approved_config(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); c.save(root/'config.json', {'timezone': 'UTC'})
            original = (root/'config.json').read_bytes(); m.record(root, 'started', 'begin')
            usage = {'source': 'host_meter', 'input_tokens': 42, 'output_tokens': 7, 'cost': 0.02, 'currency': 'USD'}
            m.record(root, 'plan_ready', 'plan', usage=usage)
            r = m.status(root)
            self.assertEqual(r['usage_reports'][0]['usage'], usage)
            self.assertIsNone(r['total_cost'])  # Partial observations do not establish a whole-course cost.
            self.assertEqual(original, (root/'config.json').read_bytes())

    def test_private_ledger_rejects_symlink_escape(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as elsewhere:
            root = Path(tmp); (root/'onboarding').symlink_to(elsewhere, target_is_directory=True)
            with self.assertRaises(ValueError): m.record(root, 'started', 'begin')
            self.assertFalse((Path(elsewhere)/'events.json').exists())



if __name__ == '__main__': unittest.main()
