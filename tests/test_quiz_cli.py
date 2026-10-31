import json,subprocess,sys,tempfile,unittest
from pathlib import Path
from test_quiz import lesson_course,definition
CLI=Path(__file__).resolve().parents[1]/'skills/omni-learning-anything/scripts/omni_learning.py'
class QuizCLITests(unittest.TestCase):
 def test_actual_cli_prepare_start_answer_resume_export(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);lesson_course(root);(root/'quiz.json').write_text(json.dumps(definition(),ensure_ascii=False))
   def run(*args):
    p=subprocess.run([sys.executable,str(CLI),'--project',str(root),'quiz',*args],text=True,capture_output=True)
    self.assertEqual(p.returncode,0,p.stderr);return json.loads(p.stdout)
   run('prepare','--input',str(root/'quiz.json'))
   attempt=run('start','--key','Day01','--request-id','user1','--consent','开始短测')['attempt_id']
   view=run('next','--attempt',attempt);self.assertNotIn('answer_id',view['question'])
   (root/'answer.json').write_text('{"text":"Ａ"}')
   answer=run('answer','--attempt',attempt,'--question','choice1','--event-id','reply1','--input',str(root/'answer.json'))
   self.assertEqual(answer['feedback']['verdict'],'correct')
   run('skip','--attempt',attempt,'--question','short1','--event-id','skip2')
   self.assertEqual(run('next','--attempt',attempt)['status'],'complete')
   run('export','--output',str(root/'result.json'),'--format','json')
   self.assertTrue((root/'result.json').exists())
