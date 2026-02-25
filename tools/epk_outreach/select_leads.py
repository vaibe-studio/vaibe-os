"""
Select a balanced set of outreach leads from a speakers CSV.

Input CSV columns (expected):
  - ФИО, Должность, Компания, Сегмент, Источник, Тема доклада

Usage (PowerShell):
  python tools/epk_outreach/select_leads.py --csv-auto --per-segment 15
  python tools/epk_outreach/select_leads.py --csv \"C:\\path\\to\\file.csv\" --per-segment 15
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal


Segment = Literal["A", "B"]


@dataclass(frozen=True)
class Lead:
    fio: str
    role: str
    company: str
    industry: str
    segment: str
    linkedin: str
    email: str
    phone: str
    source: str
    topic: str


def _norm(s: str | None) -> str:
    return (s or "").strip()


def read_leads(csv_path: Path) -> list[Lead]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        leads: list[Lead] = []
        for r in reader:
            leads.append(
                Lead(
                    fio=_norm(r.get("ФИО")),
                    role=_norm(r.get("Должность")),
                    company=_norm(r.get("Компания")),
                    industry=_norm(r.get("Отрасль")),
                    segment=_norm(r.get("Сегмент")),
                    linkedin=_norm(r.get("LinkedIn")),
                    email=_norm(r.get("Email")),
                    phone=_norm(r.get("Телефон")),
                    source=_norm(r.get("Источник")),
                    topic=_norm(r.get("Тема доклада")),
                )
            )
    return leads


def _repo_root() -> Path:
    # tools/epk_outreach/select_leads.py -> repo root is 2 levels up from tools/
    return Path(__file__).resolve().parents[2]


def auto_detect_csv() -> Path:
    """
    Try to find the most likely speakers CSV inside repo root /Инбокс/.
    We avoid requiring Cyrillic paths on the command line (Windows/PowerShell encoding quirks).
    """
    inbox = _repo_root() / "Инбокс"
    if not inbox.exists():
        raise FileNotFoundError(f"Inbox folder not found: {inbox}")

    csv_files = sorted(inbox.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not csv_files:
        raise FileNotFoundError(f"No .csv files found in: {inbox}")

    expected = {"ФИО", "Должность", "Компания", "Сегмент", "Источник", "Тема доклада"}

    best: tuple[int, float, Path] | None = None
    for p in csv_files:
        try:
            with p.open("r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                headers = set(reader.fieldnames or [])
        except Exception:
            continue

        # Score by header match + filename hints + recency.
        header_score = len(expected.intersection(headers))
        name = p.name.lower()
        name_score = 0
        if "епк" in name:
            name_score += 2
        if "спик" in name:
            name_score += 1
        if "лид" in name:
            name_score += 1

        score = header_score * 10 + name_score
        mtime = p.stat().st_mtime
        cand = (score, mtime, p)
        if best is None or cand > best:
            best = cand

    if best is None:
        raise FileNotFoundError(f"Could not parse any CSV in: {inbox}")
    return best[2]


def default_exclude_regex() -> re.Pattern[str]:
    # Keep it conservative: focus on “рыба помельче” while explicitly excluding CEO/CMO.
    # - CEO equivalents: CEO / Генеральный директор / Президент / Основатель / Глава / Председатель / Министр
    # - CMO equivalents: Директор по маркетингу, маркетинговым коммуникациям, зам. директора по маркетингу
    # - Often too senior for “warm-up”: VP / board member
    pattern = (
        r"\bCEO\b|"
        r"генеральн(ый|ого)\s+директор|"
        r"\bпрезидент\b|"
        r"основател(ь|ница)|"
        r"\bглава\b|"
        r"\bпредседател(ь|я)\b|"
        r"министр|"
        r"директор\s+по\s+маркетинг|"
        r"маркетингов(ых|ым)\s+коммуникац|"
        r"заместитель\s+директора\s+по\s+маркетин|"
        r"вице-?президент|"
        r"член\s+правления"
    )
    return re.compile(pattern, re.IGNORECASE)


def default_exclude_company_regex() -> re.Pattern[str]:
    """
    Exclude existing customers / groups we don't want to outreach in the warm-up wave.
    Current default: X5 Group and its major subsidiaries / brands.
    """
    pattern = (
        r"\bX5\b|"
        r"\bX5\s*Group\b|"
        r"\bX5\s*Tech\b|"
        r"\bX5\s*Digital\b|"
        r"\bХ5\b|"
        r"\bХ5\s*Group\b|"
        r"\bХ5\s*Tech\b|"
        r"\bПят[её]рочк[а-и]\b|"
        r"\bПерекр[её]ст[оё]к\b|"
        r"\bЧижик\b|"
        r"\bX5\s*Еда\b|"
        r"\bХ5\s*Еда\b"
    )
    return re.compile(pattern, re.IGNORECASE)


def score_lead(lead: Lead) -> int:
    role_l = lead.role.lower()
    t = f"{lead.topic} {lead.source}".lower()

    score = 0

    # Seniority + likelihood of being a decision influencer (but not CEO/CMO).
    if any(k in role_l for k in ["директор", "руководител", "начальник", "head", "лидер", "департамент", "служб", "управлен"]):
        score += 3

    # Relevance to comms/CX/CRM/data where EPK themes are natural.
    if any(
        k in role_l
        for k in [
            "cx",
            "клиентск",
            "crm",
            "cvm",
            "лояльн",
            "коммуникац",
            "аналит",
            "исслед",
            "данн",
            "ai",
            "ml",
            "ux",
            "digital",
            "онлайн",
            "сервис",
        ]
    ):
        score += 4

    if any(k in t for k in ["cx", "омник", "клиент", "лояль", "crm", "cvm", "персонал", "данн", "ai", "ml", "аналит", "канал", "total experience"]):
        score += 2

    # Deprioritize less relevant functions for an EPK comms interview warm-up wave.
    if any(k in role_l for k in ["персонал", "hr", "логист", "закуп", "финанс", "юрист"]):
        score -= 2

    # Company/segment doesn't affect score (balance is handled separately).
    return score


def pick_balanced(
    leads: Iterable[Lead],
    *,
    per_segment: int,
    exclude: re.Pattern[str],
    exclude_company: re.Pattern[str] | None = None,
    segments: tuple[Segment, ...] = ("A", "B"),
) -> list[tuple[int, Lead]]:
    candidates: list[tuple[int, Lead]] = []
    for l in leads:
        if l.segment not in segments:
            continue
        if exclude.search(l.role):
            continue
        if exclude_company and exclude_company.search(l.company):
            continue
        candidates.append((score_lead(l), l))

    candidates.sort(key=lambda x: x[0], reverse=True)

    picked: list[tuple[int, Lead]] = []
    counts = {s: 0 for s in segments}
    seen: set[tuple[str, str]] = set()

    for sc, l in candidates:
        if counts[l.segment] >= per_segment:
            continue
        key = (l.fio, l.company)
        if key in seen:
            continue
        seen.add(key)
        counts[l.segment] += 1
        picked.append((sc, l))
        if all(counts[s] >= per_segment for s in segments):
            break

    return picked


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=None, help="Path to speakers CSV")
    ap.add_argument("--csv-auto", action="store_true", help="Auto-detect speakers CSV in repo root /Инбокс/")
    ap.add_argument("--per-segment", type=int, default=15, help="How many leads to select per segment (A and B)")
    ap.add_argument(
        "--exclude-regex",
        default=None,
        help="Override exclude regex (Python regex). If omitted, a safe default is used.",
    )
    ap.add_argument(
        "--exclude-company-regex",
        default=None,
        help="Exclude companies by regex (Python regex). If omitted, a safe default is used (X5 group brands).",
    )
    args = ap.parse_args(argv)

    if args.csv:
        csv_path = Path(args.csv)
    elif args.csv_auto:
        try:
            csv_path = auto_detect_csv()
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2
    else:
        print("ERROR: Provide --csv or use --csv-auto", file=sys.stderr)
        return 2

    if not csv_path.exists():
        print(f"ERROR: CSV not found: {csv_path}", file=sys.stderr)
        return 2

    exclude = re.compile(args.exclude_regex, re.IGNORECASE) if args.exclude_regex else default_exclude_regex()
    exclude_company = (
        re.compile(args.exclude_company_regex, re.IGNORECASE)
        if args.exclude_company_regex
        else default_exclude_company_regex()
    )
    leads = read_leads(csv_path)
    picked = pick_balanced(leads, per_segment=args.per_segment, exclude=exclude, exclude_company=exclude_company)

    a = sum(1 for _, l in picked if l.segment == "A")
    b = sum(1 for _, l in picked if l.segment == "B")
    print(f"CSV\t{csv_path}")
    print(f"Picked\t{len(picked)}\tA\t{a}\tB\t{b}")
    print("N\tScore\tСегмент\tФИО\tДолжность\tКомпания\tИсточник\tТема доклада")
    for i, (sc, l) in enumerate(picked, 1):
        print(f"{i}\t{sc}\t{l.segment}\t{l.fio}\t{l.role}\t{l.company}\t{l.source}\t{l.topic}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

