---
name: linear-mcp
description: Work with Linear project management via MCP tools. Use when creating issues, updating projects, managing initiatives, or querying Linear data.
---

# Linear MCP Tools

Work with Linear project management through MCP tools.

## When to Use

- Creating or updating Linear issues
- Managing projects and initiatives
- Adding comments and activity updates
- Querying teams, users, and labels

## Core Concepts

**Linear's GraphQL API Structure:**
- All mutations use `$input: TypeInput!` input types
- `description` = short summary (shows in list views)
- `content` = full detailed description (shows in detail pages)

## Common Operations

### List Users

Get user IDs for assignments:

```json
{
  "tool_slug": "LINEAR_LIST_LINEAR_USERS",
  "arguments": {
    "first": 50
  }
}
```

### Get Teams and Initiatives

```json
{
  "tool_slug": "LINEAR_RUN_QUERY_OR_MUTATION",
  "arguments": {
    "query_or_mutation": "query { teams { nodes { id name key } } initiatives { nodes { id name description targetDate } } }",
    "variables": {}
  }
}
```

### Get Issue by ID

```json
{
  "tool_slug": "LINEAR_GET_LINEAR_ISSUE",
  "arguments": {
    "issue_id": "DVP-40"
  }
}
```

Works with both identifier (`DVP-40`) and UUID.

### Create Issue

```json
{
  "tool_slug": "LINEAR_CREATE_LINEAR_ISSUE",
  "arguments": {
    "team_id": "TEAM_ID",
    "title": "Issue title",
    "description": "Issue description with markdown",
    "project_id": "PROJECT_ID",
    "assignee_id": "USER_ID",
    "priority": 2
  }
}
```

**Priority values:**
- 0 = No priority
- 1 = Urgent
- 2 = High
- 3 = Normal
- 4 = Low

### Add Comment to Issue

```json
{
  "tool_slug": "LINEAR_CREATE_LINEAR_COMMENT",
  "arguments": {
    "issue_id": "ISSUE_UUID",
    "body": "Comment with **markdown** support"
  }
}
```

### Create Project

```json
{
  "tool_slug": "LINEAR_CREATE_LINEAR_PROJECT",
  "arguments": {
    "name": "Project Name",
    "team_ids": ["TEAM_ID"]
  }
}
```

### Update Project

```json
{
  "tool_slug": "LINEAR_RUN_QUERY_OR_MUTATION",
  "arguments": {
    "query_or_mutation": "mutation UpdateProject($id: String!, $input: ProjectUpdateInput!) { projectUpdate(id: $id, input: $input) { success project { id name description content targetDate lead { id name } } } }",
    "variables": {
      "id": "PROJECT_ID",
      "input": {
        "description": "Short summary",
        "content": "**Full description**\n\n- Point 1\n- Point 2",
        "targetDate": "2025-12-15",
        "leadId": "USER_ID"
      }
    }
  }
}
```

**ProjectUpdateInput fields:**
- `name` (String)
- `description` (String) - short summary
- `content` (String) - full markdown description
- `targetDate` (TimelessDate) - `YYYY-MM-DD`
- `leadId` (String)
- `priority` (Int) - 0-4

### Create Project Milestone

**Note:** Milestones are NOT issues. Use `projectMilestoneCreate`:

```json
{
  "tool_slug": "LINEAR_RUN_QUERY_OR_MUTATION",
  "arguments": {
    "query_or_mutation": "mutation CreateMilestone($input: ProjectMilestoneCreateInput!) { projectMilestoneCreate(input: $input) { success projectMilestone { id name description targetDate } } }",
    "variables": {
      "input": {
        "name": "Milestone Name",
        "description": "Milestone description",
        "targetDate": "2025-11-15",
        "projectId": "PROJECT_ID"
      }
    }
  }
}
```

### Create Initiative

Two-step process: Create minimal, then update with details.

**Step 1: Create**
```json
{
  "tool_slug": "LINEAR_RUN_QUERY_OR_MUTATION",
  "arguments": {
    "query_or_mutation": "mutation CreateInitiative($input: InitiativeCreateInput!) { initiativeCreate(input: $input) { success initiative { id name } } }",
    "variables": {
      "input": {
        "name": "Initiative Name"
      }
    }
  }
}
```

**Step 2: Update**
```json
{
  "tool_slug": "LINEAR_RUN_QUERY_OR_MUTATION",
  "arguments": {
    "query_or_mutation": "mutation UpdateInitiative($id: String!, $input: InitiativeUpdateInput!) { initiativeUpdate(id: $id, input: $input) { success initiative { id name description targetDate owner { id name } } } }",
    "variables": {
      "id": "INITIATIVE_ID",
      "input": {
        "description": "Short summary",
        "content": "**Full detailed content**",
        "targetDate": "2025-12-31",
        "ownerId": "USER_ID"
      }
    }
  }
}
```

### Create Labels

```json
{
  "tool_slug": "LINEAR_CREATE_LINEAR_LABEL",
  "arguments": {
    "team_id": "TEAM_ID",
    "name": "Label Name",
    "color": "#FF6B6B",
    "description": "Optional description"
  }
}
```

## Date Formats

| Field | Format | Example |
|-------|--------|---------|
| `targetDate`, `startDate` | TimelessDate | `"2025-12-15"` |
| `due_date` (issues) | Full timestamp | `"2024,12,31,23,59,59"` |

## Description vs Content

- `description` → Short summaries (1-2 sentences, shows in lists)
- `content` → Full detailed descriptions (markdown, shows in detail view)

Similar to GitHub's title vs body pattern.

## Debugging

### Inspect Schema

```json
{
  "tool_slug": "LINEAR_RUN_QUERY_OR_MUTATION",
  "arguments": {
    "query_or_mutation": "query { __type(name: \"ProjectUpdateInput\") { inputFields { name type { name kind } } } }",
    "variables": {}
  }
}
```

### Common Errors

| Error | Cause |
|-------|-------|
| Argument Validation Error | Wrong field names or missing `$input` syntax |
| Bad Request 400 | Invalid GraphQL syntax |
| CSRF Error | Retry or use alternative tools |

## Best Practices

- Test with minimal fields first, add incrementally
- Use camelCase for field names
- Always provide required variables
- Check field names match schema exactly
