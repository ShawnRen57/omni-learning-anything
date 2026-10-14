"""Real XeLaTeX integration. Uses synthetic metadata, not live-source claims."""
import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts'))
import omni_core as c,omni_pdf as p
from PIL import Image
from pypdf import PdfReader
class RenderTest(unittest.TestCase):
 @unittest.skipUnless(p.executable('xelatex'),'XeLaTeX required')
 def test_single_section_multilingual_and_tex_safety(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp); (root/'assets').mkdir();Image.new('RGB',(300,80),'teal').save(root/'assets/figure.png')
   config={'timezone':'UTC','language':'en','daily_minutes':15}
   plan={'topic':'Fixture','title':'测试 / TeX safety','days':[{'day':1,'topic':'One'}],
    'sections':[{'title':'One section','body':r'中文 English [S1]. Literal characters: \input{NEVER_EXECUTE} 50% $ & # _ ~ ^.'}],
    'figure':{'path':'assets/figure.png','caption':'Synthetic test fixture','credit':'Generated locally for testing'},
    'sources':[{'id':f'S{i}','title':f'Fixture {i}','url':f'https://example.com/source-{i}','publisher':'Test fixture','note':'Not a research source','published_at':'N/A','checked_at':'pending'} for i in range(1,6)]}
   c.initialize(root,config,plan)
   for s in plan['sources']:s['checked_at']=c.today(root)
   c.save(root/'plan.json',plan)
   m=p.render(root,root/'plan.json','plan');self.assertEqual(m['report']['links'],5)
   markdown=next((root/'sources').glob('*.md')).read_text()
   self.assertIn('## Further reading (optional)',markdown)
   self.assertIn('Published:',markdown)
   self.assertIn('Checked:',markdown)
   reader=PdfReader(root/m['pdf'])
   import pypdfium2 as pdfium
   doc=pdfium.PdfDocument(root/m['pdf']);text=''.join(doc[i].get_textpage().get_text_range() for i in range(len(doc)));doc.close()
   self.assertIn('NEVER_EXECUTE',text);self.assertIn('中文',text)
   self.assertTrue(any(list(pg.images) for pg in reader.pages))
   c.manifest_ok(root,m)
   with self.assertRaises(ValueError):c.approve(root)
   self.assertIsNone(m['reviewed_at'])
if __name__=='__main__':unittest.main()
