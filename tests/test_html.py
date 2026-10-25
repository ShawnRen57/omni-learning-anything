import base64,sys,tempfile,unittest
from pathlib import Path
from html.parser import HTMLParser
from test_documents import course
import omni_core as c,omni_document as d,omni_delivery as delivery
class Tags(HTMLParser):
 def __init__(self,text):super().__init__();self.items=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.items.append((tag,dict(attrs)))
class HtmlTests(unittest.TestCase):
 def test_standalone_escaped_localized_artifact_and_receipt(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);plan=course(root,{'platform':'html','mode':'local'});config=c.read(root/'config.json');config['language']='ar';c.save(root/'config.json',config)
   plan['sections'][0]['body']='<script>alert("x")</script> & [S1]';c.save(root/'plan.json',plan)
   self.assertEqual(delivery.default_formats(config),['html'])
   m=d.render(root,root/'plan.json','plan',['html']);artifact=root/m['artifacts']['html'];text=artifact.read_text();tags=Tags(text)
   self.assertEqual(next(a for t,a in tags.items if t=='html'),{'lang':'ar','dir':'rtl'})
   self.assertFalse(any(t in ('script','link') for t,a in tags.items))
   self.assertIn('&lt;script&gt;',text)
   self.assertEqual({a['href'] for t,a in tags.items if t=='a'},{s['url'] for s in plan['sources']})
   images=[a['src'] for t,a in tags.items if t=='img'];self.assertEqual(len(images),1)
   self.assertEqual(base64.b64decode(images[0].split(',',1)[1]),(root/plan['figure']['path']).read_bytes())
   self.assertEqual(text,(root/m['previews'][0]).read_text())
   d.review(root,'plan','Checked standalone HTML image, title, text and five links');r=delivery.publish(root,'plan');self.assertEqual(r['status'],'verified');self.assertEqual(r['artifact'],m['artifacts']['html'])
   artifact.write_text(text+'tampered')
   with self.assertRaises(ValueError):delivery.publish(root,'plan')
 def test_cli_html_default_does_not_require_tex(self):
  import subprocess,os,json
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);course(root,{'platform':'html','mode':'local'})
   cli=Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts/omni_learning.py'
   proc=subprocess.run([sys.executable,str(cli),'--project',str(root),'render','--input',str(root/'plan.json'),'--key','plan'],capture_output=True,text=True,env=dict(os.environ,PATH=''))
   self.assertEqual(proc.returncode,0,proc.stderr);m=json.loads(proc.stdout);self.assertTrue(m['artifact'].endswith('.html'))
 def test_mixed_pdf_html_keeps_selected_delivery(self):
  import omni_pdf
  if not omni_pdf.executable('xelatex'):self.skipTest('XeLaTeX unavailable')
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);course(root,{'platform':'html','mode':'local'})
   m=d.render(root,root/'plan.json','plan',['html','pdf']);self.assertIn('pdf',m['artifacts']);self.assertIn('html',m['artifacts']);c.manifest_ok(root,m)
   tags=Tags((root/m['artifacts']['html']).read_text());self.assertEqual(len([a for t,a in tags.items if t=='a']),5)
   d.review(root,'plan','Synthetic QA checks');self.assertEqual(delivery.publish(root,'plan')['artifact'],m['artifacts']['html'])
