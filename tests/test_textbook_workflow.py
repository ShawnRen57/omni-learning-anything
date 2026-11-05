"""Textbook lessons locate and cite selected source pages and preserve original figures."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_documents import course
from PIL import Image
from PIL import ImageDraw
import omni_core as core
import omni_document as document
import omni_materials as materials


class TextbookWorkflowTests(unittest.TestCase):
    def test_course_revision_retains_original_textbook_evidence(self):
        from test_textbook_fetch import fixture_pdf, source
        from omni_course_revision import apply, propose
        from omni_textbook_fetch import acquire, source_pdf
        from omni_textbooks import bind, extract_figure

        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            original = work / 'textbook.pdf'
            original.write_bytes(fixture_pdf())
            book = {'book_id': 'ct-example', 'title': 'Test textbook', 'stage': '小学',
                    'repository': 'TapXWorld/ChinaTextbook', 'commit': '1' * 40,
                    'sources': [source('textbook.pdf', original.read_bytes())]}
            root = work / 'course'
            imported = acquire(root, book, local_pdf=original)
            version = imported['sha256']
            binding = bind(root, book, imported['material']['id'], version, '1', 'Source evidence')
            selection = binding['materials']['selections'][0]
            evidence = materials.citation(root, selection, selection['units'][0], 'Textbook evidence.', 'S1')
            figure = extract_figure(root, book, version, 1, (0.05, 0.1, 0.9, 0.9), 'Original page crop')
            config = dict(binding, timezone='Asia/Shanghai', language='en', daily_minutes=10, sample_mode=True)
            plan = {'title': 'Learn from the textbook', 'topic': 'Source evidence',
                    'days': [{'day': 1, 'topic': 'Read the page'}],
                    'sections': [{'title': 'Evidence', 'body': 'Read the selected page [S1].'}],
                    'sources': [evidence], 'figure': figure}
            core.initialize(root, config, plan)
            document.render(root, root / 'plan.json', 'plan', ['html'])
            document.review(root, 'plan', 'Checked the sample plan')
            core.approve(root)

            proposed = dict(id='slower', reason='Review in a shorter session', basis='user_request', evidence=[],
                            config=dict(config, daily_minutes=8), plan=dict(plan, title='Review source evidence'))
            propose(root, proposed)
            next_course = work / 'next-course'
            applied = apply(root, 'slower', next_course, 'I accept this example revision')
            self.assertEqual(applied['status'], 'awaiting_approval')
            self.assertEqual(source_pdf(next_course, book['book_id'], version).read_bytes(), original.read_bytes())
            self.assertEqual(core.read(root / 'config.json')['daily_minutes'], 10)
            document.render(next_course, next_course / 'plan.json', 'plan', ['html'])

    def test_lesson_requires_original_crop_from_selected_edition_and_page(self):
        from omni_textbooks import bind, extract_figure, locate
        from pypdf import PdfWriter
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = course(root, {'platform': 'html', 'mode': 'local'})
            original = root / 'book.pdf'
            figure = Image.new('RGB', (300, 100), 'white')
            ImageDraw.Draw(figure).rectangle((30, 30, 150, 70), fill='blue')
            figure.save(original)
            writer = PdfWriter(clone_from=original)
            from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject, ArrayObject
            page = writer.pages[0]
            page[NameObject('/Resources')][NameObject('/Font')] = DictionaryObject({
                NameObject('/F1'): DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                                    NameObject('/Subtype'): NameObject('/Type1'),
                                                    NameObject('/BaseFont'): NameObject('/Helvetica')})})
            stream = DecodedStreamObject()
            stream.set_data(b'BT /F1 10 Tf 10 90 Td (A square has four sides.) Tj ET')
            page[NameObject('/Contents')] = ArrayObject([page.raw_get('/Contents'), stream])
            writer.add_blank_page(width=300, height=100)
            with original.open('wb') as output:
                writer.write(output)
            item = materials.import_file(root, original)
            version = item['version']
            book = {'book_id': 'book-test', 'title': 'Test geometry', 'stage': '小学', 'grade': '三年级'}
            with patch('omni_textbooks.source_pdf', return_value=original):
                binding = bind(root, book, item['id'], version, '1', 'squares')
                config = dict(core.read(root / 'config.json'), **binding)
                core.save(root / 'config.json', config)
                self.assertEqual(locate(root, item['id'], version, 'square has')['matches'][0]['page'], 1)
                self.assertEqual(locate(root, item['id'], version, 'cylinder')['matches'], [])
                selection = binding['materials']['selections'][0]
                plan['sources'] = [materials.citation(root, selection, selection['units'][0],
                                                      'A square has four sides.', 'S1')]
                with self.assertRaisesRegex(ValueError, 'original'):
                    document.validate_document(plan, root)
                plan['figure'] = extract_figure(root, book, version, 1, (0.05, 0.1, 0.9, 0.9), 'Square')
                document.validate_document(plan, root)
                wrong = extract_figure(root, book, version, 2, (0.05, 0.1, 0.9, 0.9), 'Wrong page')
                with self.assertRaisesRegex(ValueError, 'selected'):
                    document.validate_document(dict(plan, figure=wrong), root)
                (root / plan['figure']['path']).write_bytes(b'edited')
                with self.assertRaisesRegex(ValueError, 'changed'):
                    document.validate_document(plan, root)
