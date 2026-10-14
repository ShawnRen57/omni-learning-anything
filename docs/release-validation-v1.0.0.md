# v1.0.0 发布验收 / Release validation

验收日期：2026-10-09。保持轻量 Skill：没有新增后台服务、数据库、账号或调度器。宿主定时器可靠性及多自然日定时通知不在验收范围。

## 核心修复与回归

29 项测试全部通过，包含真实 XeLaTeX 编译。新增检查先复现失败，再修复：

- 重复批准同一计划保持暂停或完成状态；恢复课程用 resume。
- 初始化拒绝错误时间、星期、预算、语言和布尔字段；课时分项拒绝负值、错误类型或超预算。
- 已交付材料的 review 不可覆盖；续学和重复交付核验保存的 manifest 哈希及其文档哈希。
- 编译失败不生成有效 manifest、不推进进度；修复输入后重试同一天。
- 英文 Markdown 的扩展阅读与日期标签使用英文。

Skill 元数据校验通过。原有六组样例的 24 份 PDF、55 页再次通过归档哈希、字体、链接及文字校验；原始来源核验日期仍为 2026-10-08。

## 从短主题到课程

[新增验收样例](../validation/release-v1.0.0/README.md)共有六份最终 PDF、20 页：中文计划与 Day01–03，英文计划与 Day01。原有六组主题样例仍保留。

新主题为“旅行时看懂夜空”，零基础、肉眼和已有手机星图、3 天、每天 15 分钟。Codex CLI 从已安装 Skill 开始，实际追问偏好、联网搜索并打开来源、调用文生图、生成和逐页检查计划；计划交付后才接收明确的模拟批准。批准前的记录显示 awaiting_approval、无日课、无任务。图片是实际模型生成的教学示意，每课解释所关注的不同分区；提示词和来源记录随课程保存。

中文 Day01 由原生 CLI 生成、检查并通过最终回复交付。中文 Day02 在研究阶段遇到 CLI 账户额度限制；英文 Day01 已生成、检查，但 CLI 在最终回复前被同一额度限制中断。当前 Codex 桌面会话调用已安装 Skill 接续：复用英文待交付文件，完成中文 Day02–03，不改已批准或交付的归档。**这不是一条全部在 CLI 中完成的不中断运行。** 交付接续采用明确标注的模拟 QA 收件记录，不伪造外部通知成功。

中文 Day03 首次渲染还触发了本机 Times New Roman 的圈号数字缺字检查。没有有效 manifest，状态仍为 Day02 已交付；将未交付正文改为普通编号后，同一 Day03 重试通过。最终中文状态 complete，next 返回 complete，没有 Day04；英文状态 active，已记录 Day01，下次为 Day02。两组的 schedule 都为 null，mastery 都为空。

全部 20 页已在可读分辨率检查。最终六份文档各有至少五个具体、实际打开的扩展来源，嵌入 Times New Roman 与 FandolFang，版式警告为零。检查包括概念顺序、内文证据、目标匹配、练习答案、复习衔接、图示作用及选读范围。15 分钟为阅读与练习估算，未经真实学员计时；不以收到 PDF 推断掌握。英文计划一项来源的发布日期遗漏通过[独立勘误](../validation/release-v1.0.0/en/SOURCE-ERRATA.md)补充，保持已批准文件不变。

## 原生安装与执行检查

| 客户端 | 实际检查 |
|---|---|
| Codex CLI 0.162.0-alpha.2 / 当前桌面会话 | 完整包安装与资源读取；上述新主题、研究、计划批准及课程恢复 |
| DeepSeek Harness Desktop 0.2.0-rc.2 | 原生 Skill 加载 v1.0.0；读取已安装资源，执行 doctor 与依赖导入 |
| WorkBuddy 5.7.6 | 官方客户端上传 ZIP，风险检查后安装并启用；在对话中加载已安装资源并执行 doctor 与依赖导入 |
| 豆包桌面工作界面 2.31.4 | 官方客户端上传 ZIP，技能页选用进入本地电脑模式；在对话中执行已安装脚本 doctor 与依赖导入 |
| OpenClaw 2026.9.9 | 隔离状态目录内用原生 CLI 安装技能目录；info/list 显示 eligible、modelVisible、userInvocable；执行安装后的 doctor。未在隔离环境配置模型对话 |

这些是按平台分别执行的安装、发现和资源执行检查，没有将全部平台表述为完整学习课程验收。WorkBuddy 和豆包的操作依据为官方文档与官方产品界面；安装方式见 [install.md](../skills/omni-learning-anything/references/install.md)。OpenClaw 本地文件夹安装依据 [官方 CLI 文档](https://docs.openclaw.ai/cli/skills)。测试没有更改用户现有定时任务或 OpenClaw 网关。

环境：Python 3.12.14、XeLaTeX / TeX Live 2026；Pillow 12.3.0、pypdf 6.19.0、pypdfium2 5.14.0、tzdata 2026.5。当前环境没有仿宋时使用 FandolFang；安装包不附字体。公开记录隐藏本机个人路径，原始宿主日志和未交付修订稿保留于本地；归档中的已批准输入与最终材料哈希未改。

## 复核命令

```sh
python3 -m unittest discover -s tests -v
python3 tools/validate_artifacts.py
python3 tools/validate_release_samples.py
python3 tools/package_skill.py
```

使用 Python 3.10+，依赖按 setup.md 安装。第三条只检查已保存的验收产物，不会把历史检索标为新检索，也不会更新审批、交付或目视检查记录。最终发布包仅包含完整 Skill 运行资源；课程和测试数据留在仓库，不进入 ZIP。

历史 v1.0.0 包核对（名称与目录按当前名称展示）：当时的 Skill ZIP，23,607 bytes，12个运行资源文件；SHA256 `e9064bba37a4bcfa068b33fb639eb3478039baa787c6ccc74cfbd8e3fa632d46`。独立解压后执行 doctor、init、render，生成4页英文计划且仍为 awaiting_approval；Markdown英文标签通过核对。五个已安装的验收目录与最终包逐文件一致。
