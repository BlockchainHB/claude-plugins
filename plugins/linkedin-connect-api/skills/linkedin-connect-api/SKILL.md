---
name: linkedin-connect-api
description: Send LinkedIn connection requests via the internal Voyager API. Looks up profile URNs and sends invites programmatically without browser UI clicking. Use when sending LinkedIn connections through Claude Code.
---

# LinkedIn Connections API (Voyager)

Send connection requests programmatically via LinkedIn's internal Voyager API. No browser clicking or modal interaction needed — just run JavaScript on any `linkedin.com` page.

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

```
PROFILE URL → EXTRACT USERNAME → LOOKUP URN (API) → SEND CONNECT (API) → CHECK RESPONSE
```

---

## Extracting Username from URL

```javascript
function extractUsername(profileUrl) {
  const match = profileUrl.match(/linkedin\.com\/in\/([^/?#]+)/);
  return match ? match[1] : null;
}
```

Works with all URL formats:
- `https://www.linkedin.com/in/johndoe/`
- `https://linkedin.com/in/johndoe`
- `https://www.linkedin.com/in/johndoe?utm_source=share`

---

## Single Connection Request

Run via `javascript_tool` on any LinkedIn page. Replace `'TARGET_USERNAME'` with the actual `/in/{username}` slug:

```javascript
(async () => {
  const username = 'TARGET_USERNAME';
  const csrf = document.cookie.match(/JSESSIONID="([^"]+)"/)[1];
  const headers = {
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'csrf-token': csrf,
    'x-restli-protocol-version': '2.0.0'
  };

  // Step 1: Lookup URN from username
  const lookup = await fetch(
    '/voyager/api/identity/dash/profiles?q=memberIdentity&memberIdentity=' + username,
    { headers }
  );
  const lookupData = await lookup.text();
  const urn = lookupData.match(/urn:li:fsd_profile:[A-Za-z0-9_-]+/)?.[0];
  if (!urn) return JSON.stringify({ ok: false, error: 'URN_NOT_FOUND', username });

  // Step 2: Send connection request
  const res = await fetch(
    '/voyager/api/voyagerRelationshipsDashMemberRelationships?action=verifyQuotaAndCreateV2&decorationId=com.linkedin.voyager.dash.deco.relationships.InvitationCreationResultWithInvitee-2',
    {
      method: 'POST',
      headers: { ...headers, 'content-type': 'application/json; charset=UTF-8' },
      body: JSON.stringify({
        invitee: {
          inviteeUnion: {
            memberProfile: urn
          }
        }
      })
    }
  );

  const body = await res.json();
  return JSON.stringify({
    ok: res.status === 200,
    status: res.status,
    code: body?.data?.code || null,
    urn,
    username
  });
})()
```

---

## Batch Connection Requests

Send connections to multiple profiles in sequence. Replace the `usernames` array with target usernames:

```javascript
(async () => {
  const usernames = ['username1', 'username2', 'username3'];

  const csrf = document.cookie.match(/JSESSIONID="([^"]+)"/)[1];
  const headers = {
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'csrf-token': csrf,
    'x-restli-protocol-version': '2.0.0'
  };

  const results = [];
  for (const username of usernames) {
    // Lookup URN
    const lookup = await fetch(
      '/voyager/api/identity/dash/profiles?q=memberIdentity&memberIdentity=' + username,
      { headers }
    );
    const lookupData = await lookup.text();
    const urn = lookupData.match(/urn:li:fsd_profile:[A-Za-z0-9_-]+/)?.[0];
    if (!urn) { results.push({ ok: false, error: 'URN_NOT_FOUND', username }); continue; }

    // Send connection
    const res = await fetch(
      '/voyager/api/voyagerRelationshipsDashMemberRelationships?action=verifyQuotaAndCreateV2&decorationId=com.linkedin.voyager.dash.deco.relationships.InvitationCreationResultWithInvitee-2',
      {
        method: 'POST',
        headers: { ...headers, 'content-type': 'application/json; charset=UTF-8' },
        body: JSON.stringify({ invitee: { inviteeUnion: { memberProfile: urn } } })
      }
    );
    const body = await res.json();
    results.push({ ok: res.status === 200, status: res.status, code: body?.data?.code || null, urn, username });

    // Delay between requests
    await new Promise(r => setTimeout(r, 1000));
  }
  return JSON.stringify(results);
})()
```

**Note:** For large batches (10+), consider splitting across multiple `javascript_tool` calls to avoid the Chrome MCP ~10s timeout. Send 3-5 per call.

---

## API Reference

### URN Lookup

```
GET /voyager/api/identity/dash/profiles?q=memberIdentity&memberIdentity={username}
```

Returns profile data including `urn:li:fsd_profile:{id}`.

### Send Connection

```
POST /voyager/api/voyagerRelationshipsDashMemberRelationships
  ?action=verifyQuotaAndCreateV2
  &decorationId=com.linkedin.voyager.dash.deco.relationships.InvitationCreationResultWithInvitee-2
```

**Request body:**
```json
{
  "invitee": {
    "inviteeUnion": {
      "memberProfile": "urn:li:fsd_profile:ACoAAA..."
    }
  }
}
```

**Required headers:**
- `accept: application/vnd.linkedin.normalized+json+2.1`
- `content-type: application/json; charset=UTF-8`
- `csrf-token: {from JSESSIONID cookie}`
- `x-restli-protocol-version: 2.0.0`

---

## Response Codes

| Status | `code` field | Meaning |
|--------|-------------|---------|
| 200 | `null` | Connection sent successfully |
| 400 | `CANT_RESEND_YET` | Already sent (pending or recently sent) |
| 400 | `null` | Invalid request or blocked |
| 403 | — | Session expired — refresh LinkedIn page |

---

## Summarizing Batch Results

```javascript
const sent = results.filter(r => r.ok).length;
const alreadySent = results.filter(r => r.code === 'CANT_RESEND_YET').length;
const failed = results.filter(r => !r.ok && r.code !== 'CANT_RESEND_YET').length;
```

---

## Rate Limits

| Limit | Value |
|-------|-------|
| Connection requests per week | ~100 |
| Daily recommended | 20-25 |
| Personalized invites per month | 3-5 (free), unlimited (Premium) |

---

## Browser Fallback

If the Voyager API fails, use the browser DOM method. See `references/browser-fallback.md`.

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `URN_NOT_FOUND` | Username doesn't exist or typo | Verify the `/in/{username}` slug |
| `CANT_RESEND_YET` | Connection already pending | Skip — already sent |
| 400 with no code | Request format wrong | Check body has `invitee.inviteeUnion.memberProfile` |
| 403 | Session expired | Navigate to linkedin.com to refresh cookies |
| Rate limited | Too many requests | Add longer delays, stay under 25/day |
| "Detached while handling command" | Chrome MCP timeout on batch | Split into smaller batches (3-5 per call) |

---

*Reverse-engineered Feb 2026. LinkedIn can change internal APIs at any time. If calls start failing, re-intercept via DevTools Network tab.*
