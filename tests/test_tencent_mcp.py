import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts'))
class MCPTests(unittest.TestCase):
 def test_structured_response_and_errors_are_not_content(self):
  from omni_tencent_mcp import unpack
  self.assertEqual(unpack({'result':{'structuredContent':{'user_id':'account'}}}),{'user_id':'account'})
  self.assertEqual(unpack({'result':{'content':[{'type':'text','text':'{"user_id":"account"}'}]}}),{'user_id':'account'})
  with self.assertRaises(RuntimeError):unpack({'result':{'isError':True,'content':[{'type':'text','text':'SECRET'}]}})
 def test_account_change_is_rejected(self):
  from omni_tencent_mcp import Client
  client=Client({'account_id':'selected','auth_profile':'qa'},transport=lambda method,params:{'result':{'structuredContent':{'user_id':'other'}}})
  with self.assertRaises(ValueError):client.check_identity()
 def test_signed_upload_rejects_credentials_and_unofficial_hosts(self):
  from omni_tencent_mcp import upload_url
  for url in ['https://evil.test/upload','http://cos.ap-guangzhou.myqcloud.com/u','https://user@cos.ap-guangzhou.myqcloud.com/u']:
   with self.assertRaises(ValueError):upload_url(url)
 def test_exported_word_hyperlink_fields_are_semantic_links(self):
  import tempfile,io
  from zipfile import ZipFile,ZIP_DEFLATED
  from xml.etree import ElementTree as E
  from test_documents import course
  import omni_document as d
  from omni_tencent import check_docx
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);data=course(root);m=d.render(root,root/'plan.json','plan',['docx']);source=root/m['artifacts']['docx'];out=io.BytesIO()
   w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
   with ZipFile(source) as z,ZipFile(out,'w',ZIP_DEFLATED) as dest:
    for n in z.namelist():
     content=z.read(n)
     if n=='word/document.xml':
      tree=E.fromstring(content)
      for p in tree.iter(w+'p'):
       for link in list(p):
        if link.tag!=w+'hyperlink':continue
        p.remove(link)
       for i,url in enumerate(s['url'] for s in data['sources']):
        for tag,attrs,text in [('fldChar',{'fldCharType':'begin'},None),('instrText',{},'HYPERLINK "'+url+'"'),('fldChar',{'fldCharType':'separate'},None),('t',{},'Link'),('fldChar',{'fldCharType':'end'},None)]:
         run=E.SubElement(p,w+'r');node=E.SubElement(run,w+tag,{w+k:v for k,v in attrs.items()});node.text=text
      content=E.tostring(tree)
     if n=='word/_rels/document.xml.rels':
      tree=E.fromstring(content)
      for rel in list(tree):
       if rel.get('Type','').endswith('/hyperlink'):tree.remove(rel)
      content=E.tostring(tree)
     dest.writestr(n,content)
   check_docx(out.getvalue(),data)
   with self.assertRaises(ValueError):check_docx(out.getvalue(),dict(data,sources=[dict(s,url='https://missing.example') for s in data['sources']]))
 def test_existing_import_resumes_and_verifies_export_without_duplicate_create(self):
  import tempfile
  from test_documents import course
  import omni_document as d
  from omni_tencent_mcp import publish
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);data=course(root);m=d.render(root,root/'plan.json','plan',['docx']);blob=(root/m['artifacts']['docx']).read_bytes();calls=[]
   class Fake:
    def check_identity(self):return {'id':'selected'}
    def download(self,url):return blob
    def call(self,name,args):
     calls.append(name)
     if name=='manage.import_progress':return {'progress':100,'file_id':'existing','file_url':'https://docs.qq.com/doc/existing'}
     if name=='manage.query_file_info':return {'file_id':'existing','title':data['title'],'type':'doc'}
     if name=='manage.move_file':return {}
     if name=='manage.folder_list':return {'list':[{'id':'existing'}],'finish':True}
     if name=='manage.export_file':return {'task_id':'export1'}
     if name=='manage.export_progress':return {'progress':100,'file_url':'https://docs.qq.com/export.docx'}
     raise AssertionError(name)
   r={'task_id':'import1','status':'pending'}
   target={'account_id':'selected','auth_profile':'qa','destination':{'folder_id':'/'}}
   result=publish(root,m,target,r,lambda **x:r.update(x),client=Fake())
   if result['status']=='pending':result=publish(root,m,target,r,lambda **x:r.update(x),client=Fake())
   self.assertEqual(result['status'],'verified');self.assertNotIn('manage.async_import',calls);self.assertEqual(calls.count('manage.export_file'),1)
 def test_connect_binds_oauth_identity_to_confirmed_home(self):
  import omni_connections as conn
  class Fake:
   def check_identity(self):return {'id':'selected','name':'QA'}
   def check_destination(self,dest):assert dest=={'folder_id':'/'}
  result=conn.connect('tencent','https://docs.qq.com/desktop/',auth_profile='qa',client=Fake())
  self.assertTrue(result['ready']);self.assertEqual(result['delivery']['account_id'],'selected');self.assertEqual(result['delivery']['mode'],'mcp')
 def test_export_expiry_has_a_safe_classification(self):
  from omni_tencent_mcp import unpack,MCPError
  with self.assertRaises(MCPError) as raised:unpack({'error':{'code':-32603,'message':'tool execution failed code:323908, msg:NotFound: secret signed URL'}})
  self.assertEqual(raised.exception.kind,'not_found');self.assertNotIn('secret',str(raised.exception))
 def test_import_upload_key_is_opaque_not_an_object_id(self):
  import tempfile
  from test_documents import course
  import omni_document as d
  from omni_tencent_mcp import publish
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);data=course(root);m=d.render(root,root/'plan.json','plan',['docx']);r={};uploads=[]
   class Fake:
    def check_identity(self):return {'id':'selected'}
    def call(self,name,args):
     if name=='manage.pre_import':return {'task_id':'upload-task','file_key':'import/user/file.docx','upload_url':'https://bucket.cos.ap-guangzhou.myqcloud.com/signed'}
     if name=='manage.async_import':
      assert args['file_key']=='import/user/file.docx';return {'task_id':'import-task'}
     if name=='manage.import_progress':return {'progress':10}
     raise AssertionError(name)
   result=publish(root,m,{'destination':{'folder_id':'/'},'account_id':'selected'},r,lambda **x:r.update(x),client=Fake(),uploader=lambda path,url:uploads.append(url))
   self.assertEqual(result['status'],'pending');self.assertEqual(r['task_id'],'import-task');self.assertEqual(len(uploads),1)
