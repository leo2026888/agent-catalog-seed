# 来源与权利清单

清单覆盖此包内实际文件。详细本机路径、私有选材记录与登录检查位于仓库外，不随发布包分发。

| 范围 | 来源 | 第三方正文/素材 | 权利状态 |
| --- | --- | --- | --- |
| 根目录 Markdown 文件，包括 `README.md`、`CONTRIBUTING.md`、`SECURITY.md`、`LICENSING.md` 与本清单 | 按本次任务新写，AI 辅助创作与整理 | 仅短篇释义与官方来源链接 | CC BY 4.0；Leo and contributors，2026 |
| `docs/`、`templates/`、`showcase/`、`articles/` 与 `.github/` 下的 Markdown 模板 | 本次新写的方法、流程、入口、模板与文章，AI 辅助创作与整理 | 没有复制历史文章、客户材料或第三方长文 | CC BY 4.0；Leo and contributors，2026 |
| `schema/`、`scripts/`、`tests/`、`entries/`、`examples/`，含示例 README 与合成文本 | 本次新写，AI 辅助创作与整理；示例全部为合成内容 | 没有真实客户/账号/项目数据或安装插件副本 | MIT；Leo and contributors，2026 |
| `skills/narrated-video-review/SKILL.md`，v0.1.0 | 在本次请求授权下，依据 Leo 本地自定义剪辑工作流的通用方法重新编写，AI 辅助整理 | 未复制原个人 Skill 正文、第三方插件技能文本、专用音色、媒体、客户信息或工具实现 | MIT；Leo and contributors，2026；仅覆盖本次公开适配版指令 |
| `skills/narrated-video-review/LICENSE` | 根目录 MIT 标准许可文本的同内容副本，便于单独分发 Skill 时保留声明 | 标准许可文本 | 与根目录 LICENSE 一致；不授予实际处理素材或工具的权利 |
| `.gitignore`、`VERSION`、`SHA256SUMS.txt` 与机器配置文件 | 本次编排的仓库配置与自动生成摘要 | 没有外部服务密钥或实际账号 | MIT；Leo and contributors，2026 |
| `evidence/` 的22条目录记录和说明 | 依据公开仓库元数据、维护与社区字段、官方服务文档及首轮来源记录重新编写，AI辅助整理；精确来源URL和观察边界见各批次 | 没有复制第三方Skill正文、脚本、图片或安装包；第三方记录只保存事实字段、原创简介和官方链接 | 本项目新增摘要与编排采用CC BY 4.0；各仓库许可元数据仅描述上游声明，不由本项目重新授权第三方内容；Notion本地参考实现MIT不自动扩展到托管服务 |
| `LICENSE` | MIT 标准许可文本，仅填入本次版权署名 | 标准许可文本 | 保留正式文本；范围见 [许可与署名](LICENSING.md) |

## 可追溯的外部参考

- [GitHub 维护的 MIT 许可说明](https://choosealicense.com/licenses/mit/)：作为本次代码许可及标准文本来源，没有为历史资料补授权。
- [CC BY 4.0 官方说明](https://creativecommons.org/licenses/by/4.0/)：作为本次文档许可来源，适用范围见 [许可与署名](LICENSING.md)。
- [GitHub 私密漏洞报告配置](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)：用于渠道配置；本仓库已由 API 确认启用，维护者已打开对应草稿入口。尚未进行外部报告提交、通知送达或响应时效测试，详见 [安全政策](SECURITY.md)。
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)：作为 Schema 声明格式标识；校验脚本实现的范围见字段说明。
- [MCP Registry](https://modelcontextprotocol.io/registry/about)：用于核对批量目录字段和最新版本标识；没有连接或运行其中服务。
- GitHub公开仓库主题检索与仓库元数据：用于筛选16条高星、未归档、许可元数据明确且近期维护的候选，并保存星数、fork、watcher、issue、合并贡献、发布和推送日期等事实字段；没有复制仓库源码、README正文或软件包。
- [skills.sh](https://www.skills.sh/docs)、[Smithery Connect](https://smithery.ai/docs/use/connect)：用于 README 中区分已有基础能力和本提案范围，没有复制目录数据、执行安装或建立连接。

首轮参考核对日期为2026-09-05，批量目录元数据观察日期为2026-09-06。链接不是合作或背书；除`LICENSE`中的MIT标准许可文本，本包没有复制或再分发上述网站正文、图片或其他素材。

## 历史材料处理结论

首批收录本次新写内容及重新编写的 `narrated-video-review` 公开适配版。其来源是本次已审阅的 Leo 本地定制剪辑方法，并已获本次公开建设请求授权；原个人 Skill 文件不随包分发，特定旧项目音色和工具专有路由未纳入。该许可不外推至其他文件、媒体或第三方实现。

其余历史研发 Skill、公开分享意图的方案、产品页面和内部课程只形成仓库外的私有候选清单；“用户电脑内”“可分享版”“AI 辅助生成”“页面可见”均不足以独立证明允许全网复制。未确认材料的正文与资产不进入本包。此公开 Skill 未经独立实际剪辑评测，相关作者展示不等于安全认证或全平台兼容。
