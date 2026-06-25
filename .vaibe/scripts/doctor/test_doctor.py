#!/usr/bin/env python3
"""Regression test for doctor (batch T, task 072) — the final gate of migration 048.

Proves that the emitters reproduce the hand-made phase-3 native layout and that
`diagnose` stays green, across all types (skills × 4 tools, agents × 4 tools incl.
Codex TOML, CLAUDE.md shims). Non-destructive and idempotent: safe to run in CI
or on demand.

    uv run --project .vaibe/scripts/doctor .vaibe/scripts/doctor/test_doctor.py

The strong form of 4.5 ("delete the generated layer, `treat`, expect an empty
git diff") is documented in task 072; this test asserts the same invariant
without touching the tree: `compare_native` must be clean, per-type counts must
match the canon, and `diagnose` must report zero errors.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import canon as canon_mod  # noqa: E402
import diagnose as diagnose_mod  # noqa: E402
import emitters  # noqa: E402

VAULT_ROOT = Path(__file__).resolve().parents[3]


def test_dead_links() -> list[str]:
    """G12 (task 077): injected dead links are caught; removal constatations,
    external URLs and forbidding/anti-pattern sections are not (no false positives)."""
    import tempfile

    fails: list[str] = []
    pos = "\n".join([
        "# Test",
        "See `.vaibe/router.md` for skill discovery.",        # router → catch
        "Regenerate the VAULT-INDEX report nightly.",          # VAULT-INDEX → catch
        "Add the dependency to requirements.txt by hand.",     # requirements.txt → catch
    ])
    neg = "\n".join([
        "# Test",
        "router.md удалён — discovery is by `description` now.",    # removal constatation
        "Skill discovery is by description (no separate router).",  # negation
        "Ref: `https://responsibleailabs.ai/knowledge-hub`",        # external URL (.ai/)
        "Legacy `.ai/` paths are superseded by `.vaibe/`.",         # legacy / superseded
        "",
        "## Do not use (legacy of the old tools/ package)",
        "- `requirements.txt` (dependencies go in `pyproject.toml`);",  # forbidding section
        "- `python -m tools.X` package layout;",                        # forbidding section
    ])
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        rules = root / ".vaibe" / "rules"
        rules.mkdir(parents=True)
        (rules / "pos.md").write_text(pos, encoding="utf-8")
        (rules / "neg.md").write_text(neg, encoding="utf-8")
        out: list[diagnose_mod.Finding] = []
        diagnose_mod.lint_dead_links(root, set(), out)

    g12 = [f for f in out if f.check == "G12"]
    pos_hits = [f for f in g12 if f.path.startswith(".vaibe/rules/pos.md")]
    neg_hits = [f for f in g12 if f.path.startswith(".vaibe/rules/neg.md")]
    if len(pos_hits) != 3:
        fails.append(f"dead-links positive: expected 3 catches in pos.md, got "
                     f"{len(pos_hits)}: {[f.path for f in pos_hits]}")
    if neg_hits:
        fails.append(f"dead-links negative: false positives in neg.md: "
                     f"{[(f.path, f.message) for f in neg_hits]}")
    return fails


def main() -> int:
    root = VAULT_ROOT
    canon = canon_mod.load_canon(root)
    failures: list[str] = []

    # 1. generated == canon, byte-for-byte (the 4.5 invariant).
    nd = emitters.compare_native(root, canon)
    if not nd.clean:
        for p in nd.diff:
            failures.append(f"diff:    {p}")
        for p in nd.missing:
            failures.append(f"missing: {p}")
        for p in nd.orphan:
            failures.append(f"orphan:  {p}")

    # 2. per-type coverage: every type emitted for every tool, plus shims.
    n_skills, n_agents = len(canon.skills), len(canon.agents)
    n_shims = len(canon.agents_md_dirs)
    expected = len(emitters.TOOLS) * (n_skills + n_agents) + n_shims
    if len(nd.rendered) != expected:
        failures.append(f"count: rendered {len(nd.rendered)} != expected {expected}")
    for tool in emitters.TOOLS:
        for sub, want in (("skills", n_skills), ("agents", n_agents)):
            have = sum(1 for p in nd.rendered if p.startswith(f".{tool}/{sub}/"))
            if have != want:
                failures.append(f"count: .{tool}/{sub} has {have}, want {want}")

    # 3. diagnose green (no errors).
    errors = [f for f in diagnose_mod.run_diagnose(root, canon) if f.severity == "error"]
    for f in errors:
        failures.append(f"diagnose [{f.check}]: {f.path} — {f.message}")

    # 4. G12 dead-links behaviour (positive catches + no false positives).
    failures.extend(test_dead_links())

    print(f"types: {n_skills} skills × {len(emitters.TOOLS)} tools + "
          f"{n_agents} agents × {len(emitters.TOOLS)} + {n_shims} shims = {expected} native files")
    if failures:
        print(f"\nFAIL ({len(failures)}):")
        for line in failures:
            print(f"  {line}")
        return 1
    print(f"✓ PASS — treat reproduces the phase-3 layout ({expected} files), diagnose green")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
