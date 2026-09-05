#!/usr/bin/env python3
"""Offline seed checks; a documented JSON Schema subset, not a security audit."""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "schema/entry.v0.1.0.schema.json"
EXCLUDED = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}
HIDDEN_OK = {".github", ".gitignore", ".gitattributes", ".editorconfig"}
REQUIRED = ("README.md", "CONTRIBUTING.md", "SECURITY.md", "LICENSING.md",
            "SOURCES_AND_RIGHTS.md", "VERSION", "docs/ENTRY_FORMAT.md",
            "docs/EVALUATION.md", "docs/GOVERNANCE.md", "docs/MAINTENANCE.md",
            "docs/RELEASE_CHECKLIST.md", SCHEMA)
SUSPICIOUS = {".pem", ".key", ".p12", ".pfx", ".db", ".sqlite", ".sqlite3",
              ".zip", ".tar", ".gz", ".mp4", ".mp3", ".png", ".jpg", ".pdf"}
PATTERNS = {
    "email pattern": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "phone pattern": r"(?<![A-Za-z0-9])1[3-9]\d{9}(?![A-Za-z0-9])",
    "private path pattern": r"/(?:Users|home)/[^\s/]+/",
    "private key pattern": r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
    "credential pattern": r"(?:gh[pousr]_[A-Za-z0-9_]{15,}|sk-[A-Za-z0-9_-]{20,}|Bearer\s+[A-Za-z0-9._-]{20,})",
}


def same(a, b):
    if isinstance(a, bool) != isinstance(b, bool):
        return False
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def load_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result
    def number(value):
        result = float(value)
        if not math.isfinite(result):
            raise ValueError("non-finite number")
        return result
    def invalid(_):
        raise ValueError("non-finite number")
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_float=number, parse_constant=invalid)


def check_schema(schema):
    base = {"$schema", "$id", "title", "description", "type", "enum", "const"}
    by_type = {"object": {"properties", "required", "additionalProperties"},
               "array": {"items", "minItems", "maxItems", "uniqueItems"},
               "string": {"minLength", "maxLength", "pattern"},
               "integer": set(), "number": set(), "boolean": set(), "null": set()}
    if not isinstance(schema, dict) or not isinstance(schema.get("type"), str):
        raise ValueError("schema requires a single supported type")
    kind = schema["type"]
    if kind not in by_type or set(schema) - base - by_type[kind]:
        raise ValueError("unsupported or misplaced schema keyword")
    for key in ("$schema", "$id", "title", "description", "pattern"):
        if key in schema and not isinstance(schema[key], str):
            raise ValueError("invalid schema string")
    for key in ("minItems", "maxItems", "minLength", "maxLength"):
        if key in schema and (type(schema[key]) is not int or schema[key] < 0):
            raise ValueError("invalid schema length")
    for low, high in (("minItems", "maxItems"), ("minLength", "maxLength")):
        if low in schema and high in schema and schema[low] > schema[high]:
            raise ValueError("contradictory schema length")
    if "enum" in schema:
        values = schema["enum"]
        if not isinstance(values, list) or not values or any(
                same(v, w) for i, v in enumerate(values) for w in values[:i]):
            raise ValueError("invalid schema enum")
    if "pattern" in schema:
        try:
            re.compile(schema["pattern"])
        except re.error as exc:
            raise ValueError("invalid schema pattern") from exc
    if kind == "object":
        props, required = schema.get("properties"), schema.get("required", [])
        if not isinstance(props, dict) or schema.get("additionalProperties") is not False:
            raise ValueError("schema objects must declare closed properties")
        if (not isinstance(required, list) or not all(isinstance(k, str) for k in required)
                or len(set(required)) != len(required) or set(required) - set(props)):
            raise ValueError("invalid schema required fields")
        for subschema in props.values():
            check_schema(subschema)
    if kind == "array":
        if "uniqueItems" in schema and type(schema["uniqueItems"]) is not bool:
            raise ValueError("invalid schema uniqueness flag")
        check_schema(schema.get("items"))


def validate_value(value, schema, location="$", errors=None):
    errors = [] if errors is None else errors
    kind = schema["type"]
    valid = {"object": isinstance(value, dict), "array": isinstance(value, list),
             "string": isinstance(value, str), "integer": type(value) is int or
             (type(value) is float and math.isfinite(value) and value.is_integer()),
             "number": type(value) is int or (type(value) is float and math.isfinite(value)),
             "boolean": type(value) is bool, "null": value is None}[kind]
    if not valid:
        errors.append(f"{location}: wrong type")
        return errors
    if "const" in schema and not same(value, schema["const"]):
        errors.append(f"{location}: constant constraint failed")
    if "enum" in schema and not any(same(value, item) for item in schema["enum"]):
        errors.append(f"{location}: enum constraint failed")
    if kind == "object":
        if set(value) - set(schema["properties"]):
            errors.append(f"{location}: unknown object field")
        if set(schema.get("required", [])) - set(value):
            errors.append(f"{location}: required field missing")
        for key in value.keys() & schema["properties"].keys():
            validate_value(value[key], schema["properties"][key], location + "." + key, errors)
    if kind in ("string", "array"):
        low, high = ("minLength", "maxLength") if kind == "string" else ("minItems", "maxItems")
        if len(value) < schema.get(low, 0) or len(value) > schema.get(high, float("inf")):
            errors.append(f"{location}: length constraint failed")
    if kind == "string" and "pattern" in schema and not re.search(schema["pattern"], value):
        errors.append(f"{location}: pattern constraint failed")
    if kind == "array":
        if schema.get("uniqueItems") and any(same(v, w) for i, v in enumerate(value) for w in value[:i]):
            errors.append(f"{location}: duplicate array item")
        for i, item in enumerate(value):
            validate_value(item, schema["items"], f"{location}[{i}]", errors)
    return errors


def safe_file(root, relative):
    if (not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative
            or any(part in {"", ".", ".."} | EXCLUDED for part in relative.split("/"))):
        raise ValueError("unsafe relative file reference")
    current = root
    for part in relative.split("/"):
        current = current / part
        if current.is_symlink():
            raise ValueError("symbolic link reference")
    if not current.resolve().is_relative_to(root.resolve()) or not current.is_file():
        raise ValueError("missing or invalid file reference")
    return current


def check_entry(entry, root):
    errors, paths = [], set()
    for artifact in entry["source"]["artifacts"]:
        if artifact["path"] in paths:
            errors.append("duplicate artifact path")
        paths.add(artifact["path"])
        try:
            file = safe_file(root, artifact["path"])
            if hashlib.sha256(file.read_bytes()).hexdigest() != artifact["sha256"]:
                errors.append("artifact digest mismatch")
        except (OSError, ValueError):
            errors.append("unsafe or missing artifact reference")
    try:
        safe_file(root, entry["rights"]["ledger"])
    except (OSError, ValueError):
        errors.append("unsafe or missing rights ledger")
    return errors


def scan_package(root):
    files, errors = [], []
    for directory, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d not in EXCLUDED]
        for name in dirs[:] + names:
            path = Path(directory) / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                errors.append(f"{relative}: symbolic link prohibited")
                if name in dirs:
                    dirs.remove(name)
                continue
            if name.startswith(".") and name not in HIDDEN_OK:
                errors.append(f"{relative}: unapproved hidden package item")
            if path.is_dir():
                continue
            if not path.is_file():
                errors.append(f"{relative}: non-regular package item")
                continue
            files.append(relative)
            if path.suffix.lower() in SUSPICIOUS or name in {"id_rsa", "id_ed25519"}:
                errors.append(f"{relative}: suspicious package file type")
            try:
                content = path.read_text(encoding="utf-8")
                if "\x00" in content:
                    errors.append(f"{relative}: binary content prohibited")
                for label, pattern in PATTERNS.items():
                    if re.search(pattern, content):
                        errors.append(f"{relative}: {label}")
            except (OSError, UnicodeError):
                errors.append(f"{relative}: unreadable UTF-8 content")
    return files, errors


def verify_manifest(root, files):
    errors, seen = [], set()
    try:
        lines = safe_file(root, "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
        for line in lines:
            match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
            if not match:
                raise ValueError("invalid manifest record")
            digest, relative = match.groups()
            if relative in seen or relative == "SHA256SUMS.txt":
                raise ValueError("duplicate or self-referential manifest record")
            seen.add(relative)
            if hashlib.sha256(safe_file(root, relative).read_bytes()).hexdigest() != digest:
                errors.append("SHA256SUMS.txt: digest mismatch")
        if seen != set(files) - {"SHA256SUMS.txt"}:
            errors.append("SHA256SUMS.txt: package coverage mismatch")
    except (OSError, UnicodeError, ValueError):
        errors.append("SHA256SUMS.txt: invalid manifest or reference")
    return errors


def validate_package(root):
    files, errors = scan_package(root)
    for relative in REQUIRED:
        try:
            safe_file(root, relative)
        except (OSError, ValueError):
            errors.append(f"{relative}: required document missing or unsafe")
    try:
        schema = load_json(safe_file(root, SCHEMA))
        check_schema(schema)
    except (OSError, UnicodeError, ValueError):
        return errors + [f"{SCHEMA}: invalid or unsupported schema"]
    entries = sorted(f for f in files if f.startswith("entries/") and f.endswith(".json"))
    if not entries:
        errors.append("entries/: no entry files")
    ids = set()
    for relative in entries:
        try:
            entry = load_json(safe_file(root, relative))
            issues = validate_value(entry, schema)
            if not issues:
                issues.extend(check_entry(entry, root))
                if entry["id"] in ids:
                    issues.append("duplicate entry id")
                ids.add(entry["id"])
            errors.extend(f"{relative}: {issue}" for issue in issues)
        except (OSError, UnicodeError, ValueError):
            errors.append(f"{relative}: invalid JSON or unsafe file")
    if "SHA256SUMS.txt" in files:
        errors.extend(verify_manifest(root, files))
    return errors


if __name__ == "__main__":
    problems = sorted(set(validate_package(ROOT)))
    print("\n".join(problems) if problems else "PASS: local static package checks; no execution or evaluation performed.")
    sys.exit(bool(problems))
