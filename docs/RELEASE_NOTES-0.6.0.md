# v0.6.0-seed 发布说明

发布日期：2026-09-09。作者：Leo and contributors，AI辅助实现与整理。本文依照本仓库文档范围采用CC BY 4.0。

本版把Agent Catalog从23条扩充为24条，并将两个公开元数据初筛条目推进到固定提交有界文档复核。

- 新收录Cloudflare官方托管API MCP。官方文档说明它通过搜索OpenAPI定义并执行API请求，覆盖DNS、Workers、R2、Zero Trust等账号资源；OAuth或API Token决定实际权限。
- Cloudflare托管端点未公开独立语义版本，官方仓库没有GitHub Release；固定提交46641b2f8514...只作为证据快照。公开仓库许可证为Apache-2.0，托管服务完整条款另待复核。
- n8n-mcp仍为v2.82.1；固定提交README与MIT许可证已完整读取，补齐工作流、执行、数据表、凭据、Agents、API Key/MCP Token和只读限制配置边界。
- Firecrawl仍为v3.2.1；按单文件上限读取README前24,576/39,038字节并完整读取MIT许可证，补齐搜索、抓取、交互、监控、文件解析、OAuth/API Key和search-only端点边界；未读部分明确保留。
- 自有只读查询扩充到24条；14条具有有界文档证据，10条仍为元数据初筛。社区评分与第三方运行评测仍为0。

本版没有下载、安装或运行第三方候选，没有连接任何第三方账号、端点、工作流或Cloudflare资源，也没有复制第三方源码或软件包。公开资料评分仍不表示任务效果、安全认证、宿主兼容或真实用户满意度。
