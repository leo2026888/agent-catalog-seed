# Agent Catalog Seed

**给你的智能体，找对插件。按要完成的任务查找和比较 Skill 与 MCP 插件，看用途、版本、权限和核查记录，再决定是否尝试。** 这是早期公开目录与付费试点入口，中文优先，英文摘要见下方。工作名 `agent-catalog-seed` 尚未确定为品牌或注册商标。

网站帮助使用者按任务发现插件；GitHub 公开目录、核查记录、评测方法和后续实际评测结果，并保存许可允许再分发的 Skill。第三方按各自许可处理，受限材料只保留原创介绍与来源。只有实际评测完成后，才给出适用于相应任务、版本和平台的推荐依据。

当前可用：**1 个公开 Skill、3 条第三方资料初查**。任务入口为口播视频审阅、GitHub 仓库操作、文件处理、PDF 处理。完整运行评测、自动安装与团队持续服务仍在验证，目标是逐步建设可信插件市场。

**当前版本：v0.1.2-seed 按任务发现插件与来源说明。** 公开仓库：[leo2026888/agent-catalog-seed](https://github.com/leo2026888/agent-catalog-seed)。 本次新写的代码、Schema、合成示例与公开适配版 Skill 指令已声明 MIT 许可；文章与方法文档采用 CC BY 4.0，署名为 Leo and contributors，披露 AI 辅助创作与整理，具体范围见 [许可与署名](LICENSING.md)。GitHub 仓库已创建并核验为 public。私密漏洞报告已启用，入口及尚未完成的报告/通知测试见 [安全政策](SECURITY.md)。没有交易结算或自动评测平台，没有经过独立安全认证，没有确认的平台接入伙伴，也没有真实用户评分。当前 `entries/` 条目是本项目新写的合成示例，真实工作流 Skill 单列于成果区。第三方公开来源观察单独记录在 `evidence/`，不改写为已运行或已通过独立评测的条目。

**[查看现有插件](https://agent-catalog.sxbliuyi.chatgpt.site/#directory)** · **[提交插件需求](https://github.com/leo2026888/agent-catalog-seed/issues/new?template=plugin-request.yml)** · **[申请付费试点 · 按范围报价](https://github.com/leo2026888/agent-catalog-seed/issues/new?template=paid-pilot.yml)** · [试点交付与流程](docs/PILOT.md) · [提交纠错](https://github.com/leo2026888/agent-catalog-seed/issues/new?template=correction.yml) · [贡献证据](https://github.com/leo2026888/agent-catalog-seed/issues/new?template=evidence.yml)

公开网站已上线：[Agent Catalog](https://agent-catalog.sxbliuyi.chatgpt.site)。当前可通过 GitHub 浏览公开目录、阅读方法和提交申请。Issue 的标题、正文和附件均公开；只写可公开的任务摘要，不填凭证、客户数据、私有日志、内部链接、联系方式或敏感商业信息。安全漏洞请使用 [私密报告入口](SECURITY.md)。

**PDF 条目说明：** Anthropic PDF Skill 的作者是 Anthropic，不是 Leo。“专有许可”是作者的许可类别，不代表本站取得专项授权。未取得再分发授权，本项目不提供该 Skill 副本；查看与使用请遵循作者条款。

## 从这里开始

| 想了解什么 | 入口 |
| --- | --- |
| 团队需要监测、回归或允许清单 | [付费试点说明](docs/PILOT.md)、[按范围申请报价](https://github.com/leo2026888/agent-catalog-seed/issues/new?template=paid-pilot.yml) |
| 查看第三方公开来源观察 | [来源观察与边界](evidence/README.md) |
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

## 申请付费试点

公开目录与基础方法可以直接阅读、纠错和贡献。团队可申请**版本变化监测、固定任务回归证据或团队允许清单**的付费试点，围绕具体任务、插件版本、平台/宿主与模型条件确认范围，再给出报价。价格、第三方成本、预算上限、执行权限、交付物和验收标准在开始前明确；提交申请不构成下单或接单确认。

这是早期按范围承接的试点申请入口。目前没有现成安全认证、自动沙箱、生产评测平台、既有客户案例或可承诺的 SLA，也没有已验证成交收入。付费不购买安全结论、排名或删除失败记录；是否付费不影响纠错和证据审阅标准。参见 [试点说明](docs/PILOT.md)。

维护者的 Codex 工作区已保存并启用每日双时段安排：**07:00（Asia/Shanghai）** 记录经营判断、优先级与计划，**07:30** 推进已授权的产品、内容、证据任务，并记录预算消耗和结果。在已确认的自有 GitHub 与公开平台范围内，可以完成内容检查、发布与目标端读回；不运行未知插件，不公开内部材料。仓库没有现成自动沙箱或生产评测服务。新安排尚未完成首轮执行验收，计划启用不代表任务已经完成，详见 [商业与运营路线](docs/ROADMAP.md)。

## 本地核对

在仓库目录使用 Python 3.10 或以上运行：

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

检查器只读取此目录内的声明文件，不联网、不下载插件，也不执行条目内容。它检查本仓库采用的 Schema 约束、路径与摘要、必需文档、常见敏感内容模式和可疑包文件；它不构成安全审计，也不能证明没有敏感信息。人工审阅仍是首发步骤。

## English summary

Agent Catalog Seed helps people discover and compare Skills and MCP plugins by the task they want to complete. The website shows uses, versions, permissions and review records; GitHub hosts the catalog, review methods and results, and Skills whose licenses permit redistribution. Current scope: one public Skill and three preliminary third-party source reviews. Full runtime evaluation, automatic installation and ongoing team service remain under validation. It separates provenance, requested permissions, host compatibility, task evidence and community feedback. The seed includes a versioned entry schema, a synthetic example, an original AI-assisted article, and contribution, evaluation and governance proposals. It also includes narrated-video-review v0.1.0, a newly written MIT-licensed public adaptation of Leo's custom editing workflow; no private voice models, customer material or original personal files are distributed. This public skill has not been independently tested in an actual edit or verified across hosts.

There is no transaction platform, automated evaluation platform, verified integration, independent certification or real user rating. New code, schemas and synthetic examples are licensed under MIT; documentation and articles are under CC BY 4.0, attributed to Leo and contributors with AI assistance disclosed. Exact scope is defined in LICENSING.md. The public repository is [leo2026888/agent-catalog-seed](https://github.com/leo2026888/agent-catalog-seed). Repository creation and public visibility are verified. Private vulnerability reporting is enabled and the maintainer opened its draft form; external report submission, notification delivery and response times have not been tested. Existing private work and third-party plugin copies are excluded.

The maintainer's active Codex workspace schedule records business priorities and a plan at 07:00 Asia/Shanghai, then advances authorized product, content and evidence work at 07:30 and records budget use and outcomes. Checked content may be published to authorized, owner-controlled GitHub and public-platform destinations with target-side readback. Unknown plugins are not run and internal material is not published. The new schedule has not yet passed its first complete-run acceptance; activation is not proof of execution.

Paid pilots are open for scope-based quotes covering version monitoring, task regression evidence and team-reviewed allowlists. Apply through the [public pilot form](https://github.com/leo2026888/agent-catalog-seed/issues/new?template=paid-pilot.yml) with a non-sensitive summary only; GitHub issue titles, bodies and attachments are public. Scope, price, third-party costs, permissions and acceptance criteria are agreed before work begins. There is no established certification, automatic sandbox, customer track record or service SLA. The [public website](https://agent-catalog.sxbliuyi.chatgpt.site) is live. Corrections and evidence submissions do not require paid participation.

Anthropic PDF Skill is authored by Anthropic, not Leo. Proprietary describes the author’s terms; it does not mean this project has received special permission. No redistribution authorization has been obtained, and this repository does not provide a copy of that Skill. Refer to the author’s terms when viewing or using it.
