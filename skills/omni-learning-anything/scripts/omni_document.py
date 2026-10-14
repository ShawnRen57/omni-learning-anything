"""Shared content contract and standalone Markdown/DOCX export. PDF imports are lazy."""
import html
import re
import shutil
from pathlib import Path
from urllib.parse import quote, urlsplit
import omni_core as c


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


def validate_key(key):
    if not re.fullmatch(r'plan|Day[0-9]{2,}', key) or (key != 'plan' and int(key[3:]) < 1):
        raise ValueError('Invalid document key.')


def prepare(root, input_path, key):
    validate_key(key)
    if not input_path.is_relative_to(root):
        raise ValueError('Input must be inside project.')
    state = c.read(root / 'state.json'); plan = c.read(root / 'plan.json')
    c.validate_plan(plan)
    config = c.read(root / 'config.json'); data = c.read(input_path)
    if key == 'plan':
        if input_path != root / 'plan.json':
            raise ValueError('Plan renderer must use canonical plan.json.')
        if state['lessons']:
            raise ValueError('Preserve the started curriculum; create a new project.')
        if (root / 'manifests/plan.json').exists():
            raise ValueError('Plan already rendered; reuse it or create a revised project.')
    else:
        c.check_approval(root, state)
        day = data.get('day'); action = c.next_action(root)
        if type(day) is not int or key != f'Day{day:02d}' or action.get('day') != day or action['action'] != 'generate':
            raise ValueError('Render only the next ungenerated lesson; reuse existing artifacts.')
        if data.get('title') != plan['days'][day - 1]['topic']:
            raise ValueError('Lesson title differs from approved plan.')
        reading = data.get('reading_minutes'); practice = data.get('practice_minutes')
        if type(reading) is not int or reading < 1 or type(practice) is not int or practice < 0:
            raise ValueError('Reading minutes must be positive; practice minutes nonnegative integers.')
        if reading + practice > config['daily_minutes']:
            raise ValueError('Lesson exceeds agreed time budget.')
    validate_document(data, root)
    return data, plan, config


def subtitle(data, plan, config, date, key):
    if key == 'plan':
        label = f"Learning plan / {len(plan['days'])} days" if config.get('language') == 'en' else f"学习计划 / {len(plan['days'])} 天"
    else:
        label = f"{key}/{len(plan['days'])} | Read {data['reading_minutes']} min + practice {data['practice_minutes']} min" if config.get('language') == 'en' else f"{key}/{len(plan['days'])} | 阅读 {data['reading_minutes']} 分钟 + 练习 {data['practice_minutes']} 分钟"
    return f'{date} | {label}'


def markdown_text(data, plan, config, date, key, image_ref):
    lines = ['# ' + data['title'], subtitle(data, plan, config, date, key)]
    for i, section in enumerate(data['sections']):
        lines.extend(['## ' + section['title'], section['body']])
        if i == min(1, len(data['sections']) - 1):
            lines.extend([f"![{data['figure']['caption']}]({image_ref})", data['figure']['credit']])
    lines.append('## Further reading (optional)' if config.get('language') == 'en' else '## 扩展学习（选读）')
    for source in data['sources']:
        lines.append(f"- [{source['id']}] [{source['title']}]({source['url']}): {source['note']}; {source['publisher']} | Published: {source['published_at']} | Checked: {source['checked_at']}")
    return '\n\n'.join(lines) + '\n'


def write_docx(path, data, plan, config, image, date, key):
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from PIL import Image
    document = Document()
    document.core_properties.author = 'Omni Learning Anything'
    document.core_properties.title = data['title']
    section = document.sections[0]
    section.top_margin = section.bottom_margin = Inches(0.8)
    section.left_margin = section.right_margin = Inches(0.85)
    for name in ('Normal', 'Title', 'Heading 1', 'Heading 2'):
        style = document.styles[name]
        style.font.name = 'Times New Roman'; style.font.size = Pt(11 if name == 'Normal' else 16)
        style.element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), 'FangSong')
    document.styles['Normal'].paragraph_format.space_after = Pt(7)
    document.add_heading(data['title'], 0)
    document.add_paragraph(subtitle(data, plan, config, date, key))
    for i, item in enumerate(data['sections']):
        document.add_heading(item['title'], 1)
        for paragraph in item['body'].split('\n\n'):
            document.add_paragraph(paragraph)
        if i == min(1, len(data['sections']) - 1):
            with Image.open(image) as img:
                ratio = img.height / img.width
            width = min(6.5, 3.0 / ratio)
            shape = document.add_picture(str(image), width=Inches(width))
            shape._inline.docPr.set('descr', data['figure']['caption'])
            document.add_paragraph(data['figure']['caption'])
            document.add_paragraph(data['figure']['credit'])
    document.add_heading('Further reading (optional)' if config.get('language') == 'en' else '扩展学习（选读）', 1)
    for source in data['sources']:
        p = document.add_paragraph(f"[{source['id']}] ")
        link = OxmlElement('w:hyperlink')
        link.set(qn('r:id'), p.part.relate_to(source['url'], RT.HYPERLINK, is_external=True))
        run = OxmlElement('w:r'); properties = OxmlElement('w:rPr')
        color = OxmlElement('w:color'); color.set(qn('w:val'), '227E82'); properties.append(color)
        run.append(properties); text = OxmlElement('w:t'); text.text = source['title']; run.append(text)
        link.append(run); p._p.append(link)
        p.add_run(f": {source['note']}; {source['publisher']} | Published: {source['published_at']} | Checked: {source['checked_at']}")
    document.save(path)


def render(root, input_path, key, formats=None):
    root = Path(root).resolve(); input_path = Path(input_path).resolve()
    formats = list(dict.fromkeys(formats or ['markdown']))
    if not formats or any(f not in ('pdf', 'markdown', 'docx') for f in formats):
        raise ValueError('Choose pdf, markdown or docx formats.')
    validate_key(key)
    if 'pdf' in formats:
        import omni_pdf
        return omni_pdf.render(root, input_path, key, export_formats=formats)
    with c.lock(root):
        data, plan, config = prepare(root, input_path, key)
        for folder in ('sources', 'assets', 'manifests', 'previews'):
            path = root / folder
            if not path.resolve().is_relative_to(root):
                raise ValueError('Output directory escapes project.')
            path.mkdir(exist_ok=True)
        figure = (root / data['figure']['path']).resolve()
        if figure.suffix.lower() == '.pdf':
            raise ValueError('Markdown/DOCX figures need PNG or JPEG; convert the figure first.')
        image = root / 'assets' / ('figure-' + c.digest(figure)[:12] + figure.suffix.lower())
        if image != figure:
            shutil.copyfile(figure, image)
        artifacts = {}; outputs = [image]
        md = root / 'sources' / (key + '.md')
        text = markdown_text(data, plan, config, c.today(root), key, '../assets/' + quote(image.name))
        md.write_text(text, encoding='utf-8'); artifacts['markdown'] = str(md.relative_to(root)); outputs.append(md)
        if 'docx' in formats:
            path = root / 'sources' / (key + '.docx')
            write_docx(path, data, plan, config, image, c.today(root), key)
            artifacts['docx'] = str(path.relative_to(root)); outputs.append(path)
        preview = root / 'previews' / (key + '.html')
        body = ''.join(f'<h2>{html.escape(s["title"])}</h2><p>{html.escape(s["body"]).replace(chr(10), "<br>")}</p>' for s in data['sections'])
        links = ''.join(f'<li>[{html.escape(s["id"])}] <a href="{html.escape(s["url"], quote=True)}">{html.escape(s["title"])}</a>: {html.escape(s["note"])}; {html.escape(s["publisher"])} | {html.escape(s["published_at"])} | {html.escape(s["checked_at"])}</li>' for s in data['sources'])
        preview.write_text('<!doctype html><html lang="' + config.get('language', 'zh') + '"><meta charset="utf-8"><style>body{max-width:780px;margin:40px auto;padding:24px;font:18px/1.7 serif;color:#173747}img{max-width:100%;max-height:350px}a{color:#227e82}</style><h1>' + html.escape(data['title']) + '</h1><p>' + html.escape(subtitle(data, plan, config, c.today(root), key)) + '</p>' + body + '<figure><img src="../assets/' + quote(image.name) + '" alt="' + html.escape(data['figure']['caption'], quote=True) + '"><figcaption>' + html.escape(data['figure']['caption']) + ' — ' + html.escape(data['figure']['credit']) + '</figcaption></figure><h2>Further reading / 扩展学习（选读）</h2><ul>' + links + '</ul></html>', encoding='utf-8')
        outputs.extend([preview, input_path, root / 'plan.json', root / 'config.json'])
        manifest = {'key': key, 'artifact': artifacts.get('docx', artifacts['markdown']),
                    'artifacts': artifacts, 'input': str(input_path.relative_to(root)),
                    'created_at': c.today(root), 'files': {str(p.relative_to(root)): c.digest(p) for p in outputs},
                    'previews': [str(preview.relative_to(root))], 'reviewed_at': None,
                    'report': {'links': len(data['sources']), 'figure': str(image.relative_to(root))}}
        c.save(root / 'manifests' / (key + '.json'), manifest)
        return manifest


def review(root, key, note):
    root = Path(root).resolve(); validate_key(key)
    with c.lock(root):
        state = c.read(root / 'state.json')
        if key != 'plan' and str(int(key[3:])) in state['lessons']:
            raise ValueError('Delivered review is immutable; retain the original archive.')
        path = root / 'manifests' / (key + '.json'); manifest = c.read(path)
        c.manifest_ok(root, manifest)
        if not note.strip():
            raise ValueError('Record what was visually checked.')
        manifest.update(reviewed_at=c.today(root), review_note=note)
        c.save(path, manifest)
