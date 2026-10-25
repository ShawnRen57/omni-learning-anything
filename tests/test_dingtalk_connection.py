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
