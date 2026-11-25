"""Render translated diagrams using the same specifications as the Chinese lessons.

Run with Pillow. Arabic labels require its libraqm shaping support.
"""
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/omni-learning-anything/scripts'))
from omni_figures import build


def main():
    translations = json.loads((ROOT / 'tools/content/readme_diagram_labels.json').read_text(encoding='utf-8'))
    examples = ROOT / 'examples/teaching-figures'
    output = ROOT / 'docs/assets/figures'
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for language, diagrams in translations.items():
            for name, labels in diagrams.items():
                spec = json.loads((examples / f'{name}.json').read_text(encoding='utf-8'))
                result = build(tmp, {**spec, **labels})
                shutil.copyfile(Path(tmp) / result['path'], output / f'{name}-{language}.png')


if __name__ == '__main__':
    main()
