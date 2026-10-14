# v1.0.1 名称统一验收

日期：2026-10-14。当前 Skill、GitHub 仓库与安装包统一使用 `omni-learning-anything`，显示名为 Omni Learning Anything。没有新增别名或旧名兼容入口；学习流程、语言支持与课程内容不变。

- 29项既有回归测试通过，包括真实XeLaTeX编译与失败重试。
- Skill元数据校验通过；新ZIP有12个运行资源，23,577 bytes，与源码逐文件一致。SHA256：`ef64c80cc899bed9dd7024cfb1bc94a2b886a921947df32edf57ddf0bca2cda0`。
- 原有24份样例PDF55页、六份双语验收PDF20页的归档检查通过。
- 两份合成安装验收PDF中的名称已统一，原始内容与日期保留；两页均实际目视检查，无裁切或缺字，对应manifest哈希与字体报告同步。此项不代表重新检索或新学习课程验收。
- 本机Codex、DSH、WorkBuddy、豆包和隔离OpenClaw的已安装资源目录与元数据更新；本次没有重复五个平台的完整课程运行。
- 隔离OpenClaw原生CLI显示新技能名与skillKey，eligible/modelVisible为true；新包独立解压后的doctor检查Python、XeLaTeX与目录可写性通过。
- README、安装指南、调用示例和仓库链接统一更新。历史验收说明按当前名称展示，原始核验日期及历史包校验和不改写为新版本证明。

安装当前版本：下载 [v1.0.1 Skill ZIP](https://github.com/ShawnRen57/omni-learning-anything/releases/download/v1.0.1/omni-learning-anything-skill-v1.0.1.zip)，保留完整目录，使用 `$omni-learning-anything` 开始。
