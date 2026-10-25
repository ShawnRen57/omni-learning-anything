"""Language selection must affect real artifacts without changing authored text."""
import sys,json,tempfile,unittest
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts'))
import omni_core as core
import omni_document as document
from test_documents import course

HEADINGS={'en':'Further reading (optional)','zh':'扩展学习（选读）','ja':'参考資料（任意）','ko':'추가 읽기 자료 (선택)','es':'Lecturas complementarias (opcional)','fr':'Pour aller plus loin (facultatif)','de':'Weiterführende Literatur (optional)','pt':'Leituras complementares (opcional)','ru':'Дополнительные материалы (по желанию)','ar':'قراءات إضافية (اختيارية)'}

class LanguageTests(unittest.TestCase):
 def test_all_ten_confirmed_languages_are_valid(self):
  for code in HEADINGS:
   with self.subTest(language=code):core.validate_config({'timezone':'UTC','language':code})
  for code in ['xx','EN',None,[],{}]:
   with self.assertRaises(ValueError):core.validate_config({'timezone':'UTC','language':code})

 def test_markdown_docx_and_preview_use_selected_language(self):
  from docx import Document
  for code,heading in HEADINGS.items():
   with self.subTest(language=code),tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);plan=course(root);config=core.read(root/'config.json');config['language']=code;core.save(root/'config.json',config)
    manifest=document.render(root,root/'plan.json','plan',['markdown','docx'])
    md=(root/manifest['artifacts']['markdown']).read_text()
    self.assertIn('## '+heading,md)
    self.assertIn(plan['sections'][0]['body'],md)
    doc=Document(root/manifest['artifacts']['docx']);self.assertIn(heading,'\n'.join(p.text for p in doc.paragraphs))
    self.assertEqual(len(doc.inline_shapes),1)
    preview=(root/manifest['previews'][0]).read_text();self.assertIn('lang="'+code+'"',preview);self.assertIn(heading,preview)
    for source in plan['sources']:self.assertIn(source['url'],md)
    core.manifest_ok(root,manifest)

 def test_arabic_docx_has_bidi_and_complex_script_font(self):
  ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);plan=course(root);config=core.read(root/'config.json');config['language']='ar';core.save(root/'config.json',config)
   manifest=document.render(root,root/'plan.json','plan',['docx'])
   preview=(root/manifest['previews'][0]).read_text();self.assertIn('dir="rtl"',preview)
   with ZipFile(root/manifest['artifacts']['docx']) as z:
    tree=ET.fromstring(z.read('word/document.xml'));styles=ET.fromstring(z.read('word/styles.xml'))
    self.assertTrue(tree.findall('.//w:pPr/w:bidi',ns));self.assertTrue(tree.findall('.//w:rPr/w:rtl',ns))
    fonts=styles.findall('.//w:rFonts',ns);self.assertTrue(any(f.get('{'+ns['w']+'}cs') for f in fonts))

 def test_cjk_locales_declare_their_own_fonts(self):
  for code,allowed in [('ja',{'Hiragino Mincho ProN','Noto Serif CJK JP','Yu Mincho','MS Mincho','Arial Unicode MS'}),('ko',{'Apple SD Gothic Neo','Noto Serif CJK KR','Malgun Gothic','Batang','Arial Unicode MS'})]:
   with self.subTest(language=code),tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);plan=course(root);config=core.read(root/'config.json');config['language']=code;core.save(root/'config.json',config)
    manifest=document.render(root,root/'plan.json','plan',['docx'])
    with ZipFile(root/manifest['artifacts']['docx']) as z:
     tree=ET.fromstring(z.read('word/styles.xml'));ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
     fonts=[v.get('{'+ns['w']+'}eastAsia') for v in tree.findall('.//w:rFonts',ns)]
     self.assertTrue(any(v in allowed for v in fonts))
    text=document.subtitle({'reading_minutes':8,'practice_minutes':3},plan,config,'2026-10-25','Day01')
    self.assertNotIn('阅读',text);self.assertNotIn('Read ',text)

 def test_pdf_labels_and_script_fonts(self):
  import omni_pdf as pdf
  for code,heading in HEADINGS.items():
   with self.subTest(language=code):
    preamble=pdf.language_preamble(code)
    self.assertNotIn('Source-grounded learning',preamble) if code!='en' else None
    if code=='ar':self.assertIn(r'\setdefaultlanguage{arabic}',preamble)
    if code=='ja':self.assertIn('Hiragino Mincho ProN',preamble)
    if code=='ko':self.assertIn('Apple SD Gothic Neo',preamble)

 def test_arabic_docx_keeps_latin_dates_ltr_and_paragraphs_at_start(self):
  ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};w='{'+ns['w']+'}'
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);course(root);config=core.read(root/'config.json');config['language']='ar';core.save(root/'config.json',config)
   m=document.render(root,root/'plan.json','plan',['docx'])
   with ZipFile(root/m['artifacts']['docx']) as z:tree=ET.fromstring(z.read('word/document.xml'))
   dates=[r for r in tree.findall('.//w:r',ns) if '2026-' in ''.join(t.text or '' for t in r.findall('w:t',ns))]
   self.assertTrue(dates)
   self.assertTrue(all(r.find('w:rPr/w:rtl',ns).get(w+'val')=='0' for r in dates))
   self.assertTrue(all(p.find('w:pPr/w:jc',ns).get(w+'val')=='start' for p in tree.findall('.//w:body/w:p',ns)))

 def test_arabic_docx_dates_have_directional_boundaries(self):
  from omni_http import normalize
  self.assertEqual(normalize('2026-10-25'),normalize('\u200e2026-10-25\u200e'))
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);course(root);config=core.read(root/'config.json');config['language']='ar';core.save(root/'config.json',config)
   m=document.render(root,root/'plan.json','plan',['docx'])
   with ZipFile(root/m['artifacts']['docx']) as z:tree=ET.fromstring(z.read('word/document.xml'))
   text=''.join(t.text or '' for t in tree.iter() if t.tag.endswith('}t'))
   self.assertIn('\u200e'+core.today(root)+'\u200e',text)
