"""Task and evidence regressions for the project's own query code."""

from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from catalog_query import Catalog, QueryError


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.catalog = Catalog()

    def test_chinese_task_preserves_evidence(self):
        result = self.catalog.search("找一个帮我审阅口播视频、检查字幕的工具")
        self.assertEqual(result["returned_count"], 1)
        record = result["results"][0]
        self.assertEqual(record["id"], "narrated-video-review")
        self.assertEqual(record["version"]["value"], "0.1.0")
        self.assertFalse(record["evaluation"]["runtime_tested"])
        self.assertIsNone(record["evaluation"]["score"])
        self.assertTrue(record["source_urls"]["skill"].startswith("https://github.com/"))
        self.assertIsNone(record["source_check"])

    def test_unknown_task_does_not_invent_recommendations(self):
        result = self.catalog.search("火星温室灌溉控制")
        self.assertEqual(result["results"], [])
        self.assertEqual(result["status"], "no_match_in_local_catalog")

    def test_new_playwright_listing_preserves_permission_and_runtime_boundary(self):
        record = self.catalog.search("用浏览器做网页自动化")["results"][0]
        self.assertEqual(record["id"], "playwright-mcp")
        self.assertEqual(record["version"]["value"], "0.0.80")
        self.assertEqual(record["license"]["label"], "Apache-2.0")
        self.assertIn("workspace roots", record["permissions_note"])
        self.assertFalse(record["evaluation"]["runtime_tested"])
        self.assertEqual(record["daily_recheck"]["listing_action"], "new_accepted_listing")

    def test_expanded_catalog_exposes_public_score_without_claiming_effect(self):
        result = self.catalog.search("查最新的代码文档和 API", limit=10)
        record = next(item for item in result["results"] if item["id"] == "context7-mcp")
        self.assertEqual(result["catalog_size"], 21)
        self.assertEqual(record["public_evidence_score"]["value"], 100)
        self.assertEqual(record["community_rating"]["count"], 0)
        self.assertIsNone(record["evaluation"]["task_effect_score"])
        self.assertFalse(record["evaluation"]["runtime_tested"])
        self.assertIn("没有读取完整权限文档", record["source_check_note"])

    def test_expanded_entry_guidance_remains_manual_and_package_free(self):
        guide = self.catalog.installation_guide("aws-mcp-servers")
        self.assertEqual(guide["commands"], [])
        self.assertFalse(guide["installation_performed"])
        self.assertFalse(guide["third_party_package_provided"])
        self.assertIn("隔离环境", guide["steps"][2])

    def test_normalization_and_english_word_boundaries(self):
        self.assertEqual(self.catalog.search("ＧＩＴＨＵＢ issues")["results"][0]["id"], "github-mcp-server")
        self.assertEqual(self.catalog.search("proprietary improved platform")["results"], [])
        self.assertEqual(self.catalog.search("OCR scanning")["results"][0]["id"], "anthropic-pdf-skill")

    def test_pdf_rights_and_unknown_version_preserved_everywhere(self):
        records = [self.catalog.evidence_detail("anthropic-pdf-skill"),
                   self.catalog.search("PDF 合并")["results"][0],
                   self.catalog.installation_guide("anthropic-pdf-skill")["entry"]]
        for record in records:
            with self.subTest(record=record["id"]):
                self.assertEqual(record["author"], "Anthropic")
                self.assertIsNone(record["version"]["value"])
                self.assertEqual(record["license"]["redistribution_authorization"], "not_obtained")
                self.assertFalse(record["evaluation"]["runtime_tested"])
                self.assertFalse(record["evaluation"]["security_certified"])
                self.assertIn("LICENSE.txt", record["source_urls"]["license"])

    def test_guidance_never_installs_or_provides_third_party_packages(self):
        for entry_id in self.catalog.records:
            guide = self.catalog.installation_guide(entry_id)
            self.assertEqual(guide["commands"], [])
            self.assertFalse(guide["installation_performed"])
            self.assertFalse(guide["automatic_installation_supported"])
            self.assertFalse(guide["third_party_account_access"])
            self.assertFalse(guide["third_party_package_provided"])
        self.assertEqual(self.catalog.installation_guide("anthropic-pdf-skill")["guide_status"], "source_reference_only")

    def test_checkpoint_does_not_relabel_license_as_freshly_read(self):
        record = self.catalog.evidence_detail("filesystem-mcp-server")
        self.assertEqual(record["license"]["status"], "file_scope_review_required")
        self.assertEqual(record["upstream_id_status"], "historical_lookup_name_not_confirmed_registered")
        self.assertTrue(record["source_check"]["baseline_evidence_reused"])
        self.assertIn("not_read_today", record["source_check"])
        self.assertEqual(record["version"]["kind"], "source_manifest")

    def test_changed_checkpoint_fails_closed(self):
        original = Path.read_text
        def altered(path, *args, **kwargs):
            text = original(path, *args, **kwargs)
            if path.name == "source-checks-2026-09-06.json":
                data = json.loads(text)
                data["records"][0]["version"] = "different-version"
                return json.dumps(data)
            return text
        with patch.object(Path, "read_text", altered), self.assertRaisesRegex(ValueError, "differs"):
            Catalog()

    def test_unknown_ids_and_bad_queries(self):
        for entry_id in ("../../LICENSE", "https://example.invalid/", "release-note-checklist-demo", [], None):
            with self.subTest(entry_id=entry_id), self.assertRaises(QueryError):
                self.catalog.evidence_detail(entry_id)
        for query in ("", "  ", "字" * 513, None, []):
            with self.subTest(query=repr(query)), self.assertRaises(QueryError):
                self.catalog.search(query)
        for limit in (True, 0, 11, 1.0, "3"):
            with self.subTest(limit=limit), self.assertRaises(QueryError):
                self.catalog.search("PDF", limit)

    def test_returned_data_does_not_mutate_future_calls(self):
        first = self.catalog.evidence_detail("anthropic-pdf-skill")
        expected = deepcopy(first)
        first["license"]["redistribution_authorization"] = "wrong"
        self.assertEqual(self.catalog.evidence_detail("anthropic-pdf-skill"), expected)

    def test_limit_preserves_total_count(self):
        full = self.catalog.search("视频 仓库 文件 PDF", limit=10)
        limited = self.catalog.search("视频 仓库 文件 PDF", limit=2)
        self.assertGreaterEqual(full["total_matches"], 4)
        self.assertEqual(limited["total_matches"], full["total_matches"])
        self.assertEqual(limited["returned_count"], 2)


if __name__ == "__main__":
    unittest.main()
