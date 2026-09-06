#!/usr/bin/env python3
"""Minimal MCP stdio server for the local read-only catalog (MIT)."""

import json
import math
import sys

from catalog_query import Catalog, QueryError

PROTOCOL_VERSION = "2025-11-25"
SERVER_VERSION = "0.1.0-local"
MAX_MESSAGE_BYTES = 64 * 1024
TOOLS = [
    {
        "name": "search",
        "description": "按中文或英文任务关键词搜索5条本地公开目录记录；保留版本、许可和未实测状态。只读，不联网。",
        "inputSchema": {
            "type": "object", "required": ["query"], "additionalProperties": False,
            "properties": {
                "query": {"type": "string", "minLength": 1, "maxLength": 512},
                "limit": {"type": "integer", "minimum": 1, "maximum": 10, "default": 5},
            },
        },
    },
    {
        "name": "evidence_detail",
        "description": "按检索返回的id读取版本、来源、已查与未查、许可和未知字段；不获取外部资源。",
        "inputSchema": {
            "type": "object", "required": ["id"], "additionalProperties": False,
            "properties": {"id": {"type": "string"}},
        },
    },
    {
        "name": "installation_guide",
        "description": "返回人工阅读指引和作者链接；不安装、执行、下载候选或取得账户权限。受限PDF条目只提供来源参考。",
        "inputSchema": {
            "type": "object", "required": ["id"], "additionalProperties": False,
            "properties": {"id": {"type": "string"}},
        },
    },
]


def rpc_error(request_id, code, message):
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def tool_result(value, is_error=False):
    return {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}], "isError": is_error}


class Server:
    def __init__(self):
        self.catalog = Catalog()
        self.state = "new"

    def handle(self, request):
        if not isinstance(request, dict) or request.get("jsonrpc") != "2.0" or not isinstance(request.get("method"), str):
            return rpc_error(None, -32600, "Invalid JSON-RPC request")
        is_notification = "id" not in request
        request_id = request.get("id")
        if not is_notification and not (
            isinstance(request_id, str) or type(request_id) is int or
            (type(request_id) is float and math.isfinite(request_id))
        ):
            return rpc_error(None, -32600, "Invalid request id")
        method = request["method"]
        params = request.get("params", {})
        if is_notification:
            if method == "notifications/initialized" and self.state == "initializing" and isinstance(params, dict):
                self.state = "ready"
            return None
        if not isinstance(params, dict):
            return rpc_error(request_id, -32602, "Params must be an object")
        if method == "initialize":
            if self.state != "new":
                return rpc_error(request_id, -32600, "Already initialized")
            info = params.get("clientInfo", {})
            if not (
                isinstance(params.get("protocolVersion"), str) and
                isinstance(params.get("capabilities"), dict) and isinstance(info, dict) and
                isinstance(info.get("name"), str) and isinstance(info.get("version"), str)
            ):
                return rpc_error(request_id, -32602, "Initialization metadata required")
            self.state = "initializing"
            result = {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "agent-catalog-readonly", "version": SERVER_VERSION},
                "instructions": "只读本地5条公开记录；目录协议验证不代表候选插件已运行或宿主已接通。",
            }
        elif method == "ping" and self.state != "new":
            result = {}
        elif self.state != "ready":
            return rpc_error(request_id, -32002, "Complete initialize and notifications/initialized first")
        elif method == "tools/list":
            if set(params) - {"_meta"}:
                return rpc_error(request_id, -32602, "This server returns all tools without pagination")
            result = {"tools": TOOLS}
        elif method == "tools/call":
            name = params.get("name")
            if not isinstance(name, str) or name not in {tool["name"] for tool in TOOLS}:
                return rpc_error(request_id, -32602, "Unknown tool")
            if set(params) - {"name", "arguments", "_meta"}:
                return rpc_error(request_id, -32602, "Unexpected call parameter")
            arguments = params.get("arguments", {})
            allowed = {"query", "limit"} if name == "search" else {"id"}
            required = "query" if name == "search" else "id"
            if not isinstance(arguments, dict) or set(arguments) - allowed or required not in arguments:
                return rpc_error(request_id, -32602, "Invalid tool arguments")
            try:
                if name == "search":
                    value = self.catalog.search(arguments["query"], arguments.get("limit", 5))
                elif name == "evidence_detail":
                    value = self.catalog.evidence_detail(arguments["id"])
                else:
                    value = self.catalog.installation_guide(arguments["id"])
                result = tool_result(value)
            except QueryError as exc:
                result = tool_result({"error": {"code": exc.code, "message": str(exc)}}, True)
        else:
            return rpc_error(request_id, -32601, "Method not found")
        return {"jsonrpc": "2.0", "id": request_id, "result": result}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON member")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("Non-finite JSON number")


def serve(input_stream, output_stream):
    server = Server()
    while True:
        line = input_stream.readline(MAX_MESSAGE_BYTES + 1)
        if not line:
            return
        if len(line) > MAX_MESSAGE_BYTES:
            while line and not line.endswith(b"\n"):
                line = input_stream.readline(MAX_MESSAGE_BYTES + 1)
            response = rpc_error(None, -32700, "Message exceeds 64 KiB")
        else:
            try:
                request = json.loads(line.decode("utf-8"), object_pairs_hook=unique_object, parse_constant=reject_constant)
            except (UnicodeError, ValueError, RecursionError):
                response = rpc_error(None, -32700, "Parse error")
            else:
                try:
                    response = server.handle(request)
                except Exception:
                    print("Catalog request failed", file=sys.stderr)
                    response = None if isinstance(request, dict) and "id" not in request else rpc_error(request.get("id"), -32603, "Internal error")
        if response is not None:
            output_stream.write((json.dumps(response, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8"))
            output_stream.flush()


if __name__ == "__main__":
    try:
        serve(sys.stdin.buffer, sys.stdout.buffer)
    except BrokenPipeError:
        pass
    except (OSError, ValueError, KeyError) as exc:
        print("Catalog startup or transport failed: " + type(exc).__name__, file=sys.stderr)
        sys.exit(1)
