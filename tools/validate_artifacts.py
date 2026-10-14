"""Read-only validation of shipped samples; never marks visual review."""
import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/omni-learning-anything/scripts'))
import omni_core as c,omni_pdf as p
import pypdfium2 as pdfium
count=pages=0
for root in (ROOT/'examples').iterdir():
 if not (root/'plan.json').exists():continue
 config=c.read(root/'config.json');plan=c.read(root/'plan.json');state=c.read(root/'state.json')
 assert config['sample_mode'] and state['schedule'] is None
 assert len(plan['days'])==30 and set(state['lessons'])=={'1','2','3'}
 c.check_approval(root,state)
 for key in ('plan','Day01','Day02','Day03'):
  m=c.reviewed(root,key);data=c.read(root/'plan.json' if key=='plan' else root/'data'/(key+'.json'))
  r=p.inspect_pdf(root/m['pdf'],data['sources']);assert r==m['report'] and m['layout_warnings']==0
  doc=pdfium.PdfDocument(root/m['pdf']);text=''.join(doc[i].get_textpage().get_text_range() for i in range(len(doc)))
  assert data['title'] in text.replace(' ','') or data['title'].replace(' ','') in text.replace(' ','')
  assert '扩展学习' in text
  pages+=len(doc);doc.close();count+=1
 assert c.next_action(root)['day']==4
assert count==24
print(json.dumps({'pdfs':count,'pages':pages,'result':'all archived manifest/font/link/text checks passed'},ensure_ascii=False))
