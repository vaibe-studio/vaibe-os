#!/usr/bin/env python3
"""
YouTrack Issues Creator from Meeting Tasks

Создает задачи в YouTrack из файла meeting_tasks.md встречи.

Usage:
    python -m tools.yt_create_issues_from_meeting 3
    python -m tools.yt_create_issues_from_meeting 3 --dry-run
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict

import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Priority mapping from Russian to YouTrack
PRIORITY_MAP = {
    'высший': 'Critical',
    'критический': 'Critical',
    'высокий': 'Major',
    'средний': 'Normal',
    'обычный': 'Normal',
    'низкий': 'Minor',
}

# Default priority if not specified
DEFAULT_PRIORITY = 'Normal'


@dataclass
class Task:
    """Represents a task parsed from meeting_tasks.md."""
    number: int
    title: str
    description: str
    priority: Optional[str] = None
    assignee: Optional[str] = None
    deadline: Optional[str] = None
    
    def to_youtrack_payload(self, project_id: str) -> dict:
        """Convert task to YouTrack API payload."""
        priority = map_priority(self.priority) if self.priority else DEFAULT_PRIORITY
        
        payload = {
            "summary": self.title,
            "description": self.description,
            "project": {"id": project_id},
            "customFields": [
                {
                    "name": "Priority",
                    "value": {"name": priority},
                    "$type": "SingleEnumIssueCustomField"
                }
            ]
        }
        
        return payload


def map_priority(priority_text: str) -> str:
    """
    Map Russian priority text to YouTrack priority value.
    
    Args:
        priority_text: Priority text in Russian (e.g., "Высший", "Средний")
        
    Returns:
        YouTrack priority name (e.g., "Critical", "Normal")
    """
    if not priority_text:
        return DEFAULT_PRIORITY
    
    normalized = priority_text.strip().lower()
    return PRIORITY_MAP.get(normalized, DEFAULT_PRIORITY)


def find_meeting_folder(meeting_number: int, base_path: Path) -> Optional[Path]:
    """
    Find meeting folder by meeting number.
    
    Args:
        meeting_number: Meeting number (e.g., 3)
        base_path: Base path to search in (workspace root)
        
    Returns:
        Path to meeting folder or None if not found
    """
    meetings_dir = base_path / "Встречи"
    
    if not meetings_dir.exists():
        logger.error(f"Meetings directory not found: {meetings_dir}")
        return None
    
    # Look for folder starting with "Встреча N."
    pattern = f"Встреча {meeting_number}."
    
    for folder in meetings_dir.iterdir():
        if folder.is_dir() and folder.name.startswith(pattern):
            return folder
    
    logger.error(f"Meeting folder not found for meeting #{meeting_number}")
    return None


def parse_meeting_tasks(file_path: Path) -> list[Task]:
    """
    Parse meeting_tasks.md file and extract tasks.
    
    Args:
        file_path: Path to meeting_tasks.md
        
    Returns:
        List of Task objects
    """
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return []
    
    content = file_path.read_text(encoding='utf-8')
    tasks = []
    
    # Split by task headers (### N. Title)
    task_pattern = r'###\s+(\d+)\.\s+(.+?)(?=\n###|\n##|\Z)'
    matches = re.findall(task_pattern, content, re.DOTALL)
    
    for number_str, task_content in matches:
        number = int(number_str)
        lines = task_content.strip().split('\n')
        
        # First line is the title
        title = lines[0].strip() if lines else f"Задача {number}"
        
        # Parse the rest for metadata and description
        description_parts = []
        priority = None
        assignee = None
        deadline = None
        
        for line in lines[1:]:
            line = line.strip()
            
            # Extract priority
            priority_match = re.match(r'-\s*\*\*Приоритет\*\*:\s*(.+)', line)
            if priority_match:
                priority = priority_match.group(1).strip()
                continue
            
            # Extract assignee
            assignee_match = re.match(r'-\s*\*\*Ответственный\*\*:\s*(.+)', line)
            if assignee_match:
                assignee = assignee_match.group(1).strip()
                continue
            
            # Extract deadline
            deadline_match = re.match(r'-\s*\*\*Срок\*\*:\s*(.+)', line)
            if deadline_match:
                deadline = deadline_match.group(1).strip()
                continue
            
            # Add to description
            description_parts.append(line)
        
        # Build description from remaining content
        description = '\n'.join(description_parts).strip()
        
        # Add metadata to description for reference
        if assignee:
            description += f"\n\n**Ответственный:** {assignee}"
        if deadline:
            description += f"\n**Срок:** {deadline}"
        
        task = Task(
            number=number,
            title=title,
            description=description,
            priority=priority,
            assignee=assignee,
            deadline=deadline
        )
        tasks.append(task)
    
    logger.info(f"Parsed {len(tasks)} tasks from {file_path.name}")
    return tasks


def get_project_id(session: requests.Session, base_url: str, project_short_name: str) -> Optional[str]:
    """
    Get project database ID by short name.
    
    Args:
        session: Configured requests session
        base_url: YouTrack base URL
        project_short_name: Project short name (e.g., "UCP")
        
    Returns:
        Project database ID or None
    """
    url = f"{base_url}/api/admin/projects"
    params = {
        "fields": "id,shortName,name",
        "query": f"shortName:{project_short_name}"
    }
    
    try:
        response = session.get(url, params=params)
        response.raise_for_status()
        projects = response.json()
        
        for project in projects:
            if project.get('shortName') == project_short_name:
                return project.get('id')
        
        # If not found by query, try listing all
        response = session.get(url, params={"fields": "id,shortName,name"})
        response.raise_for_status()
        projects = response.json()
        
        for project in projects:
            if project.get('shortName') == project_short_name:
                return project.get('id')
        
        logger.error(f"Project '{project_short_name}' not found")
        return None
        
    except requests.RequestException as e:
        logger.error(f"Failed to get project ID: {e}")
        return None


def validate_token(session: requests.Session, base_url: str) -> bool:
    """
    Validate YouTrack token by checking current user.
    
    Args:
        session: Configured requests session
        base_url: YouTrack base URL
        
    Returns:
        True if token is valid
    """
    url = f"{base_url}/api/users/me"
    params = {"fields": "login,name"}
    
    try:
        response = session.get(url, params=params)
        response.raise_for_status()
        user = response.json()
        logger.info(f"Authenticated as: {user.get('name', user.get('login'))}")
        return True
    except requests.RequestException as e:
        logger.error(f"Token validation failed: {e}")
        return False


def create_issue(session: requests.Session, base_url: str, task: Task, project_id: str) -> Optional[str]:
    """
    Create issue in YouTrack.
    
    Args:
        session: Configured requests session
        base_url: YouTrack base URL
        task: Task object to create
        project_id: YouTrack project database ID
        
    Returns:
        Created issue ID (readable) or None on failure
    """
    url = f"{base_url}/api/issues"
    params = {"fields": "idReadable,summary"}
    payload = task.to_youtrack_payload(project_id)
    
    try:
        response = session.post(url, params=params, json=payload)
        response.raise_for_status()
        issue = response.json()
        issue_id = issue.get('idReadable')
        logger.info(f"Created issue: {issue_id} - {task.title}")
        return issue_id
    except requests.RequestException as e:
        logger.error(f"Failed to create issue '{task.title}': {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response: {e.response.text}")
        return None


def create_issues(
    tasks: list[Task],
    youtrack_url: str,
    token: str,
    project_short_name: str,
    dry_run: bool = False
) -> dict:
    """
    Create multiple issues in YouTrack.
    
    Args:
        tasks: List of Task objects
        youtrack_url: YouTrack instance URL
        token: YouTrack permanent token
        project_short_name: Project short name
        dry_run: If True, don't actually create issues
        
    Returns:
        Dictionary with 'created' and 'failed' lists
    """
    results = {
        'created': [],
        'failed': [],
        'total': len(tasks)
    }
    
    if not tasks:
        logger.warning("No tasks to create")
        return results
    
    if dry_run:
        logger.info("DRY RUN - no issues will be created")
        for task in tasks:
            priority = map_priority(task.priority) if task.priority else DEFAULT_PRIORITY
            logger.info(f"  Would create: [{priority}] {task.title}")
            results['created'].append({'task': task, 'issue_id': 'DRY-RUN'})
        return results
    
    # Create session with auth
    session = requests.Session()
    session.headers.update({
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })
    
    # Validate token
    if not validate_token(session, youtrack_url):
        logger.error("Invalid token or connection failed")
        results['failed'] = [{'task': t, 'error': 'Auth failed'} for t in tasks]
        return results
    
    # Get project ID
    project_id = get_project_id(session, youtrack_url, project_short_name)
    if not project_id:
        logger.error(f"Project '{project_short_name}' not found")
        results['failed'] = [{'task': t, 'error': 'Project not found'} for t in tasks]
        return results
    
    logger.info(f"Creating issues in project: {project_short_name} (ID: {project_id})")
    
    # Create issues
    for task in tasks:
        issue_id = create_issue(session, youtrack_url, task, project_id)
        if issue_id:
            results['created'].append({'task': task, 'issue_id': issue_id})
        else:
            results['failed'].append({'task': task, 'error': 'Creation failed'})
    
    return results


def print_results(results: dict, youtrack_url: str):
    """Print creation results summary."""
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ СОЗДАНИЯ ЗАДАЧ В YOUTRACK")
    print("=" * 60)
    
    created = results.get('created', [])
    failed = results.get('failed', [])
    total = results.get('total', 0)
    
    print(f"\nВсего задач: {total}")
    print(f"Создано: {len(created)}")
    print(f"Ошибок: {len(failed)}")
    
    if created:
        print("\n✓ Созданные задачи:")
        for item in created:
            task = item['task']
            issue_id = item['issue_id']
            if issue_id != 'DRY-RUN':
                url = f"{youtrack_url}/issue/{issue_id}"
                print(f"  - {issue_id}: {task.title}")
                print(f"    URL: {url}")
            else:
                print(f"  - [DRY-RUN] {task.title}")
    
    if failed:
        print("\n✗ Ошибки:")
        for item in failed:
            task = item['task']
            error = item.get('error', 'Unknown error')
            print(f"  - {task.title}: {error}")
    
    print()


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Create YouTrack issues from meeting tasks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m tools.yt_create_issues_from_meeting 3
  python -m tools.yt_create_issues_from_meeting 3 --dry-run
  python -m tools.yt_create_issues_from_meeting 3 --project UCP
        """
    )
    
    parser.add_argument(
        'meeting_number',
        type=int,
        help='Meeting number (e.g., 3 for "Встреча 3")'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Parse and show tasks without creating issues'
    )
    
    parser.add_argument(
        '--project',
        help='YouTrack project short name (overrides YOUTRACK_PROJECT_ID env)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
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
    
    # Get configuration
    youtrack_url = os.getenv('YOUTRACK_URL', 'https://yt.power-freelance.ru')
    youtrack_token = os.getenv('YOUTRACK_TOKEN')
    project_id = args.project or os.getenv('YOUTRACK_PROJECT_ID', 'UCP')
    
    if not youtrack_token and not args.dry_run:
        logger.error("YOUTRACK_TOKEN not set. Set it in .env or environment.")
        return 1
    
    # Find meeting folder
    meeting_folder = find_meeting_folder(args.meeting_number, workspace_root)
    if not meeting_folder:
        return 1
    
    # Parse tasks
    tasks_file = meeting_folder / 'meeting_tasks.md'
    if not tasks_file.exists():
        logger.error(f"meeting_tasks.md not found in {meeting_folder}")
        return 1
    
    tasks = parse_meeting_tasks(tasks_file)
    if not tasks:
        logger.error("No tasks found in meeting_tasks.md")
        return 1
    
    # Create issues
    results = create_issues(
        tasks=tasks,
        youtrack_url=youtrack_url,
        token=youtrack_token or '',
        project_short_name=project_id,
        dry_run=args.dry_run
    )
    
    # Print results
    print_results(results, youtrack_url)
    
    # Return exit code based on results
    if results.get('failed'):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
