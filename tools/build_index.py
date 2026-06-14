#!/usr/bin/env python3
"""Validate every .ircnode in nodes/ and build index.json.

Usage:
  python3 tools/build_index.py            # validate + write index.json
  python3 tools/build_index.py --check    # validate only, fail if index.json is stale

A .ircnode is a JSON manifest describing one ircuitry node (pins, params, icon, and
either a `code` script or a `subgraph`). This mirrors the loader in the main app so a
bad submission is caught in CI instead of at install time.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODES_DIR = os.path.join(ROOT, "nodes")
INDEX_PATH = os.path.join(ROOT, "index.json")

PIN_KINDS = {"Exec", "Text", "User", "Channel", "Number", "Bool", "Tool"}
# must match the NodeCategory enum in the app (case-insensitive on load)
CATEGORIES = {"Event", "Filter", "Logic", "Action", "Data", "Ai", "Storage"}


def fail(errors, f, msg):
    errors.append(f"{f}: {msg}")


def validate(f, m, errors):
    if not isinstance(m, dict):
        fail(errors, f, "top level must be a JSON object")
        return
    tid = m.get("typeId")
    if not isinstance(tid, str) or not tid.strip():
        fail(errors, f, "missing non-empty 'typeId'")
    if not isinstance(m.get("title", ""), str):
        fail(errors, f, "'title' must be a string")
    cat = m.get("category", "Action")
    if cat.lower() not in {c.lower() for c in CATEGORIES}:
        fail(errors, f, f"category '{cat}' not in {sorted(CATEGORIES)}")
    for key in ("inputs", "outputs"):
        pins = m.get(key, [])
        if not isinstance(pins, list):
            fail(errors, f, f"'{key}' must be an array")
            continue
        for p in pins:
            if not isinstance(p, dict) or "name" not in p:
                fail(errors, f, f"each {key} pin needs a 'name'")
                break
            kind = p.get("kind", "Text")
            if kind not in PIN_KINDS:
                fail(errors, f, f"pin kind '{kind}' not in {sorted(PIN_KINDS)}")
                break
    has_code = isinstance(m.get("code"), str) and m["code"].strip() != ""
    has_sub = isinstance(m.get("subgraph"), dict)
    if not has_code and not has_sub:
        fail(errors, f, "must define either 'code' (a script) or 'subgraph'")
    if has_code:
        lang = m.get("language", "python")
        if lang not in ("python", "js", "javascript", "node"):
            fail(errors, f, f"language '{lang}' must be python or js")


def entry(f, m):
    has_sub = isinstance(m.get("subgraph"), dict)
    return {
        "typeId": m.get("typeId", ""),
        "title": m.get("title", m.get("typeId", "")),
        "subtitle": m.get("subtitle", "community"),
        "category": m.get("category", "Action"),
        "icon": m.get("icon", "\U0001F9E9"),
        "iconImage": m.get("iconImage"),
        "description": m.get("description", ""),
        "language": "subgraph" if has_sub else m.get("language", "python"),
        "author": m.get("author", "ircuitry"),
        "tags": m.get("tags", []),
        "inputs": m.get("inputs", []),
        "outputs": m.get("outputs", []),
        "params": m.get("params", []),
        "file": f"nodes/{f}",
        "manifest": m,  # full manifest so the website can copy with a single fetch
    }


def main():
    check = "--check" in sys.argv
    errors = []
    seen = {}
    nodes = []
    files = sorted(x for x in os.listdir(NODES_DIR) if x.endswith(".ircnode"))
    for f in files:
        path = os.path.join(NODES_DIR, f)
        try:
            with open(path, encoding="utf-8") as fh:
                m = json.load(fh)
        except Exception as ex:
            fail(errors, f, f"invalid JSON: {ex}")
            continue
        validate(f, m, errors)
        tid = m.get("typeId", "")
        if tid in seen:
            fail(errors, f, f"duplicate typeId '{tid}' (also in {seen[tid]})")
        elif tid:
            seen[tid] = f
        nodes.append(entry(f, m))

    if errors:
        print(f"VALIDATION FAILED ({len(errors)} problem(s)):", file=sys.stderr)
        for e in errors:
            print("  - " + e, file=sys.stderr)
        sys.exit(1)

    index = {"count": len(nodes), "nodes": nodes}
    new = json.dumps(index, indent=2, ensure_ascii=False) + "\n"

    if check:
        old = ""
        if os.path.exists(INDEX_PATH):
            with open(INDEX_PATH, encoding="utf-8") as fh:
                old = fh.read()
        if old != new:
            print("index.json is stale; run: python3 tools/build_index.py", file=sys.stderr)
            sys.exit(1)
        print(f"OK: {len(nodes)} nodes valid, index.json current")
        return

    with open(INDEX_PATH, "w", encoding="utf-8") as fh:
        fh.write(new)
    print(f"OK: {len(nodes)} nodes valid, wrote index.json")


if __name__ == "__main__":
    main()
