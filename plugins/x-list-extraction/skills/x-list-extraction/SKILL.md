---
name: x-list-extraction
description: Extract tweets from X Pro (TweetDeck) lists via GraphQL API and DOM scraping. Use when automating X Pro, scraping tweet lists, or building workflows that need structured tweet data from curated lists.
---

# X Pro List Extraction

Extract tweets from X Pro (pro.x.com) lists using the internal GraphQL API or DOM scraping. Returns structured tweet data including full text, engagement metrics, author info, and direct URLs.

## Prerequisites

- Chrome browser with X Pro open (`pro.x.com`) and logged in
- Chrome MCP extension connected (`mcp__claude-in-chrome__*` tools available)
- User must be on any `pro.x.com` page (needs session cookies)

Verify Chrome MCP is available:
```
mcp__claude-in-chrome__tabs_context_mcp
```

If it errors: tell the user "Chrome MCP isn't connected. Open Chrome with the Claude extension active."

---

## Method 1: GraphQL API (Preferred)

The API returns full tweet text, 40+ tweets per call, and stable structured data. Far more reliable than DOM scraping.

### Authentication

Two tokens required. Bearer is static (same for all X Pro users). CSRF is dynamic (extract each session from cookies).

```
Bearer: AAAAAAAAAAAAAAAAAAAAAFQODgEAAAAAVHTp76lzh3rFzcHbmHVvQxYYpTw%3DckAlMINMjmCwxUcaXbAN4XqJVdgMJaHqNOFgPMK0zN1qLqLQCF
CSRF:   document.cookie.match(/ct0=([^;]+)/)[1]
```

### Step 1: Find Your List IDs

If you don't know your list IDs, fetch them:

```javascript
(async () => {
  const ct0 = document.cookie.match(/ct0=([^;]+)/)[1];
  const bearer = 'Bearer AAAAAAAAAAAAAAAAAAAAAFQODgEAAAAAVHTp76lzh3rFzcHbmHVvQxYYpTw%3DckAlMINMjmCwxUcaXbAN4XqJVdgMJaHqNOFgPMK0zN1qLqLQCF';
  const resp = await fetch('https://pro.x.com/i/api/1.1/lists/list.json', {
    credentials: 'include',
    headers: { 'authorization': bearer, 'x-csrf-token': ct0, 'x-twitter-auth-type': 'OAuth2Session', 'x-twitter-active-user': 'yes' }
  });
  const data = await resp.json();
  return data.map(l => ({ id: l.id_str, name: l.name, members: l.member_count }));
})();
```

### Step 2: Inject the Extraction Function

Run once per session via `javascript_tool`:

```javascript
window.fetchListTweets = async (listId, listName) => {
  const ct0 = document.cookie.match(/ct0=([^;]+)/)[1];
  const bearer = 'Bearer AAAAAAAAAAAAAAAAAAAAAFQODgEAAAAAVHTp76lzh3rFzcHbmHVvQxYYpTw%3DckAlMINMjmCwxUcaXbAN4XqJVdgMJaHqNOFgPMK0zN1qLqLQCF';
  const features = {
    rweb_video_screen_enabled:false,
    profile_label_improvements_pcf_label_in_post_enabled:true,
    responsive_web_profile_redirect_enabled:false,
    rweb_tipjar_consumption_enabled:true,
    verified_phone_label_enabled:false,
    creator_subscriptions_tweet_preview_api_enabled:true,
    responsive_web_graphql_timeline_navigation_enabled:true,
    responsive_web_graphql_skip_user_profile_image_extensions_enabled:false,
    premium_content_api_read_enabled:false,
    communities_web_enable_tweet_community_results_fetch:true,
    c9s_tweet_anatomy_moderator_badge_enabled:true,
    responsive_web_grok_analyze_button_fetch_trends_enabled:false,
    responsive_web_grok_analyze_post_followups_enabled:true,
    responsive_web_jetfuel_frame:true,
    responsive_web_grok_share_attachment_enabled:true,
    responsive_web_grok_annotations_enabled:false,
    articles_preview_enabled:true,
    responsive_web_edit_tweet_api_enabled:true,
    graphql_is_translatable_rweb_tweet_is_translatable_enabled:true,
    view_counts_everywhere_api_enabled:true,
    longform_notetweets_consumption_enabled:true,
    responsive_web_twitter_article_tweet_consumption_enabled:true,
    tweet_awards_web_tipping_enabled:false,
    responsive_web_grok_show_grok_translated_post:false,
    responsive_web_grok_analysis_button_from_backend:true,
    post_ctas_fetch_enabled:true,
    creator_subscriptions_quote_tweet_preview_enabled:false,
    freedom_of_speech_not_reach_fetch_enabled:true,
    standardized_nudges_misinfo:true,
    tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled:true,
    longform_notetweets_rich_text_read_enabled:true,
    longform_notetweets_inline_media_enabled:true,
    responsive_web_grok_image_annotation_enabled:true,
    responsive_web_grok_imagine_annotation_enabled:true,
    responsive_web_grok_community_note_auto_translation_is_enabled:false,
    responsive_web_enhance_cards_enabled:false
  };

  const url = 'https://pro.x.com/i/api/graphql/yy0Um4WvD38oT4GG9fIInw/ListLatestTweetsTimeline?variables=' +
    encodeURIComponent(JSON.stringify({listId,count:40,includePromotedContent:false})) + '&features=' + encodeURIComponent(JSON.stringify(features));

  const data = await fetch(url, {
    credentials: 'include',
    headers: {
      'authorization': bearer,
      'x-csrf-token': ct0,
      'x-twitter-auth-type': 'OAuth2Session',
      'x-twitter-active-user': 'yes',
      'x-twitter-client-language': 'en',
      'content-type': 'application/json'
    }
  }).then(r => r.json());

  return (data?.data?.list?.tweets_timeline?.timeline?.instructions?.find(i => i.type === 'TimelineAddEntries')?.entries || []).map(e => {
    const r = e.content?.itemContent?.tweet_results?.result;
    const tweet = r?.__typename === 'TweetWithVisibilityResults' ? r.tweet : r;
    if (!tweet?.legacy) return null;
    const leg = tweet.legacy, user = tweet.core?.user_results?.result?.core;
    const isRT = leg.full_text.startsWith('RT @');
    const orig = leg.retweeted_status_result?.result;
    const origTweet = isRT && orig ? (orig.__typename === 'TweetWithVisibilityResults' ? orig.tweet : orig) : null;
    const dLeg = origTweet?.legacy || leg;
    const dUser = origTweet?.core?.user_results?.result?.core || user;
    // Use rest_id (canonical tweet ID) — legacy.id_str can be stale/wrong and cause 404s
    const tweetId = origTweet?.rest_id || tweet.rest_id;
    const screenName = dUser?.screen_name || '';
    return { id: tweetId, text: dLeg.full_text, author: dUser?.name||'', handle: '@'+screenName, time: dLeg.created_at, likes: dLeg.favorite_count||0, replies: dLeg.reply_count||0, retweets: dLeg.retweet_count||0, followers: user?.followers_count || 0, isRT, url: `https://x.com/${screenName}/status/${tweetId}`, list: listName };
  }).filter(Boolean);
};
'ready';
```

### Step 3: Inject User Bio Fetcher (Optional)

```javascript
window.fetchUserBio = async (screenName) => {
  const ct0 = document.cookie.match(/ct0=([^;]+)/)[1];
  const bearer = 'Bearer AAAAAAAAAAAAAAAAAAAAAFQODgEAAAAAVHTp76lzh3rFzcHbmHVvQxYYpTw%3DckAlMINMjmCwxUcaXbAN4XqJVdgMJaHqNOFgPMK0zN1qLqLQCF';
  const features = {hidden_profile_subscriptions_enabled:true,hidden_profile_likes_enabled:true,rweb_tipjar_consumption_enabled:true,responsive_web_graphql_exclude_directive_enabled:true,verified_phone_label_enabled:false,subscriptions_verification_info_is_identity_verified_enabled:true,subscriptions_verification_info_verified_since_enabled:true,highlights_tweets_tab_ui_enabled:true,responsive_web_twitter_article_notes_tab_enabled:true,creator_subscriptions_tweet_preview_api_enabled:true,responsive_web_graphql_skip_user_profile_image_extensions_enabled:false,responsive_web_graphql_timeline_navigation_enabled:true};
  const variables = encodeURIComponent(JSON.stringify({screen_name:screenName,withSafetyModeUserFields:true}));
  const url = `https://pro.x.com/i/api/graphql/xc8f1g7BYqr6VTzTbvNlGw/UserByScreenName?variables=${variables}&features=${encodeURIComponent(JSON.stringify(features))}`;
  const data = await fetch(url, {
    credentials: 'include',
    headers: { 'authorization': bearer, 'x-csrf-token': ct0, 'x-twitter-auth-type': 'OAuth2Session', 'x-twitter-active-user': 'yes' }
  }).then(r => r.json());
  const u = data?.data?.user?.result?.legacy;
  return { bio: u?.description || '', followers: u?.followers_count || 0, name: u?.name || '' };
};
'fetchUserBio ready';
```

### Step 4: Fetch Tweets from Your Lists

Replace the list IDs and names with your own (from Step 1):

```javascript
window.allTweets = [];
const lists = [
  ['YOUR_LIST_ID_1', 'List Name 1'],
  ['YOUR_LIST_ID_2', 'List Name 2']
  // Add more lists as needed
];
(async () => {
  for (const [id, name] of lists) {
    try {
      const tweets = await window.fetchListTweets(id, name);
      window.allTweets.push(...tweets);
    } catch(e) {}
  }
  console.log('Total:', window.allTweets.length);
})();
'fetching lists...';
```

Wait 3 seconds, then check: `window.allTweets.length`

### Step 5: Batch-Fetch Bios (Optional)

```javascript
const handles = [...new Set(window.allTweets.slice(0, 15).map(t => t.handle.replace('@', '')))];
window.authorBios = {};
for (const h of handles) {
  try { window.authorBios[h] = await window.fetchUserBio(h); } catch(e) {}
}
JSON.stringify(Object.keys(window.authorBios).length + ' bios fetched');
```

### Before Navigating Away

**Extract and store everything as agent context.** Once you leave `pro.x.com`, all `window.*` state is gone. Save:
1. `window.allTweets` (or top N)
2. `window.authorBios` (if fetched)
3. Tweet URLs, handles, full text for each target

---

## Method 2: DOM Scraping (Fallback)

Use when the API fails or you only need visible tweets. Limited by virtualization (~10 tweets per column).

See `references/dom-extraction.md` for the complete DOM scraping approach.

---

## API Response Structure

```
data.list.tweets_timeline.timeline.instructions[].entries[].content.itemContent.tweet_results.result
  ├── __typename: "Tweet" | "TweetWithVisibilityResults"
  ├── rest_id: "tweet_id"  (ALWAYS use this, not legacy.id_str)
  ├── core.user_results.result.core
  │     ├── name: "Display Name"
  │     └── screen_name: "handle"
  └── legacy
        ├── full_text: "Complete tweet text"
        ├── favorite_count: likes
        ├── retweet_count: retweets
        ├── reply_count: replies
        └── retweeted_status_result (for RTs)
```

---

## API vs DOM Comparison

| Factor | DOM Extraction | API Extraction |
|--------|---------------|----------------|
| Content | Truncated to visible | Full text always |
| Virtualization | Only ~10 tweets/column | 40+ tweets per call |
| User data | Sometimes missing | Always present |
| Reliability | Selectors can change | Stable response format |
| Speed | Multiple scrolls needed | Single request |

---

## Critical Notes

- **Use `rest_id` not `legacy.id_str`** for tweet IDs. `legacy.id_str` can be stale and cause 404s when navigating to the tweet URL.
- **Chrome MCP `javascript_tool` times out after ~10s.** Keep scripts short. If you get "Detached while handling command", the fetch likely completed in the background.
- **Bearer token is static** across all X Pro users. CSRF token (`ct0`) must be extracted fresh each session from cookies.

---

*Reverse-engineered Feb 2026. X can change internal APIs at any time. If calls start failing, re-intercept via DevTools Network tab on pro.x.com.*
