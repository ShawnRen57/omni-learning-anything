"""Reject malformed lesson durations before generating any artifact."""
import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts'))
import omni_core as c, omni_pdf as p
from PIL import Image

class TimeBudgetTests(unittest.TestCase):
    @unittest.skipUnless(p.executable('xelatex'),'XeLaTeX required')
    def test_failed_compile_retries_same_lesson(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'assets').mkdir(); image=root/'assets/f.png'; image.write_bytes(b'broken PNG')
            plan={'topic':'QA','title':'QA','days':[{'day':1,'topic':'One'}]}
            c.initialize(root,{'timezone':'UTC','daily_minutes':15},plan)
            c.save(root/'manifests/plan.json',{'files':{'plan.json':c.digest(root/'plan.json')},'reviewed_at':c.today(root)})
            c.approve(root)
            lesson={'day':1,'title':'One','reading_minutes':8,'practice_minutes':3,
                'sections':[{'title':'QA','body':'Synthetic test [S1].'}],
                'figure':{'path':'assets/f.png','caption':'QA','credit':'Code drawn test fixture'},
                'sources':[{'id':f'S{i}','title':'QA','url':f'https://example.com/{i}','publisher':'QA',
                    'published_at':'N/A','checked_at':c.today(root),'note':'Synthetic fixture'} for i in range(1,6)]}
            c.save(root/'data/Day01.json',lesson)
            with self.assertRaises(RuntimeError): p.render(root,root/'data/Day01.json','Day01')
            self.assertFalse((root/'manifests/Day01.json').exists())
            self.assertFalse(c.read(root/'state.json')['lessons'])
            self.assertEqual(c.next_action(root),{'action':'generate','day':1,'topic':'One'})
            Image.new('RGB',(80,80),'teal').save(image)
            p.render(root,root/'data/Day01.json','Day01')
            self.assertEqual(c.next_action(root)['action'],'review_existing')
            self.assertFalse(c.read(root/'state.json')['lessons'])
    def test_invalid_components_never_render(self):
        for reading,practice in [(-5,10),(8,-1),(0,3),(True,3),(8,'3'),(8,3.5),(13,3)]:
            with self.subTest(reading=reading,practice=practice), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp); (root/'assets').mkdir(); Image.new('RGB',(80,80),'teal').save(root/'assets/f.png')
                plan={'topic':'QA','title':'QA','days':[{'day':1,'topic':'One'}]}
                c.initialize(root,{'timezone':'UTC','daily_minutes':15},plan)
                c.save(root/'manifests/plan.json',{'files':{'plan.json':c.digest(root/'plan.json')},'reviewed_at':c.today(root)})
                c.approve(root)
                lesson={'day':1,'title':'One','reading_minutes':reading,'practice_minutes':practice,
                    'sections':[{'title':'QA','body':'Synthetic test [S1].'}],
                    'figure':{'path':'assets/f.png','caption':'QA','credit':'QA fixture'},
                    'sources':[{'id':f'S{i}','title':'QA','url':f'https://example.com/{i}','publisher':'QA',
                        'published_at':'N/A','checked_at':c.today(root),'note':'Synthetic fixture'} for i in range(1,6)]}
                c.save(root/'data/Day01.json',lesson)
                with self.assertRaises(ValueError): p.render(root,root/'data/Day01.json','Day01')
                self.assertFalse((root/'manifests/Day01.json').exists())
                self.assertEqual(c.next_action(root)['action'],'generate')
