#!/usr/bin/env python3
"""[초안] T-HOME-PHOTO 후보 수집 — Wikimedia Commons API(작가·라이선스·크기 원본 메타데이터).
기준: 가로 ≥2400px · 가로형(비율 ≥1.3) · 상업 이용 가능 라이선스(CC0·PD·CC BY·CC BY-SA)만 · 비트맵.
우선 Featured/Quality 모음에서 찾고, 부족하면 일반 검색. 산출: candidates.json + thumb/<id>.jpg(480px)
"""
import json, re, sys, time, html, urllib.parse, urllib.request
from pathlib import Path
D = Path(__file__).resolve().parent
UA = "KeunsaemPreviewResearch/0.1 (church website draft; github.com/seudw79-sketch)"
API = "https://commons.wikimedia.org/w/api.php"
THEMES = {
  "wilderness": ("광야와 길", ["desert road", "desert track hills", "wilderness landscape", "Judaean Desert", "Negev landscape", "dirt road hills"]),
  "dawnfield": ("새벽·해질녘 빛 드는 들판", ["sunrise meadow", "morning mist field", "golden hour field", "dawn field light", "sunset meadow"]),
  "harvest": ("밀밭·포도원·올리브나무", ["wheat field", "vineyard", "olive grove", "olive tree", "barley field"]),
  "water": ("물가·바다·배", ["fishing boat lake calm", "Sea of Galilee", "rowing boat lake", "calm sea shore", "lake morning mist"]),
  "bible": ("펼친 성경과 빛", ["open Bible", "Bible book open", "old book open light", "Bible on table"]),
  "stone": ("돌벽·돌길·고대 유적", ["ancient stone wall", "stone path", "ancient ruins columns", "dry stone wall", "old stone steps"]),
  "sheep": ("양떼·목자", ["flock of sheep", "sheep grazing hills", "shepherd flock", "sheep pasture"]),
}
FILTERS = ["incategory:Featured_pictures_on_Wikimedia_Commons", "incategory:Quality_images", ""]
OK_LIC = re.compile(r"^(CC0|Public domain|PD|CC BY(-SA)? [0-9.]+|CC BY(-SA)?)", re.I)

def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40) as r:
                return json.load(r)
        except Exception as e:
            time.sleep(2 + 3 * i)
    return {}

def clean(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h or ""))).strip()

out = {}
for key, (label, queries) in THEMES.items():
    seen = {}
    for flt in FILTERS:
        for q in queries:
            d = get({"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6, "gsrlimit": 40,
                     "gsrsearch": f"{q} filetype:bitmap {flt}".strip(), "prop": "imageinfo",
                     "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 480})
            for p in (d.get("query", {}).get("pages", {}) or {}).values():
                ii = (p.get("imageinfo") or [{}])[0]
                w, h = ii.get("width", 0), ii.get("height", 0)
                if w < 2400 or h == 0 or w / h < 1.3 or ii.get("mime") not in ("image/jpeg", "image/png", "image/tiff"):
                    continue
                em = ii.get("extmetadata", {})
                lic = clean(em.get("LicenseShortName", {}).get("value"))
                if not OK_LIC.match(lic) or re.search(r"NC|ND", lic):
                    continue
                pid = str(p["pageid"])
                if pid in seen: continue
                seen[pid] = {
                    "id": pid, "theme": key, "title": p["title"], "w": w, "h": h, "license": lic,
                    "license_url": clean(em.get("LicenseUrl", {}).get("value")),
                    "artist": clean(em.get("Artist", {}).get("value")),
                    "credit": clean(em.get("Credit", {}).get("value"))[:200],
                    "attribution_required": clean(em.get("AttributionRequired", {}).get("value")),
                    "restrictions": clean(em.get("Restrictions", {}).get("value")),
                    "desc": clean(em.get("ImageDescription", {}).get("value"))[:240],
                    "categories": clean(em.get("Categories", {}).get("value"))[:300],
                    "page": ii.get("descriptionurl"), "original": ii.get("url"), "thumb_url": ii.get("thumburl"),
                    "tier": "featured" if "Featured" in flt else ("quality" if "Quality" in flt else "general"),
                    "query": q,
                }
            time.sleep(0.4)
        if sum(1 for v in seen.values() if v["tier"] != "general") >= 18: break
    out[key] = {"label": label, "items": list(seen.values())}
    print(key, label, len(seen), "(featured/quality:", sum(1 for v in seen.values() if v["tier"] != "general"), ")", flush=True)
(D / "candidates.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
