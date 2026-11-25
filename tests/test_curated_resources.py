"""Selection, source scope and original-course compatibility for curated resources."""
import json
import copy
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from test_documents import SCRIPTS
import omni_courses as courses


class CuratedResourcesTests(unittest.TestCase):
    def test_discovery_and_offline_binding_cover_every_curated_resource(self):
        catalog = courses.catalog()
        results = courses.resources.discover(catalog)['resources']
        self.assertEqual(Counter(r['kind'] for r in results),
                         dict(course=18, textbook=13, academic_book=8, article=14, lecture_series=4, talk=11))
        self.assertEqual(len({r['url'] for r in results}), len(results))
        self.assertEqual(len(catalog['courses']), 67)
        for r in results:
            with self.subTest(resource=r['id']):
                binding = courses.bind(r['id'])
                self.assertEqual(binding['course']['sources'][0]['url'], r['url'])
                self.assertEqual(binding['course']['access_mode'], r['access'])
                self.assertTrue(binding['unit_ids'])
                courses.validate_binding(binding)

    def test_named_search_and_filtered_browsing_are_available_through_cli(self):
        def call(*args):
            run = subprocess.run([sys.executable, str(SCRIPTS/'omni_learning.py'), 'courses', *args],
                                 text=True, capture_output=True, check=True)
            return json.loads(run.stdout)

        match = call('search', '--query', '带我学 TED 的单一故事的危险')
        self.assertEqual(match['status'], 'matched')
        self.assertEqual(match['matches'][0]['id'], 'ted-adichie')
        self.assertEqual(call('search', '--query', 'TED 古代汉语')['status'], 'not_found')
        articles = call('resources', '--kind', 'article', '--query', '图神经网络')
        self.assertEqual([r['id'] for r in articles['resources']], ['distill-gnn'])
        talks = call('resources', '--kind', 'talk', '--query', 'TED')
        self.assertEqual(talks['total'], 10)
        courses_zh = call('resources', '--kind', 'course', '--language', 'zh')
        self.assertEqual(courses_zh['total'], 9)
        self.assertEqual(call('show', '--id', 'yale-ancient-greece')['edition'], 'Fall 2007')
        self.assertEqual(len(call('bind', '--id', 'ted-adichie')['unit_ids']), 1)

    def test_binding_distinguishes_edition_record_from_chapter_access(self):
        binding = courses.bind('sutton-reinforcement-learning')
        config = {'course_pathway': binding}
        plan = {'days': [{'day': 1, 'course_units': binding['unit_ids']}]}
        with self.assertRaisesRegex(ValueError, 'authorized chapters'):
            courses.validate_course_plan(config, plan)
        with self.assertRaisesRegex(ValueError, 'adapted study'):
            courses.bind('ted-adichie', practice='original_assignments')
        c = courses.bind('openstax-biology', unit_ids=['u01'])
        context = courses.context_section(c, ['u01'], 'zh')
        self.assertIn('1–16', context['body'])
        self.assertIn('Biology 2e', context['body'])

    def test_private_chapter_from_publisher_record_works_with_strict_sources(self):
        from PIL import Image
        import omni_core as core
        import omni_document as documents
        import omni_materials as materials

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            binding = courses.bind('sutton-reinforcement-learning')
            (root / 'assets').mkdir()
            Image.new('RGB', (120, 60), 'white').save(root / 'assets/figure.png')
            chapter = root / 'chapter.md'
            quote = 'This practice passage is synthetic.'
            chapter.write_text('# Test chapter\n\n' + quote, encoding='utf-8')
            item = materials.import_file(root, chapter)
            selection = materials.select(root, item['id'], item['version'], heading='Test chapter')
            source = materials.citation(root, selection, selection['units'][0], quote, 'S1')
            source['course_ref'] = courses.source_ref(binding, 'O1', binding['unit_ids'])
            self.assertNotIn('url', source)
            config = {'timezone': 'UTC', 'daily_minutes': 10, 'course_pathway': binding,
                      'materials': {'policy': 'strict', 'selections': [selection]}}
            plan = {'topic': 'Book', 'title': 'Reading plan',
                    'days': [{'day': 1, 'topic': 'First chapter', 'course_units': binding['unit_ids']}],
                    'sections': [{'title': 'Evidence', 'body': quote + ' [S1]'}], 'sources': [source],
                    'figure': {'path': 'assets/figure.png', 'caption': 'Lesson figure', 'credit': 'Test'}}
            core.initialize(root, config, plan)
            manifest = documents.render(root, root / 'plan.json', 'plan', ['html'])
            self.assertIn(quote, (root / manifest['artifacts']['html']).read_text())
            documents.review(root, 'plan', 'Reviewed scope and exact chapter')
            core.approve(root)
            lesson = dict(plan, title='First chapter', day=1, reading_minutes=6, practice_minutes=2,
                          course_units=binding['unit_ids'])
            core.save(root / 'data/Day01.json', lesson)
            documents.render(root, root / 'data/Day01.json', 'Day01', ['markdown'])
            for broken_ref in ('book', 'quote', 'url', 'material'):
                rejected = copy.deepcopy(lesson)
                modified = rejected['sources'][0]
                if broken_ref == 'book':
                    modified['course_ref']['sha256'] = '0' * 64
                elif broken_ref == 'quote':
                    modified['material_ref']['quote'] = 'Untaught claim'
                elif broken_ref == 'url':
                    modified['url'] = binding['course']['sources'][0]['url']
                else:
                    del modified['material_ref']
                with self.subTest(broken_ref=broken_ref), self.assertRaises(ValueError):
                    documents.validate_document(rejected, root)
