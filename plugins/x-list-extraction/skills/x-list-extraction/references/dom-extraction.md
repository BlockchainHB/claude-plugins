# X Pro DOM Extraction (Fallback)

DOM-based tweet extraction from X Pro columns. Use when the GraphQL API is unavailable.

## Limitations

- Virtualization: only ~10 tweets per column are in DOM at once
- Content may be truncated
- Requires scrolling to accumulate more tweets

---

## Key Selectors

| Element | Selector |
|---------|----------|
| Tweet container | `[data-testid="tweet"]` |
| Author name | `[data-testid="User-Name"]` |
| Tweet text | `[data-testid="tweetText"]` |
| Reply button | `[data-testid="reply"]` |
| Retweet button | `[data-testid="retweet"]` |
| Like button | `[data-testid="like"]` |
| Bookmark button | `[data-testid="bookmark"]` |
| Metrics container | `[data-testid="app-text-transition-container"]` |
| Column content | `[data-testid="multi-column-layout-column-content"]` |
| Column header | `[data-testid="column-title-wrapper"]` |

---

## Extracting Author Info

The `User-Name` element contains text in format: `AuthorName@handle·time`

```javascript
const userEl = tweet.querySelector('[data-testid="User-Name"]');
const text = userEl?.textContent || '';
const author = text.split('@')[0]?.trim();
const handle = '@' + (text.split('@')[1]?.split('·')[0]?.trim() || '');
```

---

## Extracting Metrics

Metrics are inside buttons, within `app-text-transition-container`:

```javascript
const getMetric = (tweet, buttonTestId) => {
  const btn = tweet.querySelector(`[data-testid="${buttonTestId}"]`);
  return btn?.querySelector('[data-testid="app-text-transition-container"]')?.textContent || '0';
};

const replies = getMetric(tweet, 'reply');
const retweets = getMetric(tweet, 'retweet');
const likes = getMetric(tweet, 'like');
```

### Parsing Metric Numbers

Metrics may have K/M suffixes:

```javascript
const parseMetric = (s) => {
  if (!s || s === '0') return 0;
  s = s.replace(/,/g, '');
  if (s.includes('K')) return parseFloat(s) * 1000;
  if (s.includes('M')) return parseFloat(s) * 1000000;
  return parseInt(s) || 0;
};
```

---

## Extracting Timestamps

```javascript
const timeEl = tweet.querySelector('time');
const displayTime = timeEl?.textContent || '';  // "2h", "15m", etc.
const isoTime = timeEl?.getAttribute('datetime') || '';  // ISO 8601
```

---

## Extracting Tweet URL

```javascript
const timeEl = tweet.querySelector('time');
const tweetUrl = timeEl?.closest('a')?.href || '';
// Returns: "https://x.com/{handle}/status/{tweet_id}"
```

---

## Complete Extraction Script

Run via `javascript_tool` on any `pro.x.com` page:

```javascript
const extractTweets = () => {
  const tweets = [];
  const columns = document.querySelectorAll('[data-testid="multi-column-layout-column-content"]');

  columns.forEach((column) => {
    const parent = column.closest('section') || column.parentElement;
    const columnName = parent?.querySelector('[data-testid="column-title-wrapper"]')?.textContent?.trim() || 'Unknown';

    column.querySelectorAll('[data-testid="tweet"]').forEach((tweet) => {
      try {
        const author = tweet.querySelector('[data-testid="User-Name"]')?.textContent || '';
        const content = tweet.querySelector('[data-testid="tweetText"]')?.textContent || '';
        const timeEl = tweet.querySelector('time');
        const tweetUrl = timeEl?.closest('a')?.href || '';

        const parseMetric = (s) => {
          if (!s || s === '0') return 0;
          s = s.replace(/,/g, '');
          if (s.includes('K')) return parseFloat(s) * 1000;
          if (s.includes('M')) return parseFloat(s) * 1000000;
          return parseInt(s) || 0;
        };

        const getMetric = (testId) => parseMetric(
          tweet.querySelector(`[data-testid="${testId}"] [data-testid="app-text-transition-container"]`)?.textContent
        );

        if (content && content.length > 20 && tweetUrl) {
          tweets.push({
            column: columnName,
            author: author.split('@')[0]?.trim(),
            handle: '@' + (author.split('@')[1]?.split('·')[0]?.trim() || ''),
            content: content.substring(0, 400),
            time: timeEl?.textContent || '',
            datetime: timeEl?.getAttribute('datetime') || '',
            url: tweetUrl,
            replies: getMetric('reply'),
            retweets: getMetric('retweet'),
            likes: getMetric('like')
          });
        }
      } catch(e) {}
    });
  });

  return tweets;
};
JSON.stringify(extractTweets());
```

---

## Accumulation Pattern (Getting More Tweets)

X Pro uses DOM virtualization. To get more than ~10 tweets per column:

```javascript
// Initialize accumulator once
if (!window.accumulatedTweets) {
  window.accumulatedTweets = new Map();
}

// After each extraction, merge into accumulator
tweets.forEach(t => {
  const key = t.handle + ':' + t.content.substring(0, 80);
  if (!window.accumulatedTweets.has(key)) {
    window.accumulatedTweets.set(key, t);
  }
});
```

### Scroll and Accumulate Workflow

1. Run initial extraction (captures ~60-70 tweets from visible columns)
2. Scroll multiple columns down:
   ```
   scroll at (280, 400) down 5 ticks   // Column 1
   scroll at (760, 400) down 5 ticks   // Column 2
   scroll at (1200, 400) down 5 ticks  // Column 3
   ```
3. Re-run extraction — new tweets merge into accumulator, duplicates ignored
4. Repeat 2-3 times to get 100+ tweets
5. Access all accumulated tweets: `Array.from(window.accumulatedTweets.values())`

### Column X Coordinates (Typical Layout)

| Column Position | X Coordinate |
|-----------------|--------------|
| Column 1 | 280 |
| Column 2 | 760 |
| Column 3 | 1200 |
| Column 4 | 1640 |

Use Y coordinate ~400 (middle of column) for scroll actions.

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Empty results | Page still loading — add wait before extraction |
| Missing columns | User has different deck layout — adapt column detection |
| Stale data | X Pro updates in real-time — re-run extraction for fresh data |
| Metrics showing "0" | Tweet has no engagement OR selector changed |

---

*X can change DOM selectors at any time. If extraction fails, inspect the page in DevTools to find updated selectors.*
