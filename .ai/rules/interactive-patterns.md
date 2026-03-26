# Interactive Patterns: structured user input

When a command requires user input, choose the right tool:

## Decision rule

| Input type | Tool | Example |
|---|---|---|
| Finite choices (select from list) | **AskQuestion tool call** | Project, role, priority, yes/no |
| Open-ended input (free text) | Plain text question | "Describe the task", "Any context?" |
| Mixed (choices + optional comment) | **AskQuestion tool call** for choices, then text follow-up if needed | |

## AskQuestion — THIS IS A TOOL CALL, NOT A TEXT PATTERN

**AskQuestion is a native Cursor tool.** You MUST invoke it as a tool call (`AskQuestion`), not describe it in text.

When you need structured input from the user:
- **DO**: Call the AskQuestion tool with `questions` array containing `id`, `prompt`, `options[]`
- **DON'T**: Describe the AskQuestion format in text, render it as a table, or ask the user to respond in plain text

Group related choices into ONE AskQuestion call with multiple questions.
Each question needs: `id`, `prompt`, `options[]` (min 2 options with `id` + `label`).

Typical grouping for `/task-create`:
- Question 1: Project (list existing + "Other")
- Question 2: Priority (low / medium / high)
- Question 3: Proposed title (agree / suggest own)

For confirmations (yes/no/edit), use a SEPARATE AskQuestion tool call after showing the plan in text.

## Key rules

- ALWAYS invoke the AskQuestion tool when options are finite — never ask "which project?" as plain text
- ALWAYS include an escape option ("Other", "Suggest own", "Edit")
- Present analysis and hypotheses as TEXT before the AskQuestion tool call
- One AskQuestion call per interaction step (don't split related choices across multiple calls)

## Graceful degradation

AskQuestion may not be available in all models or sessions. If a tool call to AskQuestion returns `Tool not found`:

1. **Fall back to plain text** with numbered options:
   ```
   Выберите проект:
   1. МойПроект
   2. Проект-Альфа
   3. Другой
   ```
2. **Do NOT** pretend AskQuestion was used — be transparent about the fallback
3. **Do NOT** simulate AskQuestion as a markdown table — use a simple numbered list

See `.cursor/knowledge/cursor-tool-availability.md` for the tool availability matrix by model.

## Anti-patterns

- **Simulating AskQuestion in text** — describing the question format as a table or markdown instead of calling the tool. This creates the illusion of interactivity without actual structured UI.
- **Asking finite-choice questions as plain text when AskQuestion IS available** — e.g. "Which project? (A / B / C)" instead of an AskQuestion tool call
- **Not attempting AskQuestion at all** — always try the tool call first; fall back to text only if it fails
