# LinkedIn Connections API

Send LinkedIn connection requests via the internal Voyager API. Teaches Claude how to navigate LinkedIn's API to send connection invites programmatically through Chrome browser automation.

## What It Does

- Sends connection requests using LinkedIn's Voyager API (no UI clicking needed)
- Looks up profile URNs from usernames automatically
- Supports batch connection requests with built-in delays
- Handles rate limits and response codes (already sent, session expired, etc.)
- Falls back to browser DOM method when the API is unavailable
- Extracts profile research data for personalized connection messages

## Prerequisites

- Chrome browser with LinkedIn open and logged in
- Chrome MCP extension connected

## Usage

"Send a connection request to [linkedin profile url]"
"Connect with these LinkedIn profiles: [list of urls]"
"Send LinkedIn invites to these people"

Claude will extract usernames, look up URNs via the Voyager API, and send connection requests with proper rate limiting.

## Install

```
/plugin install linkedin-connect-api@blockchainhb-plugins
```

## Author
[@hasaamb](https://x.com/hasaamb)
