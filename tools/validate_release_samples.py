"""Read-only checks for the isolated v1.0.0 bilingual acceptance courses."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/omni-learning-anything/scripts'))
import omni_core as core
import omni_pdf as pdf
import pypdfium2 as pdfium

base = ROOT / 'validation/release-v1.0.0'
courses = [(base / 'zh/astronomy-sample-v1', ['plan', 'Day01', 'Day02', 'Day03']),
           (base / 'en', ['plan', 'Day01'])]
documents = []
for root, keys in courses:
    config = core.read(root / 'config.json')
    state = core.read(root / 'state.json')
    core.validate_config(config)
    core.check_approval(root, state)
    core.check_deliveries(root, state)
    assert config['sample_mode'] is True and state['schedule'] is None
    assert state['mastery'] == {}, 'Delivery is not evidence of mastery.'
    for key in keys:
        manifest = core.reviewed(root, key)
        data = core.read(root / ('plan.json' if key == 'plan' else f'data/{key}.json'))
        report = pdf.inspect_pdf(root / manifest['pdf'], data['sources'])
        assert report == manifest['report'] and manifest['layout_warnings'] == 0
        assert len({source['url'] for source in data['sources']}) >= 5
        if key != 'plan':
            assert data['reading_minutes'] + data['practice_minutes'] <= config['daily_minutes']
            assert data['title'] == core.read(root / 'plan.json')['days'][data['day'] - 1]['topic']
        doc = pdfium.PdfDocument(root / manifest['pdf'])
        texts = [doc[i].get_textpage().get_text_range() for i in range(len(doc))]
        assert all(len(text.strip()) > 80 for text in texts), 'Blank or nearly blank page.'
        text = ''.join(texts)
        assert data['title'].replace(' ', '') in text.replace(' ', '')
        assert ('Further reading' if config['language'] == 'en' else '扩展学习') in text
        doc.close()
        documents.append({'course': str(root.relative_to(base)), 'key': key, **report})
    action = core.next_action(root)
    if config['language'] == 'zh':
        assert state['status'] == 'complete' and action == {'action': 'complete'}
        assert set(state['lessons']) == {'1', '2', '3'}
        assert not (root / 'data/Day04.json').exists()
    else:
        assert state['status'] == 'active' and action['day'] == 2 and action['action'] == 'generate'
        assert set(state['lessons']) == {'1'}
        assert not (root / 'data/Day02.json').exists()
print(json.dumps({'result': 'passed', 'pdfs': len(documents),
                  'pages': sum(d['pages'] for d in documents),
                  'documents': documents}, ensure_ascii=False, indent=2))
