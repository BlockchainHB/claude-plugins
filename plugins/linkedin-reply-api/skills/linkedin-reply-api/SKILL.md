---
name: linkedin-reply-api
description: Post comments on LinkedIn posts via the internal Voyager API. No browser navigation needed — just execute JavaScript on any linkedin.com page. Use when posting LinkedIn comments through Claude Code.
---

# LinkedIn Reply API (Voyager)

Post comments on LinkedIn posts programmatically via LinkedIn's internal Voyager API. No browser clicking or navigation to individual posts needed — just run JavaScript on any `linkedin.com` page.

## Prerequisites

- Chrome browser with LinkedIn open and logged in
- Chrome MCP extension connected (`mcp__claude-in-chrome__*` tools available)
- Must be on any `linkedin.com` page (needs session cookies)

Verify Chrome MCP is available:
```
mcp__claude-in-chrome__tabs_context_mcp
```

If it errors: tell the user "Chrome MCP isn't connected. Open Chrome with the Claude extension active."

---

## How It Works

1. Extract the activity ID from the post URL
2. Extract the CSRF token from session cookies
3. POST to the Voyager comment endpoint
4. Get 201 Created on success

---

## Extracting the Activity ID

The activity ID is the only identifier you need. Use it directly as `urn:li:activity:{ID}` for posting. **No resolution step needed** — this works for all post types (ugcPost-backed and share-backed).

### From Post URL

```javascript
// URL: https://www.linkedin.com/posts/someone_some-text-activity-7424806492844949504-xxxx
// or:  https://www.linkedin.com/feed/update/urn:li:activity:7424806492844949504
const activityId = postUrl.match(/activity[:-](\d+)/)?.[1];
```

### From Apify/Scraper Output

```javascript
// post.id = "urn:li:activity:7424806492844949504"
const activityId = post.id.split(':').pop(); // "7424806492844949504"
```

---

## Posting: One Comment Per Tool Call

**Do NOT batch multiple comments in one `javascript_tool` call.** The Chrome MCP extension times out after ~10 seconds. Scripts with `await` delays get "Detached" errors, but the fetches keep running silently in the browser, causing duplicate posts if you retry.

**Post one comment at a time, with separate tool calls for each:**

```javascript
(async () => {
  const activityId = 'ACTIVITY_ID';     // numeric ID extracted above
  const commentText = 'COMMENT_TEXT';

  const csrf = document.cookie.match(/JSESSIONID="([^"]+)"/)?.[1];
  if (!csrf) return JSON.stringify({ error: 'No JSESSIONID' });

  const response = await fetch(
    '/voyager/api/voyagerSocialDashNormComments?decorationId=com.linkedin.voyager.dash.deco.social.NormComment-43',
    {
      method: 'POST',
      headers: {
        'accept': 'application/vnd.linkedin.normalized+json+2.1',
        'content-type': 'application/json; charset=UTF-8',
        'csrf-token': csrf,
        'x-restli-protocol-version': '2.0.0'
      },
      body: JSON.stringify({
        commentary: {
          text: commentText,
          attributesV2: [],
          '$type': 'com.linkedin.voyager.dash.common.text.TextViewModel'
        },
        threadUrn: 'urn:li:activity:' + activityId
      })
    }
  );

  const status = response.status;
  if (status === 201) {
    return JSON.stringify({ success: true, status, commentUrn: response.headers.get('x-restli-id') });
  } else {
    let error;
    try { error = await response.json(); } catch { error = await response.text(); }
    return JSON.stringify({ success: false, status, error });
  }
})()
```

**Wait 3-5 seconds between each tool call** (the delay lives between calls, not inside the script).

---

## API Reference

### Comment Endpoint

```
POST /voyager/api/voyagerSocialDashNormComments
  ?decorationId=com.linkedin.voyager.dash.deco.social.NormComment-43
```

### Request Headers

| Header | Value |
|--------|-------|
| `accept` | `application/vnd.linkedin.normalized+json+2.1` |
| `content-type` | `application/json; charset=UTF-8` |
| `csrf-token` | Extracted from `JSESSIONID` cookie |
| `x-restli-protocol-version` | `2.0.0` |

### Request Body

```json
{
  "commentary": {
    "text": "Your comment text here",
    "attributesV2": [],
    "$type": "com.linkedin.voyager.dash.common.text.TextViewModel"
  },
  "threadUrn": "urn:li:activity:7424806492844949504"
}
```

| Field | Type | Notes |
|-------|------|-------|
| `commentary.text` | `string` | Plain text comment body |
| `commentary.attributesV2` | `[]` | Empty for plain text. Used for @mentions. |
| `commentary.$type` | `string` | **Static**: `com.linkedin.voyager.dash.common.text.TextViewModel` |
| `threadUrn` | `string` | `urn:li:activity:{ID}` — works for all post types |

### Response

**Success**: `201 Created`
- `x-restli-id` header contains the comment URN
- Body: `{ "data": {...}, "included": [...] }`

---

## Response Codes

| Status | Meaning | Action |
|--------|---------|--------|
| 201 | Comment posted | Success |
| 400 | Bad request | Check threadUrn format is `urn:li:activity:{ID}` |
| 403 | Session expired or CSRF mismatch | Navigate to linkedin.com to refresh cookies |
| 429 | Rate limited | Wait and retry with longer delays |

---

## Browser Fallback

If the Voyager API returns 403 (session expired) and refreshing doesn't help, use the browser DOM method. See `references/browser-fallback.md`.

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `No JSESSIONID cookie found` | Not on linkedin.com or cookies expired | Navigate to any linkedin.com page first |
| 400 response | Malformed threadUrn or request body | Verify `urn:li:activity:{NUMERIC_ID}` format |
| 403 response | Session expired | Refresh the LinkedIn page, re-run |
| "Detached while handling command" | Script exceeded Chrome MCP ~10s timeout | **Do NOT retry** — the fetch likely completed. Check the post before re-sending. |

---

## Historical Note

Earlier LinkedIn API docs said the comment API required `urn:li:ugcPost:XXX` and that activity URNs needed resolution via `GET /voyager/api/feed/updates/`. Testing confirmed `urn:li:activity:{ID}` works directly as `threadUrn` for all post types (both ugcPost-backed and share-backed). The resolution step is unnecessary.

---

*Reverse-engineered Feb 2026. LinkedIn can change internal APIs at any time. If calls start failing, re-intercept via DevTools Network tab.*
