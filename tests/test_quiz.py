"""Learner-started light checks preserve delivery and every answer revision."""
import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from test_documents import course
import omni_core as c
import omni_document as document
from omni_delivery import publish


def lesson_course(root, delivered=True, practice=3):
    plan = course(root, {'platform': 'markdown', 'mode': 'local'})
    document.render(root, root/'plan.json', 'plan', ['markdown'])
    document.review(root, 'plan', 'Inspected synthetic test fixture')
    c.approve(root)
    lesson = dict(plan, day=1, title='第一课', reading_minutes=8, practice_minutes=practice)
    c.save(root/'data/Day01.json', lesson)
    document.render(root, root/'data/Day01.json', 'Day01', ['markdown'])
    document.review(root, 'Day01', 'Inspected synthetic test fixture')
    if delivered:
        publish(root, 'Day01'); c.deliver(root, 1)
    return lesson


def definition():
    common = {'objective': '辨别证据与推断', 'response_hint': '选择一个选项，或用一两句话解释',
              'source_refs': [{'source_id': 'S1', 'section_index': 0, 'quote': '保留中文、证据和图片'}],
              'hints': ['想想哪一项能回到原文核对。'], 'explanation': '引用是回到证据的入口，仍须核对主张。[S1]'}
    return {'key': 'Day01', 'revision': 1, 'estimated_minutes': 3, 'questions': [
        dict(common, id='choice1', kind='choice', prompt='哪种做法有助于核对主张？', actions=['select'],
             options=[{'id': 'source', 'text': '核对所引原文', 'feedback': '先看主张是否被原文支持。'},
                      {'id': 'length', 'text': '只看文章长度', 'feedback': '长度不能说明证据支持程度。'}], answer_id='source'),
        dict(common, id='short1', kind='short', prompt='为什么有引用仍需核对？', actions=['brief_text'],
             expected_answer='引用可能与主张不匹配，应核对原文。', rubric=[{'id': 'support', 'description': '说明需核对主张与原文是否匹配'}])
    ]}


def grading(result='met'):
    return {'criteria': [{'id': 'support', 'result': result, 'note': '根据作答与课程依据核对。'}],
            'strengths': ['识别了证据核对的作用'] if result == 'met' else [],
            'gaps': [] if result == 'met' else ['还需说明主张与原文的对应关系'],
            'explanation': '引用本身不保证支持主张。[S1]', 'source_ids': ['S1'],
            'next_step': '回看目标段落，比较一个主张与其来源。'}


class QuizTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        self.lesson = lesson_course(self.root)

    def tearDown(self): self.temp.cleanup()

    def engine(self):
        self.assertIsNotNone(importlib.util.find_spec('omni_quiz'), 'Light assessment runtime missing')
        import omni_quiz
        return omni_quiz

    def start(self, data=None, **kwargs):
        q = self.engine(); q.prepare(self.root, data or definition())
        return q.start(self.root, 'Day01', 'learner-start', '学完了，测一下我', **kwargs)['attempt_id']

    def reach_short(self):
        q = self.engine(); attempt = self.start()
        q.submit(self.root, attempt, 'choice1', 'answer-one', {'choice_id': 'source'})
        return q, attempt

    def test_public_question_hides_keys_rubric_hints_and_future_questions(self):
        q = self.engine(); attempt = self.start()
        view = q.next_question(self.root, attempt)
        self.assertEqual(view['status'], 'question')
        self.assertEqual(view['question']['id'], 'choice1')
        self.assertEqual({x['id'] for x in view['question']['options']}, {'source', 'length'})
        encoded = json.dumps(view, ensure_ascii=False)
        for secret in ('answer_id', 'expected_answer', 'rubric', 'hints', 'short1', '引用是回到证据的入口'):
            self.assertNotIn(secret, encoded)

    def test_prepare_is_immutable_and_start_requires_explicit_request(self):
        q = self.engine(); result = q.prepare(self.root, definition())
        self.assertFalse((self.root/'learning/records.json').exists())
        self.assertEqual(q.prepare(self.root, definition()), result)
        altered = definition(); altered['questions'][0]['answer_id'] = 'length'
        with self.assertRaises(ValueError): q.prepare(self.root, altered)
        with self.assertRaises(ValueError): q.start(self.root, 'Day01', 'start', '')

    def test_no_timer_or_course_state_changes(self):
        files = {p: p.read_bytes() for p in [self.root/'config.json', self.root/'plan.json', self.root/'state.json',
                 self.root/'manifests/Day01.json', self.root/'receipts/Day01.json']}
        q = self.engine(); attempt = self.start()
        q.submit(self.root, attempt, 'choice1', 'one', {'text': 'Ａ'})
        q.action(self.root, attempt, 'short1', 'skip', 'skip-two')
        self.assertEqual(q.next_question(self.root, attempt)['status'], 'complete')
        for path, before in files.items(): self.assertEqual(path.read_bytes(), before, str(path))
        self.assertIsNone(c.read(self.root/'state.json')['schedule'])
        self.assertEqual(c.read(self.root/'state.json')['mastery'], {})

    def test_stable_choice_ids_unicode_and_display_labels(self):
        q = self.engine(); data = definition(); data['questions'][0]['options'].reverse()
        attempt = self.start(data)
        view = q.next_question(self.root, attempt)
        self.assertEqual(view['question']['options'][0]['id'], 'length')
        response = q.submit(self.root, attempt, 'choice1', 'label-answer', {'text': 'Ｂ'})
        self.assertEqual(response['feedback']['verdict'], 'correct')
        self.assertFalse(response['assisted'])
        again = q.submit(self.root, attempt, 'choice1', 'label-answer', {'text': 'Ｂ'})
        self.assertEqual(again, response)
        with self.assertRaises(ValueError):
            q.submit(self.root, attempt, 'choice1', 'label-answer', {'text': 'Ａ'})

    def test_open_answer_is_persisted_before_grading_and_resumes(self):
        q, attempt = self.reach_short()
        result = q.submit(self.root, attempt, 'short1', 'raw-two', {'text': '引用可能并不能支持这句话。'})
        self.assertEqual(result['status'], 'needs_feedback')
        self.assertIn('引用可能', (self.root/'learning/records.json').read_text())
        self.assertEqual(q.next_question(self.root, attempt)['answer_id'], 'raw-two')
        resumed = q.start(self.root, 'Day01', 'continue', '继续短测')
        self.assertEqual(resumed['attempt_id'], attempt)
        result = q.feedback(self.root, attempt, 'short1', 'feedback-two', 'raw-two', grading())
        self.assertEqual(result['feedback']['verdict'], 'correct')
        self.assertEqual(q.next_question(self.root, attempt)['status'], 'complete')

    def test_stale_grading_rejected_without_losing_conversation(self):
        q, attempt = self.reach_short()
        q.submit(self.root, attempt, 'short1', 'draft1', {'text': '有引用就行？'})
        q.submit(self.root, attempt, 'short1', 'draft2', {'text': '补充：还要核对它是否支持主张。'})
        before = (self.root/'learning/records.json').read_bytes()
        with self.assertRaises(ValueError):
            q.feedback(self.root, attempt, 'short1', 'stale-feedback', 'draft1', grading())
        self.assertEqual(before, (self.root/'learning/records.json').read_bytes())
        self.assertEqual(q.next_question(self.root, attempt)['answer_id'], 'draft2')

    def test_hint_marks_assistance_and_reveal_and_skip_do_not_mark_correct(self):
        q = self.engine(); attempt = self.start()
        q.action(self.root, attempt, 'choice1', 'hint', 'hint1')
        r = q.submit(self.root, attempt, 'choice1', 'one', {'choice_id': 'source'})
        self.assertTrue(r['assisted'])
        q.action(self.root, attempt, 'short1', 'reveal', 'show2')
        summary = q.next_question(self.root, attempt)['summary']
        self.assertEqual(summary['revealed'], 1)
        self.assertEqual(summary['answered'], 1)
        self.assertEqual(summary['independent_correct'], 0)

    def test_pause_and_explicit_retake_are_idempotent(self):
        q = self.engine(); attempt = self.start()
        q.action(self.root, attempt, None, 'pause', 'later')
        self.assertEqual(q.next_question(self.root, attempt)['status'], 'paused')
        self.assertEqual(q.start(self.root, 'Day01', 'resume', '现在继续')['attempt_id'], attempt)
        q.action(self.root, attempt, 'choice1', 'skip', 'skip1')
        q.action(self.root, attempt, 'short1', 'skip', 'skip2')
        self.assertEqual(q.start(self.root, 'Day01', 'again', '继续')['attempt_id'], attempt)
        new = q.start(self.root, 'Day01', 'retake', '再测一次', new_attempt=True)['attempt_id']
        self.assertNotEqual(new, attempt)
        self.assertEqual(q.start(self.root, 'Day01', 'retake', '再测一次', new_attempt=True)['attempt_id'], new)

    def test_default_rejects_heavy_actions_but_allows_actual_practice_request(self):
        q = self.engine(); data = definition()
        data['questions'][1]['actions'] = ['write_code']
        with self.assertRaises(ValueError): q.prepare(self.root, data)
        data['practice_request'] = '我明确想通过编写代码训练这个技能。'
        self.assertEqual(q.prepare(self.root, data)['revision'], 1)

    def test_quiz_over_practice_budget_requires_extra_time_consent(self):
        q = self.engine(); data = definition(); data['estimated_minutes'] = 4
        self.assertTrue(q.prepare(self.root, data)['needs_extra_time_consent'])
        with self.assertRaises(ValueError): q.start(self.root, 'Day01', 'start', '测一下')
        self.assertIn('attempt_id', q.start(self.root, 'Day01', 'start', '愿意额外花时间', extra_time=True))

    def test_source_scope_and_duplicate_option_identity_are_rejected(self):
        q = self.engine()
        for change in ('unknown_source', 'wrong_quote', 'duplicate_id'):
            data = definition()
            if change == 'unknown_source': data['questions'][0]['source_refs'][0]['source_id'] = 'S99'
            if change == 'wrong_quote': data['questions'][0]['source_refs'][0]['quote'] = '不在课文里的句子'
            if change == 'duplicate_id': data['questions'][0]['options'][1]['id'] = 'source'
            with self.subTest(change=change), self.assertRaises(ValueError): q.prepare(self.root, data)

    def test_revision_does_not_replace_prior_attempt(self):
        q = self.engine(); attempt = self.start(); changed = definition(); changed['revision'] = 2
        changed['questions'][0]['prompt'] = '换个角度核对证据？'
        q.prepare(self.root, changed)
        self.assertEqual(q.start(self.root, 'Day01', 'resume', '继续')['attempt_id'], attempt)
        self.assertEqual(q.next_question(self.root, attempt)['revision'], 1)

    def test_feedback_requires_all_criteria_and_known_sources(self):
        q, attempt = self.reach_short(); q.submit(self.root, attempt, 'short1', 'two', {'text': '还应核对。'})
        for value in (dict(grading(), criteria=[]), dict(grading(), source_ids=['S99']), dict(grading(), score=100)):
            with self.subTest(value=value), self.assertRaises(ValueError):
                q.feedback(self.root, attempt, 'short1', 'bad', 'two', value)
        r = q.feedback(self.root, attempt, 'short1', 'uncertain', 'two', grading('uncertain'))
        self.assertEqual(r['feedback']['verdict'], 'needs_review')

    def test_feedback_corrections_append_and_revisions_are_assisted(self):
        q, attempt = self.reach_short(); q.submit(self.root, attempt, 'short1', 'two', {'text': '核对原文。'})
        q.feedback(self.root, attempt, 'short1', 'grade1', 'two', grading('not_met'))
        q.correct(self.root, attempt, 'short1', 'fix1', 'grade1', '用户指出评分遗漏已有要点。', grading())
        raw = (self.root/'learning/records.json').read_text()
        self.assertIn('grade1', raw); self.assertIn('fix1', raw)
        r = q.submit(self.root, attempt, 'short1', 'revised-answer', {'text': '我补充解释主张与原文的匹配。'}, revise=True)
        self.assertTrue(r['assisted'])

    def test_choice_key_dispute_withdraws_old_result_without_silent_rekey(self):
        q = self.engine(); attempt = self.start()
        q.submit(self.root, attempt, 'choice1', 'one', {'choice_id': 'length'})
        fix = {'verdict': 'withdrawn', 'explanation': '这道题需要重新核对。[S1]', 'source_ids': ['S1'],
               'strengths': [], 'gaps': [], 'next_step': '先不计此题，修订题目后再测。'}
        result = q.correct(self.root, attempt, 'choice1', 'fix', 'one', '用户质疑题目表述。', fix)
        self.assertEqual(result['feedback']['verdict'], 'withdrawn')
        with self.assertRaises(ValueError):
            q.correct(self.root, attempt, 'choice1', 'bad-fix', 'fix', '改变键', dict(fix, verdict='correct'))

    def test_binding_change_blocks_actions_and_keeps_answers(self):
        q = self.engine(); attempt = self.start(); q.submit(self.root, attempt, 'choice1', 'one', {'text': 'A'})
        path = self.root/'data/Day01.json'; path.write_text(path.read_text()+' ')
        with self.assertRaises(ValueError): q.next_question(self.root, attempt)
        self.assertIn('one', (self.root/'learning/records.json').read_text())

    def test_cannot_start_undelivered_lesson(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); lesson_course(root, delivered=False)
            q = self.engine(); q.prepare(root, definition())
            with self.assertRaises(ValueError): q.start(root, 'Day01', 'start', '开始')

    def test_json_csv_exports_preserve_answers_and_forget_keeps_delivery(self):
        q, attempt = self.reach_short()
        q.submit(self.root, attempt, 'short1', 'two', {'text': '=SUM(1,2)\n原始回答，保留换行'})
        self.assertIsNotNone(importlib.util.find_spec('omni_quiz_export'))
        from omni_quiz_export import export, forget
        state = (self.root/'state.json').read_bytes()
        export(self.root, self.root/'responses.json', 'json')
        self.assertIn('原始回答', (self.root/'responses.json').read_text())
        export(self.root, self.root/'responses.csv', 'csv')
        self.assertTrue((self.root/'responses.csv').exists())
        with self.assertRaises(ValueError): forget(self.root, confirm=False)
        forget(self.root, confirm=True)
        self.assertEqual((self.root/'state.json').read_bytes(), state)
        self.assertFalse((self.root/'learning/records.json').exists())
        self.assertEqual(q.status(self.root)['attempts'], [])

    def test_learning_store_rejects_symlink_escape(self):
        q = self.engine()
        with tempfile.TemporaryDirectory() as elsewhere:
            (self.root/'learning').symlink_to(elsewhere, target_is_directory=True)
            with self.assertRaises(ValueError): q.prepare(self.root, definition())
            self.assertEqual(list(Path(elsewhere).iterdir()), [])


if __name__ == '__main__': unittest.main()

class QuizRegressionTests(unittest.TestCase):
    setUp = QuizTests.setUp
    tearDown = QuizTests.tearDown
    engine = QuizTests.engine
    start = QuizTests.start
    def test_resume_request_replay_cannot_undo_a_later_pause(self):
        q=self.engine();attempt=self.start()
        q.action(self.root,attempt,None,'pause','pause1')
        q.start(self.root,'Day01','resume1','继续')
        q.action(self.root,attempt,None,'pause','pause2')
        before=(self.root/'learning/records.json').read_bytes()
        self.assertEqual(q.start(self.root,'Day01','resume1','继续')['status'],'paused')
        self.assertEqual(before,(self.root/'learning/records.json').read_bytes())
        with self.assertRaises(ValueError):q.start(self.root,'Day01','resume1','不同请求')
        with self.assertRaises(ValueError):q.start(self.root,'Day01','learner-start','学完了，测一下我',new_attempt=True)

    def test_letter_option_text_conflict_requires_canonical_selection(self):
        q=self.engine();data=definition()
        data['questions'][0]['options'][0]['text']='B'
        data['questions'][0]['options'][1]['text']='A'
        attempt=self.start(data)
        with self.assertRaises(ValueError):q.submit(self.root,attempt,'choice1','ambiguous',{'text':'B'})
        self.assertEqual(q.submit(self.root,attempt,'choice1','clear',{'choice_id':'source'})['feedback']['verdict'],'correct')
