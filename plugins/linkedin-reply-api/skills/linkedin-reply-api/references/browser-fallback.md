# LinkedIn Comment Posting — Browser Fallback

Use this method only if the Voyager API returns 403 (session expired) or is rate limited. The API method in the main SKILL.md is preferred.

---

## LinkedIn DOM Selectors

| Data | Selector |
|------|----------|
| Post container | `[data-urn]` |
| Activity URN | `el.getAttribute('data-urn')` |
| Author name | `.update-components-actor__title span[aria-hidden=true]` |
| Post text | `.break-words` |
| Reactions | `.social-details-social-counts__reactions-count` |
| Comments | `.social-details-social-counts__comments` |
| Profile link | `a[href*="/in/"]` |
| Time | `.update-components-actor__sub-description span[aria-hidden=true]` |

---

## Comment Posting via Browser

### Step 1: Click Comment Button

```javascript
document.querySelector('button[aria-label*="Comment"], button[aria-label*="comment"]').click();
```

### Step 2: Type Comment (wait 1 second after step 1)

```javascript
var editor = document.querySelector('.ql-editor[data-placeholder]');
if (editor) {
  editor.focus();
  document.execCommand('insertText', false, 'YOUR_COMMENT_HERE');
}
```

### Step 3: Submit (wait 1 second after step 2)

```javascript
document.querySelector('.comments-comment-box__submit-button--cr').click();
```

---

## Post Extraction Script

Run on any LinkedIn feed page to extract visible posts:

```javascript
var posts = [];
document.querySelectorAll('[data-urn]').forEach(function(el) {
  var u = el.getAttribute('data-urn');
  if (!u || !u.includes('activity')) return;
  var a = el.querySelector('.update-components-actor__title span[aria-hidden=true]');
  var t = el.querySelector('.break-words');
  var r = el.querySelector('.social-details-social-counts__reactions-count');
  var c = el.querySelector('.social-details-social-counts__comments');
  var pl = el.querySelector('a[href*="/in/"]');
  var txt = t ? t.innerText : '';
  var purl = pl ? pl.href.split('?')[0] : '';

  posts.push({
    urn: u,
    author: a ? a.innerText : '',
    text: txt.substring(0, 500),
    reactions: r ? r.innerText.trim() : '0',
    comments: c ? c.innerText.replace(/[^0-9]/g, '') : '0',
    profileUrl: purl,
    postUrl: 'https://www.linkedin.com/feed/update/' + u
  });
});
JSON.stringify(posts, null, 2);
```

---

## Time Format Reference

| Display | Meaning |
|---------|---------|
| `now` | Seconds ago |
| `Xm` | X minutes ago |
| `Xh` | X hours ago |
| `Xd` | X days ago |

---

## Scroll and Accumulate

LinkedIn loads ~5-8 posts initially. To get more:

1. Scroll: `scroll at (400, 500) down 5 ticks`
2. Wait 2 seconds
3. Re-run extraction script
4. Repeat 1-2 times

Accumulate across runs:
```javascript
window.allPosts = window.allPosts || new Map();
posts.forEach(function(p) { window.allPosts.set(p.urn, p); });
Array.from(window.allPosts.values()).length;
```

---

*LinkedIn DOM changes occasionally. Verify selectors if operations fail.*
