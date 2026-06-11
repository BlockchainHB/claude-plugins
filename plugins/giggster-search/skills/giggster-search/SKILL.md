---
name: giggster-search
description: Search Giggster event/venue rentals via their internal API instead of clicking through the website. Use when the user wants to find an event space, party venue, film/photo location, or asks to "check Giggster". Filters by date availability, house rules (alcohol, loud noise, smoking), capacity, budget, and overnight operating hours — then shortlists.
---

# Giggster Venue Search

Giggster's search API is unauthenticated and much faster than browsing the site
(hundreds of listings paged in the UI = a few API calls). Reverse-engineered June 2026
and verified working. If results ever come back empty or error, re-derive params from
the live bundle: fetch any giggster.com/search page, grab `/static/scripts/search.*.js`,
and look for the `async function d({query...` param builder near `ft-search`.

## Quick start

```bash
python3 scripts/giggster_search.py \
  --city toronto --activity birthday-party \
  --date 2026-06-20 --rules alcohol,loud-noises \
  --day Saturday --from 21:00 --until 30:00 \
  --min-cap 40 --max-hourly 220 --details --out /tmp/venues.csv
```

Run `--help` for all flags. Without `--out` it prints JSON to stdout. The script only
needs the Python standard library.

## Key API facts (base: https://api.giggster.com, no auth)

| Endpoint | Purpose |
|----------|---------|
| `GET /locations/ft-search` | paginated search (`items`) |
| `GET /locations/ft-total` | count only (`{"total": N}`) |
| `GET /locations/{id}` | full detail: rules dict, BYO alcohol, own DJ, PA, standing/sitting limits |
| `GET /locations/{id}/open-hours` | per-weekday hours; literal `null` body = no record (treat as unknown) |

Search params:
- `geo` (REQUIRED): map bounds `ne.lat,ne.lng,sw.lat,sw.lng`. Toronto: `43.8555,-79.1168,43.5810,-79.6393`
- `place` (city name), `country` (e.g. `CA`), `q_activity` (slug, e.g. `birthday-party`)
- `interval`: `YYYY-MM-DD HH:MM-HH:MM` — calendar availability, same-day only
- `rules`: comma list, listing must allow ALL. Valid: `alcohol`, `loud-noises`, `smoking`,
  `pets`, `cooking`, `external-catering`, `electricity-usage`, `adult-filming`
- `offset`/`limit` (max 50), `sort_order=desc`, `includes=owner`
- `sort_by` is finicky — omit it (only `distance`/`relevance`/`default` accepted, NOT `geo`)

Gotchas:
- Hours use a >24h clock: `"27:00"` = 3AM next day, `"30:00"` = 6AM. A venue listed
  `06:00-30:00` is effectively round-the-clock.
- `properties.currency.value`: 2 = CAD, 1 = USD (mixed within one city!).
- Event price = `properties["price-lvl0-event-hourly"].value`, fallback `price-base-hourly`.
- `celebrate-standing-limit` is the real party capacity; `max-attendees` can be 99999.
- Search results omit the rules dict — only `/locations/{id}` detail has it.

## Workflow for a venue shortlist

1. Run the script with rule/capacity/budget filters and `--details`.
2. **Always read descriptions of finalists** — filters lie by omission. Real examples
   caught: a "smoking friendly" patio requiring music down by 10PM; a bar that is
   strictly non-alcoholic. The script flags `MUSIC CURFEW` / `NO ALCOHOL` / `NO PARTIES`
   patterns in `red_flags`, but skim the full text of top picks anyway.
3. Compute total cost = hourly × booking hours; respect `min_hours`.
4. Cross-midnight bookings: Giggster's calendar filter only covers same-day. Verify the
   overnight stretch via open-hours AND tell the user to confirm with the host before paying.
5. Deliver the shortlist however the user prefers (table, CSV, or a spreadsheet) with
   per-venue totals, capacity, policies (BYO alcohol / own DJ / smoking), and listing links.
