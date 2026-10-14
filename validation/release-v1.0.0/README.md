# v1.0.0 验收样例 / Acceptance samples

从一句新主题开始，使用已安装 Skill 追问、检索并生成材料。两组为隔离模拟学员，批准与交付记录均为 QA，连续日课在同一天加速执行；没有真实定时任务。阅读时长为估算。

Six final PDFs / 20 pages: Chinese plan + Days 1–3, English plan + Day 1. Simulated learners, approvals and receipts; no live schedules. See the [release report](../../docs/release-validation-v1.0.0.md) for exact native-runtime scope and quota recovery.

| 语言 / Language | 文档 / Document | 页数 / Pages | PDF |
|---|---|---|---|
| 中文 | plan | 3 | [PDF](zh/astronomy-sample-v1/pdf/%E6%97%85%E8%A1%8C%E8%A7%82%E6%98%9F%E5%85%A5%E9%97%A8_%E5%AD%A6%E4%B9%A0%E8%AE%A1%E5%88%92.pdf) |
| 中文 | Day01 | 3 | [PDF](zh/astronomy-sample-v1/pdf/%E6%97%85%E8%A1%8C%E8%A7%82%E6%98%9F%E5%85%A5%E9%97%A8_%E6%AF%8F%E6%97%A5%E5%AD%A6%E4%B9%A0_Day01_%E8%BE%A8%E8%AE%A4%E4%BA%AE%E7%82%B9%EF%BC%9A%E6%81%92%E6%98%9F%E3%80%81%E8%A1%8C%E6%98%9F%E4%B8%8E%E6%89%8B%E6%9C%BA%E6%98%9F%E5%9B%BE.pdf) |
| 中文 | Day02 | 3 | [PDF](zh/astronomy-sample-v1/pdf/%E6%97%85%E8%A1%8C%E8%A7%82%E6%98%9F%E5%85%A5%E9%97%A8_%E6%AF%8F%E6%97%A5%E5%AD%A6%E4%B9%A0_Day02_%E7%90%86%E8%A7%A3%E6%9C%88%E7%9B%B8%EF%BC%9A%E4%B8%BA%E4%BB%80%E4%B9%88%E6%9C%88%E4%BA%AE%E4%BC%9A%E5%8F%98%E5%BD%A2.pdf) |
| 中文 | Day03 | 3 | [PDF](zh/astronomy-sample-v1/pdf/%E6%97%85%E8%A1%8C%E8%A7%82%E6%98%9F%E5%85%A5%E9%97%A8_%E6%AF%8F%E6%97%A5%E5%AD%A6%E4%B9%A0_Day03_%E5%AE%89%E6%8E%92%E8%A7%82%E6%98%9F%EF%BC%9A%E5%81%9A%E4%B8%80%E5%BC%A0%E8%82%89%E7%9C%BC%E5%87%BA%E8%A1%8C%E5%8D%A1.pdf) |
| English | plan | 4 | [PDF](en/pdf/Night%20Sky%20for%20Travelers_%E5%AD%A6%E4%B9%A0%E8%AE%A1%E5%88%92.pdf) |
| English | Day01 | 4 | [PDF](en/pdf/Night%20Sky%20for%20Travelers_%E6%AF%8F%E6%97%A5%E5%AD%A6%E4%B9%A0_Day01_Stars%20or%20Planets_%20Read%20the%20Sky%20with%20a%20Phone%20Chart.pdf) |

## 短提示词 / Short prompts

```text
请用 omni-learning-anything 带我学习天文学，旅行时想看懂夜空。
```

```text
Use omni-learning-anything to help me learn astronomy so I can understand the night sky when traveling.
```

模拟学员随后补充：零基础、主要在中国旅行、肉眼与已有手机星图、3天、每天15分钟、10:00 Asia/Shanghai、含周末、确认后开始Day01。语言分别为中文和英文；QA 明确使用 sample_mode，不注册任务。

Agent actually asked for the missing preferences. Simulated answers specified a three-day beginner course, 15 minutes per day, China travel, naked-eye and an existing phone chart, weekends, 10:00 Asia/Shanghai, and immediate Day 1 after approval.

## 过程与记录

中文计划和 Day01、英文计划和 Day01 的研究与渲染来自原生 Codex CLI。CLI 额度在中文 Day02 研究阶段、英文 Day01 最终发送前中断。当前桌面会话用已安装 Skill 完成接续，英文复用已有待交付文档；不声称 CLI 全程成功。中文最后返回 complete，英文下一课为 Day02。

Canonical inputs, final PDFs, editable sources, page previews and hash-bound review manifests are under each course. Research reports made before approval/delivery remain **phase snapshots**, not the final state. [report.json](report.json) and state.json describe the final acceptance state. Unreviewed historical iterations are preserved locally outside the published files; research/revision-summary.json identifies them. Auxiliary public records redact local personal paths; full retrieved web-page text is not redistributed.

[英文来源元数据勘误 / English source erratum](en/SOURCE-ERRATA.md) preserves the approved archive. [可复核脚本](../../tools/validate_release_samples.py) checks stored artifacts without modifying progress or claiming fresh research.

![中文 Day03 实际页面](zh/astronomy-sample-v1/previews/Day03-01.png)

![English Day01 actual page](en/previews/Day01-01.png)
