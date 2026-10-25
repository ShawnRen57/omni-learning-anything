# Skill validation / 验收记录

测试范围：Skill 安装、资源读取、计划确认、内容与 PDF 输出、课程状态及失败恢复。宿主的定时器可靠性不纳入测试。

- 六组样例：每组完整 30 天计划与 Day01–03，共 24 份 PDF、55 页。实际来源核验日期为 2026-10-08。
- 29 项测试覆盖审批、变更后的审批失效、连续天数、交付门禁、重复执行、失败复用、暂停完成、并发锁、路径与 TeX 安全、真实 XeLaTeX 输出。
- PDF 检查包含全部页面预览、嵌入字体、图示、至少五个链接和版式警告。PDFium 用于中文提取，pypdf 用于字体与链接对象检查。
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
