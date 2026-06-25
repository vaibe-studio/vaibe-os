#!/usr/bin/env python3
"""doctor — canon ↔ native integrity for vAIbe-OS (model A).

Two commands. Run with uv:

    uv run --project .vaibe/scripts/doctor .vaibe/scripts/doctor/main.py diagnose   # check + lint + guards
    uv run --project .vaibe/scripts/doctor .vaibe/scripts/doctor/main.py treat      # heal: native from canon

`diagnose` reports every problem that needs healing; `treat` regenerates the
missing/divergent native layer from the canon (and prints prompt-hints for the
hand-written `AGENTS.md`). The canon (`.vaibe/`, `AGENTS.md`) is never written.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Running `uv run .../main.py` puts this dir on sys.path[0]; make it explicit so
# `import canon` / `import emitters` resolve regardless of CWD.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import canon as canon_mod  # noqa: E402
import diagnose as diagnose_mod  # noqa: E402
import treat as treat_mod  # noqa: E402

# .vaibe/scripts/doctor/main.py → vault root is four levels up.
VAULT_ROOT = Path(__file__).resolve().parents[3]


def _load(root: Path) -> canon_mod.Canon:
    return canon_mod.load_canon(root)


def cmd_diagnose(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else VAULT_ROOT
    canon = _load(root)
    findings = diagnose_mod.run_diagnose(root, canon, args.check)

    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    infos = [f for f in findings if f.severity == "info"]

    print(f"canon: {len(canon.skills)} skills, {len(canon.agents)} agents")
    for sev, group in (("error", errors), ("warning", warnings), ("info", infos)):
        for f in group:
            print(f"  {sev.upper():7} [{f.check}] {f.path}")
            print(f"          {f.message}")
    print(f"\ndiagnose: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} info")
    if not errors:
        print("✓ diagnose green — canon ↔ native integrity holds")
    return 1 if errors else 0


def cmd_treat(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else VAULT_ROOT
    canon = _load(root)
    apply = not args.dry_run
    res = treat_mod.treat(root, canon, apply=apply)

    verb = "wrote" if apply else "would write"
    print(f"treat: {verb} {len(res.written)} file(s), "
          f"{len(res.orphans)} orphan(s), {len(res.hints)} hint(s)")
    for rel in res.written:
        print(f"  {'WRITE' if apply else 'WOULD'}  {rel}")
    for rel in res.orphans:
        print(f"  ORPHAN {rel} (no canon source — remove by hand if stale)")
    if res.hints:
        print("\nprompt-hints — rules with no AGENTS.md section (edit by hand, not doctor):")
        for h in res.hints:
            print(h)
    if args.dry_run and res.written:
        print("\n(dry-run — omit --dry-run to write)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="doctor", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_diag = sub.add_parser("diagnose", help="check + lint + guards (read-only)")
    p_diag.add_argument("--check", nargs="+", choices=list(diagnose_mod.CHECKS),
                        metavar="GROUP", help="run only these groups (check|lint|guards)")
    p_diag.add_argument("--root", help="vault root (default: inferred from script path)")
    p_diag.set_defaults(func=cmd_diagnose)

    p_treat = sub.add_parser("treat", help="heal: write native from canon + prompt-hints")
    p_treat.add_argument("--dry-run", action="store_true", help="show what would change, write nothing")
    p_treat.add_argument("--root", help="vault root (default: inferred from script path)")
    p_treat.set_defaults(func=cmd_treat)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
