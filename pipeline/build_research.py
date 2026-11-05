"""Writes data/research/app/*.json (hand-checked Wyoming guides), data/research/michelin.json, jbf.json and closed.json from the
compact lists below. Ported from wv-eats/pipeline/build_research.py.

Each entry cites the page that names it, read on 2026-11-05: Travel Wyoming's dated articles (the Wyoming Office of Tourism,
travelwyoming.com; robots allows them, Crawl-delay 2) and its own listing for the business (travelwyoming.com/listing/<slug>/<id>/,
read by scripts/read_wyt.py). The address comes from the map listing we already hold for that name in that town (site/wyoming.json);
a name that isn't found exactly once in its town (or at the street number given) is left out and listed in data/research/app/LEADS.md.
A place the map data doesn't show as a place to eat is added only with the street address from its tourism listing (ADDR).
Usage: ../.venv/bin/python build_research.py   (then wyoming.py)"""
import json, os, re
from brands import brand_of
from common import norm_name
ROOT = os.path.join(os.path.dirname(__file__), "..")
R = os.path.join(ROOT, "data", "research")
d = json.load(open(os.path.join(ROOT, "site", "wyoming.json")))
C, M = d["cols"], d["meta"]
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower().replace("'", "").replace("’", ""))).strip()

# each dated on its face (datePublished), or an official tourism listing (read 2026-11-05)
W = lambda slug: f"https://travelwyoming.com/listing/{slug}/"                                          # Travel Wyoming listing
TW = "https://travelwyoming.com/blog/stories/post/"
BARS = TW + "saddle-up-and-experience-the-rich-history-of-wyomings-most-unique-bars/"                 # 2026-06-15
MUST = TW + "10-must-have-wyoming-food-experiences/"                                                  # 2025-12-10
TASTE = TW + "11-ways-to-taste-wyomings-unique-flavors/"                                              # 2025-11-02
KIDS = TW + "cool-kid-friendly-restaurants/"                                                           # 2025-11-02
SWEET = TW + "your-guide-to-wyomings-best-sweet-treats/"                                               # 2025-08-05
HOTELS = TW + "10-of-the-most-historic-accommodations-in-wyoming/"                                     # 2025-06-27
FARM = TW + "wyoming-farm-to-table-6-restaurants-serving-locally-sourced-food/"                        # 2025-04-04
THERMOP = TW + "road-trips-rapids-and-restaurants-uncovering-a-hidden-gem-of-a-small-town/"            # 2025-02-28
JBF26 = "https://www.jamesbeard.org/stories/james-beard-award-semifinalists-2026"                   # 2026-01-21
JBF25 = "https://www.jamesbeard.org/stories/the-2025-james-beard-award-semifinalists"               # 2025-01-22
JBF25N = "https://www.jamesbeard.org/stories/2025-james-beard-awards-restaurant-and-chef-nominees"   # 2025-04-02
JBF12C = "https://archive.jamesbeard.org/index.php/blog/americas-classics-noras-fish-creek-inn-wilson-wy"  # 2012 America's Classics
BARS_N = "Travel Wyoming's historic-bars guide (June 2026)"

# (name as the source writes it or as our listing spells it, town as our listing has it, street number to pick the location (or
# None), note, founded, founded_note, [sources])
GUIDES = {
 "historic saloon": [   # Travel Wyoming's nine historic bars (June 2026), each with the year the guide gives
  ("Miners and Stockmen's", "Hartville", "608", "Called Wyoming's oldest bar: a carved back bar, steaks and whiskey in a tiny railroad-era town.",
   1862, f"{BARS_N}: est. 1862, Wyoming's oldest bar.", [BARS, W("miners-%26-stockmens-steakhouse/753")]),
  ("Occidental Saloon", "Buffalo", "18", "The Historic Occidental Hotel's saloon: a long wooden bar, a tin ceiling and the original bullet holes.",
   None, None, [BARS, HOTELS, W("historic-occidental-hotel-%26-saloon/527")]),
  ("Hotel Wolf", "Saratoga", None, "An 1893 Victorian hotel with swinging saloon doors and a dining room known for its burgers.",
   1893, f"{BARS_N}: opened by Max and Rose Wolf in 1893.", [BARS, HOTELS, KIDS, W("hotel-wolf-and-restaurant/558")]),
  ("Buckhorn Bar & Parlor", "Laramie", "114", "Laramie's oldest bar, with the Parlor upstairs open Friday and Saturday nights.",
   1900, f"{BARS_N}: established in 1900, the oldest bar in Laramie.", [BARS]),
  ("Irma Restaurant Grill", "Cody", "1192", "Buffalo Bill's 1902 hotel: the cherrywood back bar was a gift from Queen Victoria, and the summer buffet serves slow-roasted prime rib.",
   1902, f"{BARS_N}: built by Buffalo Bill Cody in 1902.", [BARS, TASTE, HOTELS, W("the-irma-restaurant-%26-grill/1281")]),
  ("Mint Bar", "Sheridan", "151", "A downtown meeting place for ranchers since 1907, its walls covered in photographs.",
   1907, f"{BARS_N}: open since 1907.", [BARS, W("the-mint-bar/1284")]),
  ("The Virginian Hotel", "Medicine Bow", None, "A National Historic Landmark on the Lincoln Highway; the Shiloh Saloon has bullet holes from real shootouts.",
   1911, f"{BARS_N}: the Shiloh Saloon, est. 1911.", [BARS, HOTELS, W("the-historic-virginian-hotel/3208")]),
  ("Million Dollar Cowboy Bar", "Jackson", "25", "Saddle barstools and live music on Jackson's Town Square.",
   1937, f"{BARS_N}: est. 1937.", [BARS, W("million-dollar-cowboy-bar/1751")]),
  ("Stagecoach Bar", "Wilson", "5755", "A local bar at the foot of Teton Pass with long-running live-music nights.",
   1942, f"{BARS_N}: open since 1942.", [BARS])],
 "steakhouse": [
  ("Gun Barrel Steak and Game House", "Jackson", "862", "Elk loin, bison carpaccio and steaks cooked over an open flame, in the old Wyoming Wildlife Museum with its mounts still on the walls.",
   None, None, [MUST, W("gun-barrel-steak-%26-game-house/487")]),
  ("Buffalo Jump Steakhouse", "Beulah", None, "Dry-aged steaks in an 1890s general store with a stone fireplace and creaking floors.",
   None, None, [MUST, W("buffalo-jump-steakhouse/211")]),
  ("Cavalryman Steakhouse", "Laramie", None, "Prime rib, bison London broil and Wyoming soda bread on the grounds of Fort Sanders, an 1866 post.",
   None, None, [MUST, W("cavalryman-steakhouse/1644")]),
  ("Little Bear Inn", "Cheyenne", "1700", "A steakhouse with a stone fireplace, a wagon wheel and mounted bears, moose and elk.",
   None, None, [KIDS, W("little-bear-inn/684")]),
  ("Pitchfork Fondue Western Cookout", "Pinedale", "9888", "Meat and vegetables cooked outdoors over a wood fire, with views of the Wind River Range, Thursdays to Saturdays in summer.",
   None, None, [TASTE, W("pitchfork-fondue-western-outdoor-cookout/2057")])],
 "small town cafe": [
  ("Cottage Cafe", "Casper", "116", "Homemade breads, quiche and tequila lime chicken soup in a 1906 Victorian house, locally owned since 1993.",
   None, None, [MUST]),
  ("Cowboy Cafe", "Dubois", "115", "Breakfast skillets with spicy elk or smoked bison sausage.", None, None, [TASTE, KIDS, W("cowboy-cafe/2262")]),
  ("Cowboy Cafe", "Sheridan", "138", "The Sheridan branch of Dubois's breakfast cafe: skillets, benedicts and breakfast burritos.", None, None, [KIDS]),
  ("Ponderosa Cafe", "Hulett", "115", "An Old West-style saloon and cafe near Devils Tower: chicken-fried steak, bone-in ribeyes and Wyoming beef burgers.",
   None, None, [TASTE, W("ponderosa-cafe-%26-bar/905")]),
  ("Broadway Burger Station", "Rock Springs", "628", "A locally owned 1950s-style diner with burgers and 31 milkshake flavors.", None, None, [KIDS]),
  ("The Breadboard", "Buffalo", "190", "A family-owned sandwich shop: bread baked daily, homemade bagels and soups.", None, None, [KIDS, W("breadboard/173")]),
  ("The Breadboard Cody", "Cody", "1725", "A family-owned sandwich shop: bread baked daily, homemade bagels and soups.", None, None, [KIDS, W("the-breadboard-cody/174")]),
  ("The Breadboard", "Riverton", "124", "A family-owned sandwich shop: bread baked daily, homemade bagels and soups.", None, None, [KIDS, W("breadboard-in-riverton/176")]),
  ("For Pete's Sake", "Evanston", "900", "Coffee, breakfast and lunch on Black Hills bagels; a Best of Evanston people's choice.", None, None, [KIDS]),
  ("Broadway Bakery", "Thermopolis", "509", "A small-batch artisan bakery with breakfast sandwiches and sweets.", None, None, [THERMOP])],
 "soda fountain": [
  ("Chugwater Soda Fountain", "Chugwater", None, "Wyoming's oldest operating soda fountain: scratch-made sodas, malts and a bowl of Chugwater Chili.",
   1914, "Travel Wyoming's sweet-treats guide (2025): established in 1914, the state's oldest operating soda fountain.", [SWEET, TASTE, W("chugwater-soda-fountain/285")]),
  ("Annie's Soda Saloon", "Cody", "1202", "Cane-sugar sodas, sundaes and sweet cream pancakes in the old Seidel's Saddlery building.", None, None, [SWEET, KIDS]),
  ("Moo's Gourmet Ice Cream", "Jackson", "155", "Wild huckleberry ice cream off Town Square, from 26 flavors made with local ingredients.", None, None, [SWEET]),
  ("Ice Cream Cafe", "Gillette", "202", "The McClure family's 24 homemade flavors, a summer tradition since 2013.", None, None, [SWEET, W("ice-cream-cafe/1602")]),
  ("Cowboy Creamery", "Sheridan", "1617", "Small-batch Western-style ice cream made with whole fruit and fresh cream.", None, None, [SWEET]),
  ("Big Dipper Ice Cream Shop", "Laramie", "111", "Airy ice cream from 14% butterfat milk, plus gelato, sorbetto and vegan scoops.", None, None, [SWEET, W("big-dipper-ice-cream-shop/125")])],
 "farm to table": [
  ("The Middle Fork", "Lander", "351", "Breakfast, brunch and lunch on Main Street from Lander's own farms and suppliers.", None, None, [FARM, W("the-middle-fork/746")]),
  ("Gather", "Jackson", "72", "Modern Western plates with its own microgreens; the pork buns and mushroom toast are favorites.",
   None, None, [FARM, W("gather-in-jackson-hole-for-food-%26-drink/442")]),
  ("Turpin Meadow Ranch", "Moran", None, "Local game (venison, elk, bison, duck) in an 1887 ranch's historic dining room facing the Tetons.",
   None, None, [FARM, W("turpin-meadow-ranch/1329")]),
  ("Sweet Melissa", "Laramie", "213", "Wyoming's only all-vegetarian restaurant for two decades: seitan banh mi, kimchi pancakes and smothered burritos.",
   None, None, [FARM, TASTE, KIDS, W("sweet-melissa/1227")]),
  ("Roasted Bean & Cuisine", "Riverton", "514", "A coffee shop turned restaurant: gourmet burgers, soups and tacos.", None, None, [FARM, W("roasted-bean-%26-cuisine/2247")]),
  ("Local Restaurant & Bar", "Jackson", "55", "Ranch beef and in-season produce on Town Square, from bison short-rib pasta to steak tartare.", None, None, [FARM, TASTE]),
  ("Le Rêve Restaurant & Raw Bar", "Sheridan", "1", "French technique with local meats and produce, and a raw bar, in downtown Sheridan.", None, None, [MUST, JBF25])],
 "pizza": [
  ("Pizza Carrello", "Gillette", "601", "Wood-fired pies from small-batch dough, from the strawberry steak pizza to a Nutella calzone.",
   None, None, [MUST, TASTE, KIDS, W("pizza-carrello/1612")]),
  ("Racca's Pizzeria Napoletana", "Casper", "430", "Neapolitan pies, with brunch pizzas like the Firenze (pancetta, arugula and cracked eggs).",
   None, None, [TASTE, W("raccas-pizzeria-napoletana/2378")]),
  ("Hand Fire Pizza", "Jackson", "120", "Pizza in a historic movie theater, with Wyoming toppings like bison chili.", None, None, [KIDS]),
  ("P6 Station", "Thermopolis", "544", "Pizza by the slice and cheesecake (Travel Wyoming calls it P6 Pizza).", None, None, [THERMOP])],
 "historic hotel": [
  ("The Virginian Restaurant", "Buffalo", "10", "The Occidental Hotel's dining room; the 1880 hotel hosted Teddy Roosevelt, Buffalo Bill and Calamity Jane.",
   None, None, [HOTELS, W("historic-occidental-hotel-%26-saloon/527")]),
  ("Irma Restaurant Grill", "Cody", "1192", "Buffalo Bill's 1902 hotel: the cherrywood back bar was a gift from Queen Victoria, and the summer buffet serves slow-roasted prime rib.",
   1902, f"{BARS_N}: built by Buffalo Bill Cody in 1902.", [HOTELS, TASTE, W("buffalo-bills-irma-hotel/208")]),
  ("Hotel Wolf", "Saratoga", None, "An 1893 Victorian hotel with swinging saloon doors and a dining room known for its burgers.",
   1893, f"{BARS_N}: opened by Max and Rose Wolf in 1893.", [HOTELS, KIDS, W("hotel-wolf-and-restaurant/558")]),
  ("Silver Dollar Bar", "Jackson", "50", "The Wort Hotel's bar and grill (the hotel opened in 1941): 2,032 uncirculated silver dollars are set into the bar.",
   None, None, [HOTELS, W("silver-dollar-bar-%26-grill/1747")]),
  ("Lake Yellowstone Hotel Dining Room", "Yellowstone National Park", "235", "Fine dining in the yellow lakeside hotel from the late 1800s, restored in 2014 (open in the park's summer season).",
   None, None, [HOTELS, W("lake-yellowstone-hotel-dining-room/2580")]),
  ("Mountain View Historic Hotel & Cafe", "Centennial", None, "A 1907 railroad hotel below the Snowy Range, with six rooms and a cafe.",
   None, None, [HOTELS, W("mountain-view-historic-hotel-%26-cafe/1784")]),
  ("The Virginian Hotel", "Medicine Bow", None, "A National Historic Landmark on the Lincoln Highway; the Shiloh Saloon has bullet holes from real shootouts.",
   1911, f"{BARS_N}: the Shiloh Saloon, est. 1911.", [HOTELS, BARS, W("the-historic-virginian-hotel/3208")])],
}
# places the map data doesn't show as a place to eat: the street address from the business's Travel Wyoming listing
ADDR = {("Hotel Wolf", "Saratoga"): "101 E Bridge Ave", ("The Virginian Hotel", "Medicine Bow"): "404 Lincoln Hwy",
        ("Turpin Meadow Ranch", "Moran"): "24505 Buffalo Valley Rd", ("Lake Yellowstone Hotel Dining Room", "Yellowstone National Park"): "235 Yellowstone Lake Rd",
        ("Mountain View Historic Hotel & Cafe", "Centennial"): "2747 Highway 130"}
CUISINE = {("Hotel Wolf", "Saratoga"): "American & Other", ("The Virginian Hotel", "Medicine Bow"): "Bar & Pub",
           ("Turpin Meadow Ranch", "Moran"): "American & Other", ("Lake Yellowstone Hotel Dining Room", "Yellowstone National Park"): "American & Other",
           ("Mountain View Historic Hotel & Cafe", "Centennial"): "Coffee & Café", ("Pitchfork Fondue Western Cookout", "Pinedale"): "Steakhouse",
           ("Cowboy Creamery", "Sheridan"): "Bakery & Sweets", ("Moo's Gourmet Ice Cream", "Jackson"): "Bakery & Sweets",
           ("Ice Cream Cafe", "Gillette"): "Bakery & Sweets", ("Big Dipper Ice Cream Shop", "Laramie"): "Bakery & Sweets",
           ("Chugwater Soda Fountain", "Chugwater"): "Bakery & Sweets", ("Annie's Soda Saloon", "Cody"): "Bakery & Sweets"}
# an added place whose address no geocoder places: Overture's own listing of the dining room (filed under "Mammoth"), at the hotel;
# Travel Wyoming's listing puts its pin in Cody, at the park concessioner's office
POINT = {("Lake Yellowstone Hotel Dining Room", "Yellowstone National Park"): (44.54998, -110.40105)}
# a listing name with a slogan in it shows under the business's own name
DISPLAY = {("Cowboy Creamery", "Sheridan"): "Cowboy Creamery"}
KINDS = {k: [k] for k in ("historic saloon", "steakhouse", "small town cafe", "soda fountain", "farm to table", "pizza", "historic hotel")}

# no MICHELIN Guide covers Wyoming (the Mountain West states have none; Colorado's guide is Colorado's alone)
MICHELIN = []
MI_MATCH = {}
MI_UT = None
# James Beard (facts with sources): Wyoming's America's Classic (Nora's, 2012), its 2025 finalist (Atelier Ortega, Outstanding Bakery;
# JinJu Patisserie won) and its 2025-26 semifinalists (no Wyoming finalist in 2026); jamesbeard.org pages read 2026-11-05
MT = "Best Chef: Mountain"
JBF = [{"name": "Nora's Fish Creek Inn", "city": "Wilson", "honors": ["America's Classics 2012"], "sources": [JBF12C]},
       {"name": "Glorietta Trattoria", "city": "Jackson", "honors": [f"{MT} semifinalist 2026 (Remle Colestock)"], "sources": [JBF26]},
       {"name": "Atelier Ortega", "city": "Jackson", "honors": ["Outstanding Pastry Chef or Baker semifinalist 2026 (Oscar Ortega)",
                                                              "Outstanding Bakery finalist 2025"], "sources": [JBF26, JBF25N, JBF25]},
       {"name": "Sitti's Table", "city": "Cody", "honors": [f"{MT} semifinalist 2025 (Porter Koury and Jacob Scott)"], "sources": [JBF25]},
       {"name": "Le Rêve Restaurant & Raw Bar", "city": "Sheridan", "honors": ["Best New Restaurant semifinalist 2025"], "sources": [JBF25]}]
# closed, each with a source (none verified this pass)
CLOSED = []


def key(s):
    """The name key without a leading "the": "Varsity" is our "The Varsity"."""
    return re.sub(r"^the ", "", norm(s))


def find(name, town, num):
    k = key(name)
    hits = [i for i, n in enumerate(C["name"]) if C["city"][i] is not None and M["cities"][C["city"][i]] == town
            and (key(n) == k or key(n).startswith(k + " ") or k.startswith(key(n) + " ") or key(n).replace(" ", "") == k.replace(" ", "")
                 or (key(n).split()[:2] == k.split()[:2] and len(k.split()) >= 2))]
    if num:
        hits = [i for i in hits if (C["addr"][i] or "").split(" ")[0] == num]
    return hits


leads, n_out = [], {}
for kind, rows in GUIDES.items():
    out = []
    for name, town, num, note, founded, fnote, srcs in rows:
        hits = find(name, town, num)
        if not hits and (name, town) in ADDR:
            out.append({"name": name, "address": ADDR[(name, town)], "city": town, "zip": None, "kinds": KINDS[kind], "dishes": [], "note": note,
                        "founded": founded, "founded_note": fnote, "website": None, "open": True, "evidence_date": "2026-10",
                        "sources": srcs, "match_names": []} | ({"cuisine": CUISINE[(name, town)]} if (name, town) in CUISINE else {})
                       | ({"lat": POINT[(name, town)][0], "lon": POINT[(name, town)][1]} if (name, town) in POINT else {}))
            continue
        if len(hits) != 1:
            leads.append(f"- {kind}: {name} ({town}{', ' + num if num else ''}) — {len(hits)} matches in our data; not added"); continue
        i = hits[0]
        out.append({"name": C["name"][i], "address": C["addr"][i], "city": town, "zip": str(C["zip"][i]) if C["zip"][i] else None,
                    "kinds": KINDS[kind], "dishes": [], "note": note, "founded": founded, "founded_note": fnote, "website": None, "open": True,
                    "evidence_date": "2026-10", "sources": srcs, "match_names": [name.upper()] if norm(name) != norm(C["name"][i]) else []})
        if brand_of(norm_name(name)):   # a chain shows under its own spelling at every branch, whatever the listing says
            out[-1]["display"] = name
        if (name, town) in DISPLAY:
            out[-1]["display"] = DISPLAY[(name, town)]
        if (name, town) in CUISINE:
            out[-1]["cuisine"] = CUISINE[(name, town)]
    fn = re.sub(r"[^a-z]+", "_", kind).strip("_")
    json.dump(out, open(f"{R}/app/{fn}.json", "w"), indent=1, ensure_ascii=False)
    n_out[kind] = len(out)

MI_ADDR = {}
json.dump({"restaurants": [{"name": n, "address": MI_ADDR.get(n), "city": t, "zip": None, "distinction": dist, "cuisine": cu, "green_star": False,
                             "michelin_url": MI_UT, "sources": [MI_UT], "match_names": [x.upper() for x in MI_MATCH.get(n, [])], "open": True}
                            for n, t, dist, cu in MICHELIN]}, open(f"{R}/michelin.json", "w"), indent=1, ensure_ascii=False)
json.dump([dict({"address": None}, **j, zip=None, open=True) for j in JBF], open(f"{R}/jbf.json", "w"), indent=1, ensure_ascii=False)
json.dump(CLOSED, open(f"{R}/closed.json", "w"), indent=1, ensure_ascii=False)
open(f"{R}/app/LEADS.md", "w").write("# Wyoming research leads (not yet verified)\n\nWritten by pipeline/build_research.py.\n\n" + "\n".join(leads) + """

## Waiting for a source we may use, or for the map data
- Steakhouses: Bunkhouse Saloon & Steakhouse (Cheyenne) is a heading in Travel Wyoming's "11 ways" article whose text describes a
  different restaurant (The Metropolitan Downtown), so neither is used; Legacy Butcher and Burger Co. (Cody) isn't in our map data.
- Cafes: G-ma's Diner (Casper) isn't in our map data; The Breadboard's Lander store (1374 Main St) isn't either. Busy Bee Cafe,
  Silver Spur Cafe and the other northeast picks come from a 2019 article, too old to cite.
- Sweets: Shumway Farms (Afton) is a farm store; the candy shops (Meeteetse Chocolatier, Cowtown Candy, Donells, Yippy I-O, Queen Bee
  Gardens) are shops, not places to eat, so they stay hidden with the non-restaurants.
- Farm to table: the Cheyenne Club is Brush Creek Ranch's dining room (a guest ranch); the Dining Room at Jenny Lake Lodge has no
  street address to place it (Jenny Lake Road, Moose); Durham Ranch is a ranch, not a restaurant.
- Historic hotels: the Sheridan Inn (856 Broadway St) and the Historic Elk Mountain Hotel are named for their rooms, not a dining
  room; the Old Faithful Inn appears only in passing.
- Older lists: Travel Wyoming's grain-to-glass (2018), northeast foodie (2019) and road-trip (2019) articles are too old to cite.
""")
print(n_out, "| leads:", len(leads))
for l in leads: print(l)
