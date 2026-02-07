# X Reply Posting

Post replies to tweets on X (Twitter) via Chrome browser automation. Teaches Claude how to navigate X's reply interface and submit replies reliably.

## What It Does

- Posts replies to tweets using the inline reply box on x.com
- Handles contenteditable div activation with physical clicks
- Inserts text via `execCommand` for proper React state updates
- Submits with keyboard shortcut (`cmd+Return`) for reliability
- Verifies reply appeared in DOM before confirming success
- Handles 404s by searching for tweets via X search

## Prerequisites

- Chrome browser with X/Twitter open and logged in
- Chrome MCP extension connected

## Usage

"Reply to this tweet: [url]"
"Post a reply on this X thread"
"Respond to these tweets with [message]"

Claude will navigate to the tweet, activate the reply box, insert your text, submit via keyboard shortcut, and verify the reply posted.

## Install

```
/plugin install x-reply-posting@blockchainhb-plugins
```

## Author
[@hasaamb](https://x.com/hasaamb)
