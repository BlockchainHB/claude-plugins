# LinkedIn Reply API

Post comments on LinkedIn posts via the internal Voyager API. Teaches Claude how to navigate LinkedIn's comment system through Chrome browser automation without navigating to individual posts.

## What It Does

- Posts comments on LinkedIn posts using the Voyager API
- Extracts activity IDs from any LinkedIn post URL format
- One comment per API call to avoid Chrome MCP timeouts
- Returns comment URN for verification
- Falls back to browser DOM method when the API is unavailable
- Includes post extraction script for gathering posts from the feed

## Prerequisites

- Chrome browser with LinkedIn open and logged in
- Chrome MCP extension connected

## Usage

"Comment on this LinkedIn post: [url]"
"Post replies to these LinkedIn posts"
"Leave a comment on [person]'s latest post"

Claude will extract the activity ID, authenticate via session cookies, and post your comment through the Voyager API.

## Install

```
/plugin install linkedin-reply-api@blockchainhb-plugins
```

## Author
[@hasaamb](https://x.com/hasaamb)
