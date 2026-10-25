import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts'))
class AuthTests(unittest.TestCase):
 def test_device_flow_pending_slowdown_success_and_no_secret_summary(self):
  import omni_tencent_auth as a
  saved={};calls=[];clock=[100]
  class Store:
   def get(self,name):return saved.get(name)
   def put(self,name,v):saved[name]=v
  def request(url,data=None):
   calls.append((url,data))
   if url.endswith('oauth-authorization-server'):return dict(issuer=a.ORIGIN,registration_endpoint=a.ORIGIN+'/openapi/mcp/oauth/register',device_authorization_endpoint=a.ORIGIN+'/openapi/mcp/oauth/device/code',token_endpoint=a.ORIGIN+'/openapi/mcp/oauth/token')
   if url.endswith('register'):return {'client_id':'public-client'}
   if url.endswith('code'):return dict(device_code='private-device',user_code='ABCD',verification_uri='https://docs.qq.com/activate',expires_in=600,interval=5)
   return next(results)
  results=iter([{'error':'authorization_pending'},{'error':'slow_down'},{'access_token':'private-access','refresh_token':'private-refresh','expires_in':3600}])
  client=a.Auth(Store(),request,lambda:clock[0]);summary=client.start('qa');self.assertNotIn('private',str(summary))
  clock[0]+=5;self.assertEqual(client.poll('qa')['stage'],'pending')
  clock[0]+=5;self.assertEqual(client.poll('qa')['stage'],'pending');self.assertEqual(saved['qa']['interval'],10)
  clock[0]+=10;self.assertTrue(client.poll('qa')['ready']);self.assertEqual(client.token('qa'),'private-access')
  self.assertNotIn('private',str(client.status('qa')))
 def test_metadata_and_verification_hosts_are_official_only(self):
  import omni_tencent_auth as a
  for url in ['http://docs.qq.com/x','https://docs.qq.com.evil.test/x','https://user@docs.qq.com/x','https://docs.qq.com:8443/x']:
   with self.assertRaises(ValueError):a.official_url(url)
 def test_expired_device_never_polls_or_reissues(self):
  import omni_tencent_auth as a
  class Store:
   def get(self,name):return {'expires_at':1,'device_code':'private','interval':5}
  client=a.Auth(Store(),lambda *args:self.fail('Unexpected network request'),lambda:100)
  self.assertEqual(client.poll('qa')['stage'],'expired')
 def test_pkce_callback_is_bound_to_state_and_verifier(self):
  import omni_tencent_auth as a
  saved={};calls=[]
  class Store:
   def get(self,n):return saved.get(n)
   def put(self,n,v):saved[n]=v
  def req(url,data=None):
   calls.append((url,data))
   if url.endswith('oauth-authorization-server'):return {'issuer':a.ORIGIN,'registration_endpoint':a.ORIGIN+'/register','authorization_endpoint':a.ORIGIN+'/authorize?authType=2','token_endpoint':a.ORIGIN+'/token'}
   if url.endswith('register'):return {'client_id':'public'}
   return {'access_token':'private','expires_in':3600}
  client=a.Auth(Store(),req,lambda:100)
  result=client.start_code('qa',8765);self.assertIn('code_challenge=',result['authorization_url']);self.assertNotIn('code_verifier',str(result))
  with self.assertRaises(ValueError):client.finish_code('qa','code','wrong')
  self.assertEqual(len(calls),2)
  self.assertTrue(client.finish_code('qa','code',saved['qa']['state'])['ready']);self.assertIn('code_verifier',calls[-1][1])
