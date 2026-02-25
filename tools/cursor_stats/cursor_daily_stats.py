#!/usr/bin/env python3
"""
Cursor Daily Token Statistics

Получает статистику использования токенов Cursor за текущий день.

Usage:
    python -m tools.cursor_stats
    python -m tools.cursor_stats --date 2026-01-27
"""

from __future__ import annotations

import argparse
import csv
import io
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from collections import defaultdict

import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cursor API endpoint
CURSOR_API_URL = "https://cursor.com/api/dashboard/export-usage-events-csv"


@dataclass
class UsageEvent:
    """Represents a single usage event from Cursor API."""
    timestamp: datetime
    model: str
    tokens: int
    cost: float
    request_type: str = ""
    
    @classmethod
    def from_csv_row(cls, row: dict) -> Optional["UsageEvent"]:
        """Parse a CSV row into UsageEvent."""
        try:
            # Parse timestamp - handle various formats
            timestamp_str = row.get('timestamp', row.get('time', row.get('date', '')))
            if timestamp_str:
                # Try parsing ISO format first
                try:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                except ValueError:
                    # Try parsing as Unix timestamp (milliseconds)
                    try:
                        timestamp = datetime.fromtimestamp(int(timestamp_str) / 1000, tz=timezone.utc)
                    except (ValueError, TypeError):
                        timestamp = datetime.now(timezone.utc)
            else:
                timestamp = datetime.now(timezone.utc)
            
            # Get model name
            model = row.get('model', row.get('modelName', 'unknown'))
            
            # Get tokens - try various column names
            tokens_str = row.get('tokens', row.get('totalTokens', row.get('inputTokens', '0')))
            tokens = int(float(tokens_str)) if tokens_str else 0
            
            # Get cost
            cost_str = row.get('cost', row.get('price', row.get('amount', '0')))
            cost = float(cost_str) if cost_str else 0.0
            
            # Get request type
            request_type = row.get('type', row.get('requestType', ''))
            
            return cls(
                timestamp=timestamp,
                model=model,
                tokens=tokens,
                cost=cost,
                request_type=request_type
            )
        except Exception as e:
            logger.warning(f"Failed to parse row: {row}, error: {e}")
            return None


@dataclass
class UsageStats:
    """Aggregated usage statistics."""
    date: str
    total_tokens: int = 0
    total_cost: float = 0.0
    total_requests: int = 0
    by_model: dict = field(default_factory=lambda: defaultdict(lambda: {"tokens": 0, "cost": 0.0, "requests": 0}))
    events: list = field(default_factory=list)
    
    def add_event(self, event: UsageEvent):
        """Add an event to statistics."""
        self.total_tokens += event.tokens
        self.total_cost += event.cost
        self.total_requests += 1
        
        self.by_model[event.model]["tokens"] += event.tokens
        self.by_model[event.model]["cost"] += event.cost
        self.by_model[event.model]["requests"] += 1
        
        self.events.append(event)
    
    def to_markdown(self) -> str:
        """Format statistics as Markdown."""
        lines = [
            f"# Статистика токенов Cursor за {self.date}",
            "",
            "## Резюме",
            f"- **Всего токенов:** {self.total_tokens:,}",
            f"- **Общая стоимость:** ${self.total_cost:.4f}",
            f"- **Запросов:** {self.total_requests}",
            "",
        ]
        
        # By model table
        if self.by_model:
            lines.extend([
                "## По моделям",
                "",
                "| Модель | Токены | Стоимость | Запросы |",
                "|--------|--------|-----------|---------|",
            ])
            
            for model, stats in sorted(self.by_model.items(), key=lambda x: x[1]["tokens"], reverse=True):
                lines.append(
                    f"| {model} | {stats['tokens']:,} | ${stats['cost']:.4f} | {stats['requests']} |"
                )
            lines.append("")
        
        # Detailed events table
        if self.events:
            lines.extend([
                "## Детальная таблица запросов",
                "",
                "| Время | Модель | Токены | Стоимость |",
                "|-------|--------|--------|-----------|",
            ])
            
            # Sort events by timestamp
            sorted_events = sorted(self.events, key=lambda e: e.timestamp)
            
            for event in sorted_events:
                time_str = event.timestamp.strftime("%H:%M:%S")
                lines.append(
                    f"| {time_str} | {event.model} | {event.tokens:,} | ${event.cost:.4f} |"
                )
            lines.append("")
        
        return "\n".join(lines)


def get_day_timestamps(date: Optional[datetime] = None) -> tuple[int, int]:
    """
    Get start and end timestamps for a given day in milliseconds.
    
    Args:
        date: Date to get timestamps for (defaults to today)
        
    Returns:
        Tuple of (start_ms, end_ms)
    """
    if date is None:
        date = datetime.now(timezone.utc)
    
    # Start of day (00:00:00)
    start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # End of day (23:59:59.999)
    end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    start_ms = int(start_of_day.timestamp() * 1000)
    end_ms = int(end_of_day.timestamp() * 1000)
    
    return start_ms, end_ms


def fetch_usage_data(auth_cookie: str, start_ms: int, end_ms: int) -> Optional[str]:
    """
    Fetch usage data from Cursor API.
    
    Args:
        auth_cookie: Authorization cookie value
        start_ms: Start timestamp in milliseconds
        end_ms: End timestamp in milliseconds
        
    Returns:
        CSV data as string or None on failure
    """
    params = {
        "startDate": start_ms,
        "endDate": end_ms,
        "strategy": "tokens"
    }
    
    # Prepare cookies - the cookie name may vary
    cookies = {}
    
    # If the cookie value contains '=', assume it's a full cookie string
    if '=' in auth_cookie and not auth_cookie.startswith('eyJ'):
        # Parse as "name=value" or "name=value; name2=value2"
        for part in auth_cookie.split(';'):
            part = part.strip()
            if '=' in part:
                name, value = part.split('=', 1)
                cookies[name.strip()] = value.strip()
    else:
        # Assume it's just the token value for WorkosCursorSessionToken
        cookies['WorkosCursorSessionToken'] = auth_cookie
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Accept': 'text/csv,application/csv,*/*',
    }
    
    try:
        logger.debug(f"Fetching data from {CURSOR_API_URL}")
        logger.debug(f"Params: startDate={start_ms}, endDate={end_ms}")
        
        response = requests.get(
            CURSOR_API_URL,
            params=params,
            cookies=cookies,
            headers=headers,
            timeout=30
        )
        
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '')
        logger.debug(f"Response Content-Type: {content_type}")
        logger.debug(f"Response length: {len(response.text)} bytes")
        
        return response.text
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            logger.error("Ошибка авторизации. Проверьте CURSOR_AUTH_COOKIE в .env файле.")
            logger.error("Инструкция по получению cookie:")
            logger.error("  1. Откройте cursor.com в браузере и войдите в аккаунт")
            logger.error("  2. DevTools (F12) → Application → Cookies → cursor.com")
            logger.error("  3. Скопируйте значение WorkosCursorSessionToken")
        else:
            logger.error(f"HTTP ошибка: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка сети: {e}")
        return None


def parse_csv_data(csv_data: str) -> list[UsageEvent]:
    """
    Parse CSV data into list of UsageEvents.
    
    Args:
        csv_data: Raw CSV string
        
    Returns:
        List of UsageEvent objects
    """
    events = []
    
    if not csv_data or not csv_data.strip():
        logger.warning("Empty CSV data received")
        return events
    
    try:
        # Try to detect delimiter
        first_line = csv_data.split('\n')[0]
        delimiter = ',' if ',' in first_line else '\t' if '\t' in first_line else ','
        
        reader = csv.DictReader(io.StringIO(csv_data), delimiter=delimiter)
        
        logger.debug(f"CSV columns: {reader.fieldnames}")
        
        for row in reader:
            event = UsageEvent.from_csv_row(row)
            if event:
                events.append(event)
        
        logger.info(f"Parsed {len(events)} usage events")
        
    except Exception as e:
        logger.error(f"Failed to parse CSV: {e}")
        logger.debug(f"CSV data preview: {csv_data[:500]}")
    
    return events


def get_daily_stats(auth_cookie: str, date: Optional[datetime] = None) -> Optional[UsageStats]:
    """
    Get daily usage statistics.
    
    Args:
        auth_cookie: Cursor auth cookie
        date: Date to get stats for (defaults to today)
        
    Returns:
        UsageStats object or None on failure
    """
    if date is None:
        date = datetime.now(timezone.utc)
    
    date_str = date.strftime("%Y-%m-%d")
    logger.info(f"Fetching stats for {date_str}")
    
    start_ms, end_ms = get_day_timestamps(date)
    
    csv_data = fetch_usage_data(auth_cookie, start_ms, end_ms)
    if csv_data is None:
        return None
    
    events = parse_csv_data(csv_data)
    
    stats = UsageStats(date=date_str)
    for event in events:
        stats.add_event(event)
    
    return stats


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Get Cursor token usage statistics for a day',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m tools.cursor_stats
  python -m tools.cursor_stats --date 2026-01-27
  python -m tools.cursor_stats -v
        """
    )
    
    parser.add_argument(
        '--date',
        type=str,
        help='Date to get stats for (YYYY-MM-DD format, defaults to today)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--raw',
        action='store_true',
        help='Output raw CSV data instead of formatted report'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Load .env file
    workspace_root = Path(__file__).parent.parent.parent
    env_file = workspace_root / '.env'
    if env_file.exists():
        load_dotenv(env_file)
        logger.debug(f"Loaded .env from {env_file}")
    
    # Get auth cookie
    auth_cookie = os.getenv('CURSOR_AUTH_COOKIE')
    if not auth_cookie:
        logger.error("CURSOR_AUTH_COOKIE не установлен.")
        logger.error("")
        logger.error("Для настройки:")
        logger.error("  1. Откройте cursor.com в браузере и войдите в аккаунт")
        logger.error("  2. DevTools (F12) → Application → Cookies → cursor.com")
        logger.error("  3. Скопируйте значение WorkosCursorSessionToken")
        logger.error("  4. Добавьте в .env: CURSOR_AUTH_COOKIE=ваше_значение")
        return 1
    
    # Parse date if provided
    target_date = None
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            logger.error(f"Invalid date format: {args.date}. Use YYYY-MM-DD.")
            return 1
    
    # If raw mode, just fetch and print CSV
    if args.raw:
        if target_date is None:
            target_date = datetime.now(timezone.utc)
        start_ms, end_ms = get_day_timestamps(target_date)
        csv_data = fetch_usage_data(auth_cookie, start_ms, end_ms)
        if csv_data:
            print(csv_data)
            return 0
        return 1
    
    # Get stats
    stats = get_daily_stats(auth_cookie, target_date)
    
    if stats is None:
        logger.error("Не удалось получить статистику")
        return 1
    
    # Output report
    print(stats.to_markdown())
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
