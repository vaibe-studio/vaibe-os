---
name: personal-budget
description: Analyze personal spending history, build a calibrated budget with expense scenarios, and generate a ready-to-use Google Sheets tracker via Apps Script. Triggers: бюджет, личные финансы, расходы, burn rate, personal budget, финансовый план, учёт расходов, экономия.
license: MIT
---

# Purpose

Turn raw spending history into an actionable personal budget: analyze patterns, calibrate via interview, build plan/fact tracker, generate a formatted Google Sheets workbook.

# When to use

- User wants to plan personal finances for a transition period (job change, relocation, startup)
- User has a spending history (xlsx/csv/Google Sheets) and wants to understand real burn rate
- User needs a practical tool for weekly expense tracking
- User mentions "бюджет", "расходы", "финансовый план", "burn rate"

# Procedure

## Step 1 — Import spending history

1. Locate the file (Inbox, attached, or link to Google Sheets)
2. Read structure with `openpyxl` (xlsx) or `csv` module — identify sheets, categories, time periods
3. Handle encoding issues (Windows console vs UTF-8) — always use `sys.stdout.reconfigure(encoding='utf-8')`
4. Extract per-month totals and per-category breakdowns

**Key data to extract:**
- Monthly totals (ИТОГО row)
- Group subtotals (Фиксированные / Приоритетные / Вторичные / Карманные)
- Individual category amounts (column G or equivalent summary column)

## Step 2 — Analytical report

Create `анализ-расходов.md` with:

1. **Monthly overview table** — all months × 4 groups × total
2. **Aggregates** — mean, median, min, max
3. **Per-category breakdown** — mean, median, min, max for each category
4. **Comparison with existing financial model** (if one exists) — identify gaps between assumptions and reality
5. **Optimization zones** — rank categories by savings potential (high / medium / low)

Structure optimization zones as:
- High potential: lifestyle expenses that can be cut without affecting health/work
- Medium potential: discretionary spending that can be deferred
- Low potential: fixed obligations and health-related spending

## Step 3 — Calibration interview

Use the structured-question tool (Cursor `AskQuestion`, Claude Code `AskUserQuestion`, or the IDE equivalent — see `.vaibe/rules/interactive-patterns.md`) in blocks of 4-5 questions. Group by expense type:

**Block 1 — Lifestyle (largest savings potential):**
- Each category: show current average, offer 4-5 reduction options with concrete descriptions
- Include "don't touch" option for every category

**Block 2 — Discretionary:**
- Same format; include "freeze for N months" option

**Block 3 — Fixed / priorities / clarifications:**
- Rent (current and planned), credit obligations, income sources
- Actual starting balance (often differs from assumptions)

**Important:** accept free-text answers — user may not fit into options.

## Step 4 — Personalized budget

Create `бюджет-{имя}-{период}.md` with:

1. **Single target regime** based on interview answers (not 3 abstract scenarios)
2. **Monthly table** — month × categories × plan amounts, accounting for:
   - City changes (rent, food price differences)
   - One-time events (relocation, double rent)
   - Pre-paid obligations (already paid months)
3. **P&L projection** — overlay income scenarios from financial model:
   - Realistic (scenario B)
   - Pessimistic (scenario C)
   - Zero-income stress test
4. **Break-even points** — monthly income needed per city (including tax)
5. **Balance trajectory** — show minimum balance point and whether starting balance survives
6. **Risk matrix** — checkpoints with dates and threshold actions
7. **Partner overlay estimate** (if applicable) — preliminary 50/50 split calculation

## Step 5 — Google Sheets generator

Create `setup-budget.gs` (Google Apps Script) that generates a complete workbook:

**Required sheets:**

| Sheet | Purpose | Key features |
|-------|---------|-------------|
| Дашборд | Summary view | Plan/fact for expenses and income, balance with conditional formatting (red <50K, yellow 50-150K, green >150K), checkpoints |
| План | Budget by category | Groups color-coded, plan + fact columns side by side, ИТОГО with SUM formulas, conditional formatting (fact > plan = red) |
| Учёт | Weekly tracker | 5 rows per week for entries, category dropdown, weekly subtotals (formula), month subtotals, month-color coding |
| Доходы | Income by channel | Channels × months, plan/fact, status dropdown (план/ожидание/получено/отменено), monthly totals |
| Категории | Reference | Groups, categories, type (fixed/variable), budget per city, description. Protected sheet |

**Formatting requirements:**
- Tab colors per sheet (blue, green, yellow, green, gray)
- Group background colors (fixed=blue, priority=green, secondary=orange, pocket=pink, infra=purple)
- Number format `#,##0` for amounts, `#,##0 ₽` for balances
- Frozen header rows
- Column widths set for readability
- Data validation dropdowns for categories and statuses

## Step 6 — Process checklist

Create `чек-лист-ведения-бюджета.md` with:

1. **Setup instructions** — how to deploy the Apps Script
2. **Weekly ritual** (~15 min) — collect bank statement, fill tracker, compare with plan, update dashboard
3. **Monthly ritual** (~30 min) — plan vs fact summary, checkpoint evaluation, plan adjustment
4. **Categorization rules** — table mapping ambiguous expenses to categories
5. **Alarm signals** — balance thresholds and corresponding actions

## Step 7 — Update task status

- Set task status to `в процессе`
- Update `## Прогресс` section with completed and remaining items

# Output format

Files in task's `results/v{N}/`:

| File | Format |
|------|--------|
| `анализ-расходов-{имя}.md` | Markdown with tables |
| `бюджет-{имя}-{период}.md` | Markdown with tables |
| `sheets/setup-budget.gs` | Google Apps Script |
| `чек-лист-ведения-бюджета.md` | Markdown |

# Quality bar

- [ ] Historical data analyzed (all available months)
- [ ] Real burn rate vs assumptions compared (if financial model exists)
- [ ] User interviewed on spending preferences (not just generic scenarios)
- [ ] Budget uses user's actual answers, not template values
- [ ] Starting balance is verified with user (not assumed)
- [ ] P&L covers at least 2 income scenarios + stress test
- [ ] Break-even calculated with tax
- [ ] Google Sheets script creates formatted workbook with formulas and dropdowns
- [ ] Weekly tracking process documented

# Anti-patterns

- Using assumed amounts instead of asking the user
- Building 3 abstract scenarios without user calibration
- Generating CSV without formatting (unusable in practice)
- Ignoring tax when calculating break-even
- Treating average as representative when variance is high (use median)
- Forgetting to verify starting balance (often drastically different from plan)

# Related knowledge

- `.vaibe/skills/startup-financial-modeling/SKILL.md` — unit economics, P&L structure, pricing
- `.vaibe/skills/strategy-frameworks/SKILL.md` — SWOT, BMC for strategic context
