<div align="center">

<img src="docs/assets/omni-wordmark-transparent.png" alt="Omni Learning Anything brush wordmark" width="520">

# Omni Learning Anything

[![Release](https://img.shields.io/github/v/release/ShawnRen57/omni-learning-anything?style=flat-square&color=237768&label=release)](https://github.com/ShawnRen57/omni-learning-anything/releases/latest)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-7c3aed?style=flat-square)](skills/omni-learning-anything/SKILL.md)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](skills/omni-learning-anything/references/setup.md)
[![Course languages](https://img.shields.io/badge/languages-10-0284c7?style=flat-square)](README.md#choose-your-learning-language)
[![Output formats](https://img.shields.io/badge/formats-4-0f766e?style=flat-square)](skills/omni-learning-anything/references/setup.md)
[![MIT License](https://img.shields.io/badge/license-MIT-2563eb?style=flat-square)](LICENSE)
[![Release downloads](https://img.shields.io/github/downloads/ShawnRen57/omni-learning-anything/total?style=flat-square&color=0891b2&label=downloads)](https://github.com/ShawnRen57/omni-learning-anything/releases)
[![GitHub stars](https://img.shields.io/github/stars/ShawnRen57/omni-learning-anything?style=flat-square&color=b7791f)](https://github.com/ShawnRen57/omni-learning-anything/stargazers)

[![PDF](docs/assets/badges/pdf.svg)](#output-destinations)
[![HTML](https://img.shields.io/badge/HTML-C04A21?style=flat&logo=html5&logoColor=white)](#output-destinations)
[![DOCX](docs/assets/badges/docx.svg)](#output-destinations)
[![Markdown](https://img.shields.io/badge/Markdown-425367?style=flat&logo=markdown&logoColor=white)](#output-destinations)

[![Notion](https://img.shields.io/badge/Notion-191919?style=flat&logo=notion&logoColor=white)](#output-destinations)
[![Feishu](docs/assets/badges/feishu.svg)](#output-destinations)
[![DingTalk](docs/assets/badges/dingtalk.svg)](#output-destinations)
[![Tencent Docs](docs/assets/badges/tencent-docs.svg)](#output-destinations)
[![Obsidian (local)](https://img.shields.io/badge/Obsidian%20%28local%29-6D3BC2?style=flat&logo=obsidian&logoColor=white)](#output-destinations)

[English](README.md) · [简体中文](docs/readme/README_zh.md) · [日本語](docs/readme/README_ja.md) · [한국어](docs/readme/README_ko.md) · [Español](docs/readme/README_es.md) · [Français](docs/readme/README_fr.md) · [Deutsch](docs/readme/README_de.md) · [Português](docs/readme/README_pt.md) · [Русский](docs/readme/README_ru.md) · [العربية](docs/readme/README_ar.md)

**[Download v3.0.0 Skill ZIP](https://github.com/ShawnRen57/omni-learning-anything/releases/latest/download/omni-learning-anything-skill-v3.0.0.zip)**

[skills.sh](https://skills.sh/shawnren57/omni-learning-anything/omni-learning-anything) · [Installation channels](docs/distribution-channels.md)

</div>

**Choose a university course—or bring your own books and papers. Learn at your pace, with light checks, useful feedback and review, in local files or cloud documents.**

Turn “I want to learn…” into a plan you can follow. Start with one of 12 source-backed university learning pathways, a personal goal, or your own materials. Review the plan before lessons begin.

Try **“I want to study Harvard Positive Psychology.”** The agent identifies the source course, reuses what you already told it, and asks only for details that affect your plan.

<a href="examples/README.md"><img src="docs/assets/learning-sample-gallery.png" alt="15 actual lesson pages across six languages" width="100%"></a>

## What is new in v3.0.0

- **12 university pathways:** find a starting point in Harvard, Yale, MIT and Stanford course sources without designing a syllabus yourself.
- **A pace you can sustain:** preserve the original unit order and source mapping while splitting study into sessions that fit your time.
- **Real multilingual examples:** preview PDF and HTML plans and first lessons across six languages and six subjects.
- **A gentler first step:** after installation or first use, your host agent can offer course choices in the current chat if you have not chosen a topic. The skill cannot open a new chat by itself.

<a id="university-courses"></a>
## Choose a built-in university course

Ask **“show me built-in courses”**. Choose a course, your language and available time; the agent proposes a mapped plan for approval. These are independent learning pathways based on public course sources. Complete lecture content is not bundled; no university endorsement or certificate is implied.

| University | Course and original title | Source edition |
| --- | --- | --- |
| Harvard | [Positive Psychology](https://ppc.sas.upenn.edu/sites/default/files/ppsyllabusschachar.pdf) | PSY 1504 · Spring 2006 · Tal Ben-Shahar |
| Harvard | [CS50x: Introduction to Computer Science](https://cs50.harvard.edu/x/2026/syllabus/) | CS50x · 2026 · David Malan |
| Harvard | [Justice](https://sandel.scholars.harvard.edu/justice) | 24-lecture public series · Michael Sandel |
| Yale | [Introduction to Psychology](https://oyc.yale.edu/introduction-psychology/psyc-110) | PSYC 110 · Spring 2007 · Paul Bloom |
| Yale | [Financial Markets](https://oyc.yale.edu/economics/econ-252) | ECON 252 · Spring 2011 · Robert Shiller |
| Yale | [Game Theory](https://oyc.yale.edu/economics/econ-159) | ECON 159 · Fall 2007 · Ben Polak |
| Yale | [Death](https://oyc.yale.edu/death/phil-176) | PHIL 176 · Spring 2007 · Shelly Kagan |
| Yale | [Listening to Music](https://oyc.yale.edu/music/musi-112) | MUSI 112 · Fall 2008 · Craig Wright |
| MIT | [Introduction to Computer Science and Programming in Python](https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/) | 6.0001 · Fall 2016 |
| MIT | [Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/) | 18.06 · Spring 2010 · Gilbert Strang |
| MIT | [Classical Mechanics](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/) | 8.01SC · Fall 2016 |
| Stanford | [Machine Learning](https://cs229.stanford.edu/syllabus-autumn2018.html) | CS229 · Autumn 2018 |

A 10-minute session covers a small learning step, not an entire original lecture or course. Original workload remains visible; longer readings, exercises and projects need their own time. Course sources and availability may change.

## Bring your own materials

Use PDF, TXT, Markdown, HTML, DOCX, EPUB, PPTX, SRT or VTT. Choose chapters, pages or timestamps and whether outside supplements are allowed. Explanations and checks trace back to the selected source locations. Legacy DOC and RTF need trusted conversion first.

A rough goal works too: “I want to learn a little economics.” The agent suggests useful directions, explains its assumptions and asks only questions that affect the plan. A specific goal goes straight to planning.

<a id="choose-your-learning-language"></a>
## Choose your learning language

**English · 简体中文 · 日本語 · 한국어 · Español · Français · Deutsch · Português · Русский · العربية**

Plans and lessons support all ten languages listed above, independently of the source language or the language of this page. Arabic documents use right-to-left layout.

<a id="output-destinations"></a>
## Choose where to keep your course

| Destination | How it works |
| --- | --- |
| PDF · HTML · DOCX · Markdown | Choose a folder and PDF, HTML, DOCX or Markdown. HTML keeps its illustration in one offline file; external source links need internet. |
| Notion | Connect a parent page through the official `ntn` CLI. |
| Obsidian | Choose an existing local Vault and course folder; no Obsidian API is used. |
| Feishu / 飞书 | Connect a document folder through the official `lark` CLI and user authorization. |
| DingTalk / 钉钉 | Connect a folder through the official `dws` CLI; organization approval may be required. |
| Tencent Docs / 腾讯文档 | Choose a root or folder and complete official OAuth/MCP authorization. |

Tell the agent where to save your course. It checks existing access, guides missing setup and reuses your named connection. Do not paste passwords or tokens into chat.

<a id="quick-start"></a>
## Install and start

Ask your agent to install the latest release and verify that this client can discover the skill. Keep existing courses and connections when updating. With Node.js, run:

```sh
npx skills@latest add ShawnRen57/omni-learning-anything --skill omni-learning-anything -g
```

In Claude Code, use the plugin installer:

```text
/plugin install omni-learning-anything --marketplace ShawnRen57/omni-learning-anything
```

Without Node.js, download the ZIP above and use your client’s skill upload or agent-assisted installation. `skills.sh` is live; the SkillHub listing is currently v2.6.0. Check the channel guide for version availability.

## Try your first course

```text
Show me built-in courses. Use Harvard CS50x 2026 as the source.
I am a beginner. Teach me in English, 20 minutes a day.
Preserve the original unit order and show the original workload.
Save offline HTML in my course folder. Show me the plan first.
```

Or try: “Teach me the first two chapters of my EPUB in 15-minute sessions,” or “Use Yale Financial Markets 2011 to help me understand financial institutions.”

Review and approve the plan, then ask for the first lesson. To resume, say “Continue from my earliest undelivered lesson.” Ask to pause when needed. Scheduling works only when your host supports it and you agree a time and timezone; generation begins at that time, with delivery after research and review.

## Checks, feedback and review

When you want a check, request 1–3 short questions as cards or plain text. Get source-grounded feedback and hints; a longer quiz is available if you ask. Your responses inform a learning record in the background so the lesson stays easy to follow.

Ask “What should I review today?” for a small review within your existing time budget, or “What have my answers shown this week?” for an evidence-based recap. Correct a judgment, skip a topic, or choose a new lesson. Review creates no extra automatic quiz or timer.

Approve changes to future lessons before a revised course version starts; the old plan and history remain available. Anki cards are an optional one-way CSV export, without automatic synchronization.

<a id="examples"></a>
## Real examples in six languages

Explore 15 lesson pages in the gallery above. The six university sample sets below each include a partial six-day plan and a standalone first lesson in PDF and offline HTML.

| Language | Sample subject |
| --- | --- |
| Chinese · 简体中文 | Harvard Positive Psychology |
| English | Harvard CS50 |
| Japanese · 日本語 | MIT Linear Algebra |
| French · Français | Yale Listening to Music |
| Spanish · Español | Yale Financial Markets |
| Arabic · العربية | Yale Death |

[Open the university catalog and sample files](examples/university/README.md)

Earlier PDF examples remain available:

[Technology](examples/technology/) · [Economics](examples/economics/) · [Music](examples/music/) · [Agent products](examples/agent-product/) · [Architecture](examples/architecture/) · [Ming history](examples/ming-history/)

<a id="versions"></a>
## Version guide

| Version | What it brings to your learning |
| --- | --- |
| **v3.0.0** | Choose a university pathway, see the source edition, and preview real multilingual learning documents. |
| **v2.3–v2.6** | Ask for light checks, study your own sources, review what needs attention and install or update more easily. |
| **v2** | Study in ten languages, choose four local formats, or keep your course in connected documents. |
| **v1** | Approve a personal plan and receive illustrated PDF lessons with practice and further reading. |

## Guides and requirements

[Installation and updates](skills/omni-learning-anything/references/install.md) · [Formats and fonts](skills/omni-learning-anything/references/setup.md) · [Document connections](skills/omni-learning-anything/references/onboarding.md) · [Channel status](docs/distribution-channels.md) · [v3.0.0 release validation](docs/release-validation-v3.0.0.md)

This Agent Skill uses the research, document and scheduling tools available in your host. PDF requires XeLaTeX; other output formats do not. Cloud access, cross-device sync and unattended delivery depend on your host, account and authorization. Support is checked for the current client; availability on every platform is not assumed.

[MIT](LICENSE) · [Changelog](CHANGELOG.md) · [Attribution](ATTRIBUTION.md)
