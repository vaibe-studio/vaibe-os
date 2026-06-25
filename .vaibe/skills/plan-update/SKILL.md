---
name: plan-update
description: Create or update project management plan with task statuses and priorities. Triggers: plan, sprint plan, plan-update, обновить план, план проекта, точка сборки, личный план, план работ, сохрани план, сохрани в планы.
license: MIT
---

# Purpose

Create or update a snapshot management plan for a project, incorporating current task statuses, meeting outcomes, and priorities. Choose the right plan type for the situation.

This skill is for **project planning artifacts**. If the user needs a **cross-project managerial week** with owner map, waiting list, and live weekly control surface, use `.vaibe/skills/weekly-operating-sheet/SKILL.md` instead.

# When to use

- Start of a new sprint → **sprint plan**
- Strategic review, new phase, major changes → **full plan**
- Before important meeting, milestone, decision point → **checkpoint**
- User triggers `/plan-update`
- User requests to save/persist a generated plan or work list into the project → save to `Планы/`, **not** as a task in `Задачи/`

# When NOT to use

- User wants a secretary-style weekly operating sheet across multiple projects
- User explicitly asks for owner map / waiting list / live weekly management table
- The artifact is for the user's own weekly control rhythm rather than one project's execution plan

# Plan types

Three templates available. Reference: `База знаний/Планы — справочник обозначений.md`.

| Type | Template | When | Size |
|---|---|---|---|
| **Sprint plan** | `База знаний/Образец плана — спринт.md` | Weekly planning, "what to do now?" | 80-120 lines |
| **Full plan** | `База знаний/Образец плана — полный.md` | Phase start, strategy review, major changes | 150-250 lines |
| **Checkpoint** | `База знаний/Образец плана — точка сборки.md` | Pre-meeting, milestone, decision point | 100-150 lines |

Separate artifact for managerial work:
- **Operating sheet** → `.vaibe/skills/weekly-operating-sheet/SKILL.md` + `База знаний/Образец плана — управленческая неделя.md`

Decision tree:
```
Need to make decisions / prepare for a meeting?  → Checkpoint
Need full project picture (new phase, strategy)?  → Full plan
Just planning the week's work?                    → Sprint plan
Need a cross-project managerial control sheet?    → weekly-operating-sheet.md
```

# Inputs needed

- `Проекты/{PROJECT}/README.md` — goals, team, context
- `Проекты/{PROJECT}/Задачи/*/task.md` — canonical task cards
- `Проекты/{PROJECT}/Задачи/*/results/` — results presence
- `Проекты/{PROJECT}/Встречи/*/tasks.md`, `summary.md` — meeting outcomes
- `Проекты/{PROJECT}/Планы/` — previous plan versions
- Selected template from `База знаний/Образец плана — {тип}.md`

# Procedure

## Step 1 — Determine project

- If specified → proceed
- If not → show project list, ask user to select

**STOP — wait for selection.**

## Step 2 — Select plan type

Analyze context to recommend a type:
- User's request mentions meeting/decisions/review → **Checkpoint**
- User's request mentions strategy/phase/overview → **Full plan**
- Routine update, weekly planning → **Sprint plan**
- Cross-project week, owner map, waiting list, secretary-style control → **use `.vaibe/skills/weekly-operating-sheet/SKILL.md` instead**
- If unclear → ask user to choose

Read the selected template file.

## Step 3 — Check existing plans

- Scan `Проекты/{PROJECT}/Планы/`
- Find latest plan by version number
- No plans → N=1 (first plan); existing → N+1
- Plan type can change between versions

## Step 4 — Gather data

### 4a. Project metadata
- Goals, team, context from README.md

### 4b. Task inventory
- All tasks from `Задачи/*/task.md`
- Check `results/` for versioned subdirectories (`v1/`, `v2/`, ...)
- Note version count and latest version for each task

### 4c. Meeting outcomes
- Tasks and decisions from `Встречи/*/tasks.md`, `summary.md`

### 4d. Previous plan comparison
- Load latest plan for status comparison
- Find new tasks (in `Задачи/` but not in plan)
- Find missing tasks (in plan but not in `Задачи/` — mark "⚠️ requires check")

### 4e. Integrity pre-flight (G4 — uniqueness of task numbers)
- Before generating the plan, verify task-number uniqueness within the project (invariant **G4**): scan `Задачи/*/` dir names and confirm no two tasks share the same `{NUM}`.
- Fast check: `ls -1 Проекты/{PROJECT}/Задачи | sed -E 's/^([0-9]+)-.*/\1/' | sort | uniq -d` — any output = duplicate numbers; or rely on `uv run --project .vaibe/scripts/vault_lint .vaibe/scripts/vault_lint/main.py` (reports `[G4]` lines).
- If duplicates found → surface them in the plan as **⚠️ requires check** (blockers/reminders section) with both conflicting task titles, and propose a renumber fix. Do **not** silently pick one. Empirically (batch run 01.06.2026) ~30% of active projects carried a G4 duplicate that had gone unnoticed — the check pays for itself.

## Step 5 — Classify and prioritize

Statuses, priorities, AI capability levels defined in `База знаний/Планы — справочник обозначений.md`. Reference that file; do not duplicate the full legend in the plan.

## Step 6 — Generate plan

Follow the selected template. Key UX principles for all types — **"Inverted Pyramid"** (most important first, details last):

1. **TL;DR first** — 3-5 lines at the top: phase, focus, (blocker — conditional), progress. A person reading only this block should understand the current state. **The «Главный блокер» line is included only when a LIVE blocker exists.** If there are none, **omit the line entirely** — do not write «нет блокеров» and do not recap resolved decisions here. TL;DR must be scanned in seconds; a line that only says «всё хорошо» is noise, and settled decisions belong in the log at the bottom, not in the fastest-read block.
2. **Blockers & decisions second** — immediately after TL;DR. What must be resolved before or at the start of work. This is what a manager reads first. **This section holds only LIVE (open) items.** When the user resolves a blocker/decision, do **not** leave it in place with a ✅ checkbox / «Срок: закрыто» — that keeps a settled item in the highest-attention slot and dilutes focus. **Move it out** into a resolution log (e.g. a «✅ Снято / Принятые решения» block lower down, or the «Изменения с прошлого плана» section), carrying the decision text so nothing is lost (Law 5: additivity). If every blocker is resolved, collapse the section to a bare «Открытых блокеров нет» (or omit the section per the template) — nothing else. **No pointer to the log, no re-summary of the resolved decisions** — the log sits in the same plan and is self-evident; both a «см. лог ниже» pointer and a «решили X и Y» recap just refill the high-attention slot with settled content. The whole point is to free that slot. Same rule applies to the **Open questions** table — answered questions move to the resolved block, not a checkbox in place.
3. **Sprint focus by baskets** — group tasks into thematic baskets (e.g. "Billing / Infrastructure / Notifications" or "Backend / Frontend / ML") rather than flat priority lists. Baskets emerge from sprint planning context, not from a rigid template. Include a "Cross-cutting tasks" basket for items spanning multiple baskets. **Baskets hold only actionable tasks — open / in-progress.** When a task completes (mid-sprint or via the user closing it), do **not** leave it in the basket with a ✅ — a done item in the focus zone makes it harder to see what's still open. **Move it out** to the «Изменения с прошлого плана» / «Итоги (что сделано)» log, carrying the task link so the progress is recorded (Law 5: additivity). Same logic as blockers (item 2): the high-attention sections carry live items, the logs carry settled ones.
   - **Applies to a one-line «just close this task» actualization too — this is the recurring trap.** When the user says «актуализируй план, задача N закрыта», the move is **delete N's row from its basket** and (if not already there) add it to the log — **not** flip the row's status cell to ✅. A targeted edit is not an exemption: «закрыть задачу в плане» = «вынести из фокуса в лог», always. If you are editing a plan by hand without re-running the full skill, you still owe this rule. Regression repeated **three times** on the same plan (vAIbe-OS v12, 12.06.2026) — the rule existed in this skill but was bypassed each time during a «quick» manual edit that never loaded the skill.
   - **Self-enforcing guard (root-cause fix for the bypass).** The failure mode is structural: a one-line manual plan edit does not load `.vaibe/skills/plan-update/SKILL.md`, so the rule never reaches the agent. Therefore the rule must travel **with the artifact**. Every generated plan **must embed an HTML-comment guard directly above the «Фокус спринта» baskets** restating this rule (the sprint template `База знаний/Образец плана — спринт.md` carries it; keep it in the generated file — HTML comments are invisible in render but present when the agent Reads the file before editing). When you actualize an existing plan that lacks this guard, **add it**. Because the agent always Reads a file before Editing it, the guard lands in context exactly at the moment the mistake would be made — independent of whether the skill was loaded.
4. **Open questions aggregated** — collect unresolved questions from all recent meetings into a single table with source attribution (which meeting or plan raised it) and owner (who should answer).
5. **Changes section** — what changed since last plan, prominently placed but after the actionable content.
6. **Compact archive** — previous sprint results as bullet-list, not detailed tables. Goal: acknowledge what was done without distracting from the current sprint.
7. **Backlog at the bottom** — medium/long-term tasks in a compact table. Context only, not actionable.
8. **Reference legend** — link to `Планы — справочник обозначений.md`, never inline copy. Do not duplicate the legend in the plan body.
9. **Roadmap visual** — ASCII "ВЫ ЗДЕСЬ" for full plans and checkpoints (not required for sprint plans).
10. **Task references as links** — when mentioning a task by number, wrap the id in a markdown link to its `task.md`. Path is relative from `Проекты/{PROJECT}/Планы/{file}.md`: `../Задачи/{NUM}-{TITLE}/task.md`. **Формат: `[NNN](<../Задачи/{NUM}-{TITLE}/task.md>) — {Название}`**. Правила:
   - URL in CommonMark angle-bracket syntax `<...>` with raw spaces. **Not `%20`** — Cursor doesn't decode `%20` in click-to-open.
   - **Link text — digits only `[NNN]`, no backticks `[`NNN`]`**. Cursor has a parser bug: link text from a single code-span + URL in `<...>` breaks click-to-open (it includes `>` in the file name). See the anti-pattern below.
   - Leave Cyrillic, quotes, dashes, and `.` in paths as is.
   - Example: `[014](<../Задачи/014-Раздел «Команда» — фото и описания/task.md>) — Раздел «Команда»`.
   - Apply to: focus, backlog, completed, hold, metrics, week plan, reminders. The roadmap ASCII block is the only place where bare numbers are acceptable (link syntax breaks the box-drawing alignment).
11. **Priority by importance, not urgency (Eisenhower).** Order the blockers/decisions and focus baskets by **strategic importance**, not by which deadline is nearest. Before fixing #1, anchor it to the project's **README goal** (e.g. for a revenue-stage product the #1 is almost always first revenue / first paying client). A near-term external deadline (grant submission, event, demo day) is **urgent**, but it is usually a *means*, not the goal — place it as a time-critical item **subordinate** to the strategic #1. Distinguish **root cause vs symptom**: «нет выручки для гранта» is a symptom; «не запущены продажи» is the root. This trap is most acute for **checkpoint** plans, which are triggered *by* a deadline and therefore tempt the author to crown that deadline as the priority. Sanity check: would the stated #1 still be #1 if the deadline did not exist? If yes — correct; if no — re-rank.
12. **Every stated #1 priority must be a tracked task.** If the plan declares a top priority (e.g. «закрыть первый платный проект») that has **no task card** in `Задачи/`, flag it ⚠️ and recommend creating one — an untracked priority silently falls off the board.

## Step 7 — Save

File name: `План - {N} - {DD.MM.YYYY} - {TITLE}.md`
Path: `Проекты/{PROJECT}/Планы/`

Show plan to user and confirm before saving.

# Batch mode (multiple projects)

When the user asks to update plans for **many projects at once** (e.g. «обнови планы по всем проектам с активностью за месяц»), run a batch flow instead of repeating Step 1 per project:

1. **Compute the active set.** Determine which projects qualify (e.g. files touched in last N days). Exclude build/dependency noise — count only meaningful vault files (`*.md`, `*.csv` outside `node_modules/`, `.venv/`, `.nuxt/`, `dist/`). Show the candidate list with an activity signal so the user can trim it.
2. **Confirm scope + process ONCE** via structured options: which set of projects, and how to confirm saving. Because confirming N plans one-by-one is impractical, offer an explicit **batch save** option (generate and save all without per-plan stops). This is the only sanctioned way to waive the per-plan confirmation — never assume it.
3. **Parallelize.** Run one subagent per project, each executing this skill end-to-end (Steps 2–7) for its single project and saving its versioned plan. Each subagent must receive the link-formatting rules (Step 6, item 10) verbatim — they are the most common regression.
4. **Synthesize + verify.** After all complete, run a cross-file lint of the new plans for known anti-patterns: `%20` in links, backticks-only link text, absolute paths inside link targets, and G4 duplicates surfaced by subagents. Report the roll-up to the user.

Constraints: the «по умолчанию подтверждай сохранение» rule (`AGENTS.md`) still holds — batch mode only skips per-plan confirmation when the user explicitly picks the batch option. Plan type per project is still chosen per-context (auto), not forced uniform.

# Output format

- `Проекты/{PROJECT}/Планы/План - {N} - {DD.MM.YYYY} - {TITLE}.md`
- Changes relative to previous version highlighted
- Link to legend reference, not inline copy

# Quality bar

- [ ] Project selected with user confirmation
- [ ] Plan type appropriate for the situation
- [ ] TL;DR section present with phase, focus, blocker, progress
- [ ] All tasks from `Задачи/` reflected in plan
- [ ] New tasks (since last plan) explicitly noted
- [ ] Missing tasks marked with warning
- [ ] Priorities assigned per criteria
- [ ] **Blockers/baskets ranked by importance, not nearest deadline** — #1 anchored to README goal; urgent-but-non-strategic deadlines placed subordinate (Eisenhower). Sanity check applied: «would #1 still be #1 without the deadline?»
- [ ] **Stated #1 priority has a task card** (or is flagged ⚠️ to create one)
- [ ] **«Решения и блокеры» and «Открытые вопросы» contain only open items** — resolved ones moved to the decision log, not left in place with a ✅ checkmark (Step 6, item 2)
- [ ] **Sprint focus baskets contain only open / in-progress tasks** — completed ones moved to «Изменения / Итоги», not left with a ✅ in the basket (Step 6, item 3)
- [ ] Legend referenced, not duplicated
- [ ] Previous plans not modified (new version only)
- [ ] Every 3-digit task number in the plan is wrapped in a markdown link to `task.md` (exception — the ASCII roadmap). Quick check before saving: `grep -nE '\b[0-9]{3}\b' <plan.md>` outside the roadmap block — every match must be inside `[...](...)`.

# Related knowledge

- `.vaibe/skills/strategic-planning-convergence/SKILL.md` — why a strategic plan converges (meeting → plan → correction → rule loop), the deadline-removal test, and the mapping to the five ontological laws. Read before generating a **strategic/checkpoint** plan when a recent meeting exists.

# Anti-patterns

- Editing old plans retroactively (only create new versions)
- Auto-selecting project without asking
- Missing tasks from `Задачи/` in the plan
- Creating plan without checking meeting outcomes
- Duplicating full legend in the plan body (reference the shared file)
- Putting the week plan at the end (it should be near the top)
- Using the same template type when another fits better
- **Letting a deadline hijack the priority** — ranking blockers/baskets by the urgency of the nearest deadline instead of strategic importance. Classic case: a checkpoint driven by a grant deadline puts «submit the application» above «get first revenue», even though revenue is both the business goal (README) and the root way to de-risk the application itself. A deadline is urgent, the README goal is important; important comes first, urgent-but-non-strategic is a subordinate item. Regression 2026-06-01 (plan vAIbe-studio v8): the user went through `/evolve` to close this. Check: "would this item still be #1 if the deadline did not exist?"
- **Declaring priority #1 without a task card** — if the sprint's main goal is not captured as a task in `Задачи/`, it isn't tracked and drops out of focus. Flag ⚠️ and offer to create a card.
- **Plain task numbers without markdown links** — a task number in the plan without a `[...](...)` wrapper (see item 10 in § Generate plan and the Quality bar above). Regression 2026-05-18 — the user explicitly went through `/evolve` to close this.
- **`%20`-encoded spaces in vault links** — `[text](../Задачи/NUM-Имя%20с%20пробелами/task.md)` breaks click-to-open in Cursor (the literal path with `%20` doesn't exist on disk). Use the angle-bracket form with raw spaces: `[text](<../Задачи/NUM-Имя с пробелами/task.md>)`. Regression 2026-05-19 — the user went through `/evolve`. `%20` stays valid only for **HTTP URLs** (gitlab raw API in `.vaibe/rules/discovery.md`), not for local vault links.
- **Completed tasks left in the sprint focus baskets** — завершённая (✅) задача продолжает висеть в «Корзине» фокуса рядом с открытыми, мешая видеть, что ещё в работе. Правильно — **вынести** её в лог «Изменения с прошлого плана» / «Итоги (что сделано)» со ссылкой на `task.md`; корзины оставляют только открытые / в процессе. Та же логика, что и для блокеров. **Особо опасный подвид — точечная актуализация «задача N закрыта»:** соблазн просто сменить ячейку статуса на ✅ вместо удаления строки. Это та же ошибка. Регрессия **повторилась дважды на одном плане** (vAIbe-OS v12, 12.06.2026): правило уже было в skill, но при «быстрой» ручной правке без перезапуска skill оказалось проигнорировано → пользователь прошёл через `/evolve` повторно. Вывод: правило действует и для однострочных правок плана. См. Step 6, item 3.
- **Resolved blockers/decisions left checkboxed in the top section** — после того как пользователь дал ответ по блокеру в секции «Решения и блокеры» (или вопросу в «Открытые вопросы»), пометить его ✅ / «Срок: закрыто» **на месте**, оставив в самом верху плана. Решённый пункт продолжает висеть в зоне максимального внимания и отвлекает от фокуса. Правильно — **вынести** его в лог решений («✅ Снято / Принятые решения» или «Изменения с прошлого плана»), сохранив текст решения; верхнюю секцию свернуть до «Открытых блокеров нет», если все закрыты. **Обратный перегиб тоже неверен:** в свёрнутом заголовке не пересказывать, что именно решили («приняли X и Y»), и не ставить указатель «см. лог ниже» — лог в том же плане, самоочевиден; и пересказ, и указатель снова забивают слот улажённым. Достаточно голого «Открытых блокеров нет». **А в TL;DR строку «Главный блокер» при отсутствии блокеров вообще не выводить** (ни «нет блокеров», ни пересказа решений) — TL;DR читается за секунды, см. Step 6, item 1. Регрессия 12.06.2026 (план vAIbe-OS v12) — пользователь прошёл через `/evolve` трижды (вынос → анти-тавтология в секции → удаление строки из TL;DR). См. Step 6, items 1–2.
- **Backticks-only link text + angle-bracket URL** — `` [`025`](<../path>) `` ломает click-to-open в Cursor: парсер не распознаёт angle-brackets как разделитель URL, когда link text — единственный code-span, и включает `>` в путь («Unable to open 'task.md>'»). Эмпирически проверено 19.05.2026 (тестовый файл `_test-link-formats.md`). Любая из модификаций снимает баг: убрать backticks (`[025](<...>)`), добавить текст после backticks (`[`025` — Title](<...>)`), или сменить `` `…` `` на HTML `<code>…</code>`. **Принятое правило vAIbe-OS — без backticks**: ID задачи в планах — это порядковый номер, моноширинный шрифт не нужен. Регрессия закрыта 19.05.2026 через `/evolve`.
