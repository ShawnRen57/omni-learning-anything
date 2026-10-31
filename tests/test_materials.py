"""Own-material formats, immutable ranges and citation scope."""
import importlib.util,json,subprocess,sys,tempfile,unittest,shutil,copy
from pathlib import Path
from zipfile import ZipFile
from test_documents import course
import omni_core as c
import omni_document as d

class MaterialTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
 def tearDown(self):self.tmp.cleanup()
 def module(self):
  self.assertIsNotNone(importlib.util.find_spec('omni_materials'),'Material pipeline missing')
  import omni_materials
  return omni_materials
 def imported(self,text='# First\n\nEvidence anchors explanations.\n\n# Second\n\nExcluded secret content.'):
  p=self.root/'book.md';p.write_text(text);m=self.module();r=m.import_file(self.root,p);return m,r
 def test_markdown_scope_search_and_citation(self):
  m,r=self.imported();outline=m.inspect(self.root,r['id'],r['version'])
  selected=m.select(self.root,r['id'],r['version'],heading='First')
  hits=m.search(self.root,'Evidence',selection=selected)
  self.assertTrue(hits);self.assertNotIn('Excluded',json.dumps(hits))
  source=m.citation(self.root,selected,hits[0]['unit'],'Evidence anchors explanations.','S1')
  self.assertNotIn('url',source);self.assertIn('First',source['note'])
  with self.assertRaises(ValueError):m.citation(self.root,selected,hits[0]['unit'],'invented quote','S1')
 def test_versions_do_not_retarget_previous_selection(self):
  m,r=self.imported();selection=m.select(self.root,r['id'],r['version'],heading='First')
  (self.root/'book.md').write_text('# First\n\nChanged chapter contents.')
  new=m.import_file(self.root,self.root/'book.md',material_id=r['id'])
  self.assertNotEqual(new['version'],r['version'])
  self.assertIn('Evidence',m.search(self.root,'Evidence',selection=selection)[0]['text'])
 def test_html_ignores_scripts_and_preserves_heading(self):
  p=self.root/'page.html';p.write_text('<h1>Lesson</h1><p>Actual material.</p><script>BAD SCRIPT</script><style>BAD CSS</style>')
  m=self.module();r=m.import_file(self.root,p,url='https://example.org/lesson')
  s=m.select(self.root,r['id'],r['version']);hits=m.search(self.root,'Actual',selection=s)
  self.assertNotIn('BAD',json.dumps(hits));self.assertIn('Lesson',hits[0]['locator'])
 def test_docx_and_pptx_passive_xml(self):
  m=self.module()
  for extension,path,xml in [('docx','word/document.xml','<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>Chapter</w:t></w:r></w:p><w:p><w:r><w:t>Word evidence.</w:t></w:r></w:p></w:body></w:document>'),('pptx','ppt/slides/slide1.xml','<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:t>Slide evidence.</a:t></p:sld>')]:
   p=self.root/('input.'+extension)
   with ZipFile(p,'w') as z:z.writestr(path,xml)
   r=m.import_file(self.root,p);self.assertIn(r['status'],('ready','partial'))
   s=m.select(self.root,r['id'],r['version']);self.assertTrue(m.search(self.root,'evidence',selection=s))
 def test_epub_spine_excludes_unlisted_assets(self):
  p=self.root/'book.epub'
  with ZipFile(p,'w') as z:
   z.writestr('META-INF/container.xml','<container><rootfiles><rootfile full-path="OPS/book.opf"/></rootfiles></container>')
   z.writestr('OPS/book.opf','<package><manifest><item id="one" href="one.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="one"/></spine></package>')
   z.writestr('OPS/one.xhtml','<h1>Unit One</h1><p>Published chapter.</p>')
   z.writestr('OPS/unused.xhtml','UNLISTED SECRET')
  m=self.module();r=m.import_file(self.root,p);s=m.select(self.root,r['id'],r['version'])
  self.assertNotIn('UNLISTED',json.dumps(m.search(self.root,'chapter',selection=s)))
 def test_unsafe_archive_and_entities_fail_visibly(self):
  m=self.module()
  for member,payload in [('../escape','evil'),('word/document.xml','<!DOCTYPE x [<!ENTITY e "boom">]><x>&e;</x>')]:
   p=self.root/'bad.docx'
   with ZipFile(p,'w') as z:z.writestr(member,payload)
   r=m.import_file(self.root,p);self.assertEqual(r['status'],'failed')
   with self.assertRaises(ValueError):m.select(self.root,r['id'],r['version'])
 def test_subtitles_and_text_encodings(self):
  m=self.module()
  for name,text in [('course.srt','1\n00:00:01,000 --> 00:00:03,000\n课程证据。\n'),('course.vtt','WEBVTT\n\n00:00:01.000 --> 00:00:03.000\n课程证据。\n'),('book.txt','课程证据。')]:
   p=self.root/name;p.write_bytes(text.encode('gb18030' if name.endswith('.txt') else 'utf-8'))
   r=m.import_file(self.root,p);s=m.select(self.root,r['id'],r['version'])
   self.assertIn('课程证据',json.dumps(m.search(self.root,'证据',selection=s),ensure_ascii=False))
 def test_pdf_missing_scanned_page_is_not_silently_selected(self):
  from pypdf import PdfWriter
  from pypdf.generic import NameObject,DictionaryObject,DecodedStreamObject
  p=self.root/'paper.pdf';w=PdfWriter();page=w.add_blank_page(width=300,height=300)
  font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
  page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):font})})
  stream=DecodedStreamObject();stream.set_data(b'BT /F1 12 Tf 20 200 Td (Evidence from page one.) Tj ET');page[NameObject('/Contents')]=stream
  w.add_blank_page(width=300,height=300)
  with p.open('wb') as f:w.write(f)
  m=self.module();r=m.import_file(self.root,p);self.assertEqual(r['status'],'partial')
  s=m.select(self.root,r['id'],r['version'],pages='1');self.assertTrue(m.search(self.root,'Evidence',selection=s))
  with self.assertRaises(ValueError):m.select(self.root,r['id'],r['version'],pages='1-2')
 @unittest.skipUnless(shutil.which('textutil'),'Native Word converter unavailable')
 def test_real_legacy_doc_conversion(self):
  text=self.root/'input.txt';text.write_text('Legacy document evidence.')
  doc=self.root/'input.doc';subprocess.run(['textutil','-convert','doc','-output',str(doc),str(text)],check=True,capture_output=True)
  m=self.module();r=m.import_file(self.root,doc);self.assertEqual(r['status'],'ready')
  self.assertTrue(m.search(self.root,'Legacy',selection=m.select(self.root,r['id'],r['version'])))
 def test_material_mode_renders_plain_sources_and_enforces_strict_policy(self):
  m,r=self.imported();selection=m.select(self.root,r['id'],r['version'],heading='First')
  source=m.citation(self.root,selection,selection['units'][0],'Evidence anchors explanations.','S1')
  plan=course(self.root,{'platform':'html','mode':'local'})
  config=c.read(self.root/'config.json');config['materials']={'policy':'strict','selections':[selection]};c.save(self.root/'config.json',config)
  source['checked_at']=c.today(self.root);plan['sources']=[source];plan['sections']=[{'title':'Evidence','body':'Evidence anchors explanations. [S1]'}];c.save(self.root/'plan.json',plan)
  manifest=d.render(self.root,self.root/'plan.json','plan',['html','docx','markdown'])
  self.assertIn('First',(self.root/manifest['artifacts']['html']).read_text())
  self.assertNotIn('file://',(self.root/manifest['artifacts']['markdown']).read_text())
  bad=copy.deepcopy(plan);bad['sources'].append({'id':'S2','url':'https://example.com','title':'External','publisher':'QA','published_at':'unknown','checked_at':c.today(self.root),'note':'Outside scope'})
  with self.assertRaises(ValueError):d.validate_document(bad,self.root)
 def test_tampered_selection_or_snapshot_rejected(self):
  m,r=self.imported();s=m.select(self.root,r['id'],r['version'],heading='First')
  bad=copy.deepcopy(s);bad['units'].append('unknown')
  with self.assertRaises(ValueError):m.search(self.root,'x',selection=bad)
 def test_unsupported_is_actionable_and_symlink_storage_blocked(self):
  m=self.module();p=self.root/'video.mp4';p.write_bytes(b'video')
  r=m.import_file(self.root,p);self.assertEqual(r['status'],'unsupported');self.assertTrue(r['warnings'])
  with tempfile.TemporaryDirectory() as other:
   shutil.rmtree(self.root/'materials');(self.root/'materials').symlink_to(other,target_is_directory=True)
   with self.assertRaises(ValueError):m.import_file(self.root,p)

class MaterialIntegrationTests(unittest.TestCase):
 setUp=MaterialTests.setUp
 tearDown=MaterialTests.tearDown
 module=MaterialTests.module
 imported=MaterialTests.imported
 def test_approved_scope_blocks_external_retrieval(self):
  m,r=self.imported();first=m.select(self.root,r['id'],r['version'],heading='First');second=m.select(self.root,r['id'],r['version'],heading='Second')
  c.save(self.root/'config.json',{'materials':{'policy':'strict','selections':[first]}})
  with self.assertRaises(ValueError):m.search(self.root,'secret',selection=second)
  self.assertEqual(m.search(self.root,'Excluded'),[])
 def test_cloud_readback_requires_original_locator(self):
  from omni_http import check_text
  m,r=self.imported();s=m.select(self.root,r['id'],r['version'],heading='First');source=m.citation(self.root,s,s['units'][0],'Evidence anchors explanations.','S1')
  data={'title':'Lesson','sections':[{'title':'Goal','body':'Body'}],'figure':{'caption':'Figure','credit':'QA'},'sources':[source]}
  with self.assertRaises(ValueError):check_text('Lesson Goal Body Figure QA',data)
 def test_material_pdf_and_quiz_workflow(self):
  m,r=self.imported();selection=m.select(self.root,r['id'],r['version'],heading='First')
  plan=course(self.root,{'platform':'markdown','mode':'local'});cfg=c.read(self.root/'config.json');cfg['materials']={'policy':'strict','selections':[selection]};c.save(self.root/'config.json',cfg)
  source=m.citation(self.root,selection,selection['units'][0],'Evidence anchors explanations.','S1')
  plan['sources']=[source];plan['sections']=[{'title':'Goal','body':'Evidence anchors explanations. [S1]'}];c.save(self.root/'plan.json',plan)
  manifest=d.render(self.root,self.root/'plan.json','plan',['pdf','markdown']);self.assertEqual(manifest['report']['links'],0)
  d.review(self.root,'plan','Inspected QA fixture');c.approve(self.root)
  lesson=dict(plan,day=1,title='第一课',reading_minutes=8,practice_minutes=3);c.save(self.root/'data/Day01.json',lesson)
  d.render(self.root,self.root/'data/Day01.json','Day01',['markdown']);d.review(self.root,'Day01','Inspected QA fixture')
  from omni_delivery import publish
  publish(self.root,'Day01');c.deliver(self.root,1)
  import omni_quiz as q
  from test_quiz import definition
  value=definition()
  for question in value['questions']:question['source_refs']=[{'source_id':'S1','section_index':0,'quote':'Evidence anchors explanations.'}]
  q.prepare(self.root,value);attempt=q.start(self.root,'Day01','start','开始短测')['attempt_id']
  self.assertEqual(q.next_question(self.root,attempt)['status'],'question')
 def test_cli_import_select_and_retrieve(self):
  import subprocess
  p=self.root/'input.txt';p.write_text('Evidence in a plain textbook.')
  cli=Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts/omni_learning.py'
  def run(*args):
   result=subprocess.run([sys.executable,str(cli),'--project',str(self.root),'materials',*args],capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stderr);return json.loads(result.stdout)
  r=run('import','--file',str(p));s=run('select','--id',r['id'],'--version',r['version'])
  selection=self.root/'selection.json';selection.write_text(json.dumps(s))
  self.assertTrue(run('search','--selection',str(selection),'--query','Evidence')['evidence'])

class MaterialRegressionTests(unittest.TestCase):
 setUp=MaterialTests.setUp
 tearDown=MaterialTests.tearDown
 module=MaterialTests.module
 imported=MaterialTests.imported
 def test_legacy_cannot_smuggle_unverified_local_source(self):
  plan=course(self.root,{'platform':'markdown','mode':'local'});plan['sources'][-1].pop('url');plan['sources'][-1]['material_ref']={'bogus':'unverified'}
  with self.assertRaises(ValueError):d.validate_document(plan,self.root)
 def test_repeated_headings_need_explicit_unit_selection(self):
  m,r=self.imported('# Appendix\n\nFirst content.\n\n# Main\n\nOther text.\n\n# Appendix\n\nSecond content.')
  with self.assertRaises(ValueError):m.select(self.root,r['id'],r['version'],heading='Appendix')
 def test_extraction_uses_exact_hashed_copy(self):
  from unittest.mock import patch
  import omni_material_readers as readers
  m=self.module();p=self.root/'input.txt';p.write_text('Original evidence.')
  import hashlib
  expected=hashlib.sha256(p.read_bytes()).hexdigest();actual=readers.read
  def concurrent_edit(snapshot):
   p.write_text('Changed source before extraction.');return actual(snapshot)
  with patch.object(readers,'read',side_effect=concurrent_edit):r=m.import_file(self.root,p)
  self.assertEqual(r['version'],expected)
  s=m.select(self.root,r['id'],r['version']);self.assertIn('Original',m.search(self.root,'evidence',selection=s)[0]['text'])
 def test_failed_retry_keeps_failure_history(self):
  from unittest.mock import patch
  import omni_material_readers as readers
  p=self.root/'input.txt';p.write_text('Recovered evidence.');m=self.module()
  with patch.object(readers,'read',side_effect=readers.ReaderError('Convert this file first.')):failed=m.import_file(self.root,p)
  self.assertEqual(failed['status'],'failed')
  self.assertEqual(m.import_file(self.root,p,material_id=failed['id'],retry=True)['status'],'ready')
  self.assertTrue(list((self.root/'materials/failed_attempts').glob('*/*.json')))
 def test_chapter_selection_includes_nested_subsections(self):
  m,r=self.imported('# Chapter One\n\nFoundation.\n\n## Details\n\nNested evidence.\n\n# Chapter Two\n\nExcluded evidence.')
  s=m.select(self.root,r['id'],r['version'],heading='Chapter One')
  hits=m.search(self.root,'evidence',selection=s)
  self.assertEqual(len(hits),1);self.assertIn('Nested',hits[0]['text'])
 def test_private_source_quote_is_literal_and_not_optional_enrichment(self):
  plan=course(self.root,{'platform':'markdown','mode':'local'})
  plan['sources']=[{'id':'S1','title':'Book','note':'<img src="https://tracking.invalid/x">','publisher':'User','published_at':'unknown','checked_at':c.today(self.root),'material_ref':{'unit':'u1'}}]
  config=c.read(self.root/'config.json');config['materials']={'policy':'strict','selections':[]}
  output=d.markdown_text(plan,plan,config,c.today(self.root),'plan','figure.png')
  self.assertNotIn('<img src=',output)
  self.assertNotIn('扩展学习（选读）',output)
