"""Portable XeLaTeX rendering and artifact verification; no generated TeX execution."""
import os
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlsplit
from pypdf import PdfReader
import omni_core as c


def esc(text):
    table={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','%':r'\%','$':r'\$','&':r'\&','#':r'\#','_':r'\_','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    return ''.join(table.get(ch,ch) for ch in str(text))


def executable(name):
    if shutil.which(name): return shutil.which(name)
    roots=[Path.home()/'Library/TinyTeX/bin',Path.home()/'.TinyTeX/bin',Path('/Library/TeX/texbin')]
    for root in roots:
        for path in [root/name,*root.glob('*/'+name)]:
            if path.is_file(): return str(path)
    return None


def validate_document(data,root):
    sources=data.get('sources',[])
    if len({s.get('url') for s in sources})<5: raise ValueError('At least five distinct expansion links required.')
    ids=[s.get('id') for s in sources]
    if len(set(ids))!=len(ids) or any(not re.fullmatch(r'S\d+',str(x)) for x in ids): raise ValueError('Source IDs must be unique S-numbers.')
    for s in sources:
        u=urlsplit(s.get('url',''))
        if u.scheme not in ('http','https') or not u.netloc or any(ch in s['url'] for ch in '\\{}\n\r'): raise ValueError('Invalid source URL.')
        if not all(s.get(k) for k in ('title','publisher','note','checked_at','published_at')): raise ValueError('Incomplete source metadata.')
        if s['checked_at']!=c.today(root): raise ValueError('Recheck sources on the actual generation date.')
    if not data.get('sections') or not all(s.get('title') and s.get('body') for s in data['sections']): raise ValueError('Sections need title and body.')
    text='\n'.join(s['body'] for s in data['sections'])
    if not set(re.findall(r'\[(S\d+)\]',text)).issubset(ids): raise ValueError('Unknown inline source.')
    if not re.search(r'\[S\d+\]',text): raise ValueError('Include inline evidence for key claims.')
    f=data.get('figure',{}); p=(root/f.get('path','')).resolve()
    if not p.is_relative_to(root.resolve()) or not p.is_file() or p.suffix.lower() not in ('.png','.jpg','.jpeg','.pdf'): raise ValueError('Figure must be a local supported file inside project.')
    if not f.get('caption') or not f.get('credit'): raise ValueError('Figure caption and credit required.')
    if not data.get('title'): raise ValueError('Document title required.')


PREAMBLE=r'''\documentclass[11pt]{article}
\usepackage[a4paper,margin=22mm,headheight=16pt]{geometry}
\usepackage{fontspec,xeCJK,xcolor,graphicx,enumitem,fancyhdr,titlesec}
\usepackage{hyperref}
\IfFontExistsTF{Times New Roman}{\setmainfont{Times New Roman}}{\setmainfont{TeX Gyre Termes}}
\IfFontExistsTF{FangSong}{\setCJKmainfont[AutoFakeBold=2]{FangSong}}{\IfFontExistsTF{仿宋}{\setCJKmainfont[AutoFakeBold=2]{仿宋}}{\IfFontExistsTF{FandolFang-Regular.otf}{\setCJKmainfont[AutoFakeBold=2]{FandolFang-Regular.otf}}{\setCJKmainfont{FandolSong-Regular.otf}}}}
\definecolor{ink}{HTML}{173747}\definecolor{accent}{HTML}{227E82}
\hypersetup{colorlinks=true,urlcolor=accent,linkcolor=accent}
\linespread{1.22}\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\setlist[itemize]{leftmargin=1.4em,itemsep=3pt}
\titleformat{\section}{\large\bfseries\color{ink}}{}{0pt}{}
\titlespacing*{\section}{0pt}{14pt}{7pt}
\pagestyle{fancy}\fancyhf{}\lhead{\small OMNI LEARNING / 学习手册}\rhead{\small Source-grounded learning}\cfoot{\small\thepage}
\emergencystretch=2em\widowpenalty=10000\clubpenalty=10000
\newcommand{\Needspace}[1]{\par\begingroup\dimen0=#1\relax\vskip0pt plus\dimen0\penalty-100\vskip0pt plus-\dimen0\vskip\dimen0\penalty9999\vskip-\dimen0\vskip0pt\endgroup}
\begin{document}
'''


def render(root,input_path,key):
    root=Path(root).resolve(); input_path=Path(input_path).resolve()
    if not input_path.is_relative_to(root): raise ValueError('Input must be inside project.')
    with c.lock(root):
        state=c.read(root/'state.json'); plan=c.read(root/'plan.json'); c.validate_plan(plan)
        data=c.read(input_path)
        if key=='plan':
            if input_path!=root/'plan.json': raise ValueError('Plan renderer must use canonical plan.json.')
            if state['lessons']: raise ValueError('A started curriculum must be preserved; create a new project for revisions.')
            if (root/'manifests/plan.json').exists(): raise ValueError('Plan already rendered. Reuse it, or archive this project and create a revised project.')
        else:
            c.check_approval(root,state)
            day=data.get('day'); action=c.next_action(root)
            if not isinstance(day,int) or key!=f'Day{day:02d}' or action.get('day')!=day or action['action']!='generate': raise ValueError('Render only the next ungenerated lesson; reuse existing artifacts.')
            if data.get('title')!=plan['days'][day-1]['topic']: raise ValueError('Lesson title differs from approved plan.')
            config=c.read(root/'config.json')
            reading=data.get('reading_minutes'); practice=data.get('practice_minutes')
            if type(reading) is not int or reading<1 or type(practice) is not int or practice<0:
                raise ValueError('Reading minutes must be a positive integer; practice minutes a nonnegative integer.')
            mins=reading+practice
            if not 1<=mins<=config['daily_minutes']: raise ValueError('Lesson exceeds agreed time budget.')
        validate_document(data,root)
        compiler=executable('xelatex')
        if not compiler: raise RuntimeError('XeLaTeX missing. Follow references/setup.md; no substitute PDF engine.')
        for d in ('pdf','sources','assets','manifests','previews'): (root/d).mkdir(exist_ok=True)
        safe_topic=re.sub(r'[<>:"/\\|?*\x00-\x1f]','_',plan['topic']).strip(' .')[:70]
        title=re.sub(r'[<>:"/\\|?*\x00-\x1f]','_',data['title']).strip(' .')[:90]
        stem=safe_topic+'_学习计划' if key=='plan' else f'{safe_topic}_每日学习_{key}_{title}'
        figure=(root/data['figure']['path']).resolve()
        img='figure-'+c.digest(figure)[:12]+figure.suffix.lower(); image_path=root/'assets'/img
        if figure!=image_path: shutil.copyfile(figure,image_path)
        english=c.read(root/'config.json').get('language','zh').lower().startswith('en')
        subtitle=f"{c.today(root)} | "+('学习计划 / '+str(len(plan['days']))+' 天' if key=='plan' else f"{key}/{len(plan['days'])} | 阅读 {data['reading_minutes']} 分钟 + 练习 {data['practice_minutes']} 分钟")
        if english:
            subtitle=f"{c.today(root)} | "+(f"Learning plan / {len(plan['days'])} days" if key=='plan' else f"{key}/{len(plan['days'])} | Read {data['reading_minutes']} min + practice {data['practice_minutes']} min")
        preamble=PREAMBLE.replace('学习手册','Learning guide') if english else PREAMBLE
        tex=[preamble,r'{\LARGE\bfseries\color{ink} '+esc(data['title'])+r'}\par',esc(subtitle)+r'\par\vspace{6pt}']
        md=['# '+data['title'],subtitle]
        for i,s in enumerate(data['sections']):
            tex.extend([r'\Needspace{5\baselineskip}\section*{'+esc(s['title'])+'}',esc(s['body'])]); md.extend(['## '+s['title'],s['body']])
            if i==min(1,len(data['sections'])-1):
                tex.extend([r'\begin{center}\includegraphics[width=\linewidth,height=0.26\textheight,keepaspectratio]{../assets/'+img+r'}\par',r'{\small '+esc(data['figure']['caption'])+r'}\par',r'{\footnotesize '+esc(data['figure']['credit'])+r'}\end{center}'])
                md.extend(['!['+data['figure']['caption']+'](../assets/'+img+')',data['figure']['credit']])
        tex.append(r'\Needspace{6\baselineskip}\section*{Further reading}\small Optional; outside the daily core time budget.\begin{enumerate}[leftmargin=1.6em]' if english else r'\Needspace{6\baselineskip}\section*{扩展学习 / Further reading}\small 以下为选读，不计入每日必做时间。\begin{enumerate}[leftmargin=1.6em]')
        md.append('## Further reading (optional)' if english else '## 扩展学习（选读）')
        for s in data['sources']:
            published=' | Published: ' if english else ' | 发布：'
            checked=' | Checked: ' if english else ' | 核验：'
            tex.append(r'\item ['+esc(s['id'])+r'] \href{'+esc(s['url'])+'}{'+esc(s['title'])+'} — '+esc(s['note'])+r'\par '+esc(s['publisher']+published+s['published_at']+checked+s['checked_at']))
            md.append(f"- [{s['id']}] [{s['title']}]({s['url']}): {s['note']}; {s['publisher']}{published}{s['published_at']}{checked}{s['checked_at']}")
        tex.extend([r'\end{enumerate}',r'\end{document}'])
        texfile=root/'sources'/(stem+'.tex'); texfile.write_text('\n\n'.join(tex),encoding='utf-8')
        mdfile=texfile.with_suffix('.md'); mdfile.write_text('\n\n'.join(md)+'\n',encoding='utf-8')
        env=os.environ.copy(); env['PATH']=str(Path(compiler).parent)+os.pathsep+env.get('PATH','')
        for _ in range(2):
            proc=subprocess.run([compiler,'-no-shell-escape','-halt-on-error','-interaction=nonstopmode',texfile.name],cwd=texfile.parent,env=env,capture_output=True,text=True,timeout=120)
            if proc.returncode: raise RuntimeError('XeLaTeX failed: '+proc.stdout[-2500:])
        log=texfile.with_suffix('.log').read_text(errors='replace')
        if 'Missing character:' in log: raise ValueError('Missing font glyphs. Inspect LaTeX log.')
        pdf=root/'pdf'/(stem+'.pdf'); shutil.copyfile(texfile.with_suffix('.pdf'),pdf); texfile.with_suffix('.pdf').unlink()
        report=inspect_pdf(pdf,data['sources'])
        import pypdfium2 as pdfium
        doc=pdfium.PdfDocument(pdf)
        preview_paths=[]
        for n in range(len(doc)):
            target=root/'previews'/f'{key}-{n+1:02d}.png'; doc[n].render(scale=1.25).to_pil().save(target); preview_paths.append(str(target.relative_to(root)))
        doc.close()
        files=[input_path,root/'plan.json',root/'config.json',pdf,texfile,mdfile,image_path,*[root/p for p in preview_paths]]
        manifest={'key':key,'pdf':str(pdf.relative_to(root)),'created_at':c.today(root),'files':{str(p.relative_to(root)):c.digest(p) for p in files},'previews':preview_paths,'reviewed_at':None,'report':report,'layout_warnings':len(re.findall('Overfull',log))}
        c.save(root/'manifests'/(key+'.json'),manifest)
        return manifest


def inspect_pdf(pdf,sources):
    reader=PdfReader(pdf); urls=set(); fonts=set()
    if not reader.pages: raise ValueError('Empty PDF.')
    for page in reader.pages:
        if not page.extract_text().strip(): raise ValueError('Blank PDF page.')
        for a in page.get('/Annots',[]):
            action=a.get_object().get('/A',{})
            if action.get('/URI'): urls.add(str(action['/URI']))
        for f in page.get('/Resources',{}).get('/Font',{}).values():
            font=f.get_object(); fonts.add(str(font.get('/BaseFont','')))
            descriptors=[font.get('/FontDescriptor')]
            descriptors += [d.get_object().get('/FontDescriptor') for d in font.get('/DescendantFonts',[])]
            for descriptor in descriptors:
                if descriptor is not None and not any(k in descriptor.get_object() for k in ('/FontFile','/FontFile2','/FontFile3')): raise ValueError('Font not embedded.')
    if not {s['url'] for s in sources}.issubset(urls): raise ValueError('Missing PDF links.')
    return {'pages':len(reader.pages),'links':len(urls),'fonts':sorted(fonts)}


def review(root,key,note):
    if not re.fullmatch(r'plan|Day[0-9]{2,}',key): raise ValueError('Invalid document key.')
    with c.lock(root):
        state=c.read(root/'state.json')
        if key!='plan' and str(int(key[3:])) in state['lessons']:
            raise ValueError('Delivered review is immutable; retain the original archive.')
        path=root/'manifests'/(key+'.json'); m=c.read(path); c.manifest_ok(root,m)
        if not note.strip(): raise ValueError('Record what was visually checked.')
        m.update(reviewed_at=c.today(root),review_note=note); c.save(path,m)
