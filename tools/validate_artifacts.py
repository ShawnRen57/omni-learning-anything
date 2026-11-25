"""Check published sample documents and their figures without recording a review."""
import json
import re
import sys
from pathlib import Path

from PIL import Image
from pypdf import PdfReader
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/omni-learning-anything/scripts'))
import omni_core as core
import omni_pdf as pdf
from omni_figures import validate_reading


def compact(text):
    return re.sub(r'\s+', '', text)


def inspect(course, key):
    manifest = core.reviewed(course, key)
    data = core.read(course / ('plan.json' if key == 'plan' else f'data/{key}.json'))
    figure = data['figure']
    spec = core.read(course / 'figure-specs' / f'{key}.json')
    for field in ('reading', 'caption', 'credit'):
        assert spec[field] == figure[field], (course.name, key, field)
    assert figure['path'] == 'assets/' + spec['image']
    figure_hash = core.digest(course / figure['path'])
    assert spec['image'] == f'figure-{figure_hash[:12]}.png'
    assert spec['body_reference'] in '\n'.join(section['body'] for section in data['sections'])
    validate_reading(figure, {s['id'] for s in data['sources']}, required=True)
    artifact = course / manifest['pdf']
    report = pdf.inspect_pdf(artifact, data['sources'])
    assert {**report, 'figure': figure['path']} == manifest['report']
    assert manifest['layout_warnings'] == 0 and report['pages'] == len(manifest['previews'])
    # Confirm the actual lesson image is embedded on the preview page used in the gallery.
    with Image.open(course / figure['path']) as original:
        pixels = original.convert('RGB').tobytes()
        first_page_images = PdfReader(artifact).pages[0].images
        assert any(pic.image.size == original.size and pic.image.convert('RGB').tobytes() == pixels
                   for pic in first_page_images), (course.name, key)
    with pdfium.PdfDocument(artifact) as rendered:
        content = compact(''.join(page.get_textpage().get_text_range() for page in rendered))
    for text in (data['title'], figure['reading']['question'], figure['reading']['observation'], '扩展学习'):
        assert compact(text) in content, (course.name, key, text)
    return report['pages'], figure_hash


def main():
    pages = 0
    figures = []
    for plan in sorted((ROOT / 'examples').glob('*/plan.json')):
        course = plan.parent
        config, state = core.read(course / 'config.json'), core.read(course / 'state.json')
        assert config['sample_mode'] and config['visual_guides'] and state['schedule'] is None
        assert len(core.read(plan)['days']) == 30 and set(state['lessons']) == {'1', '2', '3'}
        core.check_approval(course, state)
        for key in ('plan', 'Day01', 'Day02', 'Day03'):
            count, figure_hash = inspect(course, key)
            pages += count
            figures.append(figure_hash)
        assert core.next_action(course)['day'] == 4
    assert len(figures) == len(set(figures)) == 24
    print(json.dumps({'pdfs': len(figures), 'pages': pages, 'distinct_figures': len(set(figures))}))


if __name__ == '__main__':
    main()
