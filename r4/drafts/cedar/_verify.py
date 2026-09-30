#!/usr/bin/env python3
"""cedar 검사기 — r4/drafts/c/_verify.py(원본 하네스)를 cedar 폴더에 맞춰 호출하는 진입점(codex R1 지적 C: 검사기가 어디 있는지 남이 못 찾으면 없는 것과 같다).
검사 논리는 전부 c/_verify.py 에 있다. cedar 전용 규칙은 그 파일 안에 이름으로 있다:
  · 목적지 이탈(cedar 내부 링크가 ../c/ 등 다른 시안 폴더로 나가면 broken)  → c/_verify.py links()  `R4.name == "cedar"` 분기
  · 저장소 밖 경로(../ 4단 이상 연속이면 broken · 속성·JS 문자열 모두)         → c/_verify.py links()  첫 regex
  · 승인 제외 블록/문구(APPROVED)                                              → c/_verify.py CEDAR_APPROVED_DROP · CEDAR_APPROVED_NODE_DROP
  · 첫 화면(subhero) 글자 검사                                                 → c/_verify.py completeness()  `spread|subhero`
  · 시더 구조 라벨 허용                                                        → c/_verify.py ALLOW
사용: python3 r4/drafts/cedar/_verify.py [페이지 …]  → 창작0·누락0·링크·넘침(390/1280)·캡처(캡처_R4/cedar/) · 산출 _evidence/*.json (이 폴더)
종료 코드: 전 페이지 통과 0 · 하나라도 실패 1 (주간 잡 연동 §13 이 이 코드를 본다)
"""
import importlib.util, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("v", HERE.parent / "c" / "_verify.py"); v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
v.R4 = HERE
v.CAP = Path("/Users/sdw79/SDWjavis/큰샘교회/홈페이지_리뉴얼_20260912/캡처_R4/cedar")
PAGES = ["index", "교회소개", "예배안내", "새가족", "아카데미", "온라인예배", "재정", "주보", "칼럼"]
pages = [a for a in sys.argv[1:] if a in PAGES] or PAGES
(HERE / "_evidence").mkdir(exist_ok=True)
res = {}; fail = 0
for pg in pages:
    tp = v.text_parity(pg); lk = v.links(pg); c = v.completeness(pg)
    ov = {w: v.measure(pg, w) for w in (390, 1280)}
    for w in (390, 1280): v.capture(pg, w, min(max(ov[w].get("scrollHeight", 900) + 40, 900), 16000))
    ok = tp["parity"] and c["complete"] and not lk["broken"] and not any(m.get("overflow") for m in ov.values())
    fail += (not ok)
    res[pg] = {"parity": tp["parity"], "unmatched": tp["unmatched"], "complete": c["complete"], "missing": c["missing_blocks"] + c["missing_nodes"],
               "blocks": f"{c.get('expected_blocks')}/{c.get('gen_blocks')}", "dropped": c.get("dropped_approved"), "broken": lk["broken"],
               "overflow": {str(w): m.get("overflow") for w, m in ov.items()}, "ok": ok}
    print(f"[{pg}] parity={tp['parity']} complete={c['complete']} blocks={res[pg]['blocks']} broken={lk['broken']} overflow={res[pg]['overflow']} → {'OK' if ok else 'FAIL'}")
(HERE / "_evidence" / "verify.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK {len(pages)-fail}/{len(pages)}"); sys.exit(1 if fail else 0)
