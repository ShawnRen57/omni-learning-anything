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

 def test_arabic_pdf_preserves_multiple_paragraphs_and_mixed_scripts(self):
  import omni_pdf as pdf
  if not pdf.executable('xelatex'):self.skipTest('XeLaTeX required')
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);plan=course(root);config=core.read(root/'config.json');config['language']='ar';core.save(root/'config.json',config)
   plan['title']='خطة التعلم';plan['sections'][0]={'title':'هدف التعلم','body':'فقرة أولى [S1].\n\nفقرة ثانية مع Latin text.\n \nLATIN_PARAGRAPH [S2].\r\n\r\nفقرة أخيرة.'}
   core.save(root/'plan.json',plan)
   m=pdf.render(root,root/'plan.json','plan')
   self.assertEqual(m['report']['links'],5);core.manifest_ok(root,m)
   self.assertIn(plan['sections'][0]['body'],next((root/'sources').glob('*.md')).read_bytes().decode())
   import pypdfium2 as pdfium
   doc=pdfium.PdfDocument(root/m['pdf'])
   text=''.join(doc[i].get_textpage().get_text_range() for i in range(len(doc)));doc.close()
   self.assertIn('LATIN_PARAGRAPH',text)

 def test_pdf_mixed_target_scripts_keep_shapes_and_word_order(self):
  import omni_pdf as pdf
  import pypdfium2 as pdfium
  from unicodedata import normalize
  if not pdf.executable('xelatex'):
   self.skipTest('XeLaTeX required')
  for native, target, phrase in [('zh', '日本語', '図と안녕하세요'), ('en', 'Arabic', 'صباح الخير')]:
   with self.subTest(native=native), tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    plan = course(root)
    config = core.read(root/'config.json')
    config.update(language=native, language_course=dict(native=native, target=target,
                  starting_point='beginner', goal='Recognize a greeting'))
    core.save(root/'config.json', config)
    plan['days'][0]['can_do'] = 'Recognize a greeting'
    frame = '请读原文「{}」。[S1]' if native=='zh' else 'The expression is {} [S1].'
    plan['sections'][0]['body'] = frame.format(phrase)
    core.save(root/'plan.json', plan)
    manifest = pdf.render(root, root/'plan.json', 'plan')
    doc = pdfium.PdfDocument(root/manifest['pdf'])
    page = doc[0]
    text = page.get_textpage()
    if native=='zh':
     self.assertIn('図', text.get_text_bounded())
     self.assertIn('안녕하세요',text.get_text_bounded())
    else:
     # An LTR font can yield perfect extracted words while displaying them in
     # the wrong order. Check the physical positions of one letter in each word.
     left = {}
     for index in range(text.count_chars()):
      ch = normalize('NFKC', text.get_text_range(index, 1))
      if ch in ('ص','ر'):
       left[ch] = text.get_charbox(index)[0]
     self.assertGreater(left['ص'], left['ر'])
    doc.close()
