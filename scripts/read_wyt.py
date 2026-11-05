"""Read Travel Wyoming listings (travelwyoming.com/listing/<slug>/<id>/; robots allows them, Crawl-delay 2) -> data/research/raw/wyt.json:
the listing's name, street address, town, zip, point, website and last update, one polite request every 2.5 s. Private research notes.
Usage: .venv/bin/python scripts/read_wyt.py <slug>/<id> ..."""
import html, json, os, re, sys, time
import requests
UA = "CowboyStateEatsSourceCheck/1.0 (+https://nickstrom5.github.io/wyoming-eats/; nick@eatsranked.com)"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "research", "raw", "wyt.json")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
have = json.load(open(OUT)) if os.path.exists(OUT) else {}
F = lambda k, t: (m.group(1) if (m := re.search(r'"' + k + r'"\s*:\s*"?([^",}]*)', t)) else None)
for slug in sys.argv[1:]:
    url = slug if slug.startswith("http") else f"https://travelwyoming.com/listing/{slug.strip('/')}/"
    if url in have:
        continue
    r = requests.get(url, headers={"User-Agent": UA}, timeout=40)
    t = r.text
    rec = {"status": r.status_code, "name": html.unescape(F("title", t) or ""), "addr": html.unescape(F("address1", t) or ""),
           "city": F("city", t), "zip": F("zip", t), "lat": F("latitude", t), "lon": F("longitude", t), "web": F("weburl", t),
           "updated": F("updated", t)}
    have[url] = rec
    print(r.status_code, rec["name"], "|", rec["addr"], "|", rec["city"], rec["zip"], "|", rec["updated"], flush=True)
    json.dump(have, open(OUT, "w"), indent=1, ensure_ascii=False)
    time.sleep(2.5)
