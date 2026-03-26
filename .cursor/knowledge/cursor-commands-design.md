# Cursor Commands — Design Best Practices

Reference for creating and maintaining `.cursor/commands/` wrappers.

## Command structure (template)

```markdown
# Command Name

## Description
Brief description of what the command does.

## Parameters
- `param1`: description

## Usage
Instructions with examples.

## Dependencies
What needs to be installed before use.
```

## Principles

1. **Clear naming**: `pdf-to-markdown.md`, `extract-data.md`
2. **Full documentation**: all parameters and examples
3. **Dependencies listed**: what packages are needed
4. **Error handling**: what to do when things go wrong

## In the context of Skills Architecture

Since Phase 1 of Task 018, commands in `.cursor/commands/` serve as **thin wrappers** that point to canonical skills in `.ai/skills/`. The wrapper should:

1. Provide a Quick Reference (numbered steps)
2. Reference the canonical skill: "Read and follow `.ai/skills/{skill}.md`"
3. Add Cursor-specific enhancements (e.g., AskQuestion usage)
4. Stay under 30 lines
