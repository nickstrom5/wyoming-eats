# Cowboy State Eats (wy-eats) — notes for Claude Code sessions

Built 2026-11-05 by a side session for Nick's "build Utah, Vermont, Virginia, West Virginia and Wyoming", ported from `../wv-eats/`
(itself from `../va-eats/`, `../vt-eats/`, `../ut-eats/` and `../md-eats/`) with every fix to that day (the exact-outline county
lookup, the out-of-county truck rule, Utah's street-word merge fix, Vermont's narrowed "dejavu" rule, Virginia's near-adult-venue fix,
the per-state ZIP check). Local only: git-ignored data, no repo, no remote, nothing published. Sources: `playbook/12-sources.md`.
Brand: `playbook/05-naming.md` — **provisional**, every choice waits for Nick ("Cowboy State Eats: Wyoming Restaurants", Home Screen
"Cowboy State Eats"; a root beer float icon, concept C, on sagebrush; a landscape palette: sagebrush #3E4F3A, red-rock rust #8C3B2A,
Teton blue #2B5C8A, prairie wheat #D9A441 fill only, cream; a band of the Tetons, red-rock foothills and the plains).

## Wyoming is different
- **No official list a script may read.** The Department of Agriculture's Consumer Health Services inspects restaurants wherever no
  local health department does (Teton County runs its own); its reports sit behind a search form (agriculture.wy.gov/chs-inspection-
  reports, linked from each place; the USA Food Safety back end needs a login). Retail liquor licenses are issued by each city and
  county; the Liquor Division (liquor365.wyo.gov) publishes no licensee list. So "Serves alcohol" is unknown everywhere. 0 official places.
- **Counties:** Wyoming's 23; one detail file (`detail-wyoming.json`); the site groups pages by county. `fetch_overture.py` checks the
  border towns (Cheyenne, Evanston, Afton, Jackson, Pine Bluffs, Sheridan and Old Faithful in; West Yellowstone, Gardiner, Kimball,
  Fort Collins, Driggs, Randolph and Belle Fourche out).
- **Far listings:** a rural postal town reaches 50 km and more, so `listings.py` keeps a listing over 30 km from its town's others when
  it has a house-number address in the same county (the South Fork and Wapiti valleys, Moran) or is in Yellowstone (which spans Park
  and Teton counties). Without an address, or in another county, it's still a bad point (the Papa Murphy's filed under "Jackson").
- **Venues:** airport terminals by address (Jackson Hole 1250 E Airport Rd plus the terminal box, Casper 8500 Airport Pkwy, Cheyenne
  4020 Airport Pkwy, Gillette 2000 Airport Rd, Cody 2101 Roger Sedam Dr), War Memorial Stadium, the Arena-Auditorium, the Ford Wyoming
  Center, the CAM-PLEX, Frontier Days, the prisons, F.E. Warren AFB and Yellowstone's employee pubs.
- **Honors:** no MICHELIN Guide covers Wyoming. James Beard: Nora's Fish Creek Inn (America's Classics 2012); 2026 semifinalists
  Glorietta Trattoria (Remle Colestock, Best Chef: Mountain) and Atelier Ortega (Oscar Ortega, pastry); 2025: Atelier Ortega an
  Outstanding Bakery finalist (JinJu Patisserie won), Sitti's Table (Best Chef: Mountain) and Le Rêve (Best New Restaurant)
  semifinalists. No Wyoming finalist in 2026.
- **Guides** (tags in `wyoming.py` TAGS; bits 1..128), all from Travel Wyoming (the Wyoming Office of Tourism; robots allows it,
  Crawl-delay 2): historic saloons (its historic-bars guide, 2026-06-15), steakhouses and cookouts, small-town cafés, soda fountains and
  ice cream (sweet treats, 2025-08-05), farm to table (2025-04-04), pizza, historic hotel dining (historic accommodations, 2025-06-27),
  oldest (founding years from those guides: Miners and Stockmen's 1862 to the Stagecoach Bar 1942). 49 hand-checked entries, all
  matched; five came in by their listing's address (ADDR) and one by Overture's own point (POINT: the Lake Yellowstone Hotel Dining
  Room, whose Travel Wyoming pin sits in Cody). `scripts/read_wyt.py` reads the listings.
- **Ranking:** "Featured first" (honors, then founding year), as everywhere until Nick decides on the all-factor Ranked score
  (`eats-ranked-score-all-states-proposal-2026-11-05.md` in the shared notes); no health-grade wording anywhere.

## Rebuild
```bash
cd pipeline
../.venv/bin/python check_sources.py URL...   # a new host first
../.venv/bin/python fetch_overture.py && ../.venv/bin/python fetch_extras.py && ../.venv/bin/python fetch_official.py
../.venv/bin/python geocode_official.py && ../.venv/bin/python geocode_census.py && ../.venv/bin/python listings.py
../.venv/bin/python calibrate.py && ../.venv/bin/python wyoming.py && ../.venv/bin/python build_research.py && ../.venv/bin/python wyoming.py
WY_APP=1 ../.venv/bin/python wyoming.py && cd .. && cp data/app/places.json data/app/detail-*.json WyomingEats/Resources/
.venv/bin/python pipeline/check_websites.py && .venv/bin/python pipeline/check_websites.py --retry-transient   # then re-export
.venv/bin/python scripts/make-site.py && .venv/bin/python scripts/publish_app_data.py && .venv/bin/python scripts/publish_app_data.py --check
.venv/bin/python scripts/qa-site.py --static
```
(`listings.py` must run before `calibrate.py`, and `wyoming.py` once before `build_research.py`, which matches names against
`site/wyoming.json`.) The `.venv` is on the python.org framework Python 3.12, with md-eats' versions. `data/chain_auv.json` is a copy
of wv-eats'. `data/ucsd/meta-Wyoming.json.gz` (Google 2021, private, web build only) comes from mcauleylab.ucsd.edu's googlelocal set.

## App, site, screenshots
- App: `WyomingEats/` (XcodeGen `project.yml`, bundle `com.wyomingeats.ios`, display "Cowboy State Eats"), tests in `WyomingEatsTests/`
  (data guards: adult venues, blocklisted and multi-URL websites, bad and legal names, non-restaurants, listed twice, no Google data;
  the outline with West Yellowstone, Gardiner, Kimball, Fort Collins and Driggs). Run tests: `DEVELOPER_DIR="/Applications/Xcode
  1.app/Contents/Developer" xcodebuild test ... CODE_SIGNING_ALLOWED=NO` on a temporary simulator. Archive only with Xcode 1.app
  (27.2, 27B52); Xcode.app is a beta. Run `xcodegen generate` whenever the set of `Resources/*.json` files changes.
- Site: `scripts/make-site.py` writes `docs/` and `playbook/site-numbers.json`; `scripts/explore.js` is the web app; `scripts/qa-site.py`
  the QA. Site URL for now: nickstrom5.github.io/wyoming-eats (no CNAME). Rebuild the site before the unit tests (`ShareLinkTests` reads
  `docs/`). City pages: Jackson, Cody, Sheridan and Laramie (four or more listed places each).
- OTA data: `docs/data/app/` via `scripts/publish_app_data.py` (`../OTA-DATA.md`).
- Screenshots: `scripts/capture-screenshots.sh <sim>` (ScreenshotMode pins downtown Casper; Jackson's Town Square for farm, pizza and
  the detail), then `scripts/site-images.sh`, then make-site + qa-site. App Store frames: `scripts/appstore-screenshots.py`. Icons:
  `scripts/icon-concepts.swift` (A T-bone reads as a letter T, so it's out; B bison burger and C root beer float pass
  `state-prompts/icon-style/check.swift`) and `scripts/make-brand.swift` (C).
- Not ported: the App Store listing writer and the private Google-2021 leaderboard. `site/` holds the leaderboard's data and is
  git-ignored with `data/`.

## Fixes during the build (2026-11-05)
- The map opened over West Virginia (the port's initial region): now Wyoming's (43.0, -107.55). The App Store map shot zooms to
  Jackson's Town Square (span 0.008°) so the picks show as pins. The UI test's "my location" check used Baltimore's Inner Harbor (from
  md-eats): now Jackson.
- The export kept only Maryland's ZIPs (carried from md-eats): now Wyoming's 820xx-831xx and 83414. A doubled street ("5755 W, 5755 W
  Wy-22") is cleaned, and the state-route prefix prints as "WY-22".
- **Last full run** 2026-11-05: app 1,476 places / 1,422 restaurants, 49 unit tests on iPhone 17 Pro Max (iOS 27.0), 14 iPhone + 6
  iPad screens, `qa-site.py --static` OK, OTA 2026-11-05.1 (local only).

## Rules
No commits, pushes, public repos, App Store Connect or DNS changes without Nick's yes each time; never submit for review or accept
agreements; never publish Google-derived data. Support email nick@eatsranked.com. Commit author "Nick Soderstrom"
<329204362+nickstrom5@users.noreply.github.com> via `-c user.name -c user.email`.
