from __future__ import annotations

import argparse
import runpy
import sys


def _configure_stdio() -> None:
    """
    PowerShell/Windows often runs with a legacy codepage (e.g., cp1251),
    which may crash on some unicode characters in help output.
    Make output robust.
    """
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def _run_module_as_main(module: str, argv: list[str]) -> int:
    """
    Execute `python -m <module> ...` programmatically.
    We forward args by temporarily overwriting sys.argv.
    """
    old_argv = sys.argv
    try:
        sys.argv = [module, *argv]
        runpy.run_module(module, run_name="__main__")
        return 0
    except SystemExit as e:
        # Propagate module's exit code if it used argparse/SystemExit.
        code = e.code
        if code is None:
            return 0
        if isinstance(code, int):
            return code
        return 1
    finally:
        sys.argv = old_argv


def main(argv: list[str] | None = None) -> int:
    _configure_stdio()

    ap = argparse.ArgumentParser(
        prog="python -m tools",
        description=(
            "Единая точка входа для утилит из папки tools/. "
            "Список и примеры: tools/TOOLS_INDEX.md"
        ),
    )

    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("index", help="Показать расположение индекса tools")
    p.set_defaults(_handler="index")

    p = sub.add_parser("markdown-to-pdf", help="Markdown -> PDF")
    p.add_argument("args", nargs=argparse.REMAINDER, help="Аргументы для tools.markdown_to_pdf")
    p.set_defaults(_handler="module", _module="tools.markdown_to_pdf")

    p = sub.add_parser("pdf-to-markdown", help="PDF -> Markdown (опционально OCR)")
    p.add_argument("args", nargs=argparse.REMAINDER, help="Аргументы для tools.pdf_to_markdown")
    p.set_defaults(_handler="module", _module="tools.pdf_to_markdown")

    p = sub.add_parser("yt-create-issues-from-meeting", help="Создать задачи YouTrack из meeting_tasks.md")
    p.add_argument("args", nargs=argparse.REMAINDER, help="Аргументы для tools.yt_create_issues_from_meeting")
    p.set_defaults(_handler="module", _module="tools.yt_create_issues_from_meeting")

    p = sub.add_parser("cursor-stats", help="Статистика использования Cursor (токены/стоимость)")
    p.add_argument("args", nargs=argparse.REMAINDER, help="Аргументы для tools.cursor_stats")
    p.set_defaults(_handler="module", _module="tools.cursor_stats")

    p = sub.add_parser("epk-select-leads", help="Выбрать лидов из CSV спикеров (EPK outreach)")
    p.add_argument("args", nargs=argparse.REMAINDER, help="Аргументы для tools/epk_outreach/select_leads.py")
    p.set_defaults(_handler="script", _script="tools/epk_outreach/select_leads.py")

    p = sub.add_parser("process-deferred-kb-source", help="Обработать отложенный KB-источник (конвейер)")
    p.add_argument("args", nargs=argparse.REMAINDER, help="Аргументы для tools/process_deferred_kb_source.py")
    p.set_defaults(_handler="script", _script="tools/process_deferred_kb_source.py")

    ns = ap.parse_args(argv)

    if ns._handler == "index":
        print("tools/TOOLS_INDEX.md")
        return 0

    if ns._handler == "module":
        return _run_module_as_main(ns._module, ns.args)

    if ns._handler == "script":
        # Run script via runpy to preserve relative imports if any (none expected).
        old_argv = sys.argv
        try:
            sys.argv = [ns._script, *ns.args]
            runpy.run_path(ns._script, run_name="__main__")
            return 0
        except SystemExit as e:
            code = e.code
            if code is None:
                return 0
            if isinstance(code, int):
                return code
            return 1
        finally:
            sys.argv = old_argv

    return 2


if __name__ == "__main__":
    raise SystemExit(main())

