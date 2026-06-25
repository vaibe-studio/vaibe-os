---
name: batch-operations
description: Patterns for mass file and task operations across the vault. Reference material (non-actionable knowledge).
license: MIT
---

# Patterns for mass operations

Reference for performing batch operations (mass updates of files, tasks, projects) in vAIbe-OS. Based on practical experience standardizing tasks en masse across many projects.

## Core rule

> After any mass operation — a mandatory **full enumerate + verify** of every element.

Trust neither your memory, nor subagents, nor scripts — always verify the final result programmatically.

## Pattern: full verification

```
1. Get the FULL list of elements (Get-ChildItem / Glob)
2. For EACH, check the target condition (does the section exist? is the file in place?)
3. Compare: total == ok? If not — report issues
```

Example (PowerShell, checking `## Статус` in all task.md):
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Get-ChildItem -Path ".\Проекты" -Recurse -Filter "task.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -Encoding UTF8
    if ($content -notmatch "## Статус") { Write-Output "MISSING: $($_.FullName)" }
}
```

## Common mistakes

### 1. Skipping projects with parallel subagents

**Problem**: when distributing work across 4 subagents, one skipped a project due to encoding/path issues and did not report the error.

**Fix**: after all subagents finish — run a single verification script that enumerates ALL elements and checks each one.

### 2. Forgetting a project during manual enumeration

**Problem**: when manually distributing tasks across subagents, vAIbe-OS was missed (the 17th project out of 17).

**Fix**: always start with `Get-ChildItem -Path ".\Проекты" -Directory`, record the full list, then work from it.

### 3. Not checking edge cases

**Problem**: tasks without `results/`, tasks with inline results, tasks in the archive — all require different `## Статус` templates.

**Fix**: before a mass operation, build a taxonomy of variants and handle each.

## Parallelization recommendations

- At most 4 subagents at once (system limit)
- Give each subagent an explicit list of projects/tasks (not "the rest")
- After completion — a single verification outside the subagents
- Subagents with the `fast` model — for mass uniform edits (add a section, copy a file)

## Related rules

- `.vaibe/rules/powershell.md` — encoding for Cyrillic paths
- `.vaibe/rules/structure.md` — the `## Статус` standard in task.md
- `.vaibe/skills/task-execute/SKILL.md` — Step 7-8, result format
