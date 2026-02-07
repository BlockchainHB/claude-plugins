# X Pro List Extraction

Extract tweets from X Pro (TweetDeck) lists via GraphQL API and DOM scraping. Teaches Claude how to navigate X Pro and pull structured tweet data through Chrome browser automation.

## What It Does

- Extracts 40+ tweets per list via X Pro's internal GraphQL API
- Returns full text, engagement metrics (likes, retweets, replies), author info, and direct URLs
- Fetches user bios and profile data for context
- Falls back to DOM scraping when the API is unavailable
- Supports batch fetching from multiple lists in a single session

## Prerequisites

- Chrome browser with X Pro (`pro.x.com`) open and logged in
- Chrome MCP extension connected

## Usage

"Extract tweets from my X Pro lists"
"Pull the latest tweets from my tech list on TweetDeck"
"Get tweets with engagement metrics from X Pro"

Claude will authenticate using your session cookies, fetch tweets via the GraphQL API, and return structured data you can use for analysis or follow-up actions.

## Install

```
/plugin install x-list-extraction@blockchainhb-plugins
```

## Author
[@hasaamb](https://x.com/hasaamb)
