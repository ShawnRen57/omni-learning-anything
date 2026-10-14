# Runtime setup

All routes require Python 3.10+ and a host that researches sources, runs/files, inspects the chosen document and handles learner dialogue. The skill does not include an LLM, web-search subscription, image model, scheduler or cloud authorization. New courses select their output explicitly.

Check the interpreter version first: macOS may resolve `python3` to an older system version. Use an installed supported interpreter and an isolated environment.

## Install only the selected route's dependencies

```sh
python3 -m venv .venv
# Markdown / DOCX / cloud / Obsidian (no PDF packages or TeX):
.venv/bin/python -m pip install -r /installed/omni-learning-anything/scripts/requirements-documents.txt
# PDF, or repository development including PDF regression tests:
.venv/bin/python -m pip install -r /installed/omni-learning-anything/scripts/requirements.txt
# Tencent API route additionally needs the official COS SDK:
.venv/bin/python -m pip install -r /installed/omni-learning-anything/scripts/requirements-tencent.txt
.venv/bin/python /installed/omni-learning-anything/scripts/omni_learning.py --project /course doctor
```

Windows: use `py -3 -m venv .venv` and `.venv\Scripts\python.exe`. Select current host commands; offline installation is not promised. Standard-library Markdown/Vault export can run without DOCX/HTTP/PDF libraries; images must already be valid local PNG/JPEG. DOCX lazily imports python-docx/Pillow; API routes lazily import requests, and Tencent imports the COS SDK only when an actual upload is needed.

DOCX: render using an available approved viewer/converter and inspect all pages. Bundled generation embeds Chinese text, images, source links and image descriptions; the viewer's font availability affects rendering. Prefer FangSong/Times New Roman when available; do not install proprietary fonts or promise identical cloud fonts.

Markdown: use the generated local HTML preview plus the source/asset links. Obsidian: inspect the real Vault note and figure. Cloud: inspect the populated native document and verify learner access. Missing viewers/access require a truthful limitation; a successful API request is not visual inspection.

Secrets stay outside installed/course/repository files. API scripts consume only named environment variables, never raw JSON secrets or authentication headers returned to chat. For DingTalk use authorized official `dws`; host/UI routes require actual document tools and may not work unattended.

## XeLaTeX

First check PATH, then existing TinyTeX installations. The renderer recognizes PATH, macOS `~/Library/TinyTeX/bin/*`, Linux `~/.TinyTeX/bin/*` and `/Library/TeX/texbin`. Other locations may be added to PATH. It never uses an HTML/reportlab fallback under the label "LaTeX PDF".

Install from official distributions within the user's existing authorization:
- macOS: MacTeX or TinyTeX; official guide https://yihui.org/tinytex/ and https://www.tug.org/mactex/ .
- Linux: distro packages (Debian/Ubuntu: `texlive-xetex texlive-lang-chinese texlive-fonts-recommended texlive-latex-extra`) or TinyTeX.
- Windows: MiKTeX https://miktex.org/download or TeX Live https://tug.org/texlive/ ; reopen the shell so PATH is refreshed.

For TinyTeX/TeX Live, install missing packages with its `tlmgr`: `xelatex fontspec xecjk fandol tex-gyre geometry xcolor graphics enumitem fancyhdr titlesec hyperref`. A distribution's own package manager may be required; do not mix incompatible system and user TeX trees. Respect managed-device restrictions and report the exact blocked requirement.

The template detects FangSong / 仿宋 / FandolFang-Regular, then FandolSong-Regular; Times New Roman then TeX Gyre Termes. FandolFang is an open FangSong family supplied by TeX Live. No proprietary font is redistributed. The generated manifest records actual PDF font names; verify that report and the rendered text.

Run `doctor`, then compile the first actual plan. A binary's presence alone does not prove required packages/fonts work. Every page is rendered with pypdfium2; image review remains an agent responsibility.
