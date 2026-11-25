"""Foreign-language materials must work on paper and in the normal course workflow."""
import copy
from argparse import Namespace
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'skills/omni-learning-anything/scripts'))
import omni_core as core
import omni_language_learning as language

PROFILE = {'native': '中文', 'target': '日本語', 'starting_point': '零基础',
           'goal': '能在学校问候并致谢'}
PAIRS = [{'form': 'おはようございます', 'meaning': '早上好', 'section_index': 0, 'source_id': 'S1'},
         {'form': 'ありがとうございます', 'meaning': '谢谢您', 'section_index': 0, 'source_id': 'S1'}]


def lesson(day=1, pairs=None):
    pairs = PAIRS if pairs is None else pairs
    return {'title': '开口', 'day': day, 'sources': [{'id': 'S1'}], 'language_items': pairs,
            'sections': [{'title': '模型', 'body': '。'.join(p['form'] + ' / ' + p['meaning'] for p in pairs) + ' [S1]'}]}


class LanguageCourseTests(unittest.TestCase):
    def test_course_config_and_missing_milestone(self):
        core.validate_config({'language_course': PROFILE, 'timezone': 'UTC'})
        with self.assertRaisesRegex(ValueError, 'distinct'):
            core.validate_config({'language_course': dict(PROFILE, target='中文'), 'timezone': 'UTC'})
        with self.assertRaisesRegex(ValueError, 'can_do'):
            with tempfile.TemporaryDirectory() as tmp:
                core.initialize(Path(tmp), {'timezone': 'UTC', 'language_course': PROFILE},
                                {'topic': 'Japanese', 'days': [{'day': 1, 'topic': 'Greetings'}]})

    def test_missing_or_unsupported_meaning(self):
        for mutate in (lambda d: d.pop('language_items'), lambda d: d['language_items'][0].update(meaning='再见'),
                       lambda d: d['language_items'][1].update(source_id='S9')):
            source = copy.deepcopy(lesson())
            mutate(source)
            with self.assertRaises(ValueError):
                language.validate_items(source)

    def test_distinct_bidirectional_prompts_and_private_key(self):
        questions = language.practice([(1, lesson())], 1, PROFILE, answers=False)
        key = language.practice([(1, lesson())], 1, PROFILE, answers=True)
        self.assertIn('おはようございます', questions)
        self.assertIn('谢谢您', questions)
        self.assertNotIn('早上好', questions)
        self.assertNotIn('ありがとうございます', questions)
        opposite = language.practice([(1, lesson())], 1, PROFILE, answers=False, reverse=True)
        self.assertIn('早上好', opposite)
        self.assertNotIn('おはようございます', opposite)
        self.assertIn('ありがとうございます', opposite)
        self.assertNotIn('谢谢您', opposite)
        self.assertIn('早上好', key)
        self.assertIn('ありがとうございます', key)
        self.assertIn('S1', key)

    def test_repeat_from_prior_lesson_reverses_direction_and_deduplicates(self):
        current = lesson(2, [dict(PAIRS[1], form='失礼します', meaning='打扰了')])
        old = language.practice([(1, lesson()), (2, current)], 2, PROFILE, answers=False)
        self.assertIn('早上好', old)
        self.assertNotIn('おはようございます', old)
        self.assertIn('失礼します', old)
        self.assertNotIn('打扰了', old)

    def test_review_requires_an_earlier_delivered_day(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            core.save(root / 'config.json', {'language_course': PROFILE})
            with patch('omni_quiz.snapshot', return_value=(lesson(2), {}, {'lessons': {}})):
                for key in ('Day01', 'Day02', 'Day03'):
                    with self.assertRaises(ValueError):
                        language.worksheet(root, 'Day02', [key], answers=False)


    def test_reviewed_lesson_exports_separate_reproducible_files(self):
        import omni_document as document
        from omni_delivery import publish
        from test_documents import course
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = course(root, {'platform': 'markdown', 'mode': 'local'})
            config = core.read(root / 'config.json')
            core.save(root / 'config.json', dict(config, language_course=PROFILE))
            plan['days'][0]['can_do'] = '见面时能问候，接受帮助后能道谢'
            core.save(root / 'plan.json', plan)
            document.render(root, root / 'plan.json', 'plan', ['markdown'])
            document.review(root, 'plan', 'Reviewed daily communication goal')
            publish(root, 'plan')
            core.approve(root)
            data = dict(plan, title=plan['days'][0]['topic'], day=1, reading_minutes=7,
                        practice_minutes=4, language_items=PAIRS)
            data['sections'][0]['body'] = lesson()['sections'][0]['body']
            core.save(root / 'data/Day01.json', data)
            document.render(root, root / 'data/Day01.json', 'Day01', ['markdown'])
            request = Namespace(language_action='worksheet', key='Day01', review_from=[], reverse=False)
            with self.assertRaises(ValueError):
                language.execute(root, request)
            document.review(root, 'Day01', 'Reviewed both expressions and source locations')
            before = core.read(root / 'state.json')
            sheet = language.execute(root, request)
            self.assertEqual(sheet, language.execute(root, request))
            request.language_action = 'answer-key'
            key = language.execute(root, request)
            self.assertNotEqual(Path(sheet['path']).parent, Path(key['path']).parent)
            self.assertNotIn('ありがとうございます', (root / sheet['path']).read_text())
            self.assertIn('ありがとうございます', (root / key['path']).read_text())
            self.assertEqual(before, core.read(root / 'state.json'))
