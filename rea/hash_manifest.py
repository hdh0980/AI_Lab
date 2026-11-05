#!/usr/bin/env python3
"""Read-only SHA-256 manifest for REA case folders.

Lab rule: hash before and after every move/quarantine/cleanup and report the
measured size. This script only reads files; it never opens them as code.

  create:  python hash_manifest.py create <dir> -o before.json [--exclude GLOB ...]
  verify:  python hash_manifest.py verify before.json [--root <dir>]
  diff:    python hash_manifest.py diff before.json after.json

Symlinks/junctions are skipped (not followed) so cloud placeholders or links
outside the case are never pulled in.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import os
import sys
from pathlib import Path

CHUNK = 1024 * 1024


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest().upper()


def walk(root: Path, excludes: list[str]):
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        d = Path(dirpath)
        dirnames[:] = [n for n in dirnames if not (d / n).is_symlink()
                       and not any(fnmatch.fnmatch((d / n).relative_to(root).as_posix(), g) for g in excludes)]
        for name in sorted(filenames):
            p = d / name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink() or any(fnmatch.fnmatch(rel, g) for g in excludes):
                continue
            yield rel, p


def cmd_create(args) -> int:
    root = Path(args.dir).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    files, total = {}, 0
    for rel, p in walk(root, args.exclude):
        size = p.stat().st_size
        files[rel] = {"sha256": sha256_file(p), "size": size}
        total += size
    manifest = {
        "root": str(root),
        "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "excludes": args.exclude,
        "file_count": len(files),
        "total_bytes": total,
        "files": files,
        "limitations": ["symlinks/junctions skipped", "content not interpreted"],
    }
    out = json.dumps(manifest, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
    else:
        print(out)
    print(f"files={len(files)} total_bytes={total}", file=sys.stderr)
    return 0


def _load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _compare(a: dict, b: dict) -> dict:
    fa, fb = a["files"], b["files"]
    return {
        "missing": sorted(set(fa) - set(fb)),
        "added": sorted(set(fb) - set(fa)),
        "changed": sorted(k for k in set(fa) & set(fb) if fa[k]["sha256"] != fb[k]["sha256"]),
        "matched": sum(1 for k in set(fa) & set(fb) if fa[k]["sha256"] == fb[k]["sha256"]),
    }


def _report(result: dict, total: int) -> int:
    print(json.dumps({**result, "expected": total}, ensure_ascii=False, indent=2))
    ok = not (result["missing"] or result["changed"])
    print(f"{'OK' if ok else 'MISMATCH'}: {result['matched']}/{total} matched", file=sys.stderr)
    return 0 if ok else 1


def cmd_verify(args) -> int:
    before = _load(args.manifest)
    root = Path(args.root or before["root"]).resolve()
    now = {"files": {rel: {"sha256": sha256_file(p)} for rel, p in walk(root, before.get("excludes", []))}}
    return _report(_compare(before, now), before["file_count"])


def cmd_diff(args) -> int:
    a, b = _load(args.before), _load(args.after)
    return _report(_compare(a, b), a["file_count"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("create")
    c.add_argument("dir")
    c.add_argument("-o", "--output")
    c.add_argument("--exclude", action="append", default=[], help="glob on relative path, repeatable")
    c.set_defaults(func=cmd_create)
    v = sub.add_parser("verify")
    v.add_argument("manifest")
    v.add_argument("--root")
    v.set_defaults(func=cmd_verify)
    d = sub.add_parser("diff")
    d.add_argument("before")
    d.add_argument("after")
    d.set_defaults(func=cmd_diff)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
