"""Download the Overture Maps extracts that wyoming.py reads -> data/wy/

- overture_wy_bbox.parquet     every place in Wyoming's bounding box (name, category, address, point)
- overture_wy_sources.parquet  which datasets each Wyoming eating/drinking listing came from (Meta, Foursquare, ...)
- wy_shapes.json               simplified state and county outlines for the map
- wy_state_detail.geojson      the state outline at full detail, for the in-state test

Reads the public Overture bucket over S3 with DuckDB (no account needed). Ported from wv-eats/pipeline/fetch_overture.py.
Wyoming: land division areas; the "counties" are its 23. The script checks the towns on and near its lines (Yellowstone's gateways,
Star Valley, Evanston, Pine Bluffs) so a Montana, Idaho, Utah, Colorado, Nebraska or South Dakota listing stays out.
"""
import os, json, time
import duckdb
from shapely import wkb
from shapely.geometry import mapping, Polygon

RELEASE = "2026-10-21.0"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "wy")
# Wyoming (42.73°N–45.02°N, 71.46°W–73.44°W) plus a margin for the border towns (Derby Line, the Upper Valley, Bennington's New York
# Wyoming (41.0°N–45.0°N, 104.05°W–111.06°W) plus a margin for the border towns
BBOX = "bbox.xmin BETWEEN -111.2 AND -103.9 AND bbox.ymin BETWEEN 40.9 AND 45.1"
EAT = "('restaurant','casual_eatery','bar','fast_food_restaurant','coffee_shop','cafe','smoothie_juice_bar','brewery','food_court')"
os.makedirs(OUT, exist_ok=True)

con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs; INSTALL spatial; LOAD spatial; SET s3_region='us-west-2';")
places = f"s3://overturemaps-us-west-2/release/{RELEASE}/theme=places/type=place/*.parquet"

t = time.time()
if not os.path.exists(f"{OUT}/overture_wy_bbox.parquet"):
    con.execute(f"""
COPY (
  SELECT id, names.primary AS name, basic_category AS cat, taxonomy.primary AS tax, taxonomy.hierarchy AS hier, confidence,
         operating_status AS status, brand.names.primary AS brand, addresses[1].freeform AS street, addresses[1].locality AS city,
         addresses[1].postcode AS zip, addresses[1].region AS region, ST_Y(geometry) AS lat, ST_X(geometry) AS lon, websites[1] AS web,
         phones[1] AS phone
  FROM read_parquet('{places}', hive_partitioning=1) WHERE {BBOX}
) TO '{OUT}/overture_wy_bbox.parquet' (FORMAT PARQUET)""")
    print("places in bbox", round(time.time() - t), "s", flush=True)
if not os.path.exists(f"{OUT}/overture_wy_sources.parquet"):
    con.execute(f"""
COPY (
  SELECT id, list_transform(sources, lambda x: x.dataset) AS ds, list_transform(sources, lambda x: x.update_time) AS ut,
         list_transform(sources, lambda x: x.record_id) AS rid,
         len(socials) AS n_soc, len(websites) AS n_web, len(phones) AS n_ph
  FROM read_parquet('{places}', hive_partitioning=1)
  WHERE {BBOX} AND basic_category IN {EAT}
) TO '{OUT}/overture_wy_sources.parquet' (FORMAT PARQUET)""")
    print("sources", round(time.time() - t), "s", flush=True)

areas = f"s3://overturemaps-us-west-2/release/{RELEASE}/theme=divisions/type=division_area/*.parquet"
rows = con.execute(f"""
  SELECT subtype, names.primary AS name, ST_AsWKB(geometry) AS g
  FROM read_parquet('{areas}', hive_partitioning=1)
  WHERE country = 'US' AND region = 'US-WY' AND subtype IN ('region', 'county') AND class = 'land'
    AND bbox.xmin > -111.3 AND bbox.xmax < -103.8 AND bbox.ymin > 40.8 AND bbox.ymax < 45.2""").fetchall()


def rings(geom, tol, min_area):
    geom = geom.simplify(tol, preserve_topology=True)
    polys = [p for p in getattr(geom, "geoms", [geom]) if p.geom_type == "Polygon" and p.area >= min_area]
    return [[[round(x, 3), round(y, 3)] for x, y in p.exterior.coords] for p in polys]


out = {"state": None, "counties": []}
for sub, name, g in rows:
    geom = wkb.loads(bytes(g)).buffer(0)
    if sub == "region":
        json.dump(mapping(geom.simplify(0.0005, preserve_topology=True)), open(f"{OUT}/wy_state_detail.geojson", "w"))
        out["state"] = [[r] for r in rings(geom, 0.002, 0.000005)]
    else:
        out["counties"].append({"name": name, "c": rings(geom, 0.004, 0.00002)})
# full-detail county polygons for assigning each place to a county (not shipped)
json.dump({name: mapping(wkb.loads(bytes(g)).buffer(0).simplify(0.0003, preserve_topology=True))
           for sub, name, g in rows if sub == "county"}, open(f"{OUT}/wy_counties_detail.geojson", "w"))
json.dump(out, open(f"{OUT}/wy_shapes.json", "w"), separators=(",", ":"))
print("outlines: state", len(out["state"] or []), "rings +", len(out["counties"]), "counties;", round(time.time() - t), "s total")
# border towns: each must fall on the right side of the detailed state outline
from shapely.geometry import shape, Point
st = shape(json.load(open(f"{OUT}/wy_state_detail.geojson")))
for nm, lon, lat, want in [("Cheyenne", -104.8202, 41.1400, True), ("Evanston", -110.9632, 41.2683, True), ("Afton", -110.9318, 42.7249, True),
                           ("Jackson", -110.7624, 43.4799, True), ("Pine Bluffs", -104.0691, 41.1822, True), ("Sheridan", -106.9562, 44.7972, True),
                           ("Old Faithful (Yellowstone)", -110.8281, 44.4605, True), ("West Yellowstone, MT", -111.1047, 44.6621, False),
                           ("Gardiner, MT", -110.7058, 45.0322, False), ("Kimball, NE", -103.6630, 41.2361, False), ("Fort Collins, CO", -105.0844, 40.5853, False),
                           ("Driggs, ID", -111.1116, 43.7232, False), ("Randolph, UT", -111.1835, 41.6655, False), ("Belle Fourche, SD", -103.8441, 44.6714, False)]:
    ok = st.contains(Point(lon, lat))
    print(f"  {nm}: {'inside' if ok else 'outside'}{'' if ok == want else '  <-- WRONG'}")
print("counties:", len(out["counties"]), sorted(c["name"] for c in out["counties"]))

# the neighbours' land (Montana, South Dakota, Nebraska, Colorado, Utah, Idaho): listings.py widens Wyoming's outline ~300 m, but only
# where no neighbour's land is, so a West Yellowstone or Kimball listing on the far side of the line stays out
nb = con.execute(f"""
  SELECT region, ST_AsWKB(geometry) FROM read_parquet('{areas}', hive_partitioning=1)
  WHERE country = 'US' AND region IN ('US-MT', 'US-SD', 'US-NE', 'US-CO', 'US-UT', 'US-ID') AND subtype = 'region' AND class = 'land'""").fetchall()
from shapely.ops import unary_union
from shapely.geometry import box
near = box(-111.3, 40.8, -103.8, 45.2)
nbg = unary_union([wkb.loads(bytes(g)).buffer(0).intersection(near) for _, g in nb])
json.dump(mapping(nbg.simplify(0.0002, preserve_topology=True)), open(f"{OUT}/wy_neighbors.geojson", "w"))
print("neighbours:", sorted(r for r, _ in nb))
