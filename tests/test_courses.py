"""Named university pathways must preserve source edition, order and consent."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from test_documents import SCRIPTS, course
import omni_core as c


def blueprint():
    return {'id':'harvard-positive-psychology','title':'Positive Psychology','institution':'Harvard',
            'code':'PSY 1504','edition':'Spring 2006','instructors':['Tal Ben-Shahar'],
            'aliases':['哈佛积极心理学','Harvard Positive Psychology'],'domain':'psychology',
            'level':'introductory','prerequisites':[],'audience':'Curious learners',
            'pace':{'description':'Two 90-minute sessions weekly'},'evidence_level':'syllabus_only',
            'sources':[{'id':'O1','title':'Original syllabus','url':'https://ppc.sas.upenn.edu/syllabus.pdf',
                        'locator':'pp. 1–2','checked_at':'2026-11-01','kind':'university_archive'}],
            'units':[{'id':f'u{i:02d}','title':f'Unit {i}','locator':f'Session {i}',
                      'source_id':'O1','focus':f'Outcome {i}'} for i in range(1,4)]}


class CourseTests(unittest.TestCase):
    def engine(self):
        self.assertIsNotNone(importlib.util.find_spec('omni_courses'),'University pathway helper missing')
        import omni_courses
        return omni_courses

    def bind(self,**kwargs):
        engine=self.engine()
        with patch.object(engine,'catalog',return_value={'schema':1,'checked_at':'2026-11-01','courses':[blueprint()]}):
            return engine.bind('harvard-positive-psychology',**kwargs)

    def plan(self):
        return {'topic':'Psychology','days':[{'day':i,'topic':str(i),'course_units':[f'u{i:02d}']} for i in range(1,4)]}

    def test_snapshot_is_self_contained_and_not_retargeted_by_catalog_upgrade(self):
        e=self.engine();binding=self.bind();saved=copy.deepcopy(binding)
        with patch.object(e,'catalog',side_effect=AssertionError('Must use approved snapshot')):
            e.validate_binding(binding)
            e.validate_course_plan({'course_pathway':binding},self.plan())
        self.assertEqual(binding,saved)

    def test_modified_snapshot_or_invalid_unit_is_rejected(self):
        e=self.engine();binding=self.bind();binding['course']['edition']='Spring 2008'
        with self.assertRaises(ValueError):e.validate_binding(binding)
        with self.assertRaises(ValueError):self.bind(unit_ids=['u99'])
        with self.assertRaises(ValueError):self.bind(unit_ids=['u02','u01'])
        with self.assertRaises(ValueError):self.bind(unit_ids=['u01','u01'])

    def test_days_must_cover_selected_units_in_original_order(self):
        e=self.engine();config={'course_pathway':self.bind()};plan=self.plan()
        e.validate_course_plan(config,plan)
        for units in ([['u02'],['u01'],['u03']],[['u01'],['u03'],['u03']],[['u01'],['u02'],['u99']]):
            changed=copy.deepcopy(plan)
            for day,mapping in zip(changed['days'],units):day['course_units']=mapping
            with self.assertRaises(ValueError):e.validate_course_plan(config,changed)

    def test_explicit_partial_scope_is_supported_without_claiming_full_course(self):
        e=self.engine();binding=self.bind(unit_ids=['u01']);plan=self.plan();plan['days']=plan['days'][:1]
        e.validate_course_plan({'course_pathway':binding},plan)
        context=e.context_section(binding,['u01'],'en')
        self.assertIn('1/3',context['body']);self.assertIn('2006',context['body'])
        self.assertIn('not',context['body'].lower())

    def test_existing_course_needs_no_pathway_or_migration(self):
        self.engine().validate_course_plan({'language':'zh'},self.plan())

    def test_missing_day_mapping_refused_at_initialization(self):
        binding=self.bind();plan=self.plan();del plan['days'][0]['course_units']
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):c.initialize(Path(tmp),{'timezone':'UTC','course_pathway':binding},plan)
            self.assertFalse((Path(tmp)/'state.json').exists())

    def test_course_sources_and_context_survive_html_and_markdown(self):
        from omni_document import render
        e=self.engine();binding=self.bind(unit_ids=['u01'])
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);plan=course(root,{'platform':'html','mode':'local'})
            config=c.read(root/'config.json');config['course_pathway']=binding;c.save(root/'config.json',config)
            plan['days'][0]['course_units']=['u01'];plan['sources']=plan['sources'][:1]
            plan['sources'][0].update(url=binding['course']['sources'][0]['url'],course_ref=e.source_ref(binding,'O1',['u01']))
            c.save(root/'plan.json',plan);manifest=render(root,root/'plan.json','plan',['html','markdown'])
            for fmt in ('html','markdown'):
                text=(root/manifest['artifacts'][fmt]).read_text()
                self.assertIn('Spring 2006',text);self.assertIn('Session 1',text)
            self.assertEqual(c.read(root/'plan.json'),plan)

    def test_unbound_or_wrong_source_cannot_be_presented_as_original_course(self):
        from omni_document import validate_document
        e=self.engine();binding=self.bind(unit_ids=['u01'])
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);plan=course(root);config=c.read(root/'config.json');config['course_pathway']=binding;c.save(root/'config.json',config)
            plan['days'][0]['course_units']=['u01'];c.save(root/'plan.json',plan)
            with self.assertRaises(ValueError):validate_document(plan,root)
            plan['sources'][0]['course_ref']=e.source_ref(binding,'O1',['u01'])
            with self.assertRaises(ValueError):validate_document(plan,root)

    def test_catalog_named_request_and_ambiguous_or_unknown_requests(self):
        e=self.engine()
        with patch.object(e,'catalog',return_value={'schema':1,'checked_at':'2026-11-01','courses':[blueprint()]}):
            result=e.resolve('我想学习哈佛积极心理学')
            self.assertEqual(result['status'],'matched');self.assertEqual(result['matches'][0]['id'],'harvard-positive-psychology')
            self.assertNotEqual(e.resolve('幸福课')['status'],'matched')
            self.assertNotEqual(e.resolve('Harvard Positive Psychology 2008')['status'],'matched')
            self.assertEqual(e.resolve('哈佛量子炼金术')['status'],'not_found')

    def test_cli_and_catalog_work_offline_and_leave_no_course_files(self):
        self.engine()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for args in [('list',),('welcome',),('search','--query','我想学习哈佛积极心理学'),('show','--id','mit-linear-algebra')]:
                run=subprocess.run([sys.executable,str(SCRIPTS/'omni_learning.py'),'--project',str(root),'courses',*args],capture_output=True,text=True)
                self.assertEqual(run.returncode,0,run.stderr);self.assertIsInstance(json.loads(run.stdout),dict)
            self.assertEqual(list(root.iterdir()),[])

    def test_ordinary_words_do_not_imply_an_institution(self):
        result=self.engine().resolve('CS50x with limited time')
        self.assertEqual(result['status'],'matched')
        self.assertEqual(result['matches'][0]['id'],'harvard-cs50x')

    def test_expanded_catalog_discovery_preserves_distinct_course_names(self):
        engine = self.engine()
        courses = engine.listing()['courses']
        self.assertEqual(len(courses), 67)
        self.assertEqual(sum(c['pathway_type'] == 'course' for c in courses), 65)
        self.assertEqual(sum(c['provider_type'] == 'ai_organization' for c in courses), 12)
        for query, provider in (
            ('我想学清华中国建筑史', 'tsinghua'),
            ('我想学上海交大唐诗宋词人文解读', 'sjtu'),
            ('Applied AI Foundations', 'openai'),
            ('Anthropic AI Fluency: Framework & Foundations', 'anthropic'),
            ('Hugging Face AI Agents Course', 'hugging-face'),
        ):
            with self.subTest(query=query):
                result = engine.resolve(query)
                self.assertEqual(result['status'], 'matched')
                self.assertTrue(result['matches'][0]['id'].startswith(provider + '-'))
        self.assertEqual(engine.resolve('AI Foundations and Applied AI Foundations')['status'],
                         'needs_clarification')
        for query in ('Anthropic Applied AI Foundations', 'Claude Academy Applied AI Foundations',
                      'HF Applied AI Foundations', 'HarvardX Applied AI Foundations'):
            with self.subTest(query=query):
                self.assertEqual(engine.resolve(query)['status'], 'not_found')
        self.assertEqual({c['provider_type'] for c in engine.welcome()['courses']},
                         {'university', 'ai_organization'})

    def test_open_references_are_discoverable_and_use_reading_scope(self):
        engine = self.engine()
        for query in ('清华人工智能通识教育红皮书', 'Smarthistory Reframing Art History'):
            with self.subTest(query=query):
                match = engine.resolve(query)
                self.assertEqual(match['status'], 'matched')
                selected = match['matches'][0]
                self.assertEqual(selected['pathway_type'], 'reference')
                binding = engine.bind(selected['id'], unit_ids=['u01'])
                scope = engine.context_section(binding, ['u01'], 'en')
                self.assertEqual(scope['title'], 'Source and reading scope')
                self.assertIn(binding['course']['units'][0]['locator'], scope['body'])
                with self.assertRaises(ValueError):
                    engine.bind(selected['id'], practice='original_assignments')

    def test_subject_year_in_course_title_is_distinct_from_edition(self):
        engine = self.engine()
        self.assertEqual(engine.resolve('MIT Art Since 1940')['status'], 'matched')
        self.assertEqual(engine.resolve('MIT Art Since 1940 2024')['status'], 'needs_clarification')
        self.assertEqual(engine.resolve('MIT Art Since 1940, Fall 1940 edition')['status'],
                         'needs_clarification')


if __name__=='__main__':unittest.main()
