# v0.2.0 安装与首次使用验收 / Installation and first-use validation

Date: 2026-10-09 · macOS · Skill: `omni-learning-anything`.

历史验收记录的技能名与目录按当前名称展示；安装当前包请使用 [最新版本](https://github.com/ShawnRen57/omni-learning-anything/releases/latest)。当时发布包的大小与校验和仅用于历史记录。

**结果：Codex 与 DeepSeek Harness 均通过本次安装、原生加载与首次 PDF 生成检查。** 本次仅执行 v1.0.0 规划中的第一项，检验了安装资源与首次 PDF 输出。

## 安装来源与一致性

使用公开 [v0.2.0 release](https://github.com/ShawnRen57/omni-learning-anything/releases/tag/v0.2.0) 中的 当时的 Skill ZIP，21,620 bytes。

SHA256: `634a4e5f5c4cecb9d8650971ceb41097803ce38eba2190283ba04af103c320b6`。

匿名下载与本地发布包字节一致。ZIP 顶层为 `omni-learning-anything/`；两个安装目录的全部 11 个运行文件均与公开 ZIP 一致。测试期间两个 Agent 读取的是安装目录中的技能资源，未使用开发仓库的 Skill 源码。

| 客户端 | 实测版本 | 安装目录 | 原生首次使用 |
|---|---|---|---|
| Codex CLI | 0.162.0-alpha.2 | `~/.codex/skills/omni-learning-anything/` | 显式调用 `$omni-learning-anything`，读取安装资源并执行辅助脚本 |
| DeepSeek Harness Desktop | 0.2.0-rc.2 | `~/.dsh/skills/omni-learning-anything/` | 通过原生 Skill 工具加载，由模型在桌面客户端执行辅助脚本 |

Codex 的 GitHub 安装器整仓库下载等待较长，本次停止该下载并按 README 的轻量 ZIP 方式安装。**未将 GitHub 安装器或 Skills CLI 安装路径记为通过。** 默认 Codex 用户技能目录已安装新名称技能，后续新轮次可加载；不意味着所有 Codex 版本使用同一目录。

## 环境检查与修正

- 为测试创建干净 Python 3.12.14 虚拟环境，按安装包的 requirements 安装 Pillow 12.3.0、pypdf 6.19.0、pypdfium2 5.14.0、tzdata 2026.5。
- 使用本机已有 TinyTeX XeLaTeX（TeX Live 2026）；本次没有测试从零安装 TeX。中文使用 FandolFang 仿宋回退，英文使用已有 Times New Roman；包内不分发字体。
- 发现默认 macOS `python3` 实为 3.9.6，而旧 CLI 的 doctor 会报告 Python 正常。现已加入 3.10+ 启动检查：3.9 实测明确拒绝，3.12 实测通过，doctor 报告真实版本。
- DSH 首次枚举桌面目录时出现超过一分钟的阻塞，但精确路径读写正常，后续枚举恢复。Agent 采用明确的输入文件路径完成测试。可能与 macOS 首次访问授权有关，**根因未独立确认**；本次没有修改系统权限或客户端配置。

## 首次 PDF 生成

两个 Agent 都按安装资源中的命令完成 `doctor → init → render plan → 检查 → review`。输入为已准备好的合成测试数据，五个 example.com 链接是明确标注的占位链接，插图是代码绘制的 QA 流程图；它们不冒充研究资料、教学图片或 AIGC。

| 检查 | Codex | DSH |
|---|---|---|
| 初始化、XeLaTeX 编译 | 通过 | 通过 |
| PDF 预览 | 1 页，已实际检查 | 1 页，已实际检查 |
| 链接注解与输入一致 | 5 条 | 5 条 |
| 字体嵌入、中英显示、图片 | 通过 | 通过 |
| 版式警告 | 0 | 0 |
| 状态与批准边界 | awaiting_approval；未批准，未调度 | awaiting_approval；未批准，未调度 |

最终重新核对两组 manifest 文件哈希、安装包资源哈希、review 日期及课程状态。两个课程均为 `approved_plan: null`、`schedule: null`、`lessons: {}`。PDFium 中文提取正确；pypdf 对此 CJK 字体的中文提取仍存在兼容性限制，已记录，未据此声称所有阅读器提取一致。

- [Codex 测试 PDF](../validation/installation-v0.2.0/codex/pdf/安装验收_学习计划.pdf) · [预览](../validation/installation-v0.2.0/codex/previews/plan-01.png) · [Agent 验收记录](../validation/installation-v0.2.0/codex/acceptance-report.md)
- [DSH 测试 PDF](../validation/installation-v0.2.0/dsh/pdf/安装验收_学习计划.pdf) · [预览](../validation/installation-v0.2.0/dsh/previews/plan-01.png) · [manifest](../validation/installation-v0.2.0/dsh/manifests/plan.json)

改名及 Python 检查修改后，21 项既有测试通过，Skill 元数据验证通过；24 份历史样例的 manifest、字体、链接及文字检查通过，共 55 页。历史样例未重新生成，研究日期没有改写。

## 首次使用建议

优先下载约 22 KB 的独立 Skill ZIP，完整复制到宿主的技能目录，保留 scripts、references 和 agents。先检查 Python 版本，按 setup.md 建立环境；课程目录须可写且宿主可访问。若目录枚举卡住，先核对客户端访问权限及实际文件路径，勿直接重置课程进度。

安装目录与课程数据保持分开；调用 `$omni-learning-anything` 开始学习。

## English summary and limits

Both Codex CLI and DSH Desktop loaded the freshly installed `omni-learning-anything` bundle and produced a reviewed one-page XeLaTeX PDF using synthetic fixtures. Installed files match the public release ZIP; a clean Python environment was populated from the bundled requirements. Python <3.10 is now explicitly rejected.

The tested installation route is the lightweight release ZIP, not a completed GitHub skill-installer / Skills CLI run. Existing TeX/fonts were reused. This check covers native skill loading, installed resources, helper execution, PDF output and the approval boundary. The Skill test scope is installation, workflow, course state and document output. Host scheduler reliability is outside this scope.
