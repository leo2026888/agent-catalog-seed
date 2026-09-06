# 本地只读目录查询

2026-09-06 本地最小版，作者 Leo and contributors，AI 辅助实现与整理。代码采用 MIT，本文采用 CC BY 4.0；第三方名称及材料仍按各自权利处理。

此模块让智能体用三个操作查询本项目的21条公开记录。已用本地测试客户端完成 MCP stdio 初始化握手、工具发现及三种工具调用。**WorkBuddy、豆包、千问、Codex 的实际导入与调用均未验证。** 本地协议检查不等于候选插件运行评测，也不等于完整 MCP 一致性认证。v0.3.0-seed已发布扩充目录源代码，发布不代表客户端接入完成。

## 可用操作

| 工具 | 参数 | 返回 |
| --- | --- | --- |
| `search` | 必填 `query`，可选 `limit`，默认5、范围1–10 | 命中条目、匹配词、版本、来源、许可、证据等级及未测试状态 |
| `evidence_detail` | 必填 `id`，使用搜索返回的标识 | 原始公开证据记录，加上明确区分的9月6日来源检查点 |
| `installation_guide` | 必填 `id` | 阅读步骤、作者链接、许可与权限边界；没有自动安装命令 |

所有参数对象拒绝未声明字段，不接受自定义来源、文件路径、执行命令或令牌。工具仅查询固定本地文件；不联网，不下载或运行候选，不取得第三方账户权限。名称中的“安装指引”表示说明文字，不表示已完成安装。

## 本地运行

使用已有 Python 3.10 或以上，无第三方依赖。从仓库目录运行：

```bash
python3 -B scripts/catalog_query.py search '找一个帮我审阅口播视频、检查字幕的工具'
python3 -B scripts/catalog_query.py search '火星温室灌溉控制'
python3 -B scripts/catalog_query.py evidence_detail anthropic-pdf-skill
python3 -B scripts/catalog_query.py installation_guide anthropic-pdf-skill
```

`-B` 禁止 Python 写入字节码缓存。正常结果输出 JSON，成功时退出码为0；空查询、未知标识等输入错误返回 JSON 错误并以2退出。

MCP 客户端应启动以下子进程，通过 stdin/stdout 交换消息：

```bash
python3 -B scripts/catalog_mcp.py
```

客户端需要的通用配置值为：传输 `stdio`、可执行文件为本机 Python、参数为 `-B` 和 `scripts/catalog_mcp.py` 的实际绝对路径。程序按自身所在仓库定位数据，不依赖客户端工作目录。不同客户端的配置字段和 Python 查找方式尚未实测；本仓库没有代写任何客户端配置。

## 证据与结果

固定基线来自 [`public-directory-2026-09-05.json`](../evidence/public-directory-2026-09-05.json)，今天的新收录及复核来自 [`daily-catalog-batch-2026-09-06.json`](../evidence/daily-catalog-batch-2026-09-06.json)，必要元数据检查点来自 [`source-checks-2026-09-06.json`](../evidence/source-checks-2026-09-06.json)。查询时不重新读取上游；自有 Skill 保留9月5日静态校验日期，不虚构今天的来源重查。

| 标识 | 当前记录 | 保留的限制 |
| --- | --- | --- |
| `narrated-video-review` | 公开适配 Skill 0.1.0 | 关联作者成果，静态校验，未独立实际剪辑或逐宿主验证 |
| `github-mcp-server` | Registry 与发布标签 1.12.0 | 需认证，未连接、安装或运行测试 |
| `filesystem-mcp-server` | 固定源码清单版本0.6.3 | npm最新发行未知、文件级许可待核对、历史 Registry 查询名未确认注册 |
| `anthropic-pdf-skill` | 作者 Anthropic，独立版本 `null` | 专有许可，未取得再分发授权，只提供原创简介及作者链接 |
| `playwright-mcp` | Microsoft Playwright MCP v0.0.80 | Apache-2.0元数据声明；浏览器、网络、文件及可选权限需限定；未安装或运行 |

`null` 表示未知，不等于零分或已通过。21条记录的候选实际运行、独立效果复核与安全认证均没有完成。16条扩充候选的公开资料评分只衡量公开元数据和社区协作字段，不是任务效果分。根仓库 `entries/` 的合成示例不参与此真实目录检索。

检索采用有限的中文／英文关键词匹配，并按匹配词数量排序；它没有语义模型、向量检索或任务效果排名。重叠任务可能返回多个候选，通用词也可能产生误匹配。无匹配仅描述这21条记录的覆盖范围。搜索词最多512字符，工具单条输入消息最多64 KiB。

本地已验证的示例：

| 输入 | 实际结果摘要 |
| --- | --- |
| `search`，`query="找一个帮我审阅口播视频、检查字幕的工具"` | 命中 `narrated-video-review`；保留 MIT、版本0.1.0、来源链接、`runtime_tested=false` |
| `search`，`query="火星温室灌溉控制"` | `results=[]`，`status="no_match_in_local_catalog"` |
| `evidence_detail`，`id="anthropic-pdf-skill"` | `author="Anthropic"`，版本 `null`，`redistribution_authorization="not_obtained"` |
| `installation_guide`，同一PDF标识 | `guide_status="source_reference_only"`，`commands=[]`，`installation_performed=false` |
| 空白查询或未知标识 | 返回 `isError=true` 的工具错误，保留机器可读错误码 |
| 附加 `url`、`path`、`install` 等未声明参数 | JSON-RPC 参数错误 `-32602` |

## MCP 协议范围

本地适配器支持 `2025-11-25` 协议版本。客户端先发送 `initialize`，接受服务端返回的版本后发送 `notifications/initialized`，再使用 `tools/list` 与 `tools/call`；亦支持初始化后的 `ping`。如客户端不支持返回的版本，应断开连接。关闭 stdin 后进程退出。

消息采用 UTF-8 的逐行 JSON-RPC，stdout 只输出协议消息；工具结果位于 `result.content[0].text`，其中是可解析的 JSON 字符串。通知不产生响应。没有 HTTP 端口、OAuth、资源接口、提示词接口、服务端主动请求、分页或列表变化通知。工具集固定三项，`listChanged=false`。

本次参考三份官方规范（核对日期2026-09-06）：[生命周期](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)、[传输](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)、[工具](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)。这三份资料用于实现自己的目录适配器，没有引入任何候选插件或 SDK。

## 核对与维护

```bash
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate.py
```

新增17项测试覆盖中文任务、无匹配、受限许可、未知版本、错误参数、协议初始化顺序、真实子进程往返、消息过大和解析失败后的恢复。它们验证目录自身行为；第三方插件继续保持“未实测”。协议样例、实际命令和本地验收记录单独保存于维护者的当天交付目录，未将工作区私有路径放进公开仓库。

更新来源时，先核对条目与检查点；若检查点的版本或提交与基线不一致，服务启动失败并要求人工复核，避免把旧介绍标为新版本证据。当前输入文件名固定在代码里，没有后台同步、水位推进或自动升级。修改后重新检查敏感内容及摘要清单，再按独立授权进行发布。
