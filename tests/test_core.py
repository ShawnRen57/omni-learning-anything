import sys, tempfile, unittest, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts'))
import omni_core as c

class CoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.plan={'topic':'测试','days':[{'day':1,'topic':'一'},{'day':2,'topic':'二'}]}
        c.initialize(self.root, {'timezone':'Asia/Shanghai','sample_mode':False}, self.plan)
    def tearDown(self): self.tmp.cleanup()
    def ready(self):
        c.save(self.root/'state.json',dict(c.read(self.root/'state.json'),approved_plan=c.digest(self.root/'plan.json'),approved_config=c.digest(self.root/'config.json'),status='active'))
    def test_unapproved_cannot_continue(self):
        with self.assertRaises(ValueError): c.next_action(self.root)
    def test_changed_plan_requires_reapproval(self):
        self.ready(); c.save(self.root/'plan.json',dict(self.plan,topic='变更'))
        with self.assertRaises(ValueError): c.next_action(self.root)
    def test_progress_waits_for_delivery(self):
        self.ready(); self.assertEqual(c.next_action(self.root)['day'],1)
    def test_unreviewed_cannot_deliver(self):
        self.ready()
        with self.assertRaises(ValueError): c.deliver(self.root,1)
    def test_pause_blocks_generation(self):
        self.ready(); c.set_status(self.root,'paused')
        self.assertEqual(c.next_action(self.root)['action'],'paused')
    def test_lock_prevents_concurrency(self):
        with c.lock(self.root):
            with self.assertRaises(RuntimeError):
                with c.lock(self.root): pass
    def test_existing_project_not_overwritten(self):
        with self.assertRaises(ValueError): c.initialize(self.root,{'timezone':'UTC'},self.plan)
    def test_sequential_plan(self):
        with self.assertRaises(ValueError): c.validate_plan({'topic':'a','days':[{'day':2,'topic':'x'}]})
    def fixture_manifest(self,key):
        p=self.root/(key+'.pdf'); p.write_bytes(b'PDF state fixture')
        c.save(self.root/'manifests'/(key+'.json'),{'pdf':p.name,'files':{p.name:c.digest(p),'plan.json':c.digest(self.root/'plan.json')},'reviewed_at':c.today(self.root)})
    def test_repeat_delivery_and_daily_limit(self):
        self.ready(); self.fixture_manifest('Day01'); c.deliver(self.root,1)
        self.assertEqual(c.deliver(self.root,1)['action'],'already_recorded')
        self.assertEqual(c.next_action(self.root)['action'],'already_delivered_today')
        self.assertEqual(len(c.read(self.root/'state.json')['lessons']),1)
    def test_modified_pdf_blocks_delivery(self):
        self.ready(); self.fixture_manifest('Day01'); (self.root/'Day01.pdf').write_bytes(b'changed')
        with self.assertRaises(ValueError): c.deliver(self.root,1)
        self.assertFalse(c.read(self.root/'state.json')['lessons'])
    def test_notification_retry_reuses_file(self):
        self.ready(); self.fixture_manifest('Day01')
        self.assertEqual(c.next_action(self.root)['action'],'deliver_existing')
        self.assertEqual(c.next_action(self.root)['day'],1)
    def test_sample_cannot_schedule(self):
        self.ready(); config=c.read(self.root/'config.json'); config['sample_mode']=True; c.save(self.root/'config.json',config)
        self.ready()
        with self.assertRaisesRegex(ValueError,'Sample projects'): c.record_schedule(self.root,'codex','fake')
    def test_completion_after_last_delivery(self):
        self.ready(); config=c.read(self.root/'config.json'); config['sample_mode']=True; c.save(self.root/'config.json',config)
        self.ready()
        self.fixture_manifest('Day01'); c.deliver(self.root,1); self.fixture_manifest('Day02')
        self.assertTrue(c.deliver(self.root,2)['stop_host_schedule'])
        self.assertEqual(c.next_action(self.root)['action'],'complete')
    def test_changed_config_blocks_progress(self):
        self.ready(); config=c.read(self.root/'config.json'); config['timezone']='UTC'; c.save(self.root/'config.json',config)
        with self.assertRaises(ValueError): c.next_action(self.root)
    def test_init_checks_existence_inside_lock(self):
        from contextlib import contextmanager
        from unittest.mock import patch
        root=self.root/'race'; root.mkdir()
        @contextmanager
        def competing_lock(target):
            c.save(root/'plan.json',{'topic':'first writer'})
            yield
        with patch.object(c,'lock',competing_lock):
            with self.assertRaises(ValueError): c.initialize(root,{'timezone':'UTC'},self.plan)
        self.assertEqual(c.read(root/'plan.json')['topic'],'first writer')
    def test_render_refuses_archived_plan_before_writes(self):
        from omni_pdf import render
        self.ready(); self.fixture_manifest('plan')
        before=c.digest(self.root/'manifests/plan.json')
        with self.assertRaises(ValueError): render(self.root,self.root/'plan.json','plan')
        self.assertEqual(c.digest(self.root/'manifests/plan.json'),before)
    def test_started_plan_cannot_rerender(self):
        from omni_pdf import render
        self.ready(); st=c.read(self.root/'state.json');st['lessons']={'1':{}};c.save(self.root/'state.json',st)
        with self.assertRaises(ValueError): render(self.root,self.root/'plan.json','plan')
    def test_review_rejects_path_escape(self):
        from omni_pdf import review
        with self.assertRaises(ValueError): review(self.root,'../escape','test')
    def test_tex_escaping(self):
        from omni_pdf import esc
        self.assertIn(r'\textbackslash{}',esc(r'\input{secret}'))
    def test_validation_rejects_fewer_than_five_links(self):
        from omni_pdf import validate_document
        with self.assertRaises(ValueError): validate_document({'sources':[]},self.root)
    def test_repeat_approval_preserves_pause(self):
        self.fixture_manifest('plan'); c.approve(self.root); c.set_status(self.root,'paused')
        c.approve(self.root)
        self.assertEqual(c.read(self.root/'state.json')['status'],'paused')
    def test_repeat_approval_preserves_completion(self):
        self.fixture_manifest('plan'); c.approve(self.root)
        state=c.read(self.root/'state.json'); state['status']='complete'; c.save(self.root/'state.json',state)
        c.approve(self.root)
        self.assertEqual(c.read(self.root/'state.json')['status'],'complete')
    def test_delivered_review_is_immutable(self):
        from omni_pdf import review
        self.ready(); self.fixture_manifest('Day01'); c.deliver(self.root,1)
        before=(self.root/'manifests/Day01.json').read_bytes()
        with self.assertRaises(ValueError): review(self.root,'Day01','Overwrite delivered review')
        self.assertEqual((self.root/'manifests/Day01.json').read_bytes(),before)
    def test_modified_delivery_manifest_blocks_continuation(self):
        self.ready(); self.fixture_manifest('Day01'); c.deliver(self.root,1)
        path=self.root/'manifests/Day01.json'; c.save(path,dict(c.read(path),review_note='changed'))
        with self.assertRaises(ValueError): c.next_action(self.root)
    def test_modified_delivery_manifest_blocks_repeat_recording(self):
        self.ready(); self.fixture_manifest('Day01'); c.deliver(self.root,1)
        path=self.root/'manifests/Day01.json'; c.save(path,dict(c.read(path),review_note='changed'))
        with self.assertRaises(ValueError): c.deliver(self.root,1)
    def test_invalid_config_fails_before_initialization(self):
        for field,value in [('time','99:99'),('time','9:3'),('weekdays',['InvalidDay']),
                            ('weekdays',[]),('daily_minutes',-1),('daily_minutes',True),
                            ('daily_minutes','15'),('sample_mode','false'),('language','unknown')]:
            with self.subTest(field=field,value=value):
                root=self.root/'invalid'; config={'timezone':'UTC',field:value}
                with self.assertRaises(ValueError): c.initialize(root,config,self.plan)
                self.assertFalse((root/'state.json').exists())

if __name__=='__main__': unittest.main()
