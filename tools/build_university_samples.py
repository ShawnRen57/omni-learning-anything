"""Build real sample PDFs/HTML in stages; review pages between plans and lessons."""
import argparse
import copy
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/omni-learning-anything/scripts'))
from content.v300_samples import SAMPLES
import omni_core as c
import omni_courses as courses
import omni_document as documents

INK='#193848';TEAL='#237768';RUST='#b27543';BLUE='#3b668e';BG='#f5f6f0'
FONTS=[Path('/System/Library/Fonts/Supplemental/Arial Unicode.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]


def font(size):
    path=next((p for p in FONTS if p.exists()),None)
    if not path:raise RuntimeError('Install a Unicode font for sample figures; do not ship missing glyphs.')
    return ImageFont.truetype(str(path),size)


def arrow(draw,a,b,color=TEAL,width=7):
    draw.line([a,b],fill=color,width=width)
    angle=math.atan2(b[1]-a[1],b[0]-a[0]);length=20
    draw.polygon([b,(b[0]-length*math.cos(angle-.45),b[1]-length*math.sin(angle-.45)),
                  (b[0]-length*math.cos(angle+.45),b[1]-length*math.sin(angle+.45))],fill=color)


def label(draw,xy,text,size=34,color=INK,anchor='mm'):
    draw.text(xy,text,font=font(size),fill=color,anchor=anchor)


def box(draw,coords,text,color=TEAL):
    draw.rounded_rectangle(coords,radius=22,fill='white',outline=color,width=4)
    label(draw,((coords[0]+coords[2])/2,(coords[1]+coords[3])/2),text,30,color)


def figure(sample,path):
    slug=sample['slug'];image=Image.new('RGB',(1600,850),BG);draw=ImageDraw.Draw(image)
    if slug=='positive-psychology-zh':
        layer=Image.new('RGBA',image.size);d=ImageDraw.Draw(layer)
        for rect,color in [((310,100,880,670),(35,119,104,65)),((730,100,1300,670),(59,102,142,65)),((520,320,1090,850),(178,117,67,65))]:d.ellipse(rect,fill=color,outline=(*color[:3],220),width=4)
        image=Image.alpha_composite(image.convert('RGBA'),layer).convert('RGB');draw=ImageDraw.Draw(image)
        for xy,text in [((565,310),'体验'),((1050,310),'行动'),((800,660),'环境')]:label(draw,xy,text,58)
    elif slug=='cs50x-en':
        box(draw,(500,80,1050,190),'Any parcels left?')
        box(draw,(80,80,340,190),'Stop',RUST);arrow(draw,(500,135),(340,135),RUST);label(draw,(415,100),'no',28,RUST)
        arrow(draw,(775,190),(775,290));label(draw,(820,240),'yes',28)
        box(draw,(550,290,1000,400),'Read label')
        arrow(draw,(775,400),(775,470));box(draw,(550,470,1000,580),'LOCAL?')
        arrow(draw,(550,525),(340,525));label(draw,(445,490),'yes',28);box(draw,(100,470,340,580),'Tray L')
        arrow(draw,(1000,525),(1260,525),BLUE);label(draw,(1130,490),'no',28,BLUE);box(draw,(1260,470,1500,580),'Tray O',BLUE)
        draw.line([(220,580),(220,735),(1515,735),(1515,135),(1050,135)],fill=TEAL,width=6)
        draw.line([(1380,580),(1380,735)],fill=BLUE,width=6);arrow(draw,(1210,135),(1050,135))
        label(draw,(810,780),'Repeat until the pile is empty',30)
    elif slug=='linear-algebra-ja':
        label(draw,(400,55),'行の見方',42);label(draw,(1190,55),'列の見方',42)
        def point(origin,x,y):return (origin[0]+x*108,origin[1]-y*108)
        for origin in ((140,710),(960,710)):
            arrow(draw,point(origin,0,0),point(origin,4.4,0),INK,3);arrow(draw,point(origin,0,0),point(origin,0,5),INK,3)
            for i in range(1,5):
                p=point(origin,i,0);draw.line([(p[0],p[1]-5),(p[0],p[1]+5)],fill=INK,width=2);label(draw,(p[0],p[1]+25),str(i),23)
                p=point(origin,0,i);label(draw,(p[0]-25,p[1]),str(i),23)
        o=(140,710)
        draw.line([point(o,0,3),point(o,3,0)],fill=TEAL,width=6)
        draw.line([point(o,0,2),point(o,4,0)],fill=BLUE,width=6)
        p=point(o,2,1);draw.ellipse((p[0]-9,p[1]-9,p[0]+9,p[1]+9),fill=RUST);label(draw,(p[0]+70,p[1]-35),'(2,1)',30,RUST)
        label(draw,(430,210),'x + y = 3',30,TEAL);label(draw,(430,260),'x + 2y = 4',30,BLUE)
        o=(960,710);arrow(draw,point(o,0,0),point(o,2,2));arrow(draw,point(o,2,2),point(o,3,4),BLUE)
        arrow(draw,point(o,0,0),point(o,3,4),RUST,5)
        label(draw,(1130,590),'2(1,1)',27,TEAL);label(draw,(1330,360),'(1,2)',27,BLUE);label(draw,(1160,230),'(3,4)',27,RUST)
    elif slug=='listening-music-fr':
        start=350;step=145
        for i in range(8):
            x=start+i*step;draw.line([(x,160),(x,690)],fill='#d5dfda',width=2);label(draw,(x,110),str(i+1),32)
            draw.ellipse((x-15,225,x+15,255),fill=TEAL)
        for y,text in [(240,'Frappes'),(440,'Grave'),(640,'Aigu')]:label(draw,(165,y),text,40)
        draw.line([(start,440),(start+3*step,440)],fill=BLUE,width=13)
        draw.line([(start+4*step,440),(start+7*step,440)],fill=BLUE,width=13)
        for i,y in [(2,670),(3,620),(4,570)]:
            x=start+i*step;draw.ellipse((x-15,y-15,x+15,y+15),fill=RUST)
        label(draw,(850,775),'Repères successifs · carte conceptuelle',32)
    elif slug=='financial-markets-es':
        label(draw,(800,70),'Recursos, promesas y resultados posibles',42)
        box(draw,(80,160,490,280),'Prestamista');box(draw,(1090,160,1500,280),'Taller')
        arrow(draw,(490,210),(1090,210));label(draw,(800,165),'Hoy: 100',35)
        arrow(draw,(1090,470),(490,470),RUST);box(draw,(80,410,490,530),'Prestamista',RUST);box(draw,(1090,410,1500,530),'Taller',RUST)
        label(draw,(790,380),'Dentro de un mes',32);label(draw,(790,520),'Pago prometido: 105',30,RUST)
        box(draw,(80,650,490,770),'Clientes',BLUE);arrow(draw,(490,710),(1090,710),BLUE);box(draw,(1090,650,1500,770),'Taller',BLUE)
        label(draw,(800,665),'Ingresos: 140 u 80',32,BLUE);label(draw,(800,775),'Posibilidades, no probabilidades',26)
    elif slug=='death-ar':
        # XeLaTeX performs actual Arabic shaping; Pillow in this runtime has no RAQM.
        tex=path.with_suffix('.tex')
        tex.write_text(r'''\documentclass[border=12pt]{standalone}
\usepackage{fontspec,xcolor,tikz,polyglossia}
\setdefaultlanguage{english}\setotherlanguage{arabic}
\newfontfamily\arabicfont[Script=Arabic]{Geeza Pro}
\definecolor{ink}{HTML}{193848}\definecolor{teal}{HTML}{237768}
\begin{document}\begin{tikzpicture}[every node/.style={font=\Large,align=center},line width=1.3pt,draw=teal]
\node[draw,rounded corners,minimum width=6cm,minimum height=1.4cm] (q) at (0,3.5) {\textarabic{السؤال}};
\node[draw,rounded corners,minimum width=6cm,minimum height=1.4cm] (v) at (-4,0) {\textarabic{القيمة}};
\node[draw,rounded corners,minimum width=6cm,minimum height=1.4cm] (i) at (4,0) {\textarabic{الوجود والهوية}};
\draw[->] (q.south) -- (v.north);\draw[->] (q.south) -- (i.north);
\node[text=ink] at (-4,-2) {\textarabic{هل هو مرغوب؟}};
\node[text=ink] at (4,-2) {\textarabic{ما الذي يستمر؟}};
\end{tikzpicture}\end{document}''')
        subprocess.run(['/Library/TeX/texbin/xelatex','-no-shell-escape','-halt-on-error','-interaction=nonstopmode',tex.name],cwd=path.parent,capture_output=True,check=True,timeout=60)
        import pypdfium2 as pdfium
        pdf=pdfium.PdfDocument(tex.with_suffix('.pdf'));page=pdf[0];rendered=page.render(scale=4).to_pil().convert('RGB');pdf.close()
        rendered.thumbnail((1500,760));image.paste(rendered,((1600-rendered.width)//2,(850-rendered.height)//2))
        for suffix in ('.tex','.pdf','.aux','.log'):tex.with_suffix(suffix).unlink(missing_ok=True)
    image.save(path)


ANCHOR_NOTE={'zh':'原课定位：','en':'Original-course location: ','ja':'元の授業の位置：','fr':'Repère dans le cours original : ','es':'Ubicación en el curso original: ','ar':'الموضع في المقرر الأصلي: '}


def evidence(sample,binding,units):
    sources=copy.deepcopy(sample['sources']);course=binding['course'];anchors={}
    for unit in course['units']:
        if unit['id'] in units:anchors.setdefault(unit['source_id'],[]).append(unit['id'])
    for source_id,mapped in anchors.items():
        original=next(s for s in course['sources'] if s['id']==source_id)
        match=next((s for s in sources if s['url']==original['url']),None)
        if not match:
            match={'id':'S'+str(max(int(s['id'][1:]) for s in sources)+1),'title':original['title'],'url':original['url'],
                   'publisher':course['institution'],'note':ANCHOR_NOTE[sample['language']]+original['locator'],
                   'published_at':course['edition'],'checked_at':'2026-11-01'}
            sources.append(match)
        match['course_ref']=courses.source_ref(binding,source_id,mapped)
    return sources


def build_plans(output):
    for sample in SAMPLES:
        root=output/sample['slug'];root.mkdir(parents=True,exist_ok=True)
        if (root/'state.json').exists():raise ValueError('Existing sample preserved; choose a fresh output directory.')
        (root/'assets').mkdir();figure(sample,root/'assets/teaching.png')
        binding=courses.bind(sample['course_id'],['u01','u02','u03'])
        config={'timezone':'Asia/Shanghai','language':sample['language'],'daily_minutes':10,'sample_mode':True,
                'course_pathway':binding,'delivery':{'platform':'html','mode':'local'}}
        visual={k:sample['figure'][k] for k in ('caption','credit')};visual['path']='assets/teaching.png'
        plan={'topic':sample['title'],'title':sample['title'],'days':copy.deepcopy(sample['days']),
              'sections':sample['plan_sections'],'sources':evidence(sample,binding,binding['unit_ids']),'figure':visual}
        c.initialize(root,config,plan)
        lesson={'day':1,'title':sample['days'][0]['topic'],'course_units':['u01'],'reading_minutes':7,'practice_minutes':3,
                'sections':sample['lesson_sections'],'sources':evidence(sample,binding,['u01']),'figure':visual}
        c.save(root/'data/Day01.json',lesson)
        c.save(root/'provenance.json',{'release':'3.0.0','course_id':sample['course_id'],'language':sample['language'],
              'checked_at':'2026-11-01','sample':'Independent six-day partial learning guide; only Day01 exported.',
              'approval':'Simulated only for explicitly requested public examples; no real learner approval or job.',
              'figure':'Original code-drawn conceptual teaching diagram; no measured data or original university slide.',
              'figure_concept':sample['figure']['concept'],'builder':'tools/build_university_samples.py',
              'source_ledger':'docs/v300-sample-sources.md','live_schedule':False})
        manifest=documents.render(root,root/'plan.json','plan',['pdf','html'])
        print(sample['slug'],'plan',manifest['report'],flush=True)


def build_lessons(output):
    for sample in SAMPLES:
        root=output/sample['slug'];c.reviewed(root,'plan');c.approve(root)
        manifest=documents.render(root,root/'data/Day01.json','Day01',['pdf','html'])
        print(sample['slug'],'Day01',manifest['report'],flush=True)


def export(output):
    destination=ROOT/'examples/university'
    for sample in SAMPLES:
        root=output/sample['slug'];target=destination/sample['slug'];target.mkdir(parents=True,exist_ok=True)
        for key in ('plan','Day01'):
            manifest=c.reviewed(root,key)
            for fmt in ('pdf','html'):shutil.copyfile(root/manifest['artifacts'][fmt],target/f'{key}.{fmt}')
        for source,name in [('config.json','config.json'),('plan.json','plan.json'),('data/Day01.json','Day01.json'),('assets/teaching.png','assets/teaching.png'),('provenance.json','provenance.json')]:
            (target/name).parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(root/source,target/name)
    make_gallery(output)


def make_gallery(output):
    # Contact sheet of actual first lesson pages, not generated document mockups.
    canvas=Image.new('RGB',(2400,2300),'#e9eee8');d=ImageDraw.Draw(canvas)
    label(d,(120,85),'OMNI  /  LEARNING IN YOUR LANGUAGE',46,INK,'lm')
    label(d,(120,147),'6 subjects · 6 languages · real lesson pages',30,TEAL,'lm')
    names=['HARVARD · 中文','HARVARD · ENGLISH','MIT · 日本語','YALE · FRANÇAIS','YALE · ESPAÑOL','YALE · العربية']
    # Latin index labels keep this neutral preview usable without an RTL image shaper.
    names[-1]='YALE · ARABIC'
    for i,(sample,name) in enumerate(zip(SAMPLES,names)):
        x=100+(i%3)*760;y=240+(i//3)*1000
        preview=Image.open(output/sample['slug']/'previews/Day01-01.png').convert('RGB')
        # Keep each actual first page whole, including its teaching figure.
        crop=preview.resize((680,960),Image.Resampling.LANCZOS)
        d.rounded_rectangle((x-8,y-8,x+688,y+968),radius=14,fill='#cad7d0')
        canvas.paste(crop,(x,y));label(d,(x,y-35),name,28,INK,'lm')
    label(d,(120,2260),'Independent course guides · Open the gallery for full PDF + offline HTML',27,TEAL,'lm')
    assets=ROOT/'docs/assets';assets.mkdir(exist_ok=True);canvas.save(assets/'course-gallery-v3.png',optimize=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'tmp/v300/samples')
    parser.add_argument('stage',choices=['plans','lessons','export']);args=parser.parse_args();output=args.output.resolve()
    {'plans':build_plans,'lessons':build_lessons,'export':export}[args.stage](output)
