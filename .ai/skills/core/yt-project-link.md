---
name: yt-project-link
description: Link a vAIbe-os project with a YouTrack project
triggers: [yt-project-link, youtrack link, link youtrack]
origin: bundled
---

# Purpose

Link a local vAIbe-os project with a YouTrack project. Supports two modes: link to an existing project or create a new project in YouTrack.

**IMPORTANT**: Before use, ensure `.env` contains `YOUTRACK_URL` and `YOUTRACK_TOKEN`.

# When to use

- User wants to connect a project to YouTrack
- User triggers `/yt-project-link`

# Inputs needed

- `.env` (local): `YOUTRACK_URL`, `YOUTRACK_TOKEN`
- `Проекты/{PROJECT}/README.md` — current link state (YouTrack Integration section)

# Outputs

- Updated `Проекты/{PROJECT}/README.md` (added/updated **YouTrack Integration** section) — only after confirmation
- (optional) new project and Kanban board in YouTrack (with explicit consent)

# Critical rules

> **FORBIDDEN**: Link project without user confirmation.
> **FORBIDDEN**: Create project in YouTrack without explicit consent.
> **FORBIDDEN**: Modify README.md without showing changes.
> **REQUIRED**: Check credentials before starting.
> **REQUIRED**: Show linking plan and wait for confirmation.
> **REQUIRED**: Use structured questions for choices.

# Prerequisites

## `.env` configuration

```bash
YOUTRACK_URL=https://yt.example.com
YOUTRACK_TOKEN=perm:your-token-here
```

## Getting YouTrack token

1. Log in to YouTrack → Profile → Account Security
2. Click "New token..."
3. Name the token (e.g. "vAIbe-os Integration")
4. Select scope: `YouTrack`
5. Copy token and save to `.env`

# Procedure

## 1. Initialization
- User invokes `/yt-project-link`
- Optionally specifies project: `/yt-project-link {PROJECT_NAME}`
- Agent checks credentials in `.env`

## 2. Check configuration

Verify `YOUTRACK_URL` and `YOUTRACK_TOKEN` are set. If missing → **STOP**, show setup instructions.

## 3. Select vAIbe-os project

> **STOP POINT**: If project not specified, ask for selection.

Show list of available projects. **→ STOP. Wait for user choice.**

## 4. Check current state
- Read `Проекты/{NAME}/README.md`
- Check for "YouTrack Integration" section

If already linked — offer: update link, unlink, or leave as is. **→ STOP. Wait for choice.**

## 5. Select linking mode

> **STOP POINT**: Ask for linking mode.

Options:
1. Link to existing YouTrack project
2. Create new project in YouTrack

**→ STOP. Wait for choice.**

## 6a. Mode: Link to existing

Ask for project ID or URL. Validate via API:
```
GET /api/admin/projects/{projectId}?fields=id,name,shortName,description
```

## 6b. Mode: Create new project

> **STOP POINT**: Ask for new project parameters.

Parameters:
- Short name (Latin, up to 10 chars)
- Project name in YouTrack
- Description (optional)

**→ STOP. Wait for confirmation.**

Create project:
```
POST /api/admin/projects
{
  "shortName": "PRJ",
  "name": "Project Name",
  "description": "Description",
  "leader": {"login": "cursor"}
}
```

### Auto-create Kanban board (4 steps):

```
# Step 1: Create board
POST /api/agiles
{"name": "{Project Name}: доска Kanban", "projects": [{"id": "{project_id}"}]}

# Step 2: Configure columns (REQUIRED!)
POST /api/agiles/{agile_id}
{"columnSettings": {"field": {"id": "150-2"}}}

# Step 3: Set visibility (REQUIRED!)
POST /api/agiles/{agile_id}
{"visibleFor": {"ringId": "{ALL_USERS_RING_ID}"}, "updateableBy": {"ringId": "{ALL_USERS_RING_ID}"}}

# Step 4: Configure Kanban behavior
POST /api/agiles/{agile_id}
{"sprintsSettings": {"isExplicit": false, "disableSprints": true}}
```

⚠️ Without step 2 — board is invalid. Without step 3 — only owner sees it. Without step 4 — new issues don't auto-appear.

## 6c. Add team members

Use Hub API (`/hub/api/rest/`), NOT YouTrack API (`/api/`):

```
# 1. Get Hub user IDs
GET /hub/api/rest/users?fields=id,name,login

# 2. Get Project Team ID
GET /hub/api/rest/projectteams?query=project:{project_hub_id}&fields=id

# 3. Add user to project team (REQUIRED)
POST /hub/api/rest/projectteams/{projectteam_id}/users
{"id": "{user_hub_id}"}

# 4. Assign role (optional)
POST /hub/api/rest/users/{user_hub_id}/projectroles
{"role": {"id": "{contributor_role_id}"}, "project": {"id": "{project_hub_id}"}}
```

## 7. Confirm linking

> **STOP POINT**: Show change plan.

Show: vAIbe-os project, YouTrack project, changes to README.md. **→ STOP. Wait for confirmation.**

## 8. Execute linking

**ONLY AFTER confirmation:**
- Update project README.md with YouTrack Integration section
- Show result with links and next steps

# YouTrack Integration section format

```markdown
## YouTrack Integration
- **Project ID**: {SHORT_NAME}
- **Project URL**: {YOUTRACK_URL}/projects/{SHORT_NAME}
- **Kanban Board**: {YOUTRACK_URL}/agiles/{AGILE_ID}
- **Linked**: {YYYY-MM-DD}
- **Default Assignee**: Cursor (optional)
```

# Error handling

| Error | Action |
|-------|--------|
| Credentials missing | Show setup instructions, STOP |
| YouTrack project not found | Suggest checking ID or creating new |
| API error (401) | Token invalid/expired, show renewal instructions |
| vAIbe-os project not found | Show available projects |

# API reference

### Check connection
```
GET {YOUTRACK_URL}/api/admin/projects?fields=id,name,shortName
Authorization: Bearer {YOUTRACK_TOKEN}
```

### Get project
```
GET {YOUTRACK_URL}/api/admin/projects/{projectId}?fields=id,name,shortName,description
```

### Create project
```
POST {YOUTRACK_URL}/api/admin/projects
{"shortName": "PRJ", "name": "Name", "description": "Desc", "leader": {"login": "cursor"}}
```

### Create Kanban board
See step 6b above for the 4-step process.

### Add team members (Hub API)
See step 6c above.

# Required permissions

| Permission | Needed for |
|-----------|-----------|
| Create Project | Creating new projects |
| Read Project | Linking to existing |
| Update Project | Changing settings (optional) |
| Create Agile Board | Creating Kanban boards |
| Manage Project Roles (Hub) | Adding team members |

# Team member roles

| Role | Key | Access |
|------|-----|--------|
| System Admin | system-admin | Full access |
| Project Admin | project-admin | Manage project |
| Contributor | contributor | Create/edit issues |
| Observer | observer | View only |
| Issue Reader | youtrack-issue-reader | View issues |
| Reporter | youtrack-reporter | Create issues |

# Notes

- One vAIbe-os project can be linked to one YouTrack project only
- Linking does not auto-create issues — use `/yt-project-tasks-push`
- If YouTrack project is deleted, link remains in README.md (manual removal required)
- For multiple YouTrack instances — use different `.env` configurations

# Related commands

- `/plan-update` — create/update snapshot plan (basis for task publishing)
- `/yt-project-tasks-push` — publish tasks to YouTrack
- `/yt-project-tasks-pull` — get updates from YouTrack and create new plan
