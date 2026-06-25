---
name: csv-tabular-results
description: CSV/Excel/Git conventions for tabular results: single header, UTF-8, no multi-sheet CSV. Reference material (non-actionable knowledge).
license: MIT
---

# Tabular results in the vault (CSV, Excel, Git)

Practical reference: how to save **`.csv`** in `Проекты/.../Задачи/.../results/v{N}/` so files stay **friendly to Git, scripts, and Excel (RU)**.

## Why it matters

- One extra row on top (e.g. `Column1;Column2;…`) breaks the "first row = field header" expectation for `pandas`, shell utilities, and code review.
- The **CSV format does not support multiple sheets**, unlike **`.xlsx`**. When exporting from Excel to CSV, usually **only the active sheet** is captured; a "second sheet" is not carried into a single CSV as a sheet — only if you manually concatenate blocks (which often produces a garbage first row).
- Cyrillic and characters like **Д / У / Н** break if the file is saved as something other than **UTF-8**, or if Excel opens UTF-8 as the system ANSI code page.

## Default rules (canon for vAIbe-OS)

1. **One header row** — field names (`cell_id`, `C`, …), without an Excel-prefixed `Column1…` row.
2. **Encoding: UTF-8.** To open in Excel on Windows without Cyrillic surprises, prefer **UTF-8 with BOM**.
3. **Default delimiter for human-facing CSV:** **`;`**. This is the primary format for results the user is likely to open by hand in Excel on Windows/RU.
4. **Use the `,` delimiter only deliberately** — when the CSV is primarily meant for scripts, external APIs, pandas pipelines, or systems that expect comma-separated format.
5. **Multiple logical tables:** don't concatenate into one CSV with two headers in a row — either **separate files** (`matrix-cells.csv`, `matrix-modifiers.csv`), or one **`.xlsx`** with sheets **plus**, if needed, one "canonical" CSV for automation.
6. **Quotes and line breaks in fields:** per RFC, fields with `;` or line breaks go in double quotes; when editing by hand in Excel, verify the export didn't split rows.

## Practical default: Excel-friendly CSV

If a tabular artifact is created for a human inside vAIbe-OS and there is no explicit requirement for machine comma-CSV, treat the default as:

- **delimiter:** `;`
- **encoding:** `UTF-8 with BOM`
- **first row:** real headers only

This rule is needed because the typical Windows user scenario is: double-click the file in Explorer or open via Excel without a separate import. In that scenario comma-CSV often opens as **a single column** due to locale.

## When to make `.xlsx` right away

Prefer `.xlsx` alongside the CSV if:

- the table is clearly intended for manual filtering, sorting, and notes in Excel;
- comfortable viewing of long text fields is needed;
- there are several logical sheets;
- active manual work by the user is expected, not just reading or parsing.

A good pattern:

- `report.csv` — canonical flat export for Git and automation
- `report.xlsx` — convenient user-facing version for Excel

## What to check before committing

- Open the file in an editor with UTF-8 display: Cyrillic is readable, verdicts didn't turn into ``.
- The first row has meaningful column names, not `Column1`.
- Data rows = the expected number (e.g. 25 for a 5×5 matrix).
- If the file was made for manual opening in Excel on Windows: on a test open, the data doesn't collapse into a single column.

## Related material

- Versioning `results/v{N}/`: `.vaibe/rules/structure.md` (section on task results).
- Tasks with expense tables and xlsx: `.vaibe/skills/personal-budget/SKILL.md` (reading sheets).

## Origin

Insight recorded after analyzing `matrix-cells.csv` (vAIbe-studio task 021): an Excel export, an extra top row, conflation of "second sheet" expectations with a single CSV, and a risk of encoding breakage.

Further refined in task `vAIbe-studio 044`: comma-CSV proved inconvenient for ordinary opening in Excel on Windows/RU because the data collapsed into a single column. After that, the human-facing default was refined to `;` + `UTF-8 with BOM`.
