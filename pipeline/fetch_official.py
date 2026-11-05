"""Wyoming's open official records -> data/raw/official/ (git-ignored, never public). Nothing to fetch yet.

Checked 2026-11-05 (playbook/12-sources.md): the Department of Agriculture's restaurant inspection reports are reached only through a
search form (agriculture.wy.gov/chs-inspection-reports; its USA Food Safety back end needs a login), and Teton County keeps its own;
retail liquor licenses are issued by each city and county, and the Liquor Division (liquor365.wyo.gov) publishes no licensee list.
When a list we may use turns up (a county export Nick approves), add its loader to official.py and its download here.
"""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "official")
os.makedirs(OUT, exist_ok=True)
json.dump({}, open(os.path.join(OUT, "meta.json"), "w"))
print("Wyoming: no official list to fetch (see the docstring)")
