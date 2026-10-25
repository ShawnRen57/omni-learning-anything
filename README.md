<div align="center">

![Omni Learning Anything](docs/assets/omni-banner.svg)

# Omni Learning Anything

[![Release](https://img.shields.io/badge/version-2.2.0-237768)](https://github.com/ShawnRen57/omni-learning-anything/releases) [![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

[English](README.md) · [简体中文](docs/readme/README_zh.md) · [日本語](docs/readme/README_ja.md) · [한국어](docs/readme/README_ko.md) · [Español](docs/readme/README_es.md) · [Français](docs/readme/README_fr.md) · [Deutsch](docs/readme/README_de.md) · [Português](docs/readme/README_pt.md) · [Русский](docs/readme/README_ru.md) · [العربية](docs/readme/README_ar.md)

**[Download Skill ZIP](https://github.com/ShawnRen57/omni-learning-anything/releases/latest/download/omni-learning-anything-skill-v2.2.0.zip)**

</div>

**Turn “I want to learn…” into a course you can follow.**

Tell your agent what you want to learn. Omni builds a plan around your goal, experience and available time, then helps you work through illustrated daily lessons with sources, practice and self-checks.

<a id="versions"></a>
## Version guide

| | |
| --- | --- |
| **v1** | Your personal PDF course: approve a learning plan, then receive illustrated lessons with exercises and further reading. |
| **v2** | Keep your course where you study: choose local files, Notion, Obsidian, Feishu, DingTalk or Tencent Docs. The agent guides connection and remembers your chosen location. |
| **v2.2.0** | Read offline HTML in your browser, learn in 10 languages, and connect DingTalk or Tencent Docs through guided official authorization. |

## What you can do

- Learn for your own goal: a trip, a work project, an interview or a new interest.
- Set a manageable daily pace with explanations, an illustration, practice and answer guidance.
- Follow the evidence: inline citations and at least five explained further-reading links in every document.
- Keep going after an interruption; review your plan before daily lessons begin.

## Choose your learning language

**English · 简体中文 · 日本語 · 한국어 · Español · Français · Deutsch · Português · Русский · العربية**

Plans and lessons can be authored in any of the languages below. Your topic, source language and README language can differ from your course language. Arabic output uses right-to-left layout.

## Choose where to keep your course

| Destination | What you tell the agent |
| --- | --- |
| Local PDF · HTML · DOCX · Markdown | A course folder and preferred format. HTML includes its image in one offline file; source links open online. |
| Notion | A parent-page link and the workspace you want to use. |
| Obsidian | An existing local Vault and course subfolder; no API key is needed. |
| Feishu / 飞书 | A course folder link; complete official app setup and user authorization if needed. |
| DingTalk / 钉钉 | A document folder link and your organization; an administrator may need to enable CLI access. |
| Tencent Docs / 腾讯文档 | Your home root or a personal folder link; sign in and review the official authorization page. |

Say where you want to save the course. The agent checks existing access, asks only for missing details, guides the platform steps and reuses your named connection. You do not need to find object IDs or write configuration files. Do not paste passwords or tokens into chat. Organization approvals can require additional steps.

<a id="quick-start"></a>
## Start through chat

Send this to your agent:

```text
Install omni-learning-anything from https://github.com/ShawnRen57/omni-learning-anything.
Use the latest Skill ZIP from Releases and keep the complete skill folder.
Verify that this client can discover the skill, then tell me how to start.
```

Then describe what you want to learn:

```text
Use omni-learning-anything to teach me architectural history for travel.
I am a beginner. Plan 30 days, 15 minutes a day, in English.
Save the course as offline HTML in my course folder. Show me the plan first.
```

Review the plan, request changes, then approve it. If your agent supports scheduling, agree the time and timezone. Otherwise, ask it to continue when you are ready. A scheduled time starts generation; delivery follows research and review.

```text
Continue my Omni Learning Anything course from the earliest undelivered lesson.
Pause this course and its schedule.
Preserve my old course and propose a revised plan for my new goal.
```

<a id="examples"></a>
## Explore example courses

Browse complete plans and daily PDFs for technology, economics, music, Agent product design, architecture and Ming history. The linked archives retain their original source-check dates; they are examples you can adapt.

| Technology | Economics | Music |
| :---: | :---: | :---: |
| [![Technology](docs/screenshots/technology.png)](examples/technology/) | [![Economics](docs/screenshots/economics.png)](examples/economics/) | [![Music](docs/screenshots/music.png)](examples/music/) |

| Agent products | Architecture | Ming history |
| :---: | :---: | :---: |
| [![Agent products](docs/screenshots/agent-product.png)](examples/agent-product/) | [![Architecture](docs/screenshots/architecture.png)](examples/architecture/) | [![Ming history](docs/screenshots/ming-history.png)](examples/ming-history/) |

## Installation and guides

[Install on your agent](skills/omni-learning-anything/references/install.md) · [Format and font setup](skills/omni-learning-anything/references/setup.md) · [Connect your documents](skills/omni-learning-anything/references/onboarding.md) · [Release validation](docs/release-validation-v2.2.0.md)

An Agent Skill, powered by your agent’s research, document and scheduling tools. PDF needs XeLaTeX; other output formats do not. Cloud writing uses official APIs/CLIs; Obsidian writes local Vault files. Cross-device sync and unattended scheduling depend on your host and account.

[MIT](LICENSE) · [Changelog](CHANGELOG.md) · [Attribution](ATTRIBUTION.md)
