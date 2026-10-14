"""Package only runtime skill files, never course data or local credentials."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib
import re
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'dist';out.mkdir(exist_ok=True)
skill=ROOT/'skills/omni-learning-anything'
version=re.search(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$',(skill/'SKILL.md').read_text(),re.M).group(1)
archive=out/f'omni-learning-anything-skill-v{version}.zip'
with ZipFile(archive,'w',ZIP_DEFLATED) as z:
 for p in sorted((ROOT/'skills/omni-learning-anything').rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name!='.DS_Store':
   z.write(p,Path('omni-learning-anything')/p.relative_to(ROOT/'skills/omni-learning-anything'))
(out/'SHA256SUMS').write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n')
print(archive.name,archive.stat().st_size)
