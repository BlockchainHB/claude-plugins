<div align="center">

# `@blockchainhb/plugins`

**Battle-tested Claude Code plugins for real workflows — git, social APIs, project management, and research.**

[![Skills](https://www.skills.sh/b/BlockchainHB/claude-plugins)](https://skills.sh/BlockchainHB/claude-plugins)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](./LICENSE)
[![Plugins](https://img.shields.io/badge/plugins-11-blue.svg)](#whats-inside)
[![Claude Code](https://img.shields.io/badge/Claude_Code-marketplace-d97757.svg)](https://code.claude.com/docs/en/plugins)

<br>

```
/plugin marketplace add BlockchainHB/claude-plugins
```

</div>

<br>

## What's Inside

Every plugin ships a skill that Claude auto-triggers when relevant — no memorizing commands. Several encode reverse-engineered internal APIs (LinkedIn Voyager, X GraphQL, Giggster) so Claude works through fast API calls instead of slow UI clicking.

<br>

### ⚡ Git & Delivery

| Plugin | What it does |
|:-------|:-------------|
| **[git-commit](./plugins/git-commit)** | Detailed, well-structured commits in conventional format. <br><sub>`conventional commits` `safety checks` `detailed messages`</sub> |
| **[pull-request](./plugins/pull-request)** | PRs with comprehensive descriptions, labels, and review setup. <br><sub>`PR templates` `labels` `review setup`</sub> |
| **[feature-setup](./plugins/feature-setup)** | New features set up systematically, from planning to implementation. <br><sub>`requirements` `branching` `architecture`</sub> |
| **[linear-mcp](./plugins/linear-mcp)** | Linear project management via MCP tools. <br><sub>`issues` `projects` `initiatives` `GraphQL`</sub> |

### 📣 Social & Outreach

| Plugin | What it does |
|:-------|:-------------|
| **[linkedin-connect-api](./plugins/linkedin-connect-api)** | Connection requests via LinkedIn's internal Voyager API — no UI clicking. <br><sub>`Voyager API` `batch requests` `rate limits`</sub> |
| **[linkedin-reply-api](./plugins/linkedin-reply-api)** | Comments on LinkedIn posts via the Voyager API. <br><sub>`Voyager API` `comments` `activity URNs`</sub> |
| **[x-list-extraction](./plugins/x-list-extraction)** | Tweet extraction from X Pro lists via GraphQL + DOM scraping. <br><sub>`GraphQL` `engagement metrics` `structured data`</sub> |
| **[x-reply-posting](./plugins/x-reply-posting)** | Replies posted to X through Chrome browser automation. <br><sub>`Chrome automation` `keyboard submit` `verification`</sub> |

### ✍️ Content & Design

| Plugin | What it does |
|:-------|:-------------|
| **[tailwind-illustrations](./plugins/tailwind-illustrations)** | Polished, interactive landing-page illustrations with Tailwind CSS. <br><sub>`dashboard previews` `hero sections` `tab-based screenshots`</sub> |
| **[human-writing](./plugins/human-writing)** | Authentic, human-sounding content that avoids AI writing patterns. <br><sub>`landing pages` `emails` `blogs` `marketing copy`</sub> |

### 🔎 Research & Utilities

| Plugin | What it does |
|:-------|:-------------|
| **[giggster-search](./plugins/giggster-search)** | Event/venue search via Giggster's internal API — hundreds of listings filtered in seconds. <br><sub>`availability` `house rules` `capacity` `budget` `overnight hours`</sub> |

<br>

## Install

**Option 1 — Claude Code plugin (full experience)**

```
/plugin marketplace add BlockchainHB/claude-plugins
/plugin install <plugin-name>@blockchainhb-plugins
```

**Option 2 — Skills only, any agent ([skills.sh](https://skills.sh))**

Works with Claude Code, Cursor, Codex, and ~70 other agents. Installs just the skills — plugin hooks/commands/MCP servers need Option 1.

```
npx skills add BlockchainHB/claude-plugins
```

<br>

## Quality

Every release passes:

```
claude plugin validate .                  # marketplace manifest
claude plugin validate ./plugins/<name>   # each plugin
```

…and is verified discoverable by `npx skills add`.

<br>

---

<div align="center">
<sub>MIT © <a href="https://x.com/hasaamb">@hasaamb</a> · Built with Claude Code</sub>
</div>
