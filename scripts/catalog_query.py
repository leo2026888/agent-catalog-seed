#!/usr/bin/env python3
"""Read-only queries over this project's public Agent Catalog records (MIT)."""

import argparse
from copy import deepcopy
import json
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "evidence/public-directory-2026-09-05.json"
CHECKPOINT = "evidence/source-checks-2026-09-06.json"
BATCH = "evidence/daily-catalog-batch-2026-09-06.json"
EXPANSION = "evidence/catalog-expansion-2026-09-06.json"
DAILY = "evidence/daily-catalog-batch-2026-09-07.json"
DAILY_LATEST = "evidence/daily-catalog-batch-2026-09-08.json"
BASE_ALIASES = {
    "narrated-video-review": ("口播", "视频", "剪辑", "字幕", "镜头", "声音", "video", "narration", "caption"),
    "github-mcp-server": ("github", "仓库", "代码审查", "议题", "拉取请求", "工作流", "issue", "issues", "pr", "pull request", "repository"),
    "filesystem-mcp-server": ("文件", "文件夹", "目录", "读写", "filesystem", "file", "files", "directory"),
    "anthropic-pdf-skill": ("pdf", "合并", "拆分", "表单", "扫描件", "ocr"),
    "playwright-mcp": ("浏览器", "网页", "自动化", "可访问性", "playwright", "browser", "web automation", "accessibility"),
}


class QueryError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def normalize(value):
    return unicodedata.normalize("NFKC", value).casefold().strip()


def matches(query, term):
    if term.isascii():
        return re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", query) is not None
    return term in query


class Catalog:
    """Fixed local inputs; tool callers cannot select a path or URL."""

    def __init__(self):
        baseline = json.loads((ROOT / BASELINE).read_text(encoding="utf-8"))
        checkpoint = json.loads((ROOT / CHECKPOINT).read_text(encoding="utf-8"))
        batch = json.loads((ROOT / BATCH).read_text(encoding="utf-8"))
        expansion = json.loads((ROOT / EXPANSION).read_text(encoding="utf-8"))
        daily = json.loads((ROOT / DAILY).read_text(encoding="utf-8"))
        daily_latest = json.loads((ROOT / DAILY_LATEST).read_text(encoding="utf-8"))
        new_records = [record for record in batch["records"] if record["listing_action"] == "new_accepted_listing"]
        daily_by_id = {
            **{record["id"]: record for record in daily["records"]},
            **{record["id"]: record for record in daily_latest["records"]},
        }
        expanded_records = [daily_by_id.get(record["id"], record) for record in expansion["records"]]
        daily_new_records = [record for record in daily["records"] if record["listing_action"] == "new_accepted_listing"]
        latest_new_records = [record for record in daily_latest["records"] if record["listing_action"] == "new_accepted_listing"]
        records = baseline["records"] + new_records + expanded_records + daily_new_records + latest_new_records
        checks = checkpoint["records"]
        self.records = {record["id"]: record for record in records}
        self.checks = {record["id"]: record for record in checks}
        self.batch_checks = {record["id"]: record for record in batch["records"]}
        self.daily_checks = daily_by_id
        self.daily_ids = set(daily_by_id)
        self.latest_daily_ids = {record["id"] for record in daily_latest["records"]}
        self.expansion_ids = {record["id"] for record in expanded_records}
        self.aliases = dict(BASE_ALIASES)
        for record in expanded_records + daily_new_records + latest_new_records:
            terms = [record["task"], record["name"], record["author"], *record["task_tags"]]
            locator = record.get("repository") or record.get("service_endpoint", "")
            terms.extend(locator.replace("/", " ").split())
            self.aliases[record["id"]] = tuple(dict.fromkeys(normalize(term) for term in terms))
        self.record_origins = {
            **{record["id"]: BASELINE for record in baseline["records"]},
            **{record["id"]: BATCH for record in new_records},
            **{record["id"]: EXPANSION for record in expanded_records},
            **{record["id"]: DAILY for record in daily["records"]},
            **{record["id"]: DAILY_LATEST for record in daily_latest["records"]},
        }
        if len(self.records) != len(records) or set(self.records) != set(self.aliases):
            raise ValueError("Unexpected public catalog membership")
        if len(self.checks) != len(checks) or set(self.checks) != set(BASE_ALIASES) - {"narrated-video-review", "playwright-mcp"}:
            raise ValueError("Unexpected checkpoint membership")
        for entry_id, check in self.checks.items():
            version = self.records[entry_id]["version"]
            if check["version"] != version["value"] or check["repository_commit"] != version["repository_commit"]:
                raise ValueError("Checkpoint differs from baseline; review required")
            if check["change_status"] != "no_change_in_checked_scope":
                raise ValueError("Changed source requires reviewed catalog data")

    def evidence_detail(self, entry_id):
        if not isinstance(entry_id, str) or entry_id not in self.records:
            raise QueryError("unknown_entry", "未找到该目录标识；请先检索并使用返回的 id。")
        record = deepcopy(self.records[entry_id])
        record["record_origin"] = self.record_origins[entry_id]
        record["source_check"] = deepcopy(self.daily_checks.get(entry_id) or self.checks.get(entry_id) or self.batch_checks.get(entry_id))
        record["daily_recheck"] = deepcopy(self.daily_checks.get(entry_id) or self.batch_checks.get(entry_id))
        if entry_id in self.latest_daily_ids:
            record["source_check_note"] = "9月8日官方来源、使用条款或固定提交README与许可证有界复核；没有下载或运行候选。"
        elif entry_id in self.daily_ids:
            record["source_check_note"] = "9月7日官方来源、固定提交README与许可证有界复核；没有下载或运行候选。"
        elif entry_id in self.expansion_ids:
            record["source_check_note"] = "9月6日GitHub公开元数据与社区字段初筛；没有读取完整权限文档或运行候选。"
        elif entry_id in self.batch_checks:
            record["source_check_note"] = "9月6日新增或复核所列官方元数据与文档节选；没有运行候选。"
        else:
            record["source_check_note"] = "本条没有9月6日补充复核；保留原证据日期。"
        record["query_boundary"] = {
            "local_public_records_only": True,
            "network_access_performed": False,
            "candidate_execution_performed": False,
            "host_compatibility": "unverified",
        }
        if entry_id == "filesystem-mcp-server":
            record["upstream_id_status"] = "historical_lookup_name_not_confirmed_registered"
        return record

    def search(self, query, limit=5):
        if not isinstance(query, str) or not normalize(query) or len(query) > 512:
            raise QueryError("invalid_query", "query 必须是1至512字符的非空任务描述。")
        if type(limit) is not int or not 1 <= limit <= 10:
            raise QueryError("invalid_limit", "limit 必须是1至10的整数。")
        normalized = normalize(query)
        hits = []
        for entry_id, terms in self.aliases.items():
            matched = [term for term in terms if matches(normalized, term)]
            if normalized == entry_id:
                matched.append(entry_id)
            if matched:
                record = self.evidence_detail(entry_id)
                # Preserve evidence and rights on search results, not just a title.
                hit = {key: record[key] for key in (
                    "id", "name", "type", "relationship", "summary", "version", "dates",
                    "license", "evidence_label", "permissions_note", "evaluation", "source_urls",
                    "source_check", "source_check_note", "query_boundary",
                    "daily_recheck",
                ) if key in record}
                for key in ("author", "task", "task_tags", "repository", "public_evidence_score",
                            "community_rating", "community_signals", "upstream_id_status"):
                    if key in record:
                        hit[key] = record[key]
                hit["matched_terms"] = matched
                hits.append(hit)
        hits.sort(key=lambda item: -len(item["matched_terms"]))
        return {
            "query": query,
            "match_method": "curated_keyword_overlap; not semantic or quality ranking",
            "catalog_size": len(self.records),
            "total_matches": len(hits),
            "returned_count": min(limit, len(hits)),
            "results": hits[:limit],
            "status": "matched" if hits else "no_match_in_local_catalog",
            "scope_note": f"仅搜索{len(self.records)}条本地公开记录；无匹配不代表外部市场没有相应工具。匹配和公开资料评分不是效果推荐或安全认证。",
        }

    def installation_guide(self, entry_id):
        record = self.evidence_detail(entry_id)
        steps = {
            "narrated-video-review": [
                "阅读固定版本的公开 Skill 与 MIT 许可，确认任务需要与宿主的 Skill 支持方式。",
                "如自行导入公开适配版指令，保留许可和署名；原个人材料、媒体和声音不在许可范围。",
                "实际剪辑与导出须另行验证；本目录没有代为导入或验证任一宿主。",
            ],
            "github-mcp-server": [
                "打开作者 v1.12.0 发布页及固定提交清单，确认作者当前提供的接入方式。",
                "先确认所需仓库权限与作者认证说明；认证由使用者在目标宿主完成，本目录不收取令牌。",
                "安装、依赖、远程服务条款和宿主兼容性尚未实测；本目录仅提供来源指引。",
            ],
            "filesystem-mcp-server": [
                "阅读固定提交的 README、package.json 与根许可；0.6.3是源码声明，npm最新版本未知。",
                "先厘清具体文件的许可范围，再决定复制或分发；本目录不提供组件分发包。",
                "如另行测试，应明确允许目录及写入范围；目录隔离和客户端 Roots 行为尚未验证。",
            ],
            "anthropic-pdf-skill": [
                "前往 Anthropic 作者来源和独立 LICENSE.txt 查看其使用条款。",
                "本目录未取得再分发授权，只提供原创简介及作者链接，不提供该 Skill 的副本、代码或安装包。",
                "独立版本号、实际任务效果与宿主兼容性未知；专有许可不表示目录获得专项授权。",
            ],
            "playwright-mcp": [
                "打开Microsoft官方仓库、v0.0.80发布页及Apache-2.0许可，确认作者当前要求。",
                "按目标宿主说明自行配置，并先限定网页来源、workspace roots、文件访问和可选浏览器权限；本目录不收集认证信息。",
                "本站未安装或运行该组件；Node、依赖、浏览器二进制、宿主兼容和任务效果均需另行验证。",
            ],
            "notion-mcp": [
                "打开Notion官方MCP文档，确认托管远程服务、OAuth授权和当前支持的工具；不要把本地参考实现v2.1.0当作远程服务版本。",
                "只授权需要的页面、数据库和内容范围，并由工作区或组织管理员管理、列出或撤销连接；本目录不收取凭证。",
                "本站未连接或运行Notion MCP；完整服务条款、数据保留、任务效果和宿主兼容仍需另行验证。",
            ],
            "figma-mcp": [
                "打开Figma官方MCP文档、工具清单和适用于账号计划的服务条款，确认远程服务当前能力；托管服务未公开独立版本。",
                "连接前核对账号、席位、文件编辑权限、素材下载上传、设计写入和可能的信用额度；本目录不收取Figma凭证。",
                "本站未连接或运行Figma MCP；精确认证scope、数据保留、费用、任务效果和宿主兼容仍需另行验证。",
            ],
        }
        if entry_id not in steps:
            steps[entry_id] = [
                "打开作者公开仓库，确认当前版本、许可、文档和维护状态；本目录不提供第三方安装包。",
                "在安装或连接前单独核对认证、数据流和写入权限；公开资料评分不包含运行安全或任务效果。",
                "如需评测，应在隔离环境使用合成数据并记录成功、失败、费用和人工干预；本站尚未执行。",
            ]
        return {
            "entry": record,
            "guide_status": "source_reference_only" if entry_id == "anthropic-pdf-skill" else "manual_source_guidance",
            "steps": steps[entry_id],
            "commands": [],
            "automatic_installation_supported": False,
            "installation_performed": False,
            "third_party_account_access": False,
            "third_party_package_provided": False,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="operation", required=True)
    search = subparsers.add_parser("search")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=5)
    for name in ("evidence_detail", "installation_guide"):
        subparsers.add_parser(name).add_argument("id")
    args = parser.parse_args()
    try:
        catalog = Catalog()
        result = catalog.search(args.query, args.limit) if args.operation == "search" else getattr(catalog, args.operation)(args.id)
    except QueryError as exc:
        print(json.dumps({"error": {"code": exc.code, "message": str(exc)}}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
