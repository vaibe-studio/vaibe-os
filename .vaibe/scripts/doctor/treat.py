"""doctor treat — write the native layer from canon (batch R, task 070).

The executive half of doctor: it brings the generated layer up to the canon by
writing every native file the emitters (068) produce that is missing or has
drifted. It is the cure for what `diagnose check` reports.

Hard boundaries (U12):
- **Only the generated layer is written** — `.{tool}/skills|agents/*` and the
  `CLAUDE.md` shims (every path comes from `emit_all`). The hand-written canon
  (`.vaibe/`, root and nested `AGENTS.md`) is never touched.
- **Orphans are never deleted** — a native file with no canon source is reported
  for the author to remove by hand (deletion is destructive).
- **The hand-written part is not edited silently** — a new `.vaibe/rules/X.md`
  with no section in `AGENTS.md` produces a *prompt-hint* (a section skeleton to
  paste), not an automatic write.

Idempotent: with the canon unchanged, a second `treat` writes nothing and the
git diff stays empty (the regression test of batch 072).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import canon as canon_mod
import diagnose as diagnose_mod
import emitters


@dataclass
class TreatResult:
    written: list[str] = field(default_factory=list)   # diff + missing that were (or would be) written
    orphans: list[str] = field(default_factory=list)
    hints: list[str] = field(default_factory=list)      # rules missing an AGENTS.md section
    applied: bool = False


# §3.0 section skeleton an author pastes into AGENTS.md for an unreflected rule.
_HINT_TEMPLATE = (
    "  add to AGENTS.md (do not let doctor write canon):\n"
    "    ## {title}\n\n"
    "    {{2–4 lines — what must always be in context.}}\n\n"
    "    Full spec: `{rule}`"
)


def _rule_title(rule_path: str) -> str:
    stem = Path(rule_path).stem
    return stem.replace("-", " ").capitalize()


def treat(root: Path, canon: canon_mod.Canon, apply: bool = True) -> TreatResult:
    nd = emitters.compare_native(root, canon)
    res = TreatResult(applied=apply)

    # 1. Write missing/divergent generated files (canon → native).
    for rel in sorted(nd.diff + nd.missing):
        res.written.append(rel)
        if apply:
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(nd.rendered[rel], encoding="utf-8")

    # 2. Orphans — reported only (deletion is destructive; left to the author).
    res.orphans = list(nd.orphan)

    # 3. Prompt-hints for the hand-written part (never auto-written).
    for rule in diagnose_mod.unreferenced_rules(root, canon):
        res.hints.append(_HINT_TEMPLATE.format(title=_rule_title(rule), rule=rule))

    return res
