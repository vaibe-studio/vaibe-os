# Discovery: verifying search results

Goal: avoid false conclusions that a file, folder, task, or project is absent due to the limitations of a single search tool. For the vault, a false negative is a **critical error**: better one extra check than a missed item.

## Core rule

You **must not** conclude that a "file / folder is absent" based on a single search tool.

- If `Glob`, `Grep`, or another search returns an empty or suspicious result — **always** run a fallback check by a different means: an alternative search (`rg`), reading by the expected path, a scoped directory listing.
- If the user has already stated that a file/folder exists — re-verify by several means first, and only then conclude there is a discrepancy.
- If an **exact path** is given — first try `Read` on that path; for ignored paths this works even when search returns empty.

## Why search yields false-empty results

Native IDE search tools (Glob/Grep and analogues) may **fail to find** existing files for two reasons:

1. **Cyrillic in paths.** On some platforms (especially Windows) the indexer fails to find files with Cyrillic names — the bug is independent of terminal settings or code pages. The pattern is unpredictable: some files are found, some are not.
2. **Ignore-aware.** Search respects `.gitignore`: directories with a `*` pattern (e.g. `Инбокс/`) or personal projects under the `/Проекты/*Личное*/` pattern will be **empty** for search, even though the files exist.

## High false-negative-risk zones

For these zones, **do not rely on a single discovery tool**:

- `Проекты/*Личное*` (personal projects under a `.gitignore` pattern)
- `Проекты/_Архив/` (archives, excluded from Git)
- `База знаний/Личное/` (personal materials)
- `Инбокс/` (the `*` pattern in `.gitignore`)
- any path with Cyrillic segments

## Verification methods

1. **Read by exact path** — `Read` the target file (works even for ignored paths).
2. **Alternative search** — `rg` instead of Glob or vice versa; a scoped search over a specific directory.
3. **Directory listing via the OS** — e.g. Python `os.listdir()` (reliable for Unicode names) or PowerShell with `[Console]::OutputEncoding = UTF8`.

> Platform-specific recipes for Windows (encodings, Unicode escapes, listing directories with Cyrillic names) — in `.vaibe/rules/powershell.md`.

## Related
- Windows specifics of file operations and encodings: `.vaibe/rules/powershell.md`
- Cross-platform git work (Cyrillic paths, case): `.vaibe/rules/git-cross-platform.md`
