# Giggster Venue Search

Search Giggster event/venue rentals via their internal API instead of clicking through the website. Teaches Claude how to query Giggster's unauthenticated search API directly, filter hundreds of listings in seconds, and produce a vetted shortlist.

## What It Does

- Queries Giggster's internal API (`api.giggster.com`) — no login or API key needed
- Filters by date availability, house rules (alcohol, loud noise, smoking, pets, catering), capacity, and budget
- Checks per-venue operating hours, including overnight windows (Giggster uses a >24h clock: `30:00` = 6AM next day)
- Enriches finalists with full policy details: BYO alcohol, own DJ, PA system, real standing capacity
- Scans listing descriptions for red flags the filters miss (music curfews, "no parties", non-alcoholic venues)
- Outputs JSON or CSV, ready to drop into a spreadsheet

## Includes

- `scripts/giggster_search.py` — end-to-end CLI (Python stdlib only, no dependencies)
- City presets for Toronto, Mississauga, Vancouver; any city works with `--place/--geo/--country`

## Usage

"Find me an event space on Giggster for a birthday party June 20, 40 people, $2000 budget"
"Check Giggster for film shoot locations in Toronto that allow smoking"
"Search Giggster for venues open past 2AM that allow loud music"

Claude will run the search script with the right filters, read the finalists' fine print, and deliver a shortlist with per-venue totals, capacities, policies, and listing links.

## Install

```
/plugin install giggster-search@blockchainhb-plugins
```
