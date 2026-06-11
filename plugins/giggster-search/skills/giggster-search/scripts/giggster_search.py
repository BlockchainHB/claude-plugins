#!/usr/bin/env python3
"""Giggster venue search via their internal (unauthenticated) API.

Reverse-engineered June 2026 from giggster.com's search bundle.
Endpoints (base https://api.giggster.com):
  GET /locations/ft-search   - paginated listing search
  GET /locations/ft-total    - count only ({"total": N})
  GET /locations/{id}        - full listing detail (rules, limits, prices)
  GET /locations/{id}/open-hours - per-day hours; "30:00" = 6AM next day; null body = no record

Usage examples:
  giggster_search.py --activity birthday-party --date 2026-06-20 --rules alcohol,loud-noises
  giggster_search.py --city toronto --activity wedding --min-cap 100 --max-hourly 200 \
      --date 2026-07-04 --from 21:00 --until 28:00 --out venues.csv
"""
import argparse, csv, html, json, re, sys, time
import urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

API = "https://api.giggster.com"
UA = {"User-Agent": "Mozilla/5.0"}

# geo = "ne.lat,ne.lng,sw.lat,sw.lng" (map bounds). Add cities as needed.
CITY_PRESETS = {
    "toronto": {"place": "Toronto", "country": "CA", "geo": "43.8555,-79.1168,43.5810,-79.6393"},
    "mississauga": {"place": "Mississauga", "country": "CA", "geo": "43.7315,-79.5249,43.4810,-79.8104"},
    "vancouver": {"place": "Vancouver", "country": "CA", "geo": "49.3168,-123.0234,49.1984,-123.2247"},
}

# Valid values for --rules (require ALL listed): adult-filming, electricity-usage,
# smoking, pets, external-catering, cooking, alcohol, loud-noises
RULES = ["adult-filming", "electricity-usage", "smoking", "pets",
         "external-catering", "cooking", "alcohol", "loud-noises"]


def get(path, params=None, retries=3):
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode())
        except Exception:
            if i == retries - 1:
                return None
            time.sleep(1.5)


def hhmm(s):
    h, m = s.split(":")
    return int(h) + int(m) / 60


def search_all(args):
    params = {
        "place": args.place, "country": args.country, "geo": args.geo,
        "offset": 0, "limit": 50, "sort_order": "desc", "includes": "owner",
    }
    if args.activity:
        params["q_activity"] = args.activity
    if args.date:
        # interval only supports same-day windows; overnight is checked via open-hours
        params["interval"] = f"{args.date} {args.avail_from}-{args.avail_to}"
    if args.rules:
        params["rules"] = args.rules
    items, seen = [], set()
    while True:
        d = get("/locations/ft-search", params)
        if not d or not d.get("items"):
            break
        new = [i for i in d["items"] if i["id"] not in seen]
        if not new:
            break
        for i in new:
            seen.add(i["id"])
        items.extend(new)
        if len(d["items"]) < 50:
            break
        params["offset"] += 50
        time.sleep(0.5)
    return items


def fetch_hours(ids):
    def one(lid):
        return lid, get(f"/locations/{lid}/open-hours")
    with ThreadPoolExecutor(6) as ex:
        return dict(ex.map(one, ids))


def fetch_details(ids):
    def one(lid):
        return lid, get(f"/locations/{lid}")
    with ThreadPoolExecutor(6) as ex:
        return dict(ex.map(one, ids))


def day_fit(hours_rec, day, start_f, end_f):
    """Return (fit_label, hours_str). end_f may exceed 24 (e.g. 28.0 = 4AM next day)."""
    if not hours_rec or "opening_hours" not in (hours_rec or {}):
        return "unknown", "no record"
    d = hours_rec["opening_hours"].get(day)
    if not d or not d.get("is_open"):
        return "closed", "closed"
    o, c = d["hours"]
    of, cf = hhmm(o), hhmm(c)
    s = f"{o}-{c}"
    if of <= start_f and cf >= end_f:
        return "full", s
    if of <= start_f and cf >= min(end_f, 24):
        return "partial", s
    return "limited", s


DESC_RED_FLAGS = [
    (r"non-?alcoholic", "NO ALCOHOL"),
    (r"turned down by \d|music.{0,30}down by|no music after|quiet hours|noise curfew", "MUSIC CURFEW"),
    (r"no part(y|ies)", "NO PARTIES"),
]


def main():
    ap = argparse.ArgumentParser(description="Search Giggster venues")
    ap.add_argument("--city", default="toronto", help=f"preset: {', '.join(CITY_PRESETS)} (or pass --place/--geo/--country)")
    ap.add_argument("--place"); ap.add_argument("--geo"); ap.add_argument("--country")
    ap.add_argument("--activity", default="", help="e.g. birthday-party, wedding, film-shoot")
    ap.add_argument("--date", help="YYYY-MM-DD availability date")
    ap.add_argument("--avail-from", default="09:00", help="same-day availability window start")
    ap.add_argument("--avail-to", default="23:59", help="same-day availability window end")
    ap.add_argument("--rules", default="", help=f"comma list, require all: {','.join(RULES)}")
    ap.add_argument("--day", default="Saturday", help="weekday for open-hours fit check")
    ap.add_argument("--from", dest="from_h", default="21:00", help="party start HH:MM")
    ap.add_argument("--until", default="28:00", help="party end; >24:00 = past midnight (28:00 = 4AM)")
    ap.add_argument("--min-cap", type=int, default=0, help="min standing capacity / max attendees")
    ap.add_argument("--max-hourly", type=int, default=0, help="max event hourly price")
    ap.add_argument("--details", action="store_true", help="fetch full detail per match (BYO/DJ/smoking/red flags)")
    ap.add_argument("--out", help="write CSV here (default: print JSON to stdout)")
    args = ap.parse_args()

    preset = CITY_PRESETS.get(args.city, CITY_PRESETS["toronto"])
    args.place = args.place or preset["place"]
    args.geo = args.geo or preset["geo"]
    args.country = args.country or preset["country"]

    items = search_all(args)
    print(f"search returned {len(items)} listings", file=sys.stderr)

    hours = fetch_hours([i["id"] for i in items])
    start_f, end_f = hhmm(args.from_h), hhmm(args.until)

    rows = []
    for it in items:
        p = it.get("properties", {})
        cap = p.get("max-attendees", {}).get("value") or 0
        price = (p.get("price-lvl0-event-hourly", {}).get("value")
                 or p.get("price-base-hourly", {}).get("value"))
        if args.min_cap and cap < args.min_cap:
            continue
        if args.max_hourly and (not price or price > args.max_hourly):
            continue
        fit, hstr = day_fit(hours.get(it["id"]), args.day, start_f, end_f)
        if fit in ("closed", "limited"):
            continue
        rows.append({
            "id": it["id"], "title": html.unescape(it["title"]),
            "url": f"https://giggster.com/listing/{it['slug']}",
            "hours_fit": fit, "day_hours": hstr,
            "capacity": cap, "event_hourly": price,
            "min_hours": p.get("min-hours", {}).get("value"),
            "rating": round(((it.get("rating") or {}).get("summary") or 0) * 5, 2),
            "bookings": it.get("bookings_count", 0),
            "zipcode": it.get("address", {}).get("zipcode", ""),
        })

    if args.details and rows:
        details = fetch_details([r["id"] for r in rows])
        for r in rows:
            d = details.get(r["id"]) or {}
            p = d.get("properties", {})
            rules = p.get("rules", {}).get("value", {})
            desc = html.unescape(d.get("description", "")).lower()
            flags = [label for pat, label in DESC_RED_FLAGS if re.search(pat, desc)]
            r.update({
                "byo_alcohol": p.get("celebrate-byo-alcohol", {}).get("checked"),
                "own_dj": p.get("celebrate-own-dj", {}).get("checked"),
                "pa_system": p.get("celebrate-pa-system", {}).get("checked"),
                "standing_limit": p.get("celebrate-standing-limit", {}).get("value"),
                "smoking_indoors": rules.get("smoking"),
                "alcohol_rule": rules.get("alcohol"),
                "loud_noises_rule": rules.get("loud-noises"),
                # currency: 2 = CAD, 1 = USD
                "currency": {1: "USD", 2: "CAD"}.get(p.get("currency", {}).get("value")),
                "red_flags": "; ".join(flags),
            })

    rows.sort(key=lambda r: (r["hours_fit"] != "full", -(r["rating"] or 0), -(r["bookings"] or 0)))
    print(f"{len(rows)} venues after filters", file=sys.stderr)

    if args.out:
        keys = list(rows[0].keys()) if rows else []
        with open(args.out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        json.dump(rows, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
