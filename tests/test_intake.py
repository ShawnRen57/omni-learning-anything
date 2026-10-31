"""Brief contracts preserve user wording without guessing intent from length."""
import copy
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts'))
import omni_core as c


def brief():
    return {'request': '学点经济学', 'interpretation': '生活中的经济学入门',
            'outcomes': ['解释机会成本并用于一个日常选择'],
            'scope': {'included': ['选择与机会成本'], 'excluded': ['计量推导']},
            'prerequisites': [],
            'sequence': [{'topic': '选择与约束', 'outcome': '比较两种选择的代价'}],
            'assumptions': [{'statement': '先以日常应用为主', 'status': 'proposed'}],
            'open_questions': []}


class IntakeTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('omni_intake'), 'Structured brief support missing')
        import omni_intake
        return omni_intake

    def test_preserves_raw_request_and_marks_assumptions_for_review(self):
        value = brief(); original = copy.deepcopy(value)
        result = self.module().validate_brief(value)
        self.assertEqual(value, original)
        self.assertTrue(result['needs_confirmation'])
        value['request'] = 'SQL JOIN 面试'; value['assumptions'] = []
        self.assertFalse(self.module().validate_brief(value)['needs_confirmation'])

    def test_invalid_assumption_status_and_missing_scope_are_rejected(self):
        module = self.module()
        for change in ({'scope': {}}, {'outcomes': []}, {'sequence': []},
                       {'assumptions': [{'statement': '初学者', 'status': 'inferred_as_fact'}]}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                module.validate_brief(dict(brief(), **change))

    def test_initialize_validates_optional_brief_and_preserves_legacy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); config = {'timezone': 'UTC', 'learning_brief': brief()}
            c.initialize(root, config, {'topic': '经济学', 'days': [{'day': 1, 'topic': '选择'}]})
            self.assertEqual(c.read(root/'config.json')['learning_brief'], brief())
            state = c.read(root/'state.json')
            state.update(approved_plan=c.digest(root/'plan.json'), approved_config=c.digest(root/'config.json'), status='active')
            c.save(root/'state.json', state)
            c.save(root/'config.json', dict(config, learning_brief=dict(brief(), interpretation='换成投资课')))
            with self.assertRaisesRegex(ValueError, 'settings changed'):
                c.next_action(root)
        with tempfile.TemporaryDirectory() as tmp:
            bad = dict(brief(), outcomes=[])
            with self.assertRaises(ValueError):
                c.initialize(Path(tmp), {'timezone': 'UTC', 'learning_brief': bad}, {'topic': 'X', 'days': [{'day': 1, 'topic': 'X'}]})
            self.assertFalse((Path(tmp)/'config.json').exists())


if __name__ == '__main__': unittest.main()
