"""Validate the generated v2 skill ZIP in an isolated extraction; no external writes."""
import argparse
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--archive', type=Path, default=ROOT/'dist/omni-learning-anything-skill-v2.0.1.zip')
args = parser.parse_args()
archive = args.archive.resolve()
with tempfile.TemporaryDirectory(prefix='omni-v2-install-') as temp:
    target = Path(temp).resolve()
    with ZipFile(archive) as z:
        for member in z.infolist():
            output = (target/member.filename).resolve()
            if not output.is_relative_to(target):
                raise ValueError('Unsafe ZIP path')
            if member.filename.startswith('.') or '/.' in member.filename or '.local.' in member.filename:
                raise ValueError('Unexpected private file in ZIP')
        z.extractall(target)
    skill = target/'omni-learning-anything'
    cli = skill/'scripts/omni_learning.py'
    p = subprocess.run([sys.executable,str(cli),'--version'],capture_output=True,text=True,check=True)
    assert p.stdout.strip() == 'omni-learning-anything 2.0.1'
    for file in (skill/'scripts').glob('*.py'):
        compile(file.read_text(), str(file), 'exec')
    for name in ('omni_notion.py','omni_feishu.py','omni_tencent.py','omni_dingtalk.py','omni_obsidian.py','omni_delivery.py'):
        assert (skill/'scripts'/name).is_file(), name
    for name in ('notion','feishu','tencent','dingtalk','obsidian','generic'):
        assert (skill/'references/providers'/f'{name}.md').is_file(), name
    subprocess.run([sys.executable,str(cli),'--project',str(target),'doctor'],check=True,capture_output=True)
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    assert checksum in (archive.parent/'SHA256SUMS').read_text()
    print('v2 ZIP extraction, runtime syntax, CLI version/doctor, provider resources and SHA256: passed')
