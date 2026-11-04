<div align="center">

<img src="../../docs/assets/omni-wordmark-transparent.png" alt="Omni Learning Anything brush wordmark" width="520">

# Omni Learning Anything

[![Release](https://img.shields.io/github/v/release/ShawnRen57/omni-learning-anything?style=flat-square&color=237768&label=release)](https://github.com/ShawnRen57/omni-learning-anything/releases/latest)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-7c3aed?style=flat-square)](../../skills/omni-learning-anything/SKILL.md)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](../../skills/omni-learning-anything/references/setup.md)
[![Course languages](https://img.shields.io/badge/languages-10-0284c7?style=flat-square)](../../README.md#choose-your-learning-language)
[![Output formats](https://img.shields.io/badge/formats-4-0f766e?style=flat-square)](../../skills/omni-learning-anything/references/setup.md)
[![MIT License](https://img.shields.io/badge/license-MIT-2563eb?style=flat-square)](../../LICENSE)
[![Release downloads](https://img.shields.io/github/downloads/ShawnRen57/omni-learning-anything/total?style=flat-square&color=0891b2&label=downloads)](https://github.com/ShawnRen57/omni-learning-anything/releases)
[![GitHub stars](https://img.shields.io/github/stars/ShawnRen57/omni-learning-anything?style=flat-square&color=b7791f)](https://github.com/ShawnRen57/omni-learning-anything/stargazers)

[![PDF](https://img.shields.io/badge/PDF-B52632?style=flat)](#output-destinations)
[![HTML](https://img.shields.io/badge/HTML-C04A21?style=flat&logo=html5&logoColor=white)](#output-destinations)
[![DOCX](https://img.shields.io/badge/DOCX-245A9C?style=flat)](#output-destinations)
[![Markdown](https://img.shields.io/badge/Markdown-425367?style=flat&logo=markdown&logoColor=white)](#output-destinations)

[![Notion](https://img.shields.io/badge/Notion-191919?style=flat&logo=notion&logoColor=white)](#output-destinations)
[![飞书](https://img.shields.io/badge/%E9%A3%9E%E4%B9%A6-245BDB?style=flat)](#output-destinations)
[![钉钉](https://img.shields.io/badge/%E9%92%89%E9%92%89-0067C7?style=flat)](#output-destinations)
[![腾讯文档](https://img.shields.io/badge/%E8%85%BE%E8%AE%AF%E6%96%87%E6%A1%A3-1767B7?style=flat)](#output-destinations)
[![Obsidian（本地）](https://img.shields.io/badge/Obsidian%EF%BC%88%E6%9C%AC%E5%9C%B0%EF%BC%89-6D3BC2?style=flat&logo=obsidian&logoColor=white)](#output-destinations)

[English](../../README.md) · [简体中文](README_zh.md) · [日本語](README_ja.md) · [한국어](README_ko.md) · [Español](README_es.md) · [Français](README_fr.md) · [Deutsch](README_de.md) · [Português](README_pt.md) · [Русский](README_ru.md) · [العربية](README_ar.md)

**[下载 v3.1.0 技能 ZIP](https://github.com/ShawnRen57/omni-learning-anything/releases/download/v3.1.0/omni-learning-anything-skill-v3.1.0.zip)**

[skills.sh](https://skills.sh/shawnren57/omni-learning-anything/omni-learning-anything) · [安装渠道说明](../../docs/distribution-channels.md)

</div>

**选一门大学名课，或带上自己的书与论文。按你的节奏学习，用轻量自测、反馈与复习巩固理解，保存到本地或云文档。**

把“我想学……”变成走得下去的学习计划。你可以从 32 条有原课来源的高校及 AI 机构学习路径开始，也可以提出自己的目标、上传个人材料。先确认计划，再开始每日学习。

发一句 **“我想学清华中国建筑史”** 或 **“我想学 OpenAI Applied AI Foundations”** 就能开始。Agent 会识别原课程，复用你已提供的信息，只补问影响学习计划的必要细节。

<a href="../../examples/README.md"><img src="../../docs/assets/learning-sample-gallery.png" alt="六种语言的 15 页真实学习样张" width="100%"></a>

## v3.1.0 带来了什么

- **新增 20 条学习路径。** 看古建筑、赏昆曲、读唐诗宋词，也可以学艺术史、经济学和气候科学。从高校、OpenAI Academy 和 Anthropic 的课程建立 AI 素养，或用 Hugging Face 的课程动手写 Agent。
- **适合自己的节奏：** 保留原课程单元顺序与来源映射，再按你的可用时间拆分学习任务。
- **真实多语言样例：** 预览六种语言、六个领域的 PDF 与 HTML 学习计划和首日学习指南。
- **更容易迈出第一步：** 安装完成或首次使用时，如果你还没选题，宿主 Agent 可在当前聊天中介绍课程选项；技能不能自行新建聊天。

<a id="university-courses"></a>
## 选择内置课程

告诉 Agent：**“展示内置课程”**。选课程、学习语言与可用时间，Agent 会先提交带原课程映射的计划。这些是依据公开课程来源编排的独立学习路径，不打包完整授课内容，不代表大学背书，也不提供大学证书。

[查看全部 32 条学习路径和来源说明](../../docs/course-catalog-sources.md)。下表列出首版收录的 12 条路径。

| 大学 | 课程与原名 | 来源版本 |
| --- | --- | --- |
| Harvard | [积极心理学 / Positive Psychology](https://ppc.sas.upenn.edu/sites/default/files/ppsyllabusschachar.pdf) | PSY 1504 · 2006年春季 · Tal Ben-Shahar |
| Harvard | [计算机科学导论 / CS50x: Introduction to Computer Science](https://cs50.harvard.edu/x/2026/syllabus/) | CS50x · 2026 · David Malan |
| Harvard | [公正 / Justice](https://sandel.scholars.harvard.edu/justice) | 24 讲公开系列 · Michael Sandel |
| Yale | [心理学导论 / Introduction to Psychology](https://oyc.yale.edu/introduction-psychology/psyc-110) | PSYC 110 · 2007年春季 · Paul Bloom |
| Yale | [金融市场 / Financial Markets](https://oyc.yale.edu/economics/econ-252) | ECON 252 · 2011年春季 · Robert Shiller |
| Yale | [博弈论 / Game Theory](https://oyc.yale.edu/economics/econ-159) | ECON 159 · 2007年秋季 · Ben Polak |
| Yale | [死亡 / Death](https://oyc.yale.edu/death/phil-176) | PHIL 176 · 2007年春季 · Shelly Kagan |
| Yale | [聆听音乐 / Listening to Music](https://oyc.yale.edu/music/musi-112) | MUSI 112 · 2008年秋季 · Craig Wright |
| MIT | [计算机科学与 Python 编程导论 / Introduction to Computer Science and Programming in Python](https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/) | 6.0001 · 2016年秋季 |
| MIT | [线性代数 / Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/) | 18.06 · 2010年春季 · Gilbert Strang |
| MIT | [经典力学 / Classical Mechanics](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/) | 8.01SC · 2016年秋季 |
| Stanford | [机器学习 / Machine Learning](https://cs229.stanford.edu/syllabus-autumn2018.html) | CS229 · 2018年秋季 |

每天 10 分钟意味着完成一个小学习步骤，并不等于学完原课程的一整讲或整门课。原始学习量会明确标示，长篇阅读、习题和项目需要另留时间；来源内容与可访问性也可能变化。

## 用自己的材料学习

支持 PDF、TXT、Markdown、HTML、DOCX、EPUB、PPTX、SRT 和 VTT。可指定章节、页码或时间戳，并决定是否允许外部补充。讲解与自测会追溯到选定的原文位置。旧版 DOC、RTF 需先通过可信工具转换。

想法模糊也能开始，比如“我想懂一点经济学”。Agent 会提出可选方向，说明假设，只追问会影响课程的问题；目标清楚时则直接进入计划。

<a id="choose-your-learning-language"></a>
## 选择学习语言

**English · 简体中文 · 日本語 · 한국어 · Español · Français · Deutsch · Português · Русский · العربية**

学习计划与课程正文支持上述十种语言，可与原始材料或本页语言不同。阿拉伯语文档使用从右向左的排版。

<a id="output-destinations"></a>
## 选择课程保存位置

| 保存位置 | 使用方式 |
| --- | --- |
| PDF · HTML · DOCX · Markdown | 指定课程文件夹与 PDF、HTML、DOCX 或 Markdown 格式。HTML 把配图保存在同一个离线文件中，外部来源链接需联网。 |
| Notion | 通过官方 `ntn` CLI 连接父页面。 |
| Obsidian | 指定现有本地 Vault 与课程子目录，不调用 Obsidian API。 |
| Feishu / 飞书 | 通过官方 `lark` CLI 和用户授权连接文档文件夹。 |
| DingTalk / 钉钉 | 通过官方 `dws` CLI 连接文件夹，可能需要组织管理员批准。 |
| Tencent Docs / 腾讯文档 | 指定根目录或文件夹，通过官方 OAuth/MCP 完成授权。 |

告诉 Agent 想存在哪里，它会检查已有访问权限、引导补齐配置，并复用已命名的连接。请不要在聊天中粘贴密码或令牌。

<a id="quick-start"></a>
## 安装与开始

请 Agent 安装最新版本，并确认当前客户端能发现和使用技能。升级时保留已有课程与连接。已安装 Node.js 时可运行：

```sh
npx skills@latest add ShawnRen57/omni-learning-anything --skill omni-learning-anything -g
```

在 Claude Code 中使用插件安装器：

```text
/plugin install omni-learning-anything --marketplace ShawnRen57/omni-learning-anything
```

没有 Node.js，也可下载上方 ZIP，通过客户端技能上传或请 Agent 协助安装。`skills.sh` 已上线；SkillHub 当前上架版本为 v2.6.0。各渠道可用版本请查看渠道说明。

## 试着开始第一门课

```text
展示内置课程。以哈佛 CS50x 2026 为来源。
我是初学者，用中文教我，每天 20 分钟。
保留原单元顺序，标明原始学习量。
保存为课程文件夹中的离线 HTML，先让我确认计划。
```

也可以说：“用每天 15 分钟带我读这本 EPUB 的前两章”，或“用耶鲁《金融市场》2011 版帮我理解金融机构”。

确认计划后，请 Agent 开始第一课。回来时说“从最早未交付的一课继续”，需要时可暂停。只有宿主支持定时、且你确认时间与时区后才能安排自动执行；约定时间开始生成，完成检索与检查后交付。

## 轻量自测、反馈与复习

想检查理解时，可要 1–3 道卡片或纯文字小题，获得基于来源的反馈与提示；想做长测验也可以主动提出。作答会在后台形成学习记录，不让记录流程打断阅读。

问“今天该复习什么”，可在已有时间预算内安排少量复习；问“这周的回答说明了什么”，可看到有依据的回顾。你能纠正判断、跳过主题，或优先学新课。复习不会额外创建自动测验或计时任务。

未来课程的调整先由你确认，再开启新版本；原计划与历史仍可查阅。还可按需单向导出 Anki CSV 卡片，不自动双向同步。

<a id="examples"></a>
## 六种语言的真实样例

上方拼图展示了 15 页真实学习样张。下面六组大学课程样例各含一份局部六天学习计划和一份可独立阅读的首日材料，提供 PDF 和离线 HTML。

| 语言 | 样例主题 |
| --- | --- |
| 中文 | 哈佛积极心理学 |
| 英语 | 哈佛 CS50 |
| 日语 | MIT 线性代数 |
| 法语 | 耶鲁聆听音乐 |
| 西班牙语 | 耶鲁金融市场 |
| 阿拉伯语 | 耶鲁死亡 |

[打开大学课程目录与样例文件](../../examples/university/README.md)

早期 PDF 样例继续保留：

[科技](../../examples/technology/) · [经济学](../../examples/economics/) · [音乐](../../examples/music/) · [Agent 产品](../../examples/agent-product/) · [建筑史](../../examples/architecture/) · [明朝历史](../../examples/ming-history/)

<a id="versions"></a>
## 版本指南

| 版本 | 对学习的帮助 |
| --- | --- |
| **v3.0.0** | 直接选择大学课程路径，核对来源版本，预览真实多语言学习文档。 |
| **v2.3–v2.6** | 按需轻量自测、使用个人材料、复习薄弱点，并更方便地安装与升级。 |
| **v2** | 十种学习语言、四种本地格式，或把课程保存在连接的文档平台中。 |
| **v1** | 先确认个人学习计划，再获取含配图、练习与延伸阅读的 PDF 课程。 |

## 使用指南与运行条件

[安装与升级](../../skills/omni-learning-anything/references/install.md) · [格式与字体](../../skills/omni-learning-anything/references/setup.md) · [连接文档平台](../../skills/omni-learning-anything/references/onboarding.md) · [分发渠道状态](../../docs/distribution-channels.md) · [v3.1.0 版本验证](../../docs/release-validation-v3.1.0.md)

这是一个 Agent Skill，使用宿主提供的检索、文档与定时工具。仅 PDF 需要 XeLaTeX。云端访问、跨设备同步与无人值守交付取决于宿主、账号和授权条件；会检查当前客户端能力，不承诺所有平台通用。

[MIT](../../LICENSE) · [Changelog](../../CHANGELOG.md) · [Attribution](../../ATTRIBUTION.md)
