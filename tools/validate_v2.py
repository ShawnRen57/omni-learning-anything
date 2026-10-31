"""Validate the generated v2 skill ZIP in an isolated extraction; no external writes."""
import argparse
import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
current_version = re.search(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$', (ROOT/'skills/omni-learning-anything/SKILL.md').read_text(), re.M).group(1)
parser.add_argument('--archive', type=Path, default=ROOT/f'dist/omni-learning-anything-skill-v{current_version}.zip')
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
    version = re.search(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$', (skill/'SKILL.md').read_text(), re.M).group(1)
    assert p.stdout.strip() == 'omni-learning-anything '+version
    for file in (skill/'scripts').glob('*.py'):
        compile(file.read_text(), str(file), 'exec')
    for name in ('omni_notion.py','omni_feishu.py','omni_tencent.py','omni_dingtalk.py','omni_obsidian.py','omni_delivery.py','omni_connections.py','omni_official_cli.py','omni_html.py','omni_locale.py','omni_tencent_auth.py','omni_tencent_mcp.py'):
        assert (skill/'scripts'/name).is_file(), name
    for name in ('notion','feishu','tencent','dingtalk','obsidian','generic'):
        assert (skill/'references/providers'/f'{name}.md').is_file(), name
    assert (skill/'references/onboarding.md').is_file()
    result = subprocess.run([sys.executable,str(cli),'connect','--platform','notion'],check=True,capture_output=True,text=True)
    import json
    assert json.loads(result.stdout)['stage'] == 'location'
    subprocess.run([sys.executable,str(cli),'--project',str(target),'doctor'],check=True,capture_output=True)
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    assert checksum in (archive.parent/'SHA256SUMS').read_text()
    print('v2 ZIP extraction, runtime syntax, CLI version/doctor, provider resources and SHA256: passed')
