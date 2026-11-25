# Skill validation / 验收记录

测试范围：Skill 安装、资源读取、计划确认、内容与 PDF 输出、课程状态及失败恢复。宿主的定时器可靠性不纳入测试。

- 六组中文样例各含一份 30 天计划和前三课，共 24 份 PDF、56 页。2026-11-25 已核对来源并逐页检查。每份都有独立的教学图、读图问题、观察依据和出处。[样例 PDF](../examples/README.md) · [逐页预览](review/)
- 同期更新的积极心理学计划与第一课各有 3 页。计划区分自评、参与意愿与场地记录，第一课让读者分别比较勾选人数和组内比例。两份 PDF 和对应的离线 HTML 均已核对配图、读图说明与来源链接。[大学课程样例](../examples/university/README.md)
- 此次更新通过了全部 302 项自动化测试，涵盖计划审批、课程状态、多语言输出及教学配图等功能。
- PDF 检查包括嵌入字体、来源链接、版式警告和读图文字。验收脚本还逐像素核对 PDF 首页内嵌图片与课程原图，并检查 24 份文件是否使用 24 张不同的图。
- [首次安装验收](installation-validation.md)：Codex CLI 与 DSH Desktop 从公开包加载资源并生成测试 PDF；使用干净 Python 环境，保留原始测试输入与输出。
- 元数据验证与独立 ZIP 解压检查确认包自包含。安装方法依据见 [install.md](../skills/omni-learning-anything/references/install.md)。

样例计划批准与交付为明确标注的模拟操作。来源真实性、教学质量及页面目视检查由执行 Agent 核对；脚本不会自动判断事实正确或学习者是否掌握。

[v1.0.0 发布验收](release-validation-v1.0.0.md)记录新增双语样例、原生安装、恢复行为与测试边界；[六份最终 PDF 索引](../validation/release-v1.0.0/README.md)。

[v1.0.1 名称统一验收](rename-validation-v1.0.1.md)。

## v2.1.0 — 2026-10-25

[官方 API 与首次连接验收](release-validation-v2.1.0.md)：105 项测试通过；Notion 官方 `ntn` 与飞书官方 `lark-cli` 的计划和 Day01 在真实账号完成 API 写入、图文与五个链接、目录及回执复用检查。Obsidian 保留本地 Vault 例外；腾讯文档、钉钉文档写入与无人值守调度仍未通过真实验收。

## Reproduce

```sh
python3 -m unittest discover -s tests -v
python3 tools/validate_artifacts.py
python3 tools/validate_release_samples.py
python3 tools/package_skill.py
```

使用 Python 3.10+，按 Skill 的 setup.md 安装依赖。集成测试需要 XeLaTeX。样例检查不改写来源核验日期。

## v0.2.1 verification — 2026-10-09

21 项测试与 Skill 元数据校验通过。独立 ZIP 解压后，实际运行 doctor、init、render；新模块与锁名称正确，计划保持待确认。样例仅更新页眉品牌，逐份核对 TeX 正文不变，并检查全部 55 页预览；manifest 与课程中的文档哈希已同步，24 份 PDF 的链接、字体及文字校验通过。WorkBuddy 5.7.6 和豆包 2.31.4 的上传入口与格式要求在官方客户端界面核对，未以第三方教程作为操作依据。
