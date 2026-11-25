import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/omni-learning-anything/scripts'
sys.path.insert(0, str(SCRIPTS))
import omni_core
from omni_figures import build, caption, validate_reading


class FigureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.spec = {
            'layout': 'comparison', 'title': 'Rate vs. total', 'credit': 'Teaching example',
            'columns': ['Group A', 'Group B'],
            'rows': [{'label': 'Count', 'values': ['20', '15']},
                     {'label': 'Sample', 'values': ['100', '30']}],
            'reading': {'question': 'Which group has a larger share?',
                        'observation': 'Read both rows. Group B has 15 of 30, or half.',
                        'source_ids': ['S1']},
        }

    def test_diagrams_are_visible_document_figures(self):
        from PIL import Image
        flow = dict(self.spec, layout='sequence', steps=[
            {'label': 'Count', 'detail': 'Find the cases.'},
            {'label': 'Divide', 'detail': 'Use the total in this group.'}])
        for spec in [self.spec, flow]:
            fig = build(self.root, spec)
            self.assertEqual(fig, build(self.root, spec))
            with Image.open(self.root / fig['path']) as im:
                self.assertEqual(im.format, 'PNG')
                self.assertGreater(im.width, im.height)
            validate_reading(fig, ['S1'], required=True)
            self.assertIn(spec['reading']['observation'], caption(fig))
            self.assertIn('[S1]', caption(fig))

    def test_fraction_lengths_share_the_same_origin_and_scale(self):
        from PIL import Image
        spec = dict(self.spec, layout='fraction-bars', unit='One metre',
                    bars=[{'numerator': n, 'denominator': d} for n, d in [(1, 2), (2, 4), (3, 4), (4, 4)]])
        f = build(self.root, spec)
        # Measure the rendered colored regions. Internal subdivision marks do not change their endpoints.
        with Image.open(self.root / f['path']) as image:
            color = (25, 106, 103)
            pixels = image.load()
            previous_y = -2
            bands = []
            for y in range(image.height):
                samples = [x for x in range(150, image.width) if pixels[x, y] == color]
                if len(samples) > 30:
                    if y != previous_y + 1:
                        spans = []
                        bands.append(spans)
                    spans.append((samples[0], samples[-1]))
                    previous_y = y
            self.assertEqual(len(bands), 4)
            self.assertTrue(all(len(set(spans)) == 1 for spans in bands))
            endpoints = [spans[0] for spans in bands]
            left, end = endpoints[-1]
            self.assertTrue(all(start == left for start, stop in endpoints))
            self.assertEqual(endpoints[0], endpoints[1])
            for (_, stop), expected in zip(endpoints, (0.5, 0.5, 0.75, 1.0)):
                self.assertAlmostEqual((stop - left) / (end - left), expected, places=2)

    def test_invalid_fractions_are_rejected(self):
        for n, d in [(-1, 4), (5, 4), (1, 0), (1, 40), (True, 2), (1, '2'), (0.5, 2)]:
            spec = dict(self.spec, layout='fraction-bars', unit='One metre',
                        bars=[{'numerator': 1, 'denominator': 2}, {'numerator': n, 'denominator': d}])
            with self.subTest(n=n, d=d), self.assertRaisesRegex(ValueError, 'fraction'):
                build(self.root, spec)

    def test_reading_is_visible_in_html_docx_and_markdown(self):
        from docx import Document
        from omni_document import render
        from test_documents import course
        plan = course(self.root)
        plan['figure'] = build(self.root, self.spec)
        omni_core.save(self.root / 'plan.json', plan)
        outputs = render(self.root, self.root / 'plan.json', 'plan', ['html', 'docx', 'markdown'])['artifacts']
        guide = self.spec['reading']['question']
        html = (self.root / outputs['html']).read_text()
        self.assertIn(guide, html.split('<figcaption>')[1].split('</figcaption>')[0])
        md = (self.root / outputs['markdown']).read_text()
        self.assertTrue(any(guide in line and not line.startswith('![') for line in md.splitlines()))
        paragraphs = Document(self.root / outputs['docx']).paragraphs
        self.assertTrue(any(guide in p.text for p in paragraphs))

    def test_bad_shape_and_empty_evidence_rejected(self):
        self.spec['rows'][0]['values'] = ['15']
        with self.assertRaises(ValueError):
            build(self.root, self.spec)
        for sources in ([], ['S2']):
            with self.assertRaises(ValueError):
                validate_reading({'reading': self.spec['reading']}, sources, required=True)
        with self.assertRaises(ValueError):
            validate_reading({}, ['S1'], required=True)
        validate_reading({}, ['S1'], required=False)

    def test_plan_enables_guides_for_future_lessons_and_legacy_input_survives(self):
        plan = {'topic': 'Rates', 'days': [{'day': 1, 'topic': 'Rates'}],
                'figure': {'reading': self.spec['reading']}, 'sources': [{'id': 'S1'}]}
        omni_core.initialize(self.root, {'timezone': 'UTC'}, plan)
        self.assertTrue(omni_core.read(self.root / 'config.json')['visual_guides'])
        plan.pop('figure')
        with self.assertRaises(ValueError):
            omni_core.initialize(self.root / 'new', {'timezone': 'UTC', 'visual_guides': True}, plan)
        omni_core.initialize(self.root / 'old', {'timezone': 'UTC'}, plan)
