from __future__ import annotations

import re
from pathlib import Path


def _clean_source_markdown(raw: str) -> str:
    """
    Remove non-content HTML noise that sometimes appears in exported markdown:
    - top <img ...> line
    - hidden <span style="display:none">...</span> blocks
    - center divider "⁂"
    - null characters
    """
    lines = raw.splitlines(True)
    out: list[str] = []
    skip_hidden = False

    for line in lines:
        line = line.replace("\x00", "")

        if line.lstrip().startswith("<img "):
            continue

        if '<span style="display:none">' in line:
            skip_hidden = True
            continue
        if skip_hidden:
            if "</span>" in line:
                skip_hidden = False
            continue

        if line.strip() == '<div align="center">⁂</div>':
            continue

        out.append(line)

    cleaned = "".join(out).strip() + "\n"
    return cleaned


def _extract_blocks(cleaned: str) -> list[tuple[str, str]]:
    lines = cleaned.splitlines()
    blocks: list[tuple[str, str]] = []

    in_section = False
    for ln in lines:
        if ln.strip() == "## Десять основных блоков документации":
            in_section = True
            continue
        if in_section:
            if ln.startswith("## ") and ln.strip() != "## Десять основных блоков документации":
                break
            m = re.match(r"^###\s+([IVX]+)\.\s+(.*)$", ln.strip())
            if m:
                blocks.append((m.group(1), m.group(2)))

    return blocks


def _extract_principles(cleaned: str) -> list[str]:
    lines = cleaned.splitlines()
    principles: list[str] = []

    in_section = False
    for ln in lines:
        if ln.strip() == "## Ключевые принципы структуры":
            in_section = True
            continue
        if in_section:
            if ln.startswith("## ") and ln.strip() != "## Ключевые принципы структуры":
                break
            if ln.strip().startswith("**") and "**:" in ln:
                principles.append(ln.strip())

    return principles


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    deferred = (
        root
        / "Инбокс"
        / "Отложено"
        / "Структура документации Второго мозга (отложено).md"
    )
    if not deferred.exists():
        raise FileNotFoundError(deferred)

    kb = root / "База знаний"
    sources_dir = kb / "Исходники"
    sources_dir.mkdir(parents=True, exist_ok=True)

    cleaned_out = sources_dir / "Структура документации Второго мозга (источник, очищено).md"
    summary_out = kb / "Структура документации Второго мозга (конспект).md"

    raw = deferred.read_text(encoding="utf-8", errors="replace")
    cleaned = _clean_source_markdown(raw)
    cleaned_out.write_text(cleaned, encoding="utf-8")

    blocks = _extract_blocks(cleaned)
    principles = _extract_principles(cleaned)

    summary: list[str] = []
    summary.append("# Структура документации «Второго мозга» — конспект\n")
    summary.append(
        "**Источник**: `База знаний/Исходники/Структура документации Второго мозга (источник, очищено).md`\n"
    )
    summary.append("\n")

    summary.append("## Ключевые идеи\n")
    if principles:
        for p in principles[:3]:
            summary.append(f"- {p}\n")
    else:
        summary.append(
            "- Документация строится вокруг симбиоза человека и ИИ, эволюционности и практической применимости.\n"
        )
    summary.append("\n")

    summary.append("## 10 блоков документации (каркас)\n")
    for roman, title in blocks:
        summary.append(f"- **{roman}. {title}**\n")
    summary.append("\n")

    summary.append("## Как использовать (объективно, без привязки к проекту)\n")
    summary.append(
        "- **Чек-лист полноты**: пройтись по 10 блокам и отметить, что уже есть / чего не хватает.\n"
    )
    summary.append(
        "- **Карта артефактов**: каждый новый документ сразу относить к одному из блоков.\n"
    )
    summary.append(
        "- **Фильтр качества**: добавлять только то, что поддерживает действия/решения; остальное — в исходники или в отдельную очередь.\n"
    )
    summary.append("\n")

    summary.append("## Статус обработки\n")
    summary.append(
        "- Исходник очищен от служебных HTML-элементов и скрытых блоков.\n"
    )
    summary.append("- Конспект фиксирует структуру и способы применения.\n")

    summary_out.write_text("".join(summary), encoding="utf-8")

    # remove from deferred queue after successful processing
    deferred.unlink()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

