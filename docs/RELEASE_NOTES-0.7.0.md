# v0.7.0-seed 发布说明

发布日期：2026-09-10。作者：Leo and contributors，AI辅助实现与整理。本文依照本仓库文档范围采用CC BY 4.0。

本版把Agent Catalog从24条扩充为25条，并将两个公开元数据初筛条目推进到固定提交有界文档复核。

- 新收录Microsoft Learn官方远程MCP。官方文档说明它通过Streamable HTTP提供文档搜索、完整文章获取和官方代码样例搜索；公开端点无需认证且当前免费。
- Microsoft Learn托管端点未公开独立语义版本，工具与schema可能动态变化，官方仓库没有GitHub Release；固定提交bb124f19c930...只作为证据快照。托管服务适用Microsoft Learn使用条款，仓库另标示CC BY 4.0与MIT许可范围。
- AWS MCP Servers最新GitHub Release为2026.09.20260908143235；读取固定提交README前24,576/202,894字节及完整Apache-2.0许可证，补充单个服务器权限差异、AWS凭据、IAM、写入、文件和费用边界。
- Apify MCP最新GitHub Release为v0.15.5；读取固定提交README前24,576/33,362字节及完整MIT许可证，补充OAuth/Token、Actors外网抓取、任务发布、数据存储及按次或链上支付边界。
- 自有只读查询扩充到25条；17条具有有界文档证据，8条仍为元数据初筛。社区评分与第三方运行评测仍为0。

本版没有下载、安装或运行第三方候选，没有连接任何第三方账号或MCP端点，没有调用AWS、Apify或Microsoft服务，也没有复制第三方源码或软件包。公开资料评分仍不表示任务效果、安全认证、宿主兼容或真实用户满意度。
