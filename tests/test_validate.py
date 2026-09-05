"""Adversarial checks for package boundaries; no plugin or fixture execution."""
import copy
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("seed_validate", ROOT / "scripts/validate.py")
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


class ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = V.load_json(ROOT / V.SCHEMA)
        cls.entry = V.load_json(ROOT / "entries/release-note-checklist-demo.json")

    def test_demo_is_valid_and_digest_bound(self):
        V.check_schema(self.schema)
        self.assertEqual(V.validate_value(self.entry, self.schema), [])
        self.assertEqual(V.check_entry(self.entry, ROOT), [])

    def test_schema_rejects_unknown_malformed_nested_and_duplicate_keys(self):
        for change in (lambda s: s.update({"oneOf": []}),
                       lambda s: s["properties"]["name"].update({"minLength": True}),
                       lambda s: s.update({"additionalProperties": True}),
                       lambda s: s["required"].append("absent")):
            schema = copy.deepcopy(self.schema)
            change(schema)
            with self.assertRaises(ValueError):
                V.check_schema(schema)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.json"
            for text in ('{"a":1,"a":2}', '{"n":NaN}', '{"n":1e999}'):
                path.write_text(text)
                with self.assertRaises(ValueError):
                    V.load_json(path)

    def test_self_rating_and_unproven_compatibility_fail(self):
        for field, change in (("evaluation", {"status": "certified", "score": 100}),
                              ("compatibility", [{"host": "any", "status": "tested", "evidence": []}]),
                              ("installable", True)):
            entry = copy.deepcopy(self.entry)
            entry[field] = change
            self.assertTrue(V.validate_value(entry, self.schema))

    def test_nested_unknown_permissions_and_network_fail(self):
        entry = copy.deepcopy(self.entry)
        entry["requested_permissions"]["secret_permission"] = True
        self.assertTrue(V.validate_value(entry, self.schema))
        entry = copy.deepcopy(self.entry)
        entry["requested_permissions"]["network_destinations"] = ["example.invalid"]
        self.assertTrue(V.validate_value(entry, self.schema))

    def test_traversal_absolute_windows_and_symlinks_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "ok.md").write_text("safe")
            (root / "alias.md").symlink_to(root / "ok.md")
            (root / "linked").symlink_to(root, target_is_directory=True)
            for excluded in V.EXCLUDED:
                (root / excluded).mkdir()
                (root / excluded / "private.md").write_text("excluded source")
                with self.assertRaises(ValueError):
                    V.safe_file(root, excluded + "/private.md")
            for ref in ("../ok.md", "/ok.md", "a/../ok.md", "C:/ok.md", "a\\ok.md",
                        "./ok.md", "a//ok.md", "alias.md", "linked/ok.md"):
                with self.subTest(ref=ref), self.assertRaises(ValueError):
                    V.safe_file(root, ref)
            self.assertEqual(V.safe_file(root, "ok.md"), root / "ok.md")

    def test_digest_mismatch_and_missing_rights_ledger_fail(self):
        entry = copy.deepcopy(self.entry)
        entry["source"]["artifacts"][0]["sha256"] = "0" * 64
        self.assertIn("artifact digest mismatch", V.check_entry(entry, ROOT))
        entry = copy.deepcopy(self.entry)
        entry["rights"]["ledger"] = "missing.md"
        self.assertIn("unsafe or missing rights ledger", V.check_entry(entry, ROOT))

    def test_hidden_token_private_path_and_binary_fail_without_value_leak(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            token = "gh" + "p_" + "a" * 30
            (root / ".private").write_text(token)
            (root / "paths.md").write_text("/" + "Users" + "/sample/private")
            (root / "blob.bin").write_bytes(b"\x00\xff")
            (root / "key.pem").write_text("placeholder")
            _, errors = V.scan_package(root)
            report = "\n".join(errors)
            for issue in ("hidden", "credential", "private path", "UTF-8", "suspicious"):
                self.assertIn(issue, report)
            self.assertNotIn(token, report)

    def test_manifest_requires_exact_coverage_and_correct_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "a.md").write_text("safe")
            manifest = root / "SHA256SUMS.txt"
            manifest.write_text(hashlib.sha256(b"safe").hexdigest() + "  a.md\n")
            self.assertEqual(V.verify_manifest(root, ["a.md", "SHA256SUMS.txt"]), [])
            self.assertTrue(V.verify_manifest(root, ["a.md", "extra.md", "SHA256SUMS.txt"]))
            (root / "a.md").write_text("changed")
            self.assertIn("SHA256SUMS.txt: digest mismatch", V.verify_manifest(root, ["a.md", "SHA256SUMS.txt"]))

    def test_boolean_is_not_numeric_and_array_items_are_recursive(self):
        self.assertTrue(V.validate_value(True, {"type": "integer"}))
        schema = {"type": "array", "items": {"type": "string", "minLength": 2}, "uniqueItems": True}
        self.assertTrue(V.validate_value(["x", "x"], schema))
        self.assertFalse(V.same(True, 1))

    def test_hash_substrings_are_not_phone_numbers_but_plain_numbers_are(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            number = "138" + "0" * 8
            path = root / "sample.md"
            path.write_text("a" * 20 + number + "f" * 33)
            self.assertEqual(V.scan_package(root)[1], [])
            path.write_text("phone: " + number)
            self.assertTrue(any("phone pattern" in e for e in V.scan_package(root)[1]))


if __name__ == "__main__":
    unittest.main()
