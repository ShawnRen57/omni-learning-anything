# Runtime setup

Requires Python 3.10+, XeLaTeX and a host that can search/read webpages, write/run local files and inspect PDF previews. The skill itself does not include an LLM, web-search subscription, image model or scheduler. No specific API key is required by this package; the host may charge for its tools.

Check `python3 --version` first; macOS may resolve `python3` to Python 3.9. Select an installed Python 3.10+ interpreter (for example `python3.12`) before creating the environment. The CLI rejects an older interpreter with a clear message.

Use an isolated Python environment where possible:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r /path/to/omni-learning-anything/scripts/requirements.txt
.venv/bin/python /path/to/omni-learning-anything/scripts/omni_learning.py doctor
```

Windows: `py -3 -m venv .venv`, then `.venv\Scripts\python.exe -m pip install -r PATH\scripts\requirements.txt`. Use a Python command appropriate to the host. Offline package install cannot be promised.

## XeLaTeX

First check PATH, then existing TinyTeX installations. The renderer recognizes PATH, macOS `~/Library/TinyTeX/bin/*`, Linux `~/.TinyTeX/bin/*` and `/Library/TeX/texbin`. Other locations may be added to PATH. It never uses an HTML/reportlab fallback under the label "LaTeX PDF".

Install from official distributions within the user's existing authorization:
- macOS: MacTeX or TinyTeX; official guide https://yihui.org/tinytex/ and https://www.tug.org/mactex/ .
- Linux: distro packages (Debian/Ubuntu: `texlive-xetex texlive-lang-chinese texlive-fonts-recommended texlive-latex-extra`) or TinyTeX.
- Windows: MiKTeX https://miktex.org/download or TeX Live https://tug.org/texlive/ ; reopen the shell so PATH is refreshed.

For TinyTeX/TeX Live, install missing packages with its `tlmgr`: `xelatex fontspec xecjk fandol tex-gyre geometry xcolor graphics enumitem fancyhdr titlesec hyperref`. A distribution's own package manager may be required; do not mix incompatible system and user TeX trees. Respect managed-device restrictions and report the exact blocked requirement.

The template detects FangSong / 仿宋 / FandolFang-Regular, then FandolSong-Regular; Times New Roman then TeX Gyre Termes. FandolFang is an open FangSong family supplied by TeX Live. No proprietary font is redistributed. The generated manifest records actual PDF font names; verify that report and the rendered text.

Run `doctor`, then compile the first actual plan. A binary's presence alone does not prove required packages/fonts work. Every page is rendered with pypdfium2; image review remains an agent responsibility.
