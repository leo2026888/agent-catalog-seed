# Agent Catalog Seed

**跨平台、按任务和版本提供可复核证据的插件目录。** 这是早期提案，中文优先，英文摘要见下方。工作名 `agent-catalog-seed` 尚未确定为品牌或注册商标。

这里探索一个可追溯的公共入口：让使用者找到适合任务的能力，看清来源、权限、已知局限和可复核证据；让创作者展示自己有权公开的产品、文章与研发经验。

**当前版本：v0.1.0-seed 开源首版内容。** 公开仓库：[leo2026888/agent-catalog-seed](https://github.com/leo2026888/agent-catalog-seed)。 本次新写的代码、Schema、合成示例与公开适配版 Skill 指令已声明 MIT 许可；文章与方法文档采用 CC BY 4.0，署名为 Leo and contributors，披露 AI 辅助创作与整理，具体范围见 [许可与署名](LICENSING.md)。GitHub 仓库已创建并核验为 public。私密漏洞报告已启用，入口及尚未完成的报告/通知测试见 [安全政策](SECURITY.md)。没有上线市场，没有经过独立安全认证，没有确认的平台接入伙伴，也没有真实用户评分。当前 `entries/` 条目是本项目新写的合成示例，真实工作流 Skill 单列于成果区。

## 从这里开始

| 想了解什么 | 入口 |
| --- | --- |
| 目录如何表达来源和边界 | [版本化条目 Schema](schema/entry.v0.1.0.schema.json)、[字段说明](docs/ENTRY_FORMAT.md) |
| 一个完整但尚未评测的条目 | [发布说明转检查清单：示例条目](entries/release-note-checklist-demo.json)、[合成材料](examples/release-note-checklist/README.md) |
| 安全与效果如何分别评测 | [评测方法](docs/EVALUATION.md)、[评测报告模板](templates/evaluation-report.md) |
| 创作者成果和文章放在哪里 | [成果入口](showcase/README.md)、[本次新写文章](articles/why-evidence-before-stars.zh-CN.md) |
| Leo 的公开 Skill 如何使用 | [口播视频剪辑与复核 v0.1.0](showcase/narrated-video-review.md)、[完整 Skill](skills/narrated-video-review/SKILL.md) |
| 如何贡献、纠错、披露利益关系 | [贡献规范](CONTRIBUTING.md)、[透明治理](docs/GOVERNANCE.md) |
| 哪些内容可以复制与使用 | [来源和权利清单](SOURCES_AND_RIGHTS.md)、[许可与署名](LICENSING.md) |
| 如何持续维护 | [人工维护流程](docs/MAINTENANCE.md)、[首发检查单](docs/RELEASE_CHECKLIST.md) |

## 首批内容

- 一个 JSON Schema 和相应的静态检查脚本，用于记录版本、来源、摘要、请求权限、平台兼容状态、评测状态与权利依据。
- 一个本次新写的合成示例，包含输入、预期输出与验收边界。它不是已接入或验证有效的插件。
- 一份从 Leo 自定义剪辑方法重新编写的公开 Skill：`narrated-video-review` v0.1.0，MIT 许可，覆盖音画对应、镜头完整、字幕声音和真实文件复核。它尚未独立实测或逐平台验证，原个人文件、媒体和音色未公开。
- 一篇本次新写、AI 辅助整理的方法文章；它没有被标为创作者过去发表的文章。
- 贡献、治理、安全报告和人工发布规范。

公开 Skill 是本次授权后重新编写的通用适配版。其余历史产品、客户方案、课程、文章和个人 Skill 需要逐项确认作者、单位权利、素材许可与对外口径。**首包未复制历史原文件、截图、录音、客户数据或第三方安装插件副本。** 本地私有候选清单不属于此仓库。

## 先建立目录，再验证互通

“一次接入，多平台发现”是设计方向。目前只提供交换信息的约定，没有自动安装、平台适配器或代执行服务。平台是否可安装、是否可运行、是否在具体任务有效，分别留下证据；一个平台的结果不能直接推给另一个平台。

不把星数、付费推荐或作者自述作为安全结论。权限范围、运行风险、任务效果和社区体验分别呈现。没有证据时显示“未评测”，保留失败、时间和版本边界。

已有目录与连接能力应优先复用。[MCP Registry](https://modelcontextprotocol.io/registry/about) 提供中立元数据，把策展、社区评价和额外安全检查留给下游；这是本项目拟对接的上游来源，还未实施同步。[skills.sh](https://www.skills.sh/docs) 已有基于安装遥测的榜单与例行审计，安装热度不等于任务成功率。[Smithery](https://smithery.ai/docs/use/connect) 已提供连接和 OAuth 管理；本项目仍需用真实任务验证自己的价值。上述官方资料核对于 2026-09-05。

个人成果展示与中立评价分开标识。关联作者作品可陈列，自测必须注明关系；没有独立复核时，不发放独立认证徽章。

## 小团队商业化方向

本项目以商业化为方向，开源用于公开规则、建立信任和吸引贡献。优先验证企业与智能体落地团队是否愿为**常用插件版本变化监控、任务回归证据和团队允许清单**持续付费；公开目录与基础证据可免费，订阅、平台数据 API 与明确披露的赞助作为收入假设。当前没有已收费产品、客户或收入。

维护者的 Codex 工作区已启用每日 **09:00（Asia/Shanghai）** 的任务唤醒，范围仅为公开元数据与公开文本的初步检查，以及本地审阅草稿。该安排不执行插件、运行生产回归或自动发布；启用计划也不表示某次检查已经完成。仓库本身没有独立采集器、评测服务或 GitHub Actions 自动发布工作流。实际测试与对外发布仍须按范围人工审阅，参见 [商业与运营路线](docs/ROADMAP.md)。

## 本地核对

在仓库目录使用 Python 3.10 或以上运行：

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

检查器只读取此目录内的声明文件，不联网、不下载插件，也不执行条目内容。它检查本仓库采用的 Schema 约束、路径与摘要、必需文档、常见敏感内容模式和可疑包文件；它不构成安全审计，也不能证明没有敏感信息。人工审阅仍是首发步骤。

## English summary

Agent Catalog Seed is an early, Chinese-first proposal for a traceable cross-platform catalog of AI skills and plugins. It separates provenance, requested permissions, host compatibility, task evidence and community feedback. The seed includes a versioned entry schema, a synthetic example, an original AI-assisted article, and contribution, evaluation and governance proposals. It also includes narrated-video-review v0.1.0, a newly written MIT-licensed public adaptation of Leo's custom editing workflow; no private voice models, customer material or original personal files are distributed. This public skill has not been independently tested in an actual edit or verified across hosts.

There is no live marketplace, verified integration, independent certification or real user rating. New code, schemas and synthetic examples are licensed under MIT; documentation and articles are under CC BY 4.0, attributed to Leo and contributors with AI assistance disclosed. Exact scope is defined in LICENSING.md. The public repository is [leo2026888/agent-catalog-seed](https://github.com/leo2026888/agent-catalog-seed). Repository creation and public visibility are verified. Private vulnerability reporting is enabled and the maintainer opened its draft form; external report submission, notification delivery and response times have not been tested. Existing private work and third-party plugin copies are excluded.

A daily 09:00 Asia/Shanghai wakeup is active in the maintainer's Codex workspace for preliminary checks of public metadata/text and local review drafts only. It does not authorize plugin execution, production testing or publication. This repository contains no independent collection or evaluation service and no automated outbound publishing workflow; release decisions require human review.
