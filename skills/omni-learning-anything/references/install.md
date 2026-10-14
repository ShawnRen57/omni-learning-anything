# Install / 安装

## A. 通用快捷安装 / Install through chat

把下面的指令发送到 Agent 对话框：

```text
请安装 omni-learning-anything：
https://github.com/ShawnRen57/omni-learning-anything
请优先下载 Releases 最新的轻量 Skill ZIP，按当前 Agent 的原生技能安装方式安装，
保留 SKILL.md、scripts、references、agents。安装后确认技能可发现，并告诉我如何开始使用。
```

The agent should obtain the latest skill ZIP, use its host's native skill installation mechanism and verify discovery. Read `platforms.md` for host scheduling only after a learning plan is approved. If installation requires a user-operated upload dialog, provide the downloaded ZIP and the precise steps below. Do not replace installation with pasting SKILL.md into an ordinary conversation.

## B. 手动安装 / Manual installation

先从 [Releases](https://github.com/ShawnRen57/omni-learning-anything/releases/latest) 下载 Skill ZIP。解压后的顶层目录为 `omni-learning-anything/`。需要文件夹安装时，复制整个文件夹；需要上传时，选择原 ZIP。以下按 2026-10-09 官方文档或官方客户端界面核对。

### Codex

将解压后的文件夹放入 `~/.agents/skills/omni-learning-anything/`，或项目的 `.agents/skills/omni-learning-anything/`。确认该目录中直接存在 SKILL.md。Codex 会检测新技能；未出现时重启。使用 `$omni-learning-anything` 调用。

Copy the extracted folder into the user or project `.agents/skills` directory. Verify discovery and invoke `$omni-learning-anything`.

依据：[官方 Skills 文档](https://learn.chatgpt.com/docs/build-skills)，其中也支持通过 `$skill-installer` 从 GitHub 安装。

### WorkBuddy

左侧 **专家 · 技能 · 连接器 → 技能 → 添加技能 → 上传技能**，拖入 ZIP 或点 **选择文件**。导入完成后在已安装列表启用。

Open **Experts / Skills / Connectors → Skills → Add skill → Upload skill**, select the ZIP and enable the imported skill.

依据：[官方技能说明](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)，并在官方桌面端 5.7.6 核对了“添加技能 → 上传技能”和包格式要求。

### DeepSeek Harness

解压 ZIP，把整个文件夹复制到 `~/.dsh/skills/omni-learning-anything/`，或项目 `.dsh/skills/omni-learning-anything/`。自定义 DSH_HOME 时使用其 `skills/` 子目录。确认技能目录出现 `omni-learning-anything`。

Copy the bundle into the configured user/project DSH skill root. The filesystem provider discovers a folder with SKILL.md one level below that root.

**插件 → 添加插件**安装的是有 package.json 和组合包 patch 的 DSH 插件；当前包按原生文件系统 Skill 方式安装，不能把 Skill ZIP 当作插件组合包填入该对话框。

依据：[官方文件系统 Skill provider](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md)、[官方插件安装说明](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-plugin-manager/README.zh.md)。

### OpenClaw

解压后，在终端运行（替换文件夹路径）：

```sh
openclaw skills install /path/to/omni-learning-anything --global
openclaw skills list
```

也可把完整文件夹放到 `~/.openclaw/skills/omni-learning-anything/`；仅当前工作区使用时放到工作区 `skills/` 中。

Install the local extracted folder with the native `openclaw skills install` command, then check the inventory. Use `--global` for all local agents.

依据：[官方 Skills 文档](https://docs.openclaw.ai/tools/skills)、[官方 CLI 说明](https://docs.openclaw.ai/cli/skills)。Git 仓库安装要求源根目录有 SKILL.md；本仓库的技能在 skills 子目录，因此这里采用已解压的技能文件夹。

### 豆包 / Doubao desktop work mode

左侧 **插件 · 技能 · 伙伴 → 技能 → 添加 → 上传技能**，选择 **选择文件**上传 ZIP，或 **选择文件夹**选择解压后的技能目录。导入后在技能页查看并选用。

Open **Plugins / Skills / Partners → Skills → Add → Upload skill**; choose the ZIP or extracted folder.

依据：[豆包官方客户端](https://www.doubao.com/)。2026-10-09 在官方 macOS 桌面端 2.31.4 的工作界面核对了上述入口及上传弹窗：包或文件夹须包含 SKILL.md，且其 YAML 元数据须包含技能名称和描述。该条依据是官方产品界面，不是第三方教程；普通聊天页没有该入口时，先切换到提供技能功能的工作界面。

## 安装后 / After installation

用一句学习主题开始，例如“用 omni-learning-anything 带我学习西方建筑史”。Agent 检查生成文档所需的环境并收集学习偏好；Python/XeLaTeX 设置见 `setup.md`。安装 Skill 与开始学习是两个步骤，计划确认前不创建每日任务。
