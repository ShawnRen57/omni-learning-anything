"""Evidence-based, learner-started review, bounded budgets and safe future versions."""
import copy
import csv
import io
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from test_quiz import lesson_course, definition, grading
import omni_core as c
import omni_quiz as q
import omni_learning_store as store


class StudyFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)/'course'
        self.root.mkdir(); lesson_course(self.root)
        q.prepare(self.root, definition())
        self.original = {p: p.read_bytes() for p in self.root.rglob('*.json')}

    def tearDown(self): self.tmp.cleanup()

    def engine(self):
        import omni_study
        return omni_study

    def answered(self, choice='length', hint=False):
        a = q.start(self.root, 'Day01', 'start', '测一下')['attempt_id']
        if hint: q.action(self.root, a, 'choice1', 'hint', 'hint')
        q.submit(self.root, a, 'choice1', 'one', {'choice_id': choice})
        return a

    def item(self): return self.engine().profile(self.root)['items'][0]


class StudyTests(StudyFixture):
    def test_delivery_and_silence_are_not_learning(self):
        s = self.engine(); self.assertEqual(s.profile(self.root)['items'], [])
        report = s.report(self.root)
        self.assertEqual(report['answered_questions'], 0)
        self.assertEqual(report['observed_study_days'], 0)
        self.assertEqual(report['delivered_lessons'], 1)
        self.assertEqual(s.plan(self.root)['items'], [])

    def test_wrong_due_now_and_no_course_or_schedule_changes(self):
        self.answered(); s = self.engine(); item = self.item()
        self.assertEqual(item['judgment'], 'review')
        self.assertEqual(item['evidence']['answer_id'], 'one')
        self.assertEqual(item['source_refs'][0]['source_id'], 'S1')
        plan = s.plan(self.root)
        self.assertEqual(len(plan['items']), 1)
        self.assertLessEqual(plan['review_minutes']+plan['new_minutes'], plan['daily_minutes'])
        for path, before in self.original.items(): self.assertEqual(path.read_bytes(), before)
        self.assertNotIn('answer_id', plan['items'][0])
        self.assertNotIn('expected_answer', str(plan))

    def test_assisted_correct_due_tomorrow_and_independent_due_later(self):
        self.answered('source', hint=True); s = self.engine(); item = self.item()
        self.assertEqual(item['judgment'], 'assisted')
        self.assertEqual(s.plan(self.root)['items'], [])
        self.assertEqual(len(s.plan(self.root, now=datetime.now(timezone.utc)+timedelta(days=2))['items']), 1)
        self.assertEqual(s.report(self.root)['independent_correct'], 0)

    def test_pending_skip_and_disputed_are_not_wrong(self):
        a = self.answered('source')
        q.submit(self.root, a, 'short1', 'two', {'text': '不确定'})
        s = self.engine(); states = s.profile(self.root)['items']
        self.assertEqual(states[-1]['judgment'], 'pending_feedback')
        q.feedback(self.root, a, 'short1', 'grade', 'two', grading('uncertain'))
        self.assertEqual(s.profile(self.root)['items'][-1]['judgment'], 'clarify')
        self.assertFalse(any(x['question_id']=='short1' for x in s.plan(self.root)['items']))

    def test_annotation_is_private_idempotent_and_self_report_separate(self):
        self.answered(); s = self.engine(); item = self.item()
        s.annotate(self.root, item['id'], 'exclude', '不用复习这题', 'note1')
        s.annotate(self.root, item['id'], 'exclude', '不用复习这题', 'note1')
        self.assertEqual(s.plan(self.root)['items'], [])
        with self.assertRaises(ValueError): s.annotate(self.root,item['id'],'include','不同','note1')
        s.annotate(self.root,item['id'],'self_report','我自认为已经会了','note2')
        self.assertEqual(self.item()['judgment'], 'review')
        self.assertEqual(len(self.item()['annotations']), 2)
        s.annotate(self.root,item['id'],'include','继续复习','note3')
        self.assertEqual(len(s.plan(self.root)['items']), 1)
        self.assertEqual(s.evidence(self.root,item['id'])['observations'][0]['answer']['raw_answer'], {'choice_id':'length'})

    def test_review_is_single_question_isolated_and_requires_consent(self):
        original = self.answered(); s = self.engine(); item = self.item()
        with self.assertRaises(ValueError): s.start(self.root,item['id'],'review','')
        before = store.records(self.root)['attempts'][original]
        view = s.start(self.root,item['id'],'review','复习一下')
        review = view['attempt_id']; self.assertNotEqual(review, original)
        self.assertEqual(s.start(self.root,item['id'],'review','复习一下'), view)
        q.submit(self.root,review,'choice1','review-answer',{'choice_id':'source'})
        self.assertEqual(q.next_question(self.root,review)['status'], 'complete')
        self.assertEqual(q.start(self.root,'Day01','normal','继续短测')['attempt_id'], original)
        self.assertEqual(q.next_question(self.root,original)['question']['id'], 'short1')
        self.assertEqual(store.records(self.root)['attempts'][original]['events'], before['events'])
        self.assertEqual(self.item()['judgment'], 'independent')
        self.assertEqual(s.plan(self.root)['items'], [])
        with self.assertRaises(ValueError): q.submit(self.root,review,'short1','illegal',{'text':'no'})

    def test_budget_modes_and_honest_no_automatic_lesson_trimming(self):
        self.answered(); s = self.engine()
        s.settings(self.root,minutes=1)
        self.assertEqual(s.plan(self.root)['items'], [])  # item takes 2 minutes
        for mode in ('balanced','new_first','review_only'):
            result = s.plan(self.root,mode=mode,minutes=3)
            self.assertLessEqual(result['review_minutes']+result['new_minutes'], result['daily_minutes'])
            self.assertEqual(result['new_minutes'],0 if mode=='review_only' else result['daily_minutes']-result['review_minutes'])
        with self.assertRaises(ValueError): s.plan(self.root,minutes=10000)
        with self.assertRaises(ValueError): s.settings(self.root,minutes=-1)

    def test_correction_invalidates_prior_judgment_and_anki(self):
        a = self.answered(); s = self.engine()
        body=grading();body.pop('criteria');body['verdict']='withdrawn'
        q.correct(self.root,a,'choice1','correction','one','题目歧义',body)
        self.assertEqual(self.item()['judgment'],'withdrawn')
        self.assertEqual(s.plan(self.root)['items'],[])
        from omni_study_export import anki
        with self.assertRaises(ValueError): anki(self.root,Path(self.tmp.name)/'cards.csv')

    def test_anki_literal_csv_stable_identity_sources_no_overwrite(self):
        self.answered(); from omni_study_export import anki
        output=Path(self.tmp.name)/'cards.csv'; result=anki(self.root,output)
        self.assertEqual(result['cards'],1)
        raw=output.read_text(); self.assertTrue(raw.startswith('#separator:Comma\n#html:false\n'))
        rows=list(csv.reader(io.StringIO(raw.split('#columns:Front,Back,Tags\n',1)[1])))
        self.assertEqual(len(rows),1);self.assertEqual(len(rows[0]),3)
        self.assertIn('Omni-ID:',rows[0][0]);self.assertIn('[S1]',rows[0][1])
        self.assertEqual(anki(self.root,output),result)
        output.write_text('user data')
        with self.assertRaises(ValueError): anki(self.root,output)
        self.assertEqual(output.read_text(),'user data')

    def test_stale_bound_documents_fail_closed(self):
        self.answered(); s=self.engine(); data=c.read(self.root/'data/Day01.json');data['title']='changed';c.save(self.root/'data/Day01.json',data)
        with self.assertRaises(ValueError): s.plan(self.root)

    def test_forget_review_does_not_delete_answers_or_course(self):
        self.answered();s=self.engine();item=self.item();s.annotate(self.root,item['id'],'self_report','个人笔记','n')
        answers=(self.root/'learning/records.json').read_bytes()
        with self.assertRaises(ValueError):s.forget(self.root)
        s.forget(self.root,confirm=True)
        self.assertEqual((self.root/'learning/records.json').read_bytes(),answers)
        self.assertEqual(self.item()['annotations'],[])

    def test_weekly_report_excludes_old_events_but_preserves_current_correction(self):
        a=self.answered();s=self.engine();now=datetime.now(timezone.utc)
        records=store.records(self.root);records['attempts'][a]['events'][0]['at']=(now-timedelta(days=10)).isoformat();store.save(self.root,('records.json',),records)
        report=s.report(self.root,now=now)
        self.assertEqual(report['answered_questions'],0)
        self.assertEqual(report['observed_study_days'],0)
        with self.assertRaises(ValueError):s.report(self.root,days=0)


class RevisionTests(StudyFixture):
    def proposal(self):
        import omni_course_revision as r
        config=c.read(self.root/'config.json');config['daily_minutes']=20
        plan=c.read(self.root/'plan.json');plan['days'][0]['topic']='未来课程的新重点'
        return r, {'id':'next-v2','reason':'我想放慢进度','basis':'user_request','evidence':[], 'config':config,'plan':plan}

    def test_proposal_immutable_confirmed_separate_pending_course(self):
        r,data=self.proposal();value=r.propose(self.root,data)
        self.assertEqual(r.propose(self.root,data),value)
        changed=copy.deepcopy(data);changed['reason']='changed'
        with self.assertRaises(ValueError):r.propose(self.root,changed)
        destination=Path(self.tmp.name)/'course-v2'
        with self.assertRaises(ValueError):r.apply(self.root,data['id'],destination,'')
        result=r.apply(self.root,data['id'],destination,'同意此方案')
        self.assertEqual(c.read(destination/'state.json')['status'],'awaiting_approval')
        self.assertIsNone(c.read(destination/'state.json')['schedule'])
        self.assertEqual(c.read(destination/'state.json')['lessons'],{})
        self.assertEqual(r.apply(self.root,data['id'],destination,'同意此方案'),result)
        for path,before in self.original.items():self.assertEqual(path.read_bytes(),before)
        with self.assertRaises(ValueError):r.apply(self.root,data['id'],self.root/'nested','同意')
        for path in destination.rglob('*.json'):self.assertFalse(path.is_symlink())

    def test_proposal_evidence_and_original_binding_validate(self):
        a=self.answered();r,data=self.proposal();data['basis']='assessment';data['evidence']=[{'attempt_id':a,'question_id':'choice1','answer_id':'one','grade_id':'one'}]
        r.propose(self.root,data)
        body=grading();body.pop('criteria');body['verdict']='needs_review'
        q.correct(self.root,a,'choice1','correction','one','有疑义',body)
        with self.assertRaises(ValueError):r.apply(self.root,data['id'],Path(self.tmp.name)/'next','同意')

    def test_no_destination_changes_or_fabricated_assessment_basis(self):
        r,data=self.proposal();data['config']['delivery']={'platform':'html','mode':'local'}
        with self.assertRaises(ValueError):r.propose(self.root,data)
        r,data=self.proposal();data['basis']='assessment'
        with self.assertRaises(ValueError):r.propose(self.root,data)

class StudyIntegrationTests(StudyFixture):
    def invoke(self,*args,success=True):
        import subprocess,sys,json
        cli=Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts/omni_learning.py'
        result=subprocess.run([sys.executable,str(cli),'--project',str(self.root),*args],capture_output=True,text=True)
        self.assertEqual(result.returncode,0 if success else 1,result.stderr)
        return json.loads(result.stdout if success else result.stderr)

    def test_cli_review_feedback_recap_and_export(self):
        self.answered()
        plan=self.invoke('study','plan');self.assertEqual(len(plan['items']),1)
        item=plan['items'][0]['id']
        started=self.invoke('study','start','--item',item,'--request-id','review','--consent','复习')
        body=Path(self.tmp.name)/'answer.json';c.save(body,{'choice_id':'source'})
        self.invoke('quiz','answer','--attempt',started['attempt_id'],'--question','choice1','--event-id','answer','--input',str(body))
        self.assertEqual(self.invoke('quiz','next','--attempt',started['attempt_id'])['status'],'complete')
        self.assertEqual(self.invoke('study','report')['independent_correct'],1)
        output=Path(self.tmp.name)/'anki.csv'
        self.assertEqual(self.invoke('study','anki','--output',str(output))['cards'],1)
        self.assertFalse(self.invoke('study','forget',success=False)['ok'])

    def test_current_dispute_is_not_erased_by_a_later_retake(self):
        a=self.answered();body=grading();body.pop('criteria');body['verdict']='withdrawn'
        q.correct(self.root,a,'choice1','bad-question','one','这题有问题',body)
        q.action(self.root,a,'short1','skip','skip')
        second=q.start(self.root,'Day01','retake','再测一次',new_attempt=True)['attempt_id']
        q.submit(self.root,second,'choice1','new-answer',{'choice_id':'source'})
        self.assertEqual(self.item()['judgment'],'withdrawn')
        self.assertEqual(self.engine().plan(self.root)['items'],[])

    def test_repeated_review_request_pause_resume_and_answer_deletion(self):
        self.answered();s=self.engine();item=self.item();started=s.start(self.root,item['id'],'r1','复习');attempt=started['attempt_id']
        q.action(self.root,attempt,None,'pause','pause')
        resumed=s.start(self.root,item['id'],'r2','继续复习');self.assertEqual(resumed['attempt_id'],attempt)
        self.assertEqual(resumed['status'],'question')
        with self.assertRaises(ValueError):s.start(self.root,item['id'],'r2','不同请求')
        from omni_quiz_export import forget
        forget(self.root,confirm=True)
        self.assertEqual(s.profile(self.root)['items'],[])
        self.assertEqual(s.report(self.root)['observed_study_days'],0)

    def test_export_cannot_overwrite_course_or_follow_symlink(self):
        self.answered();from omni_study_export import anki
        with self.assertRaises(ValueError):anki(self.root,self.root/'cards.csv')
        target=Path(self.tmp.name)/'user.csv';target.write_text('private')
        link=Path(self.tmp.name)/'link.csv';link.symlink_to(target)
        with self.assertRaises(ValueError):anki(self.root,link)
        self.assertEqual(target.read_text(),'private')

    def test_new_revision_preserves_old_history_but_retires_old_queue(self):
        self.answered();d=definition();d['revision']=2;q.prepare(self.root,d)
        self.assertTrue(self.item()['retired']);self.assertEqual(self.engine().plan(self.root)['items'],[])

    def test_successful_review_interval_increases_without_mastery_claim(self):
        self.answered('source');s=self.engine();item=self.item();first=item['due']
        review=s.start(self.root,item['id'],'r','我想复习')['attempt_id']
        q.submit(self.root,review,'choice1','review-answer',{'choice_id':'source'})
        self.assertGreater(self.item()['due'],first)
        self.assertNotIn('mastery',self.item())

    def test_review_preferences_symlink_is_rejected(self):
        self.answered();external=Path(self.tmp.name)/'outside';external.mkdir()
        (self.root/'learning/review.json').symlink_to(external/'review.json')
        with self.assertRaises(ValueError):self.engine().settings(self.root,minutes=2)

    def test_new_course_copies_selected_material_snapshot(self):
        import omni_materials as m
        import omni_course_revision as r
        file=Path(self.tmp.name)/'book.txt';file.write_text('Chapter 1\nA source paragraph with enough learning context.')
        imported=m.import_file(self.root,file)
        selection=m.select(self.root,imported['id'],imported['version'])
        config=c.read(self.root/'config.json');config['materials']={'policy':'strict','selections':[selection]}
        data={'id':'materials-next','basis':'user_request','reason':'改用这份资料','evidence':[],'config':config,'plan':c.read(self.root/'plan.json')}
        r.propose(self.root,data);destination=Path(self.tmp.name)/'material-course'
        r.apply(self.root,data['id'],destination,'同意')
        self.assertEqual(m.verify_selection(destination,selection),m.verify_selection(self.root,selection))
        self.assertEqual(c.read(destination/'state.json')['status'],'awaiting_approval')

class ReviewRegressionTests(StudyFixture):
    def test_answer_revision_does_not_clear_unresolved_withdrawal(self):
        a=self.answered();body=grading();body.pop('criteria');body['verdict']='withdrawn'
        q.correct(self.root,a,'choice1','withdraw','one','题目本身有问题',body)
        q.submit(self.root,a,'choice1','revised-answer',{'choice_id':'source'},revise=True)
        self.assertEqual(self.item()['judgment'],'withdrawn')
        self.assertEqual(self.item()['evidence']['grade_id'],'withdraw')
        self.assertEqual(self.engine().plan(self.root)['items'],[])
        from omni_study_export import anki
        with self.assertRaises(ValueError):anki(self.root,Path(self.tmp.name)/'cards.csv')

    def test_paused_open_review_resumes_waiting_feedback(self):
        a=self.answered('source');q.submit(self.root,a,'short1','text',{'text':'不确定'})
        q.feedback(self.root,a,'short1','grade','text',grading('not_met'))
        s=self.engine();item=next(x for x in s.profile(self.root)['items'] if x['question_id']=='short1')
        review=s.start(self.root,item['id'],'review','复习这一题')['attempt_id']
        q.submit(self.root,review,'short1','new-text',{'text':'这次我解释一下'})
        q.action(self.root,review,None,'pause','pause')
        resumed=s.start(self.root,item['id'],'resume','继续复习')
        self.assertEqual(resumed['attempt_id'],review)
        self.assertEqual(resumed['status'],'needs_feedback')
        q.feedback(self.root,review,'short1','new-grade','new-text',grading())
        self.assertEqual(q.next_question(self.root,review)['status'],'complete')

    def test_same_answer_resolved_feedback_does_not_stay_disputed(self):
        a=self.answered('source');q.submit(self.root,a,'short1','text',{'text':'说明原文支持'})
        q.feedback(self.root,a,'short1','uncertain','text',grading('uncertain'))
        q.correct(self.root,a,'short1','resolved','uncertain','核对原文后确认',grading())
        item=next(x for x in self.engine().profile(self.root)['items'] if x['question_id']=='short1')
        self.assertEqual(item['judgment'],'independent')

    def test_proposal_cannot_use_revised_answer_to_hide_withdrawn_evidence(self):
        a=self.answered();body=grading();body.pop('criteria');body['verdict']='withdrawn'
        q.correct(self.root,a,'choice1','withdraw','one','题目有误',body)
        q.submit(self.root,a,'choice1','new-one',{'choice_id':'source'},revise=True)
        import omni_course_revision as r
        data={'id':'bad-basis','reason':'降低难度','basis':'assessment','evidence':[{'attempt_id':a,'question_id':'choice1','answer_id':'new-one','grade_id':'new-one'}], 'config':c.read(self.root/'config.json'),'plan':c.read(self.root/'plan.json')}
        with self.assertRaises(ValueError):r.propose(self.root,data)

    def test_course_timezone_sets_due_dates_and_recap_days(self):
        a=self.answered('source');records=store.records(self.root)
        records['attempts'][a]['events'][0]['at']='2026-10-30T18:30:00+00:00'
        store.save(self.root,('records.json',),records)
        s=self.engine();now=datetime(2026,11,2,16,5,tzinfo=timezone.utc)
        self.assertEqual(s.profile(self.root,now=now)['items'][0]['due'],'2026-11-03')
        self.assertEqual(len(s.plan(self.root,now=now)['items']),1)
        recap=s.report(self.root,days=4,now=now)
        self.assertEqual(recap['period'],{'from':'2026-10-31','to':'2026-11-03'})
        self.assertEqual(recap['observed_study_days'],1)

    def test_heavy_practical_question_is_never_default_review_or_anki(self):
        d=definition();d['revision']=2;d['practice_request']='用户明确要求训练编写代码';d['questions'][0]['actions']=['select','write_code']
        q.prepare(self.root,d)
        a=q.start(self.root,'Day01','practical','练习编程',revision=2)['attempt_id']
        q.submit(self.root,a,'choice1','answer',{'choice_id':'length'})
        s=self.engine();item=s.profile(self.root)['items'][0]
        self.assertFalse(item['lightweight']);self.assertEqual(s.plan(self.root)['items'],[])
        with self.assertRaises(ValueError):s.start(self.root,item['id'],'review','复习')
        from omni_study_export import anki
        with self.assertRaises(ValueError):anki(self.root,Path(self.tmp.name)/'heavy.csv')
