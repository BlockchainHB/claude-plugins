# LinkedIn Connections — Browser Fallback

Use this method only if the Voyager API fails. The API method in the main SKILL.md is preferred.

---

## Profile Research Extraction

Run on a profile page to gather context for personalized connection messages:

```javascript
const research = {
  name: document.querySelector('h1')?.textContent?.trim() || '',
  headline: document.querySelector('.text-body-medium')?.textContent?.trim() || '',
  location: document.querySelector('.text-body-small.inline.t-black--light')?.textContent?.trim() || '',
  currentCompany: document.querySelector('button[aria-label*="Current company"]')?.textContent?.trim() || '',
  followers: document.querySelector('.t-bold')?.textContent?.trim() || '',
  connectionDegree: document.querySelector('.dist-value')?.textContent?.trim() || '',
  about: document.querySelector('#about ~ .display-flex .pv-shared-text-with-see-more')?.textContent?.trim()?.substring(0, 300) || '',
  mutualConnections: document.querySelector('[href*="mutual-connections"]')?.textContent?.trim() || ''
};
JSON.stringify(research, null, 2);
```

---

## Profile Page Selectors

| Element | Selector |
|---------|----------|
| Name | `h1` |
| Headline | `.text-body-medium` |
| Location | `.text-body-small.inline.t-black--light` |
| Current company | `button[aria-label*="Current company"]` |
| More actions button | `button[aria-label="More actions"]` |
| Connection degree | `.dist-value` |
| About section | `#about ~ .display-flex .pv-shared-text-with-see-more` |

---

## Connection Modal Selectors

| Element | Selector |
|---------|----------|
| Modal container | `[role="dialog"]` |
| Add a note button | `[aria-label="Add a note"]` |
| Message textarea | `#custom-message` or `textarea[name="message"]` |
| Send button | `[aria-label="Send invitation"]` |
| Send without note | `[aria-label="Send without a note"]` |
| Dismiss button | `[aria-label="Dismiss"]` |

---

## Complete Browser Send Flow

### Step 1: Open More Dropdown

```javascript
const profileSection = document.querySelector('.ph5.pb5');
const moreBtn = profileSection.querySelector('button[aria-label="More actions"]');
moreBtn.click();
'More dropdown opened';
```

### Step 2: Click Connect (wait 500ms after step 1)

```javascript
const connectOpt = document.querySelector('[aria-label*="Invite"][aria-label*="to connect"]');
if (connectOpt) {
  connectOpt.click();
  'Connect clicked';
} else {
  'Connect not found - may already be connected or pending';
}
```

### Step 3: Click Add a Note (wait 500ms after step 2)

```javascript
const addNoteBtn = document.querySelector('[aria-label="Add a note"]');
if (addNoteBtn) {
  addNoteBtn.click();
  'Add note clicked';
} else {
  'Add note not found';
}
```

### Step 4: Enter Message

**LinkedIn's Ember framework doesn't respond well to programmatic input.** Use the `computer` tool with physical typing:

1. Triple-click in textarea to select any existing text
2. Type the new message via `computer` tool
3. Click Send

Or use `form_input` with the ref from `read_page`:
```
ref_X = textarea (id="custom-message")
ref_Y = Send invitation button
```

### Step 5: Click Send

```javascript
const btns = document.querySelectorAll('[role="dialog"] button');
btns.forEach(btn => {
  if (btn.textContent.trim() === 'Send') btn.click();
});
```

### Step 6: Verify Success

```javascript
const toast = document.querySelector('.artdeco-toast-item');
toast?.textContent?.includes('invitation to connect was sent');
```

---

## Profile Types

LinkedIn has two profile types with different Connect button locations:

### Type A: Direct Connect Button Visible
```javascript
const connectBtn = document.querySelector('button[aria-label*="Invite"][aria-label*="to connect"]');
if (connectBtn) connectBtn.click();
```

### Type B: "Follow First" Profiles (Connect in More Dropdown)
Click More actions first, then Connect in the dropdown.

---

## Success Indicators

| Element | Selector |
|---------|----------|
| Toast notification | `.artdeco-toast-item` |
| Pending button | `button:contains("Pending")` |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Send button disabled | Message over 200 chars — shorten it |
| Connect not in dropdown | Already connected or request pending |
| "Add a note" not appearing | May have used all personalized invites for the month |
| Message not registering | Use `computer` tool to physically type instead of JS |
| Modal not opening | Page not fully loaded — wait and retry |

---

*LinkedIn DOM changes occasionally. Verify selectors if operations fail.*
