#!/usr/bin/env python3
"""
vault-lint: автоматическая проверка инвариантов vAIbe-OS (GUARDS.md).

⚠ ЛЕГАСИ / SUPERSEDED (фаза 4, задача 069): канонический чекер инвариантов —
`.vaibe/scripts/doctor/main.py diagnose`. Этот прообраз указывает на мёртвые
`.ai/`-пути (G6/G7) и проверяет несуществующее поле `triggers:`. Сохранён до
явного удаления владельцем; для проверок используйте doctor diagnose.

Проверки:
  G1  Каждый проект содержит README.md с полем «Видимость»
  G2  Каждая задача содержит task.md с секцией «## Статус» в конце
  G3  Файлы/папки — на русском (кроме исключений)
  G4  Номера задач уникальные, с ведущими нулями
  G5  results/ — версионирование v{N}/
  G6  .ai/skills/ — каждый skill имеет YAML frontmatter
  G7  (информационный) Отчёт о broken markdown links
  G10 `repositories/` содержит только git submodules
  PL  (информационный) Пути длиннее 200 символов (риск Windows MAX_PATH)

Запуск:
  uv run .vaibe/scripts/vault_lint/main.py
  uv run .vaibe/scripts/vault_lint/main.py --guard G1 G2
  uv run .vaibe/scripts/vault_lint/main.py --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent.parent

LATIN_ALLOWED_PREFIXES = (
    ".ai", ".cursor", ".claude", ".git", ".venv", ".github",
    "tools", "repositories", "node_modules",
)

SYSTEM_FILENAMES = {
    "README.md", "AGENTS.md", "CLAUDE.md", "task.md",
    "summary.md", "transcript.md", "tasks.md",
    ".gitignore", ".gitattributes", ".gitmodules",
    "requirements.txt", "package.json", "Makefile",
    "LICENSE", "CODEOWNERS", "Dockerfile",
    "__init__.py", "__main__.py",
    "results",
}

LATIN_ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".yaml", ".yml",
    ".html", ".css", ".scss", ".xml", ".csv", ".sql",
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico",
    ".mp4", ".mp3", ".wav", ".webm",
    ".pdf", ".docx", ".xlsx", ".pptx",
    ".sh", ".bash", ".zsh", ".bat", ".ps1",
    ".toml", ".cfg", ".ini", ".env", ".lock",
}

CYRILLIC_RE = re.compile(r"[а-яА-ЯёЁ]")
TASK_DIR_RE = re.compile(r"^(\d+)-(.+)$")
RESULTS_V_RE = re.compile(r"^v(\d+)$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


@dataclass
class Issue:
    guard: str
    severity: str  # "error" | "warning" | "info"
    path: str
    message: str


@dataclass
class LintReport:
    issues: list[Issue] = field(default_factory=list)
    stats: dict[str, int] = field(default_factory=dict)

    def add(self, guard: str, severity: str, path: str | Path, message: str) -> None:
        self.issues.append(Issue(guard, severity, str(path), message))

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "warning"]


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


# ---------------------------------------------------------------------------
# G1: Projects — README.md + Видимость
# ---------------------------------------------------------------------------

def check_g1(report: LintReport) -> None:
    projects_dir = VAULT_ROOT / "Проекты"
    if not projects_dir.is_dir():
        report.add("G1", "warning", projects_dir, "Директория Проекты/ не найдена")
        return

    count = 0
    for proj in sorted(projects_dir.iterdir()):
        if not proj.is_dir() or proj.name.startswith((".", "_")):
            continue
        count += 1
        readme = proj / "README.md"
        if not readme.is_file():
            report.add("G1", "error", proj, f"Проект «{proj.name}» не содержит README.md")
            continue

        content = _read_text(readme)
        if content is None:
            report.add("G1", "error", readme, "Не удалось прочитать README.md")
            continue

        if "Видимость:" not in content and "видимость:" not in content.lower():
            report.add("G1", "error", readme, f"README.md проекта «{proj.name}» не содержит поле «Видимость»")

    report.stats["projects_total"] = count


# ---------------------------------------------------------------------------
# G2: Tasks — task.md + ## Статус
# ---------------------------------------------------------------------------

def check_g2(report: LintReport) -> None:
    projects_dir = VAULT_ROOT / "Проекты"
    if not projects_dir.is_dir():
        return

    task_count = 0
    for proj in sorted(projects_dir.iterdir()):
        if not proj.is_dir() or proj.name.startswith((".", "_")):
            continue
        tasks_dir = proj / "Задачи"
        if not tasks_dir.is_dir():
            continue

        for task_dir in sorted(tasks_dir.iterdir()):
            if not task_dir.is_dir() or task_dir.name.startswith("."):
                continue
            task_count += 1
            task_md = task_dir / "task.md"
            if not task_md.is_file():
                report.add("G2", "error", task_dir, f"Задача «{task_dir.name}» не содержит task.md")
                continue

            content = _read_text(task_md)
            if content is None:
                report.add("G2", "error", task_md, "Не удалось прочитать task.md")
                continue

            if "## Статус" not in content:
                report.add("G2", "error", task_md, f"task.md задачи «{task_dir.name}» не содержит секцию «## Статус»")
                continue

            h2_sections = re.findall(r"^## (.+)$", content, re.MULTILINE)
            if h2_sections and h2_sections[-1].strip() != "Статус":
                report.add("G2", "warning", task_md,
                           f"Секция «## Статус» не последняя H2 (последняя: «{h2_sections[-1].strip()}»)")

    report.stats["tasks_total"] = task_count


# ---------------------------------------------------------------------------
# G3: Russian language for files/folders
# ---------------------------------------------------------------------------

def _is_latin_allowed(rel_path: Path) -> bool:
    parts = rel_path.parts
    if not parts:
        return True
    first = parts[0]
    if first in LATIN_ALLOWED_PREFIXES or first.startswith("."):
        return True
    # Inside results/v{N}/ latin is allowed
    for i, part in enumerate(parts):
        if part == "results" and i + 1 < len(parts) and RESULTS_V_RE.match(parts[i + 1]):
            return True
    return False


def check_g3(report: LintReport) -> None:
    violations = 0
    for path in sorted(VAULT_ROOT.rglob("*")):
        if not path.is_dir() and not path.is_file():
            continue

        rel = path.relative_to(VAULT_ROOT)
        if _is_latin_allowed(rel):
            continue

        name = path.name
        if name in SYSTEM_FILENAMES:
            continue
        if name.startswith("."):
            continue
        suffix = Path(name).suffix.lower()
        if suffix in LATIN_ALLOWED_EXTENSIONS:
            continue

        if not CYRILLIC_RE.search(name):
            violations += 1
            if violations <= 20:
                report.add("G3", "warning", rel,
                           f"Имя «{name}» не содержит кириллицы")

    if violations > 20:
        report.add("G3", "warning", "...",
                    f"...и ещё {violations - 20} файлов/папок без кириллицы (показаны первые 20)")
    report.stats["g3_violations"] = violations


# ---------------------------------------------------------------------------
# G4: Task numbering — unique, leading zeros
# ---------------------------------------------------------------------------

def check_g4(report: LintReport) -> None:
    projects_dir = VAULT_ROOT / "Проекты"
    if not projects_dir.is_dir():
        return

    for proj in sorted(projects_dir.iterdir()):
        if not proj.is_dir() or proj.name.startswith((".", "_")):
            continue
        tasks_dir = proj / "Задачи"
        if not tasks_dir.is_dir():
            continue

        numbers: dict[str, str] = {}  # num_str -> dir_name
        for task_dir in sorted(tasks_dir.iterdir()):
            if not task_dir.is_dir() or task_dir.name.startswith("."):
                continue

            m = TASK_DIR_RE.match(task_dir.name)
            if not m:
                report.add("G4", "warning", task_dir,
                           f"Папка задачи «{task_dir.name}» не соответствует формату {{NUM}}-{{TITLE}}")
                continue

            num_str = m.group(1)
            if len(num_str) < 3:
                report.add("G4", "error", task_dir,
                           f"Номер задачи «{num_str}» менее 3 цифр (нужны ведущие нули: {num_str.zfill(3)})")

            num_normalized = str(int(num_str))
            if num_normalized in numbers:
                report.add("G4", "error", task_dir,
                           f"Дубликат номера задачи {num_str} (конфликт с «{numbers[num_normalized]}»)")
            else:
                numbers[num_normalized] = task_dir.name


# ---------------------------------------------------------------------------
# G5: Results versioning — results/v{N}/
# ---------------------------------------------------------------------------

def check_g5(report: LintReport) -> None:
    projects_dir = VAULT_ROOT / "Проекты"
    if not projects_dir.is_dir():
        return

    for proj in sorted(projects_dir.iterdir()):
        if not proj.is_dir() or proj.name.startswith((".", "_")):
            continue
        tasks_dir = proj / "Задачи"
        if not tasks_dir.is_dir():
            continue

        for task_dir in sorted(tasks_dir.iterdir()):
            if not task_dir.is_dir():
                continue
            results_dir = task_dir / "results"
            if not results_dir.is_dir():
                continue

            loose_files = [f for f in results_dir.iterdir() if f.is_file()]
            if loose_files:
                report.add("G5", "warning", results_dir,
                           f"Файлы напрямую в results/ (legacy): {', '.join(f.name for f in loose_files[:5])}")

            for subdir in sorted(results_dir.iterdir()):
                if not subdir.is_dir():
                    continue
                if not RESULTS_V_RE.match(subdir.name):
                    report.add("G5", "error", subdir,
                               f"Подпапка results/«{subdir.name}» не соответствует формату v{{N}}")


# ---------------------------------------------------------------------------
# G6: Skills — YAML frontmatter
# ---------------------------------------------------------------------------

def check_g6(report: LintReport) -> None:
    skills_dir = VAULT_ROOT / ".ai" / "skills"
    if not skills_dir.is_dir():
        report.add("G6", "warning", skills_dir, "Директория .ai/skills/ не найдена")
        return

    skill_count = 0
    for md_file in sorted(skills_dir.glob("*.md")):
        skill_count += 1
        content = _read_text(md_file)
        if content is None:
            report.add("G6", "error", md_file, "Не удалось прочитать файл")
            continue

        if not content.startswith("---"):
            report.add("G6", "error", md_file, f"Skill «{md_file.name}» не содержит YAML frontmatter")
            continue

        fm_match = FRONTMATTER_RE.match(content)
        if not fm_match:
            report.add("G6", "error", md_file, f"Skill «{md_file.name}»: не удалось распарсить frontmatter")
            continue

        fm_text = fm_match.group(1)
        for required_field in ("name:", "description:", "triggers:"):
            if required_field not in fm_text:
                report.add("G6", "error", md_file,
                           f"Skill «{md_file.name}»: отсутствует поле «{required_field.rstrip(':')}» в frontmatter")

    report.stats["skills_total"] = skill_count


# ---------------------------------------------------------------------------
# G7: Broken markdown links (informational)
# ---------------------------------------------------------------------------

def check_g7(report: LintReport) -> None:
    broken = 0
    checked_files = 0
    key_files = [
        VAULT_ROOT / "AGENTS.md",
        VAULT_ROOT / "CLAUDE.md",
        VAULT_ROOT / ".ai" / "ONTOLOGY.md",
        VAULT_ROOT / ".ai" / "GUARDS.md",
        VAULT_ROOT / ".ai" / "router.md",
    ]

    for md_path in key_files:
        if not md_path.is_file():
            continue
        checked_files += 1
        content = _read_text(md_path)
        if content is None:
            continue

        for match in MD_LINK_RE.finditer(content):
            link = match.group(2)
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = md_path.parent / link
            if not target.exists():
                broken += 1
                report.add("G7", "info", md_path.relative_to(VAULT_ROOT),
                           f"Битая ссылка: [{match.group(1)}]({link})")

    report.stats["broken_links"] = broken
    report.stats["files_checked_links"] = checked_files


# ---------------------------------------------------------------------------
# G10: repositories/ contains only git submodules
# ---------------------------------------------------------------------------

def check_g10(report: LintReport) -> None:
    repositories_dir = VAULT_ROOT / "repositories"
    gitmodules = VAULT_ROOT / ".gitmodules"
    if not repositories_dir.is_dir():
        return

    gitmodules_text = _read_text(gitmodules) or ""
    declared_paths = set(re.findall(r"^\s*path\s*=\s*(.+?)\s*$", gitmodules_text, re.MULTILINE))
    declared_repo_paths = {Path(p).as_posix() for p in declared_paths if p.startswith("repositories/")}

    checked = 0
    for entry in sorted(repositories_dir.iterdir()):
        if entry.name.startswith("."):
            continue
        rel = entry.relative_to(VAULT_ROOT).as_posix()

        if entry.is_file():
            report.add("G10", "error", rel,
                       "В repositories/ запрещены обычные файлы; допустимы только директории-submodule")
            continue

        checked += 1
        if rel not in declared_repo_paths:
            report.add("G10", "error", rel,
                       "Директория в repositories/ не зарегистрирована в .gitmodules")
            continue

        if not (entry / ".git").exists():
            report.add("G10", "error", rel,
                       "Директория в repositories/ не выглядит как git submodule (.git отсутствует)")

    for declared in sorted(declared_repo_paths):
        if not (VAULT_ROOT / declared).exists():
            report.add("G10", "error", declared,
                       "Путь объявлен в .gitmodules, но отсутствует в repositories/")

    report.stats["repositories_entries"] = checked


# ---------------------------------------------------------------------------
# PL: Path Length — Windows MAX_PATH risk
# ---------------------------------------------------------------------------

MAX_PATH_WARN = 200
PL_SKIP_PREFIXES = ("repositories", ".venv", ".git", "node_modules", "tools")

def check_pl(report: LintReport) -> None:
    long_paths = []
    for path in sorted(VAULT_ROOT.rglob("*")):
        rel = path.relative_to(VAULT_ROOT)
        if rel.parts and rel.parts[0] in PL_SKIP_PREFIXES:
            continue
        rel_str = str(rel)
        if len(rel_str) > MAX_PATH_WARN:
            long_paths.append((rel_str, len(rel_str)))

    for rel_str, length in long_paths[:10]:
        report.add("PL", "info", rel_str,
                   f"Путь {length} символов (Windows MAX_PATH = 260, с учётом корня репо может превысить лимит)")

    if len(long_paths) > 10:
        report.add("PL", "info", "...",
                   f"...и ещё {len(long_paths) - 10} длинных путей (показаны первые 10)")
    report.stats["long_paths"] = len(long_paths)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

ALL_GUARDS = {
    "G1": check_g1,
    "G2": check_g2,
    "G3": check_g3,
    "G4": check_g4,
    "G5": check_g5,
    "G6": check_g6,
    "G7": check_g7,
    "G10": check_g10,
    "PL": check_pl,
}


def run_lint(guards: list[str] | None = None) -> LintReport:
    report = LintReport()
    selected = guards or list(ALL_GUARDS.keys())
    for guard_id in selected:
        fn = ALL_GUARDS.get(guard_id.upper())
        if fn:
            fn(report)
        else:
            report.add("?", "error", "", f"Неизвестный guard: {guard_id}")
    return report


def print_report(report: LintReport) -> None:
    print("=" * 60)
    print("  vault-lint — отчёт о проверке инвариантов vAIbe-OS")
    print("=" * 60)
    print()

    if report.stats:
        print("Статистика:")
        for k, v in sorted(report.stats.items()):
            print(f"  {k}: {v}")
        print()

    errors = report.errors
    warnings = report.warnings
    infos = [i for i in report.issues if i.severity == "info"]

    if not report.issues:
        print("Все инварианты соблюдены.")
        return

    if errors:
        print(f"ОШИБКИ ({len(errors)}):")
        for issue in errors:
            print(f"  [{issue.guard}] {issue.path}")
            print(f"        {issue.message}")
        print()

    if warnings:
        print(f"ПРЕДУПРЕЖДЕНИЯ ({len(warnings)}):")
        for issue in warnings:
            print(f"  [{issue.guard}] {issue.path}")
            print(f"        {issue.message}")
        print()

    if infos:
        print(f"ИНФОРМАЦИЯ ({len(infos)}):")
        for issue in infos:
            print(f"  [{issue.guard}] {issue.path}")
            print(f"        {issue.message}")
        print()

    print("-" * 60)
    print(f"Итого: {len(errors)} ошибок, {len(warnings)} предупреждений, {len(infos)} инфо")


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="vault-lint",
        description="Проверка инвариантов vAIbe-OS (GUARDS.md)",
    )
    ap.add_argument(
        "--guard", nargs="+", metavar="ID",
        help="Проверить только указанные guards (G1, G2, ...)",
    )
    ap.add_argument(
        "--json", action="store_true", dest="output_json",
        help="Вывести результат в JSON",
    )
    args = ap.parse_args()

    report = run_lint(args.guard)

    if args.output_json:
        data = {
            "stats": report.stats,
            "issues": [
                {"guard": i.guard, "severity": i.severity, "path": i.path, "message": i.message}
                for i in report.issues
            ],
        }
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print_report(report)

    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
