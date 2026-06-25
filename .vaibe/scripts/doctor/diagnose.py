"""doctor diagnose — load-bearing integrity check for vAIbe-OS (batch Q, task 069).

Three layers, all machine-checkable:

1. **check** — `generated == canon` (G11): every native file equals what the
   emitters (068) would produce from the current canon. Drift → error.
2. **lint** — structural integrity of the canon itself:
   - `agents-rules` (§3.3): every `.vaibe/rules/*.md` is reflected by a section
     with a link in some `AGENTS.md`; no dangling `.vaibe/…` links.
   - `skill-validity` (G6): SKILL.md frontmatter, `name == folder`, latin slug.
   - `reachability` (lesson 065): every skill `references/`, `assets/` file has an
     incoming link — no orphaned canon artifacts.
   - `dead-links` (G12, task 077): canon prose (.md) has no live reference to an
     entity the vision removed (router.md, `.ai/`, tools.md, VAULT-INDEX, …);
     forbidding/removal lines, anti-pattern sections and external URLs are exempt.
3. **guards** — the structural invariants of `.vaibe/rules/guards.md` (G1–G5, G10).
   guards.md stays as the human spec; this module is its executable form.

G7 (knowledge protection) is a *process* guard fired before deletion, not a
lint-time assertion — reported as info. G8/G9 (reference freshness, glossary
sync) are heuristic and advisory — info, never a hard failure.

Read-only. Stdlib only. Reuses `compare_native` from emitters for the `check`.
"""

from __future__ import annotations

import re
import subprocess
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import canon as canon_mod
import emitters

SLUG_RE = re.compile(r"^[a-z0-9-]+$")
# Product folders use the canonical latin `vAIbe-{product}` form (naming-convention).
PRODUCT_NAME_RE = re.compile(r"^vAIbe-")
TASK_DIR_RE = re.compile(r"^(\d+)-(.+)$")
RESULTS_V_RE = re.compile(r"^v(\d+)$")
CYRILLIC_RE = re.compile(r"[а-яА-ЯёЁ]")
H2_RE = re.compile(r"^## (.+)$", re.MULTILINE)
# Links into the canon written as `.vaibe/...` inside markdown/backticks.
VAIBE_LINK_RE = re.compile(r"`?(\.vaibe/[^\s`)\"]+\.md)`?")

# Latin-named top-level dirs that are not user content (G3 exceptions, .vaibe layout).
LATIN_TOP_DIRS = {
    ".vaibe", ".claude", ".cursor", ".codex", ".opencode",
    ".git", ".github", ".venv", "repositories", "node_modules",
}
SYSTEM_FILENAMES = {
    "README.md", "AGENTS.md", "CLAUDE.md", "task.md",
    "summary.md", "transcript.md", "tasks.md", "results",
    ".gitignore", ".gitattributes", ".gitmodules",
}
LATIN_OK_SUFFIXES = {
    ".py", ".js", ".ts", ".json", ".yaml", ".yml", ".toml", ".lock",
    ".html", ".css", ".csv", ".svg", ".png", ".jpg", ".jpeg", ".webp",
    ".pdf", ".docx", ".xlsx", ".pptx", ".sh", ".mp3", ".mp4", ".ico",
}


@dataclass
class Finding:
    check: str        # "check" | "lint:agents-rules" | "G1" | ...
    severity: str     # "error" | "warning" | "info"
    path: str
    message: str


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def ignored_prefixes(root: Path) -> set[str]:
    """Git-ignored paths (vault-relative posix, no trailing slash).

    diagnose checks the *tracked* vault — personal data (`Видимость: личный`)
    lives in git-ignored folders and is out of scope (rule git-cross-platform).
    """
    try:
        res = subprocess.run(
            # core.quotePath=false → non-ASCII (Cyrillic) paths come back literal,
            # not C-quoted, so prefix matching below works.
            ["git", "-c", "core.quotePath=false", "-C", str(root), "ls-files",
             "--others", "--ignored", "--exclude-standard", "--directory"],
            # Explicit UTF-8: Windows defaults to cp1252 and crashes on Cyrillic paths.
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=30, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return set()
    if not res.stdout:
        return set()
    # NFC-normalize: macOS iterdir() yields NFD paths, git yields NFC — compare in NFC.
    # Normalize slashes: git/Path may use `\` on Windows; _is_ignored compares posix `/`.
    return {unicodedata.normalize("NFC", line.strip().replace("\\", "/").rstrip("/"))
            for line in res.stdout.splitlines() if line.strip()}


def _is_ignored(rel_posix: str, ignored: set[str]) -> bool:
    rel_posix = unicodedata.normalize("NFC", rel_posix)
    return any(rel_posix == p or rel_posix.startswith(p + "/") for p in ignored)


# ── 1. check: generated == canon (G11) ────────────────────────────────────

def check_generated(root: Path, canon: canon_mod.Canon, out: list[Finding]) -> None:
    nd = emitters.compare_native(root, canon)
    for p in nd.diff:
        out.append(Finding("check", "error", p, "drift: native file differs from canon (run `doctor treat`)"))
    for p in nd.missing:
        out.append(Finding("check", "error", p, "missing: canon expects this native file (run `doctor treat`)"))
    for p in nd.orphan:
        out.append(Finding("check", "error", p, "orphan: native file has no canon source"))


# ── 2a. lint: AGENTS.md ↔ rules synchrony (§3.3) ───────────────────────────

def _agents_md_links(root: Path, canon: canon_mod.Canon) -> tuple[set[str], list[tuple[str, str]]]:
    """Return (all `.vaibe/…` links referenced in any AGENTS.md, dangling pairs)."""
    referenced: set[str] = set()
    dangling: list[tuple[str, str]] = []  # (agents_md_rel, link)
    for dir_rel in canon.agents_md_dirs:
        agents_md = (root / dir_rel / "AGENTS.md") if dir_rel else (root / "AGENTS.md")
        text = _read(agents_md)
        if text is None:
            continue
        for m in VAIBE_LINK_RE.finditer(text):
            link = m.group(1)
            referenced.add(link)
            if link.startswith(".vaibe/rules/") and not (root / link).exists():
                dangling.append((str(agents_md.relative_to(root)), link))
    return referenced, dangling


def unreferenced_rules(root: Path, canon: canon_mod.Canon) -> list[str]:
    """Canon rules with no section/link in any AGENTS.md (§3.3) — treat prompt-hints."""
    rules = {f".vaibe/rules/{p.name}" for p in (root / ".vaibe" / "rules").glob("*.md")}
    referenced, _ = _agents_md_links(root, canon)
    return sorted(rules - referenced)


def lint_agents_rules(root: Path, canon: canon_mod.Canon, out: list[Finding]) -> None:
    _, dangling = _agents_md_links(root, canon)
    for agents_md_rel, link in dangling:
        out.append(Finding("lint:agents-rules", "error", agents_md_rel, f"dangling link to {link}"))
    for rule in unreferenced_rules(root, canon):
        out.append(Finding("lint:agents-rules", "error", rule,
                            "rule not reflected by a section/link in any AGENTS.md (§3.3)"))


# ── 2b. lint: SKILL.md validity (G6) ───────────────────────────────────────

def lint_skill_validity(root: Path, canon: canon_mod.Canon, out: list[Finding]) -> None:
    for skill_md in sorted((root / ".vaibe" / "skills").glob("*/SKILL.md")):
        folder = skill_md.parent.name
        text = _read(skill_md)
        rel = str(skill_md.relative_to(root))
        if text is None or not text.startswith("---"):
            out.append(Finding("G6", "error", rel, "missing YAML frontmatter"))
            continue
        fm, _ = canon_mod.parse_frontmatter(text)
        name = fm.get("name", "")
        if not name:
            out.append(Finding("G6", "error", rel, "frontmatter missing `name`"))
        elif name != folder:
            out.append(Finding("G6", "error", rel, f"name `{name}` != folder `{folder}`"))
        elif not SLUG_RE.match(name):
            out.append(Finding("G6", "error", rel, f"name `{name}` is not a latin slug [a-z0-9-]"))
        if not fm.get("description"):
            out.append(Finding("G6", "error", rel, "frontmatter missing `description`"))


# ── 2c. lint: reachability of canon artifacts (lesson 065) ─────────────────

def lint_reachability(root: Path, out: list[Finding]) -> None:
    vaibe = root / ".vaibe"
    # Candidate artifacts that must have an incoming link.
    targets: list[Path] = []
    for sub in ("references", "assets"):
        targets += list(vaibe.glob(f"skills/*/{sub}/*"))
    targets = [t for t in targets if t.is_file()]
    if not targets:
        return

    # Corpus of all canon + index text (skip the artifact bodies themselves so a
    # file referencing a sibling counts, but a file is not "reachable" via itself).
    corpus: dict[Path, str] = {}
    for md in list(vaibe.rglob("*.md")) + [root / "AGENTS.md", root / "Проекты" / "AGENTS.md"]:
        if md.is_file():
            corpus[md.resolve()] = _read(md) or ""

    for tgt in targets:
        name = tgt.name
        reachable = any(
            name in text for src, text in corpus.items() if src != tgt.resolve()
        )
        if not reachable:
            out.append(Finding("lint:reachability", "error", str(tgt.relative_to(root)),
                               "no incoming link — orphaned canon artifact"))


# ── 2d. lint: dead links to removed entities (G12, task 077) ───────────────

# Entities the vision removed/cancelled; a *live* reference in canon prose is drift.
# Scope is deliberately minimal — only dead links/paths/practices, not stale headers.
DEAD_ENTITY_RES: list[tuple[str, re.Pattern]] = [
    ("router",           re.compile(r"\brouter\b")),
    (".ai/ path",        re.compile(r"(?<![\w.])\.ai/")),
    ("tools.md",         re.compile(r"\btools\.md\b")),
    ("VAULT-INDEX",      re.compile(r"VAULT[-_]INDEX")),
    ("python -m tools.", re.compile(r"python\s+-m\s+tools\.")),
    ("requirements.txt", re.compile(r"\brequirements\.txt\b")),
    ("pyenv",            re.compile(r"\bpyenv\b")),
    (".cursor/commands", re.compile(r"\.cursor/commands\b")),
    ("*-brief.md",       re.compile(r"[\w-]+-brief\.md\b")),
]
# A line that forbids a pattern or states its removal is correct, not drift.
_NEG_RE = re.compile(
    r"удал|легаси|бывш|отмен|больше нет|вытеснен|устарел|не использ|вместо|"
    r"removed|legacy|former|deprecat|supersed|no longer|instead of|without|"
    r"\bno\b|\bnot\b|\bnever\b|\bбез\b|\bне\b|\bнет\b",
    re.IGNORECASE)
_URL_RE = re.compile(r"https?://")
# An H2 section that is a "do not use"/anti-pattern/legacy block — or the G12 spec
# section itself, which enumerates the removed entities — forbids by context.
_FORBID_SECTION_RE = re.compile(
    r"do not use|don'?t use|anti-?pattern|legacy|устарел|не использ|запрещ|мёртв|dead",
    re.IGNORECASE)


def lint_dead_links(root: Path, ignored: set[str], out: list[Finding]) -> None:
    """Canon *prose* (.md) must not reference entities the vision removed (§1, task 077).

    Closes the anti-drift blind spot: `diagnose` checked `generated == canon` and
    structure, but not semantic drift of links inside canon prose (e.g. a dead
    `router.md` mention). Scope = dead links only. False positives are excluded — a
    line that forbids a pattern or states its removal, an H2 "do not use"/anti-pattern/
    legacy section, and external URLs are not drift. Prose = `.vaibe/**/*.md` + the
    two `AGENTS.md` (script `.py` docstrings and project task cards are out of scope).
    """
    vaibe = root / ".vaibe"
    md_files = list(vaibe.rglob("*.md"))
    for extra in (root / "AGENTS.md", root / "Проекты" / "AGENTS.md"):
        if extra.is_file():
            md_files.append(extra)
    for md in md_files:
        rel = md.relative_to(root).as_posix()
        if _is_ignored(rel, ignored):
            continue
        text = _read(md)
        if text is None:
            continue
        section = ""  # current H2 title
        for i, line in enumerate(text.splitlines(), 1):
            if line.startswith("## "):
                section = line[3:]
            if _FORBID_SECTION_RE.search(section):
                continue
            if _NEG_RE.search(line) or _URL_RE.search(line):
                continue
            for name, rx in DEAD_ENTITY_RES:
                if rx.search(line):
                    out.append(Finding("G12", "error", f"{rel}:{i}",
                                       f"dead reference to removed `{name}` — canon prose "
                                       f"must not link to entities the vision removed"))


# ── 3. structural guards G1–G5, G10 ────────────────────────────────────────

def _projects(root: Path, ignored: set[str]) -> list[Path]:
    base = root / "Проекты"
    if not base.is_dir():
        return []
    return [p for p in sorted(base.iterdir())
            if p.is_dir() and not p.name.startswith((".", "_"))
            and not _is_ignored(p.relative_to(root).as_posix(), ignored)]


def guard_g1(root: Path, ignored: set[str], out: list[Finding]) -> None:
    for proj in _projects(root, ignored):
        readme = proj / "README.md"
        text = _read(readme)
        if text is None:
            out.append(Finding("G1", "error", str(proj.relative_to(root)), "no README.md"))
        elif "Видимость" not in text:
            out.append(Finding("G1", "error", str(readme.relative_to(root)), "README.md lacks `Видимость` field"))


def guard_g2(root: Path, ignored: set[str], out: list[Finding]) -> None:
    for proj in _projects(root, ignored):
        tasks = proj / "Задачи"
        if not tasks.is_dir():
            continue
        for td in sorted(tasks.iterdir()):
            if not td.is_dir() or td.name.startswith("."):
                continue
            task_md = td / "task.md"
            text = _read(task_md)
            rel = str(td.relative_to(root))
            if text is None:
                out.append(Finding("G2", "error", rel, "no task.md"))
                continue
            h2 = H2_RE.findall(text)
            if "Статус" not in [s.strip() for s in h2]:
                out.append(Finding("G2", "error", str(task_md.relative_to(root)), "no `## Статус` section"))
            elif h2[-1].strip() != "Статус":
                out.append(Finding("G2", "warning", str(task_md.relative_to(root)),
                                   f"`## Статус` is not the last H2 (last: «{h2[-1].strip()}»)"))


def guard_g3(root: Path, ignored: set[str], out: list[Finding]) -> None:
    violations = 0
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if not rel.parts or rel.parts[0] in LATIN_TOP_DIRS or rel.parts[0].startswith("."):
            continue
        if _is_ignored(rel.as_posix(), ignored):  # personal / ignored data
            continue
        if any(part == "results" and i + 1 < len(rel.parts) and RESULTS_V_RE.match(rel.parts[i + 1])
               for i, part in enumerate(rel.parts)):
            continue
        name = path.name
        if name in SYSTEM_FILENAMES or name.startswith(".") or Path(name).suffix.lower() in LATIN_OK_SUFFIXES:
            continue
        if PRODUCT_NAME_RE.match(name):  # canonical `vAIbe-{product}` latin name
            continue
        if not CYRILLIC_RE.search(name):
            violations += 1
            if violations <= 20:
                out.append(Finding("G3", "warning", str(rel), f"name «{name}» has no Cyrillic"))
    if violations > 20:
        out.append(Finding("G3", "warning", "...", f"...and {violations - 20} more (first 20 shown)"))


def guard_g4(root: Path, ignored: set[str], out: list[Finding]) -> None:
    for proj in _projects(root, ignored):
        tasks = proj / "Задачи"
        if not tasks.is_dir():
            continue
        seen: dict[str, str] = {}
        for td in sorted(tasks.iterdir()):
            if not td.is_dir() or td.name.startswith("."):
                continue
            m = TASK_DIR_RE.match(td.name)
            rel = str(td.relative_to(root))
            if not m:
                out.append(Finding("G4", "warning", rel, "dir does not match {NUM}-{TITLE}"))
                continue
            num = m.group(1)
            if len(num) < 3:
                out.append(Finding("G4", "error", rel, f"task number `{num}` < 3 digits"))
            norm = str(int(num))
            if norm in seen:
                out.append(Finding("G4", "error", rel, f"duplicate task number {num} (conflicts with «{seen[norm]}»)"))
            else:
                seen[norm] = td.name


def guard_g5(root: Path, ignored: set[str], out: list[Finding]) -> None:
    for proj in _projects(root, ignored):
        tasks = proj / "Задачи"
        if not tasks.is_dir():
            continue
        for td in sorted(tasks.iterdir()):
            results = td / "results"
            if not results.is_dir():
                continue
            for sub in sorted(results.iterdir()):
                if sub.is_dir() and not RESULTS_V_RE.match(sub.name):
                    out.append(Finding("G5", "error", str(sub.relative_to(root)),
                                       f"results subdir «{sub.name}» does not match v{{N}}"))


def guard_g10(root: Path, out: list[Finding]) -> None:
    repos = root / "repositories"
    if not repos.is_dir():
        return
    gm = _read(root / ".gitmodules") or ""
    declared = {Path(p).as_posix() for p in re.findall(r"^\s*path\s*=\s*(.+?)\s*$", gm, re.MULTILINE)
                if p.startswith("repositories/")}
    # Registration in .gitmodules is the invariant. We do NOT require entry/.git:
    # a registered submodule may legitimately be un-checked-out (CI with
    # GIT_SUBMODULE_STRATEGY=none, fresh clone without --recurse-submodules).
    for entry in sorted(repos.iterdir()):
        if entry.name.startswith("."):
            continue
        rel = entry.relative_to(root).as_posix()
        if entry.is_file():
            out.append(Finding("G10", "error", rel, "plain file in repositories/ (submodules only)"))
        elif rel not in declared:
            out.append(Finding("G10", "error", rel, "dir not registered in .gitmodules"))


# ── runner ─────────────────────────────────────────────────────────────────

CHECKS = {
    "check": lambda root, canon, ignored, out: check_generated(root, canon, out),
    "lint": lambda root, canon, ignored, out: (
        lint_agents_rules(root, canon, out),
        lint_skill_validity(root, canon, out),
        lint_reachability(root, out),
        lint_dead_links(root, ignored, out),
    ),
    "guards": lambda root, canon, ignored, out: (
        guard_g1(root, ignored, out), guard_g2(root, ignored, out),
        guard_g3(root, ignored, out), guard_g4(root, ignored, out),
        guard_g5(root, ignored, out), guard_g10(root, out),
    ),
}


def run_diagnose(root: Path, canon: canon_mod.Canon,
                 groups: list[str] | None = None) -> list[Finding]:
    out: list[Finding] = []
    ignored = ignored_prefixes(root)
    for group in (groups or list(CHECKS)):
        fn = CHECKS.get(group)
        if fn:
            fn(root, canon, ignored, out)
        else:
            out.append(Finding("?", "error", "", f"unknown check group: {group}"))
    return out
