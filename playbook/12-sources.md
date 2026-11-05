# Wyoming sources and calibration (checked 2026-11-05)

## Official sources
| Source | What it has | Can a script read it? | Used |
|---|---|---|---|
| Department of Agriculture, Consumer Health Services (agriculture.wy.gov/chs-inspection-reports) | restaurant inspections wherever no local health department inspects | no: a search form; its USA Food Safety back end (wda.safefoodinspection.com) is a login page | the reports page is linked from every place |
| Teton County Health Department | its own food program | no list found | not used |
| Liquor Division (liquor365.wyo.gov/license) | license types and fees | no licensee list: retail licenses are issued by each city and county | no |

## Calibration
- Overture: 3,040 eating and drinking listings in Wyoming; 3,038 after cleaning (24 far-from-town points dropped, 16 kept by the
  own-county rule); the web build keeps 1,997 places; the App Store build ships **1,476 places, 1,422 restaurants** (23 counties).
- Google 2021 (private, web build only): 1,925 WY food listings, 1,411 matched.
- Website links: 712 OK of 1,223 after the check and the transient retry; 16 lapsed or hijacked domains (gambling, adult, a lottery
  link) dropped.

## Research sources (each place cites its own)
- Travel Wyoming (travelwyoming.com, the Wyoming Office of Tourism; robots allows all but its CRM counter, Crawl-delay 2), read
  2026-11-05, articles dated by their own datePublished: historic bars (2026-06-15), 10 must-have food experiences (2025-12-10),
  11 ways to taste Wyoming and kid-friendly restaurants (2025-11-02), sweet treats (2025-08-05), historic accommodations (2025-06-27),
  farm to table (2025-04-04), Thermopolis road trip (2025-02-28); its listings (travelwyoming.com/listing/<slug>/<id>/, 2,098 in the
  sitemap), read by scripts/read_wyt.py. Too old to cite: grain to glass (2018), the northeast foodie guide and the road trip (2019).
- jamesbeard.org: 2026 semifinalists and nominees (no Wyoming finalist), 2025 semifinalists, nominees (Atelier Ortega, Outstanding
  Bakery) and winners (JinJu Patisserie won it), and the 2012 America's Classic (Nora's Fish Creek Inn, on the Foundation's archive).
- Not used: a "Bunkhouse Saloon & Steakhouse" heading whose text describes another restaurant; listing pins that disagree with the
  place (the Lake Yellowstone Hotel Dining Room's sits in Cody).
