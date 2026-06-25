# Interactive Patterns: structured user input

When a command requires user input, choose the right tool:

## Decision rule

| Input type | Tool | Example |
|---|---|---|
| Finite choices (select from list) | **Structured-choice tool call** | Project, role, priority, yes/no |
| Open-ended input (free text) | Plain text question | "Describe the task", "Any context?" |
| Mixed (choices + optional comment) | **Structured-choice tool call** for choices, then text follow-up if needed | |

## Structured choice — THIS IS A TOOL CALL, NOT A TEXT PATTERN

The structured-choice tool is **native to the IDE** and named differently across tools:

| Tool | Native structured-choice tool |
|---|---|
| Cursor | `AskQuestion` |
| Claude Code | `AskUserQuestion` |
| Others | equivalent native choice mechanism |

You MUST invoke it as a **tool call**, not describe it in text. When you need structured input from the user:
- **DO**: call the native choice tool with a `questions` array; each question has a header, prompt text, and `options[]` (min 2 options with a `label`)
- **DON'T**: describe the question format in text, render it as a table, or ask the user to respond in plain text

Group related choices into ONE call with multiple questions.

Typical grouping for task creation:
- Question 1: Project (list existing + "Other")
- Question 2: Priority (low / medium / high)
- Question 3: Proposed title (agree / suggest own)

For confirmations (yes/no/edit), use a SEPARATE choice-tool call after showing the plan in text.

### Task execution (the "plan" step)

Before the choice-tool call, a **complete markdown plan in the same reply is mandatory**: subtasks, files, complexity estimate, recommendations on open decisions. The choice widget is only for final answers (plan OK, execution mode, etc.), never for delivering the plan itself. The phrase "plan below" without the actual plan is an agent error, not a UI one (see the anti-pattern in the task-execution skill).

## Key rules

- ALWAYS invoke the structured-choice tool when options are finite — never ask "which project?" as plain text
- ALWAYS include an escape option ("Other", "Suggest own", "Edit")
- Present analysis and hypotheses as TEXT before the structured-choice tool call
- For task execution: present the **complete execution plan** as TEXT before the structured-choice tool call
- One structured-choice call per interaction step (don't split related choices across multiple calls)

## Graceful degradation

The structured-choice tool is not available in all models or sessions. If the call returns `Tool not found` (or an equivalent):

1. **Fall back to plain text** with numbered options:
   ```
   Choose a project:
   1. vAIbe-OS
   2. Альфа
   3. Other
   ```
2. **Do NOT** pretend the tool was used — be transparent about the fallback
3. **Do NOT** simulate the choice tool as a markdown table — use a simple numbered list

## Anti-patterns

- **Plan-only choice** (task execution) — calling the choice tool without the full plan in the message text; the user sees only the choice buttons. Fix: write the markdown plan first, then the choice tool or the numbered fallback.
- **Simulating the choice tool in text** — describing the question format as a table or markdown instead of calling the tool. This creates the illusion of interactivity without actual structured UI.
- **Asking finite-choice questions as plain text when the tool IS available** — e.g. "Which project? (A / B / C)" instead of a structured-choice tool call
- **Not attempting the tool at all** — always try the tool call first; fall back to text only if it fails
