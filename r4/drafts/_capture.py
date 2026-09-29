#!/usr/bin/env python3
"""[초안] 캡처·넘침 측정 — verify.py 의 measure/capture 를 drafts 폴더에 그대로 적용. 산출: 캡처_R4/_drafts/*.png · drafts/_measure.json"""
import importlib.util, json, sys
from pathlib import Path
D = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("verify", D.parent / "_evidence" / "verify.py")
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
v.R4 = D
v.CAP = v.CAP / "_drafts"
pages = sys.argv[1:] or ["hero_gallery_A", "hero_gallery_B", "hero_gallery_C"]
res = {}
for p in pages:
    res[p] = {"390": v.measure(p, 390), "1280": v.measure(p, 1280),
              "cap390": v.capture(p, 390, 900), "cap1280": v.capture(p, 1280, 1000)}
    print(p, "overflow390=", res[p]["390"].get("overflow"), "overflow1280=", res[p]["1280"].get("overflow"),
          "caps=", res[p]["cap390"]["exists"], res[p]["cap1280"]["exists"])
(D / "_measure.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
