# 申请付费试点：按任务与范围报价

Agent Catalog Seed 提供公开的早期目录、证据方法和贡献入口，并接受**按明确范围报价的付费试点申请**。试点面向需要持续使用 AI Skills、MCP 服务或平台插件的团队，围绕具体任务、插件版本、宿主与模型条件，记录变化、复测结果和允许使用的范围。

**[申请付费试点](https://github.com/leo2026888/agent-catalog-seed/issues/new?template=paid-pilot.yml)** · [查看公开目录与成果](../showcase/README.md) · [返回项目](../README.md)

公开网站已上线：[Agent Catalog](https://agent-catalog.sxbliuyi.chatgpt.site)。当前可通过 GitHub 提交申请、纠错与贡献证据。**GitHub Issue 的标题、正文和附件均公开**；请只提交有权公开的概述，不放凭证、客户数据、私有日志、内部链接、联系方式、采购底价或合同附件。需要保密的内容先写“需另行确认私密渠道”，双方确认渠道与处理范围后再交换。安全漏洞使用 [SECURITY.md](../SECURITY.md) 中的私密报告入口，该入口不用于商务申请。

## 可以申请哪些交付

下表是可以讨论的试点范围，不是已部署的标准套餐。实际接单与执行取决于可复现条件、权限、资源和双方确认的报价。

| 试点范围 | 可以约定的交付 | 开始前需要固定 |
| --- | --- | --- |
| 版本变化监测 | 已约定插件的版本与来源变化记录、权限声明差异、待复核事项和观察时间 | 插件清单、公开或获授权来源、基线版本、检查频率、通知条件 |
| 固定任务回归 | 版本化任务用例、完整尝试与失败记录、环境和制品摘要、结果与成本/耗时口径 | 任务与验收标准、宿主/模型版本、合成数据、运行次数、隔离方式、权限与预算 |
| 团队允许清单 | 对指定任务与环境形成“允许、受限、待补证据、不纳入”的建议清单及理由 | 团队规则、用途、版本、权限上限、复核人和复核触发条件 |

允许清单由团队负责人确认后使用；它不是产品安全证书，也不能代替平台权限控制。某个宿主或任务上的结果不自动适用于其他宿主、模型、版本或客户场景。只做文本检查的项目会标明“未运行”，不能得到运行评测结论。

## 怎样确定报价与验收

提交申请后，维护者先判断范围与可行性，再给出报价建议。**没有统一公开价格，按范围报价；提交 Issue 不构成下单、扣款或接单确认。** 暂无可引用的已成交客户、收入或 SLA，也不承诺申请必然获接受或固定响应时限。

报价前逐项确认：

- 要解决的具体任务与失败/维护问题，以及谁负责确认验收；初次公开申请只需写角色。
- 插件、版本与制品来源，宿主/平台与模型组合，是否具备合法测试与内容使用权限。
- 交付哪些报告或清单、测试哪些场景、尝试次数、人工复核范围及明确不包含的内容。
- 试点周期、变化检查频率、复测触发条件、通知方式与双方投入的时间。
- 服务费用、币种、第三方模型/API/计算成本是否包含、预算上限、付款节点与范围变更方式。
- 验收标准、失败结果如何交付、无法复现时如何处理，以及哪些成果可公开、哪些仅按约定交付。

先从少量关键任务和版本开始，复用团队已有的可公开或合成案例，减少准备成本。报告保留失败、未知项和证据缺口；付费不购买通过率、安全结论、排名、认证或删除失败记录。

## 申请到交付的步骤

1. **公开提交最小摘要。** 写团队类型、实际任务、插件版本/平台、已遇到的问题，以及愿意付费覆盖的工作范围。未知项如实标记。
2. **确认可行性与沟通边界。** 维护者判断能否承接；如确需非公开信息，先确认双方可用的私密渠道、数据权限和处理范围，不要求在 Issue 补交敏感材料。
3. **确认范围与报价。** 固定交付物、测试边界、费用、预算、验收与变更规则，双方明确接受后再开始收费工作。
4. **按约定检查或执行。** 文本初查与实际运行分别留证；运行仅限预先批准的对象、合成数据、隔离环境和权限。新增权限或外部写入必须重新确认范围。
5. **审阅结果并验收。** 交付成功、失败与未知项，关联版本、平台、时间与完整样本；由双方按约定标准复核，决定结束、补测或继续维护。

本仓库**没有现成的安全认证、自动沙箱或生产评测平台**，没有既有客户案例或可承诺的服务等级。工作区每日 07:00（Asia/Shanghai）记录经营判断与计划，07:30 推进已授权的产品、内容、证据任务和预算记录；可在已授权自有公开入口完成内容检查、发布与读回。这不构成客户监测服务，不运行未知插件，不公开内部材料；具体插件测试仍须约定对象、权限与预算。新日程尚未完成首轮验收，不能作为服务时效或交付结果的证明。试点执行遵循 [评测方法](EVALUATION.md)、[安全政策](../SECURITY.md)与[治理规则](GOVERNANCE.md)。

## 不需要付费也可以改进目录

- **[提交事实纠错](https://github.com/leo2026888/agent-catalog-seed/issues/new?template=correction.yml)**：指出条目/文件、具体陈述、当前版本和可公开依据。
- **[贡献评测或观察证据](https://github.com/leo2026888/agent-catalog-seed/issues/new?template=evidence.yml)**：写清来源、任务、版本、平台、日期、完整样本和利益关系，未运行则标明。
- **[补充目录提案](https://github.com/leo2026888/agent-catalog-seed/issues/new?template=catalog-change.md)**：保留原有入口；真实 Skill 和第三方条目先经人工审阅，当前 Schema 仍只接受本地合成示例。

是否购买试点不影响事实纠错和证据的审阅标准。外部材料、评测报告和社区观察必须有可公开权利依据；仓库的 MIT/CC BY 4.0 许可不会自动为第三方内容补授权，见 [许可与署名](../LICENSING.md)及[贡献规范](../CONTRIBUTING.md)。

## English summary

Apply for a paid pilot scoped to specific tasks, artifact versions, hosts and models. Possible deliverables are version-change records, task regression evidence and a team-reviewed allowlist. Pricing, third-party costs, execution permissions, acceptance criteria and publication rights are agreed before work starts; an issue is neither an order nor acceptance of a project.

GitHub issues are public. Submit only a non-sensitive summary, with no credentials, customer data, private logs, contact details or confidential commercial terms. The project has no established certification, automatic sandbox, customer track record or response SLA. The active workspace schedule plans at 07:00 Asia/Shanghai and advances authorized work with budget/outcome records at 07:30; it may publish checked content to approved owner-controlled destinations. It is not a client monitoring service, does not run unknown plugins or publish internal data, and has not yet passed its first complete-run acceptance. Corrections and evidence contributions remain open regardless of paid participation.
