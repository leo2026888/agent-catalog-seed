"""Real child-process stdio tests; no candidate plugin is started."""

import json
from pathlib import Path
import selectors
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from catalog_mcp import MAX_MESSAGE_BYTES, PROTOCOL_VERSION


class StdioTests(unittest.TestCase):
    def setUp(self):
        self.process = subprocess.Popen(
            [sys.executable, "-B", str(ROOT / "scripts/catalog_mcp.py")],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.process.stdout, selectors.EVENT_READ)
        self.next_id = 0

    def tearDown(self):
        self.selector.close()
        self.process.stdin.close()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=5)
            self.fail("Server did not exit after EOF")
        finally:
            self.process.stdout.close()
            stderr = self.process.stderr.read().decode("utf-8")
            self.process.stderr.close()
        self.assertEqual(self.process.returncode, 0)
        self.assertEqual(stderr, "")

    def receive(self):
        self.assertTrue(self.selector.select(timeout=5), "No response within 5 seconds")
        line = self.process.stdout.readline()
        self.assertTrue(line.endswith(b"\n"))
        return json.loads(line)

    def send(self, message, expect_response=True):
        self.process.stdin.write((json.dumps(message, ensure_ascii=False) + "\n").encode("utf-8"))
        self.process.stdin.flush()
        return self.receive() if expect_response else None

    def request(self, method, params=None):
        self.next_id += 1
        result = self.send({"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params or {}})
        self.assertEqual(result["id"], self.next_id)
        return result

    def initialize(self, requested=PROTOCOL_VERSION):
        result = self.request("initialize", {
            "protocolVersion": requested, "capabilities": {},
            "clientInfo": {"name": "local-acceptance-client", "version": "0.1.0"},
        })
        self.assertEqual(result["result"]["protocolVersion"], PROTOCOL_VERSION)
        self.send({"jsonrpc": "2.0", "method": "notifications/initialized"}, False)
        return result

    def call(self, name, arguments):
        return self.request("tools/call", {"name": name, "arguments": arguments})

    def test_handshake_list_and_all_three_tools(self):
        self.initialize()
        tools = self.request("tools/list")["result"]["tools"]
        self.assertEqual([tool["name"] for tool in tools], ["search", "evidence_detail", "installation_guide"])
        for tool in tools:
            self.assertFalse(tool["inputSchema"]["additionalProperties"])
        calls = [
            ("search", {"query": "审阅口播视频字幕"}),
            ("evidence_detail", {"id": "anthropic-pdf-skill"}),
            ("installation_guide", {"id": "anthropic-pdf-skill"}),
        ]
        for name, args in calls:
            result = self.call(name, args)["result"]
            self.assertFalse(result["isError"])
            payload = json.loads(result["content"][0]["text"])
            if name == "search":
                self.assertEqual(payload["results"][0]["id"], "narrated-video-review")
            else:
                record = payload if name == "evidence_detail" else payload["entry"]
                self.assertEqual(record["author"], "Anthropic")
                self.assertIsNone(record["version"]["value"])
                self.assertFalse(record["evaluation"]["runtime_tested"])

    def test_lifecycle_and_protocol_negotiation(self):
        self.assertEqual(self.request("tools/list")["error"]["code"], -32002)
        self.initialize("unsupported-client-version")
        self.assertEqual(self.request("ping")["result"], {})
        self.assertEqual(self.request("initialize")["error"]["code"], -32600)

    def test_initialization_notification_required(self):
        self.request("initialize", {"protocolVersion": PROTOCOL_VERSION, "capabilities": {},
                                   "clientInfo": {"name": "test", "version": "1"}})
        self.assertEqual(self.request("tools/list")["error"]["code"], -32002)
        self.send({"jsonrpc": "2.0", "method": "notifications/initialized"}, False)
        self.assertIn("tools", self.request("tools/list")["result"])

    def test_no_match_and_expected_tool_failures(self):
        self.initialize()
        result = self.call("search", {"query": "火星温室灌溉控制"})["result"]
        self.assertFalse(result["isError"])
        self.assertEqual(json.loads(result["content"][0]["text"])["results"], [])
        for name, args, code in (
            ("search", {"query": "  "}, "invalid_query"),
            ("search", {"query": "PDF", "limit": True}, "invalid_limit"),
            ("evidence_detail", {"id": "../../LICENSE"}, "unknown_entry"),
        ):
            result = self.call(name, args)["result"]
            self.assertTrue(result["isError"])
            self.assertEqual(json.loads(result["content"][0]["text"])["error"]["code"], code)

    def test_unknown_operations_and_external_inputs_rejected(self):
        self.initialize()
        for name, args in (
            ("execute", {}),
            ("search", {"query": "PDF", "url": "https://example.invalid/"}),
            ("installation_guide", {"id": "anthropic-pdf-skill", "install": True}),
            ("evidence_detail", {"path": "LICENSE"}),
        ):
            self.assertEqual(self.call(name, args)["error"]["code"], -32602)
        self.assertEqual(self.request("resources/read", {"uri": "LICENSE"})["error"]["code"], -32601)
        self.assertEqual(self.request("tools/list", {"cursor": "any"})["error"]["code"], -32602)

    def test_parse_errors_recover_and_notifications_are_silent(self):
        for raw in (b"not-json\n", b'{"jsonrpc":"2.0","jsonrpc":"2.0"}\n', b"\xff\n", b"NaN\n"):
            self.process.stdin.write(raw)
            self.process.stdin.flush()
            self.assertEqual(self.receive()["error"]["code"], -32700)
        self.assertEqual(self.send([])["error"]["code"], -32600)
        self.initialize()
        self.send({"jsonrpc": "2.0", "method": "notifications/unknown"}, False)
        self.assertEqual(self.request("ping")["result"], {})

    def test_oversize_frame_recovers(self):
        self.process.stdin.write(b"x" * (MAX_MESSAGE_BYTES + 2) + b"\n")
        self.process.stdin.flush()
        self.assertEqual(self.receive()["error"]["code"], -32700)
        self.initialize()
        self.assertEqual(self.request("ping")["result"], {})


if __name__ == "__main__":
    unittest.main()
