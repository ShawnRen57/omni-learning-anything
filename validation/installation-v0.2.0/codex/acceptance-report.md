# 原生安装与首次使用验收

实际结果：doctor、init、render --key plan、review 均成功；PDF 1 页已实际预览。验收范围仅为合成数据安装和首次渲染，不代表学习内容或实时调度验收。

- 技能名称：omni-learning-anything，版本 0.2.0。
- 加载入口：/Users/renxiaohan1/.codex/skills/omni-learning-anything/SKILL.md
- 已读取安装资源：references/setup.md、references/platforms.md（应用 Codex 部分）、references/content.md、references/commands.md。
- 执行入口：/Users/renxiaohan1/.codex/skills/omni-learning-anything/scripts/omni_learning.py
- 辅助检查所读取的包内模块：scripts/omni_pdf.py；未读取开发仓库技能源码。
- Python：<verification-workspace>/tmp/first-use-venv/bin/python（3.12.14），使用其已有依赖，未修改虚拟环境或安装目录。
- XeLaTeX：/Users/renxiaohan1/Library/TinyTeX/bin/universal-darwin/xelatex。
- 执行命令：doctor；--project . init --config input-config.json --plan input-plan.json；--project . render --input plan.json --key plan；--project . review --key plan --note（实际检查记录）。
- 所有产物写入当前验收目录，原始 input-config.json / input-plan.json 保留；输入为已有合成测试数据，无重新检索或新教学内容。

## PDF 检查

已检查 previews/plan-01.png 全部 1 页。中英文、标题、正文、原有测试插图、图注、五条参考链接和页码均可见，无裁切、重叠、空白页。FandolFang-Regular、TimesNewRomanPSMT、TimesNewRomanPS-BoldMT 均已嵌入。5 个 PDF Link 注释的 URL 与输入完全一致；占位链接未联网验证。

完整编译日志无 Overfull、Underfull、Missing character 或 LaTeX/Package Warning。存在 fontspec 的 CJK script 支持 Info 提示，已按提示核对中文预览正常。missfont.log 记录了 FangSong 探测，实际使用包模板支持的 FandolFang 回退。

附加兼容性发现：PDFium 中文文本提取正常；pypdf 提取中文出现误码，中文字体字典未包含 ToUnicode。此项不影响已检查的可视显示，但记录为文本提取兼容性限制。

## 状态与证据

review 已写入 manifests/plan.json。最终再次核对 manifest 所有文件哈希及原始输入哈希一致。state.json 保持 awaiting_approval，approved_plan=null、schedule=null、lessons={}。未运行 approve、未创建定时任务、未生成日课。

PDF：pdf/安装验收_学习计划.pdf
检查证据：doctor.json、init-result.json、render-result.json、review-result.json、pdf-check.json、pdf-extracted-text.txt、sources/安装验收_学习计划.log、manifests/plan.json、state.json。
