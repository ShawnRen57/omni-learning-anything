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

**[Download v4.0.0 Skill ZIP](https://github.com/ShawnRen57/omni-learning-anything/releases/download/v4.0.0/omni-learning-anything-skill-v4.0.0.zip)**

[skills.sh](https://skills.sh/shawnren57/omni-learning-anything/omni-learning-anything) · [Installation channels](docs/distribution-channels.md)

</div>

**Choose a university course—or bring your own books and papers. Learn at your pace, with light checks, useful feedback and review, in local files or cloud documents.**

Turn “I want to learn…” into a plan you can follow. Pick from 65 courses and two open references, or start with a personal goal or your own materials. Review the plan before lessons begin.

Try **“I want to study the History of Chinese Architecture at Tsinghua.”** or **“I want to study OpenAI Applied AI Foundations.”** The agent identifies the source course, reuses what you already told it, and asks only for details that affect your plan.

<a href="examples/README.md"><img src="docs/assets/learning-sample-gallery.png" alt="15 actual lesson pages across six languages" width="100%"></a>

## What is new in v4.0.0

Study from mainland China’s primary, junior-secondary and senior-secondary textbooks. Choose the subject, grade, edition and volume, then study the whole book or focus on a chapter, concept or formula. The skill adapts the explanations to the learner’s age and crops illustrations directly from the cited textbook pages.

[See the textbook workflow](skills/omni-learning-anything/references/textbooks.md)

<a id="university-courses"></a>
## Choose a built-in course

Ask **“show me built-in courses”**. Choose a course, your language and available time; the agent proposes a mapped plan for approval. These are independent learning pathways based on public course sources. Complete lecture content is not bundled; no university endorsement or certificate is implied.

[Source editions and access notes](docs/course-catalog-sources.md)

| University or organization | Courses and open references |
| --- | --- |
| Tsinghua University | [中国建筑史——史前至两宋辽金](https://higher.smartedu.cn/course/687eb7bf16c43a09c0e58c23) · [文物精品与文化中国](https://higher.smartedu.cn/course/6a5e9b52b44e493c768f8c9c) · [中国建筑史（下）（自主模式）](https://v1-www.xuetangx.com/courses/course-v1%3ATsinghuaX%2B80000901X_2%2Bsp/about) · [艺术的启示](https://higher.smartedu.cn/course/6786ec4c225d72705e5dc29e) · [校园风物与大学文化——以清华大学为例](https://higher.smartedu.cn/course/6a5e9b60b44e493c768f8cba) · [人工智能通识教育红皮书](https://aige.cs.tsinghua.edu.cn/redbook/) *(open reference)* |
| Peking University | [经典昆曲欣赏](https://www.icourse163.org/course/PKU-1470426173?tid=1474265476) · [人工智能与信息社会](https://www.icourse163.org/course/PKU-1003471009?tid=1476756462) · [西方音乐欣赏](https://www.icourse163.org/course/PKU-1207132813?tid=1207476216) · [人工智能原理](https://www.icourse163.org/course/PKU-1002188003?tid=1472399493) |
| Fudan University | [人工智能，语言与伦理](https://www.icourse163.org/course/FUDAN-1205951803?tid=1475942449) · [比较文化研究](https://umoocs.unipus.cn/course/7944/tasks) · [深度学习及其应用](https://higher.smartedu.cn/course/622ac9f0bee70ef79f419877) · [中华优秀传统文化](https://higher.smartedu.cn/course/63ffd464af1f1b5d3ecfd579) · [政治学原理](https://www.icourse163.org/course/FUDAN-1461787179?tid=1462604462) |
| Shanghai Jiao Tong University | [唐诗宋词人文解读](https://higher.smartedu.cn/course/69b0942995df98bb27ba19b4) · [数学的天空](https://higher.smartedu.cn/course/690530295345b68214577952) · [机器的征途：空天科技](https://higher.smartedu.cn/course/62354d7a9906eace0490b2aa) · [经济法](https://higher.smartedu.cn/course/67c2473d225d72705e7bb8c8) · [关爱生命——急救与自救技能](https://higher.smartedu.cn/course/69b0942695df98bb27ba19a1) |
| Zhejiang University | [唐诗经典](https://higher.smartedu.cn/course/6982720195df98bb27cadb06) |
| Beijing Normal University | [书法欣赏](https://www.icourse163.org/course/BNU-1003240002?tid=1488313456) |
| Harvard University | [Positive Psychology](https://ppc.sas.upenn.edu/sites/default/files/ppsyllabusschachar.pdf) · [CS50’s Introduction to Computer Science](https://cs50.harvard.edu/x/2026/syllabus/) · [Justice](https://sandel.scholars.harvard.edu/justice) · [Rhetoric: The Art of Persuasive Writing and Public Speaking](https://pll.harvard.edu/course/rhetoric-art-persuasive-writing-and-public-speaking) · [CS50’s Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/) · [Masterpieces of World Literature](https://www.edx.org/learn/literature/harvard-university-masterpieces-of-world-literature) · [Pyramids of Giza: Ancient Egyptian Art and Archaeology](https://giza.fas.harvard.edu/videos/) |
| Yale University | [Introduction to Psychology](https://oyc.yale.edu/introduction-psychology/psyc-110) · [Financial Markets](https://oyc.yale.edu/economics/econ-252) · [Game Theory](https://oyc.yale.edu/economics/econ-159) · [Death](https://oyc.yale.edu/death/phil-176) · [Listening to Music](https://oyc.yale.edu/music/musi-112/lecture-1) · [Roman Architecture](https://oyc.yale.edu/history-of-art/hsar-252) · [Introduction to Theory of Literature](https://oyc.yale.edu/english/engl-300) · [The Atmosphere, the Ocean, and Environmental Change](https://oyc.yale.edu/geology-and-geophysics/gg-140) · [European Civilization, 1648-1945](https://oyc.yale.edu/history/hist-202) · [Philosophy and the Science of Human Nature](https://oyc.yale.edu/philosophy/phil-181) · [Principles of Evolution, Ecology and Behavior](https://oyc.yale.edu/ecology-and-evolutionary-biology/eeb-122) |
| MIT | [Introduction to Computer Science and Programming in Python](https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/video_galleries/lecture-videos/) · [Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/calendar/) · [Classical Mechanics](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/) · [Introduction to Art History](https://ocw.mit.edu/courses/4-601-introduction-to-art-history-fall-2018/pages/calendar/) · [Principles of Microeconomics](https://ocw.mit.edu/courses/14-01-principles-of-microeconomics-fall-2023/pages/calendar/) · [Art Since 1940](https://ocw.mit.edu/courses/4-651-art-since-1940-fall-2010/pages/lecture-notes/) · [Philosophy of Film](https://ocw.mit.edu/courses/24-213-philosophy-of-film-fall-2004/pages/calendar/) · [Introduction to Deep Learning](https://introtodeeplearning.com/2026/index.html) · [Introduction to Sustainable Energy](https://ocw.mit.edu/courses/22-081j-introduction-to-sustainable-energy-fall-2010/pages/calendar/) |
| Stanford University | [Machine Learning](https://cs229.stanford.edu/syllabus-autumn2018.html) · [Deep Learning for Computer Vision](https://cs231n.stanford.edu/2026/schedule.html) |
| UC Berkeley | [Introduction to Artificial Intelligence](https://inst.eecs.berkeley.edu/~cs188/sp26/) |
| University of Helsinki & MinnaLearn | [Elements of AI: Introduction to AI](https://opin.fi/en/study-options/HY/elements-of-ai-introduction-to-ai/89eb0e79-873e-4d2a-aec5-d694d7762118) · [Elements of AI: Building AI](https://buildingai.elementsofai.com/) |
| OpenAI Academy | [AI Foundations](https://academy.openai.com/public/courses/ai-foundations-dnq5w) · [Applied AI Foundations](https://academy.openai.com/public/courses/applied-ai-foundations-szsmv) · [Agents and Workflows](https://academy.openai.com/public/courses/agents-and-workflows-y0qoc) · [AI for College Students](https://academy.openai.com/public/courses/ai-for-college-students-gxgmr) |
| Anthropic · Claude Academy | [AI Fluency: Framework and foundations](https://academy.claude.com/courses/ai-fluency-framework-foundations) · [AI Fluency for students](https://academy.claude.com/courses/ai-fluency-for-students) · [AI Fluency for educators](https://academy.claude.com/courses/ai-fluency-for-educators) |
| DeepLearning.AI | [AI For Everyone](https://www.coursera.org/learn/ai-for-everyone/) · [Generative AI for Everyone](https://www.coursera.org/learn/generative-ai-for-everyone/) |
| Google | [Google AI Essentials](https://grow.google/ai-essentials/) |
| Microsoft | [Generative AI for Beginners](https://github.com/microsoft/generative-ai-for-beginners/blob/79a4334e158147d4f36c27d805e0cb163c1e445b/README.md#-lessons) |
| Hugging Face | [AI Agents Course](https://huggingface.co/learn/agents-course/unit0/introduction) |
| Smarthistory | [Reframing Art History](https://smarthistory.org/reframing-art-history/) *(open reference)* |

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

### Textbook lesson samples

The two public samples use original illustrations from public-domain historical textbooks.

[Textbook lesson samples](examples/textbooks/README.md)

| [Sun and Moon](examples/textbooks/sun-and-moon.md) | [The Lever and the Balance](examples/textbooks/lever-balance.md) |
| --- | --- |
| <img src="examples/textbooks/sun-moon-original.png" alt="Sun and Moon" height="140"> | <img src="examples/textbooks/balance-original.png" alt="The Lever and the Balance" height="140"> |

Earlier PDF examples remain available:

[Technology](examples/technology/) · [Economics](examples/economics/) · [Music](examples/music/) · [Agent products](examples/agent-product/) · [Architecture](examples/architecture/) · [Ming history](examples/ming-history/)

<a id="versions"></a>
## Version guide

| Version | What it brings to your learning |
| --- | --- |
| **v4.0.0** | Study mainland Chinese school textbooks with age-specific lessons, exact page references and original illustrations. |
| **v3.0.0** | Choose a university pathway, see the source edition, and preview real multilingual learning documents. |
| **v2.3–v2.6** | Ask for light checks, study your own sources, review what needs attention and install or update more easily. |
| **v2** | Study in ten languages, choose four local formats, or keep your course in connected documents. |
| **v1** | Approve a personal plan and receive illustrated PDF lessons with practice and further reading. |

## Guides and requirements

[Installation and updates](skills/omni-learning-anything/references/install.md) · [Formats and fonts](skills/omni-learning-anything/references/setup.md) · [Document connections](skills/omni-learning-anything/references/onboarding.md) · [Channel status](docs/distribution-channels.md) · [v4.0.0 release validation](docs/release-validation-v4.0.0.md)

This Agent Skill uses the research, document and scheduling tools available in your host. PDF requires XeLaTeX; other output formats do not. Cloud access, cross-device sync and unattended delivery depend on your host, account and authorization. Support is checked for the current client; availability on every platform is not assumed.

[MIT](LICENSE) · [Changelog](CHANGELOG.md) · [Attribution](ATTRIBUTION.md)
