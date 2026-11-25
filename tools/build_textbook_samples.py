"""Build and export the five Chinese textbook lesson samples in reviewable stages."""
import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/omni-learning-anything/scripts'))
from content.v400_textbook_samples import SAMPLES
import omni_core as core
import omni_document as document
import omni_materials as materials
from omni_textbook_fetch import acquire
from omni_textbook_index import get
from omni_textbook_ocr import ocr
from omni_textbooks import bind, extract_figure, locate

EXAMPLES = ROOT / 'examples'
DESTINATION = EXAMPLES / 'textbooks'


def prepare(output, sources):
    for sample in SAMPLES:
        root = output / sample['slug']
        if (root / 'state.json').exists():
            raise ValueError(f'{root} already has a plan. Use a fresh sample directory.')
        book = get(sample['book'])
        local_pdf = sources / (book['book_id'] + '.pdf') if sources else None
        result = acquire(root, book, local_pdf=local_pdf)
        sha = result['sha256']
        material = result['material']
        page = sample['page']
        if sample.get('ocr'):
            material = ocr(root, book['book_id'], material['id'], sha, str(page))
        match = next(hit for hit in locate(root, material['id'], sha, sample['quote'])['matches']
                     if hit['page'] == page)
        binding = bind(root, book, material['id'], sha, str(page), sample['title'])
        selection = binding['materials']['selections'][0]
        evidence = materials.citation(root, selection, match['unit'], sample['quote'], 'S1')
        evidence.update(publisher=sample['publisher'], published_at=sample['edition'].split('，', 1)[1])
        evidence['note'] += f"。书内第 {sample['printed_page']} 页，ISBN {sample['isbn']}。"
        figure = extract_figure(root, book, sha, page, sample['box'], sample['caption'])
        reading, practice = sample['minutes']
        title = sample['title']
        config = dict(binding, timezone='Asia/Shanghai', language='zh',
                      daily_minutes=reading + practice, sample_mode=True)
        plan = dict(topic=title, title=f'教材学习计划｜{title}', days=[{'day': 1, 'topic': title}],
                    sources=[evidence], figure=figure, sections=[
                        {'title': '教材和范围', 'body': f"{sample['level']}。{sample['edition']}，书内第 {sample['printed_page']} 页，PDF 第 {page} 页 [S1]。"},
                        {'title': '这一课怎么学', 'body': f'先看教材原图，再读分步讲解，最后完成迁移练习并自查。阅读与读图约 {reading} 分钟，练习约 {practice} 分钟。'},
                    ])
        lesson_sections = [{'title': '教材和范围', 'body': plan['sections'][0]['body']}]
        lesson_sections.extend({'title': heading, 'body': body} for heading, body in sample['sections'])
        lesson = dict(title=title, day=1, reading_minutes=reading, practice_minutes=practice,
                      figure=figure, sources=[evidence], sections=lesson_sections)
        core.initialize(root, config, plan)
        core.save(root / 'data/Day01.json', lesson)
        manifest = document.render(root, root / 'plan.json', 'plan', ['pdf', 'html'])
        print(sample['slug'], 'plan', manifest['previews'], flush=True)


def lessons(output, review):
    for sample in SAMPLES:
        root = output / sample['slug']
        document.review(root, 'plan', review)
        core.approve(root)
        manifest = document.render(root, root / 'data/Day01.json', 'Day01', ['pdf', 'html'])
        print(sample['slug'], 'Day01', manifest['previews'], flush=True)


def export(output, review):
    for sample in SAMPLES:
        root = output / sample['slug']
        document.review(root, 'Day01', review)
        manifest = core.reviewed(root, 'Day01')
        target = DESTINATION / sample['slug']
        target.mkdir(parents=True, exist_ok=True)
        for fmt in ('pdf', 'html'):
            shutil.copyfile(root / manifest['artifacts'][fmt], target / f'Day01.{fmt}')
        lesson = core.read(root / 'data/Day01.json')
        source = lesson['sources'][0]
        core.save(target / 'source.json', {
            'title': lesson['title'],
            'edition': sample['edition'],
            'isbn': sample['isbn'],
            'source': source['url'],
            'physical_pdf_page': sample['page'],
            'printed_page': sample['printed_page'],
            'original_figure': lesson['figure']['textbook_ref'],
            'generated_on': manifest['created_at'],
            'sample_mode': True,
            'ocr': bool(sample.get('ocr')),
            'lesson_pdf_sha256': hashlib.sha256((target / 'Day01.pdf').read_bytes()).hexdigest(),
        })
    gallery()


def example_pdf(folder, day):
    return next((EXAMPLES / folder / 'pdf').glob(f'*_Day{day:02d}_*.pdf'))


def first_page(path, size):
    with pdfium.PdfDocument(path) as pdf:
        page = pdf[0]
        try:
            bitmap = page.render(scale=1.3)
            try:
                return bitmap.to_pil().convert('RGB').resize(size, Image.Resampling.LANCZOS)
            finally:
                bitmap.close()
        finally:
            page.close()


def language_previews(sources, size):
    """Capture the actual lessons and render their Markdown exercises for the gallery.

    The gallery build uses Chrome/Chromium and the Python Markdown package.
    """
    import markdown

    browser = (shutil.which('google-chrome') or shutil.which('chromium') or
               shutil.which('chromium-browser') or '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    if not Path(browser).is_file():
        raise RuntimeError('Install Chrome or Chromium to build the language previews.')
    previews = {}
    with tempfile.TemporaryDirectory(prefix='omni-gallery-') as directory:
        work = Path(directory)
        for source in sources:
            page = source
            if source.suffix == '.md':
                # Keep every prompt and link as authored. Add only page typography.
                markup = markdown.markdown(source.read_text(encoding='utf-8'))
                page = work / (source.stem + '.html')
                page.write_text(
                    '<!doctype html><html lang="zh"><meta charset="utf-8"><style>'
                    '*{box-sizing:border-box}body{margin:0;padding:36px;color:#173747;background:white;'
                    'font:21px/1.6 system-ui,sans-serif}h1{font-size:34px;line-height:1.25;'
                    'margin:0 0 32px}p{margin:12px 0}strong{color:#237768}a{color:#245fa4}'
                    'main:not(:has(strong)){font-size:31px;line-height:1.8}'
                    '</style><main>' + markup + '</main></html>', encoding='utf-8')
            screenshot = work / 'preview.png'
            screenshot.unlink(missing_ok=True)
            subprocess.run([browser, '--headless', '--disable-gpu', '--hide-scrollbars',
                            '--disable-background-networking', '--no-first-run',
                            '--user-data-dir=' + str(work / 'profile'), '--window-size=720,1020',
                            '--screenshot=' + str(screenshot), page.resolve().as_uri()],
                           capture_output=True, timeout=45, check=True)
            with Image.open(screenshot) as image:
                previews[source] = image.convert('RGB').resize(size, Image.Resampling.LANCZOS)
    return previews


def gallery():
    university = EXAMPLES / 'university'
    # Keep the first four rows stable as new examples are added.
    previous = [
        ('Positive Psychology', 'HARVARD / CHINESE', university / 'positive-psychology-zh/Day01.pdf'),
        ('AI Agent Design', 'CHINESE / DAY 01', example_pdf('agent-product', 1)),
        ('Ming Dynasty History', 'CHINESE / DAY 01', example_pdf('ming-history', 1)),
        ('Western Architecture', 'CHINESE / DAY 01', example_pdf('architecture', 1)),
        ('Listening to Music', 'YALE / FRENCH', university / 'listening-music-fr/Day01.pdf'),
        ('Computer Science', 'HARVARD / ENGLISH', university / 'cs50x-en/Day01.pdf'),
        ('Agent Workflows', 'CHINESE / DAY 02', example_pdf('agent-product', 2)),
        ('Linear Algebra', 'MIT / JAPANESE', university / 'linear-algebra-ja/Day01.pdf'),
        ('Roman Arches', 'CHINESE / DAY 03', example_pdf('architecture', 3)),
        ('Philosophy of Death', 'YALE / ARABIC', university / 'death-ar/Day01.pdf'),
        ('Stargazing', 'CHINESE / DAY 01', next((ROOT / 'validation/release-v1.0.0/zh/astronomy-sample-v1/pdf').glob('*_Day01_*.pdf'))),
        ('Technology Systems', 'CHINESE / DAY 01', example_pdf('technology', 1)),
        ('Economics', 'CHINESE / DAY 01', example_pdf('economics', 1)),
        ('Financial Markets', 'YALE / SPANISH', university / 'financial-markets-es/Day01.pdf'),
        ('Music Fundamentals', 'CHINESE / DAY 01', example_pdf('music', 1)),
    ]
    labels = ['认识空气', '长方形的周长', '读懂四四拍', '地球的大小与形状', '职业结构与因果']
    languages = EXAMPLES / 'languages'
    language_row = [
        ('Japanese Study Plan', 'CHINESE → JAPANESE', languages / 'zh-ja/plan.html'),
        ('Morning Greetings', 'JAPANESE / LESSON 01', languages / 'zh-ja/day01.html'),
        ('Two-way Recall', 'JAPANESE / DAYS 01–03', languages / 'zh-ja/day03-worksheet.md'),
        ('At a Reading Group', 'JAPANESE / INDEPENDENT TASK', languages / 'zh-ja/day03-task.md'),
        ('Meeting a Colleague', 'ENGLISH → GERMAN', languages / 'en-de/day01.html'),
    ]
    entries = [(title, sample['level'], DESTINATION / sample['slug'] / 'Day01.pdf')
               for title, sample in zip(labels, SAMPLES)] + previous + language_row
    font_path = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
    heading = ImageFont.truetype(font_path, 53)
    label = ImageFont.truetype(font_path, 37)
    detail = ImageFont.truetype(font_path, 24)
    cell_width, cell_height = 484, 759
    width, height = 2520, 260 + cell_height * ((len(entries) + 4) // 5)
    ink, teal = '#173747', '#237768'
    canvas = Image.new('RGB', (width, height), '#e9eee8')
    draw = ImageDraw.Draw(canvas)
    draw.text((65, 45), 'OMNI  /  LEARNING SAMPLE GALLERY', font=heading, fill=ink)
    draw.text((66, 114), f'{len(entries)} real previews  ·  Textbooks, courses and foreign language practice', font=detail, fill=teal)
    page_size = (448, 634)
    screenshots = language_previews([entry[2] for entry in language_row], page_size)
    for index, (title, subtitle, path) in enumerate(entries):
        row, col = divmod(index, 5)
        x, y = 65 + col * cell_width, 177 + row * cell_height
        draw.text((x, y), title, font=label, fill=ink)
        draw.text((x, y + 49), subtitle, font=detail, fill=teal)
        draw.rounded_rectangle((x - 5, y + 84, x + 453, y + 728), radius=10, fill='#cad7d0')
        preview = screenshots[path] if path in screenshots else first_page(path, page_size)
        canvas.paste(preview, (x, y + 89))
    draw.text((65, height - 49), 'Open the sample library to read the lessons, try the exercises and check the sources.', font=detail, fill=teal)
    canvas.save(ROOT / 'docs/assets/learning-sample-gallery.png', optimize=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['plans', 'lessons', 'export', 'gallery'])
    parser.add_argument('--output', type=Path, required=True, help='Private build archive outside the skill.')
    parser.add_argument('--sources', type=Path, help='Optional folder of verified PDFs named by textbook ID.')
    parser.add_argument('--review', help='Actual inspection note, required to approve or export.')
    args = parser.parse_args()
    if args.stage in ('lessons', 'export') and not args.review:
        parser.error('Provide --review after visually inspecting every page.')
    if args.stage == 'plans':
        prepare(args.output.resolve(), args.sources)
    elif args.stage == 'lessons':
        lessons(args.output.resolve(), args.review)
    elif args.stage == 'export':
        export(args.output.resolve(), args.review)
    else:
        gallery()
