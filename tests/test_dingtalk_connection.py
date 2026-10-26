import sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts'))
import omni_connections as conn
class DingTalkConnectionTests(unittest.TestCase):
 def test_official_folder_and_org_identity_are_pinned(self):
  class Client:
   def check_identity(self):return {'id':'corp:user','name':'QA'}
   def check_destination(self,d):self.destination=d
  client=Client()
  with patch.object(conn.shutil,'which',return_value='/official/dws'):
   r=conn.connect('dingtalk','https://alidocs.dingtalk.com/i/nodes/Folder123',client=client)
  self.assertTrue(r['ready']);self.assertEqual(r['delivery']['account_id'],'corp:user');self.assertEqual(r['delivery']['cli_profile'],'corp:user');self.assertEqual(client.destination,{'folder_id':'Folder123'})
 def test_publication_rejects_changed_account_before_write(self):
  from omni_dingtalk import check_identity
  calls=[]
  def run(args):calls.append(args);return {'success':True,'authenticated':True,'corp_id':'other','user_id':'user'}
  with self.assertRaises(ValueError):check_identity({'account_id':'corp:user','cli_profile':'corp:user'},run)
  self.assertEqual(calls[0][-2:],['--profile','corp:user'])
 def test_unofficial_link_rejected(self):
  with self.assertRaises(ValueError):conn.location('dingtalk','https://alidocs.dingtalk.com.evil.test/i/nodes/Folder')
 def test_escaped_readback_resumes_same_document(self):
  import tempfile
  from test_documents import course
  import omni_document as d
  from omni_dingtalk import publish
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);plan=course(root);m=d.render(root,root/'plan.json','plan',['docx'])
   text=(root/m['artifacts']['markdown']).read_text().replace('[S1]',r'\[S1\]').replace('../assets/', 'https://official.example/').replace('.png)', '.png "")')
   receipt={'remote_id':'existing','url':'https://alidocs.dingtalk.com/i/nodes/existing'}
   def runner(args):
    self.assertNotIn('import',args)
    return {'contentType':'ALIDOC'} if 'info' in args else {'markdown':text}
   self.assertEqual(publish(root,m,{'destination':{'folder_id':'qa'}},receipt,lambda **x:receipt.update(x),runner)['status'],'verified')

 def test_readback_accepts_http_and_markdown_destination_syntax_without_import(self):
  import tempfile
  from test_documents import course
  import omni_document as d
  from omni_dingtalk import publish
  cases=[('http://example.com/reference',None),('https://example.com/Architecture_(history)',None),('https://example.com/a_(b_(c))',None),('https://example.com/Architecture_(history)',r'https://example.com/Architecture_\(history\) "Title"'),('https://example.com/Architecture_(history)',"<https://example.com/Architecture_(history)> 'Title'")]
  for url,destination in cases:
   with self.subTest(url=url,destination=destination),tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);plan=course(root);plan['sources'][0]['url']=url
    import omni_core as core
    core.save(root/'plan.json',plan);m=d.render(root,root/'plan.json','plan',['docx'])
    text=(root/m['artifacts']['markdown']).read_text().replace('../assets/','https://official.example/')
    if destination:text=text.replace(']('+url+')',']('+destination+')')
    receipt={'remote_id':'existing','url':'https://alidocs.dingtalk.com/i/nodes/existing'}
    def runner(args):
     self.assertNotIn('import',args)
     return {'contentType':'ALIDOC'} if 'info' in args else {'markdown':text}
    self.assertEqual(publish(root,m,{'destination':{'folder_id':'qa'}},receipt,lambda **x:receipt.update(x),runner)['status'],'verified')

 def test_readback_rejects_plain_urls_wrong_targets_and_images_as_sources(self):
  import tempfile
  from test_documents import course
  import omni_document as d
  from omni_dingtalk import publish
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);plan=course(root);m=d.render(root,root/'plan.json','plan',['docx'])
   original=(root/m['artifacts']['markdown']).read_text().replace('../assets/','https://official.example/')
   link='[参考 1](https://example.com/1)'
   for replacement in ('参考 1 https://example.com/1','[参考 1](https://example.com/wrong) https://example.com/1','!'+link):
    with self.subTest(replacement=replacement):
     text=original.replace(link,replacement);receipt={'remote_id':'existing','url':'https://alidocs.dingtalk.com/i/nodes/existing'}
     def runner(args):
      self.assertNotIn('import',args)
      return {'contentType':'ALIDOC'} if 'info' in args else {'markdown':text}
     with self.assertRaisesRegex(ValueError,'semantic source links'):publish(root,m,{'destination':{'folder_id':'qa'}},receipt,lambda **x:receipt.update(x),runner)
