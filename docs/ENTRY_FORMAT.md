# 条目格式 0.1.0

Schema 位于 [`schema/entry.v0.1.0.schema.json`](../schema/entry.v0.1.0.schema.json)。`urn:agent-catalog-seed:*` 只是本提案的命名空间，不代表已注册标准。`schema_version` 与文件版本一致；`source.revision` 是本地材料的人工版本标签，不冒充 Git commit 或上游发布证明。

本版只接收本次新写的合成、不可安装、未评测示例。`kind` 预留 `skill`、`mcp-server`、`platform-plugin`、`workflow`、`article`、`product` 六类；类型名称不会赋予运行能力。纳入真实第三方条目、实际运行权限或评测报告前，需要明确新版本迁移规则并扩展 Schema。

| 字段 | 含义与本版限制 |
| --- | --- |
| `id`、`name`、`summary` | 稳定提案标识、名称与简述；不得声称合作、安全认证或未证实效果 |
| `installable` | 固定 `false`，没有安装或执行入口 |
| `provenance` | 固定 AI 辅助原创合成来源，附文字说明；不证明版权归属 |
| `source` | `local`，人工版本标签，以及每个材料的仓库相对路径、实际 SHA-256 |
| `requested_permissions` | 读写范围、网络请求和数据目的地显式列出；本版均为空或 `false`，因为材料不可执行 |
| `compatibility` | 主机记录固定 `unknown`，无测试证据；列出主机不等于兼容或接入 |
| `evaluation` | 固定 `not_evaluated`，无独立评审、无证据或评分；期望输出不能充当实测输出 |
| `conflicts` | 明示维护者参与创作及利益相关关系 |
| `rights` | 固定 `MIT`、`declared`，指向来源权利清单；本次合成条目及材料已声明 MIT 许可，范围见 [许可与署名](../LICENSING.md)。许可声明不代表安全、效果或独立权利审查 |

## 校验器范围

从仓库根目录运行 `python3 scripts/validate.py`。仅用 Python 3.10+ 标准库，不联网、不安装包、不执行条目材料。

它先检查 Schema 自身，再递归检查条目。本仓库采用且实现的 JSON Schema 子集为：注释/标识键 `$schema`、`$id`、`title`、`description`；单个 `type`（object、array、string、integer、number、boolean、null）；`properties`、`required`、固定为 `false` 的 `additionalProperties`；`items`、`minItems`、`maxItems`、`uniqueItems`；`minLength`、`maxLength`、`pattern`；`enum`、`const`。未知 Schema 关键字、重复 JSON 键、非有限数值和数据对象中的未知字段均拒绝。正则由 Python `re` 实现；仅使用本 Schema 中与常见 JSON Schema 实现一致的简单表达式。本脚本不是完整 JSON Schema 引擎，不支持 `$ref`、组合、条件、格式验证或类型数组，不会静默忽略它们。

额外静态检查包括：重复条目 ID；同一条目重复材料路径；拒绝绝对路径、反斜线、冒号、空段、`.`、`..`、符号链接、被排除的 Git/缓存目录和超出仓库的目标；确认材料是文件并核对 SHA-256；确认权利清单与必需文档存在。路径采用 `/` 分隔且大小写与实际文件一致。被引用文件的摘要只能证明字节一致，不能证明作者身份、无恶意或版权。

检查器遍历仓库所有文件（包括隐藏文件），排除 `.git`、`__pycache__`、`.pytest_cache`、`.mypy_cache`，拒绝其他未知隐藏文件、常见密钥/数据库/归档/媒体扩展名和非 UTF-8 文件；再筛查常见邮箱、手机号、本机私有目录、私钥头与部分凭证模式。测试中的模拟敏感值在运行时拼接，避免把真实凭证或完整模拟凭证放进源码。报错仅显示相对文件名与问题类型，不输出命中值。

若存在 `SHA256SUMS.txt`，还检查其条目、路径和摘要，要求覆盖除清单自身与排除目录外的全部包文件。生成归档前必须重新生成清单；此清单不能作为签名或发布者身份证明。

有限正则会漏报，也可能误报；脚本不做 OCR、语义隐私判断、依赖漏洞检查、沙箱执行或恶意行为证明。人工检查正文、来源权利、图像、链接、许可和发布归属仍不可省略。校验通过只表示本地静态检查通过，不能标记为“安全”“有效”“已发布”。
