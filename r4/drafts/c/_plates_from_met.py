#!/usr/bin/env python3
"""plates.json 도판 대장 생성 — 기계칸은 Met Collection API 원문, 사람칸은 아래 HUMAN 표(한 곳).
근거: r4/drafts/plates_스키마.md(772ac9c·7a44c81·846bb4b) · master 판정 [캡션 3건]·[안견 표기]·[T-HOME-C-EXPAND]
사용: python3 _plates_from_met.py  → _src/plates.json (실행마다 API 재조회 · isPublicDomain 재확인)
"""
import json, datetime, urllib.request
from pathlib import Path
from PIL import Image

D = Path(__file__).resolve().parent
ART = D.parent / "art_master"           # 원본(master 확보) — 건드리지 않음
CAND = json.load(open(ART / "candidates.json", encoding="utf-8"))

K="국립국어원 외래어 표기 용례(korean.go.kr/kornorms/example 원어 표기 검색 2026-09-30)"
# 사람이 적는 칸 — no: (no_alt, artist_ko, title_ko, title_suffix, date_ko, crop, pages, file, note)
# date_ko 규칙 = 스키마 §8(Met objectDate 원문만 · 추정은 추정답게 · 해석 금지)
# artist_ko 한글 표기: 22·27·10·19 는 시안C 캡션(master 작성) 그대로 · 나머지는 worker 표기(confidence Med — Met 공식 한글 없음)
HUMAN = {
 "22": ([],          "피터르 브뤼헐",     "추수하는 사람들",            "", "1565",
        {"partial": False, "focus": "center 45%"},
        [{"page":"index","slot":"spread"}], "art22",
        f"표기: {K} 「브뤼헐, 피터르(Brueghel, Pieter)」 · 오너 첫 화면 확정(2026-09-30) · 민 14:8 젖과 꿀 · 원경 언덕에 마을 교회 첨탑 작게 있음(gemini 실측 · master: 두드러지지 않아 그대로)"),
 "27": ([],          "와타나베 시코(渡辺始興)", "산수",                      "", "18세기 전반",
        {"partial": False, "focus": "center 50%"},
        [{"page":"index","slot":"grid","order":1},{"page":"아카데미","slot":"spread"}], "art27", f"표기: 성 와타나베는 {K} 다수(渡邊/渡部) · 이름 始興(しこう)은 일본어 표기법 규칙 적용(용례 없음) → 원어 병기 · 두 폭 병풍 · 여백"),
 "10": (["05","16"], "쥘 뒤프레",         "여울을 건너는 소 떼",         "", "1836",
        {"partial": False, "focus": "center 40%"},
        [{"page":"index","slot":"grid","order":2},{"page":"새가족","slot":"spread"}], "art10", f"표기: {K} 「뒤프레, 쥘(Dupré, Jules)」 · master 판정 ②: 「소들」→「소 떼」 통일"),
 "19": ([],          "야코프 판 라위스달", "밀밭",                      "", "1660년대 중·후반",
        {"partial": False, "focus": "center 50%"},
        [{"page":"index","slot":"grid","order":3},{"page":"예배안내","slot":"spread"}], "art19", f"표기: {K} 「라위스달, 야코프 판(Ruysdael, Jacob van)」"),
 "21": ([],          "야코프 마리스(Jacob Maris)", "레이스베이크의 네덜란드 운하", "", "19세기 후반",
        {"partial": False, "focus": "center 50%"},
        [{"page":"index","slot":"grid","order":4},{"page":"온라인예배","slot":"spread"}], "art21",
        f"표기: {K} 용례 없음 → 네덜란드어 규칙(야코프=용례 라위스달 건과 동일) · 원어 병기 · 31 대체(master ④ 2026-09-30) — 수채 · 운하·다리·초가·인물, 교회·절 없음(worker 화면 실측)"),
 "15": ([],          "카미유 피사로",     "퐁투아즈의 잘레 언덕",        "", "1867",
        {"partial": False, "focus": "center 50%"},
        [{"page":"교회소개","slot":"spread"}], "art15", f"표기: {K} 「피사로, 카미유(Pissarro, Camille)」 · 언덕 위 작은 교회탑 有(브뤼헐과 같은 수준 · worker 화면 실측)"),
 "30": ([],          "가와바타 교쿠쇼(川端玉章)", "산수",                      "", "1887–92년 무렵",
        {"partial": True, "focus": "center 30%"},
        [{"page":"주보","slot":"spread"}], "art30", f"표기: 성 가와바타는 {K}(川端康成 등) · 이름 玉章(ぎょくしょう)은 규칙 적용 → 원어 병기 · 세로 그림 — 첫 판면은 4:3 부분 크롭 → 캡션 (부분)"),
 "37": ([],          "앙리 판탱라투르",   "꽃과 과일이 있는 정물",        "", "1866",
        {"partial": True, "focus": "center 45%"},
        [{"page":"칼럼","slot":"spread"}], "art37", f"표기: {K} 「판탱라투르, 이냐스 앙리 장 테오도르(Fantin-Latour)」 — 앞서 쓴 팡탱라투르는 오기 · 세로 그림 — 부분 크롭"),
 "20": ([],          "요한 크리스티안 달(Johan Christian Dahl)", "해 질 녘 폭포 앞의 두 사람",    "", "1823",
        {"partial": True, "focus": "center 40%"}, [], "art20", f"표기: {K} 용례 없음(노르웨이어) → 원어 병기 · 세로 그림 · 미배치"),
 "33": ([],          "요제프 안톤 코흐(Joseph Anton Koch)", "무지개가 있는 영웅적 풍경",     "", "1824",
        {"partial": True, "focus": "center 40%"}, [], "art33", f"표기: 성 코흐는 {K}(Koch, Robert 독일) · 이름 용례 없음 → 원어 병기 · 세로 그림 · 미배치 · 시트 분류 '동양-한국'은 오기(독일 화가)"),
 "31": ([],          "안견 화풍",         "연사모종",                  "소상팔경 중", "1450–1500년 무렵",
        {"partial": True, "focus": "center 30%"}, [], "art31",
        "★도판 목록 제외(master ④): Met 제목 'Evening bell from mist-shrouded temple' — 절이 제목에 있음 · Met artistPrefix 'Style of' → 화풍"),
 "24": (["32"],      "공현(龔賢)",       "시가 있는 산수",             "", "1688",
        {"partial": False, "focus": "center 50%"}, [], "art24", "표기: 신해혁명 이전 중국 인명 → 한자음(외래어 표기법 제4장) · 원어 병기 · 원본 1000px — 전폭 불가 · 미배치"),
}
# Met artistPrefix → 한글 한정어 대응표(master 판정 ② 2026-09-30) — 표에 없는 prefix 는 master 에게 묻는다(비슷한 것 고르기 금지)
PREFIX_KO = {"": "", "Attributed to": "전(傳) {n}", "Workshop of": "{n} 공방", "Circle of": "{n} 유파",
             "Follower of": "{n} 를 따른 작가", "Style of": "{n} 화풍", "Manner of": "{n} 화풍",
             "After": "{n} 원작 모사", "Copy after": "{n} 원작 모사"}

def met(obj_id):
    with urllib.request.urlopen(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}", timeout=30) as r:
        return json.load(r)

plates = []
for no, (no_alt, artist_ko, title_ko, suffix, date_ko, crop, pages, file, note) in HUMAN.items():
    c = CAND[int(no)]
    m = met(c["id"])
    assert m["isPublicDomain"] is True, (no, "PD 아님")
    if m.get("artistPrefix","") not in PREFIX_KO:
        raise SystemExit(f"{no}: 대응표에 없는 artistPrefix {m['artistPrefix']!r} — master 에게 물을 것")
    w, h = Image.open(ART / f"{no}.jpg").size
    date = m.get("objectDate","") or ""
    if date.strip().isdigit(): assert date_ko == date, (no, "확정 연도는 원문 그대로")
    if not date: assert date_ko == "", (no, "원문 연도 없음 → date_ko 비움")
    plates.append({
        "no": no, "no_alt": no_alt, "met_id": c["id"],
        "artist_en": m.get("artistDisplayName",""), "artist_prefix": m.get("artistPrefix",""), "artist_ko": artist_ko,
        "title_en": m.get("title",""), "title_ko": title_ko, "title_suffix": suffix,
        "date": date, "date_ko": date_ko, "medium": m.get("medium",""),
        "collection": "메트로폴리탄 미술관", "object_url": m.get("objectURL",""), "image_url": c.get("img",""),
        "src_px": [w, h], "portrait": h > w, "crop": crop, "pages": pages, "file": file, "note": note,
    })

out = {"_meta": {"source": "메트로폴리탄 미술관 Open Access (Met Collection API)", "license": "Public Domain — CC0",
                 "verified": datetime.date.today().isoformat(), "filter": "grayscale(1) sepia(.13) contrast(1.02)",
                 "prefix_ko": PREFIX_KO, "schema": "r4/drafts/plates_스키마.md"},
       "plates": plates}
(D / "_src" / "plates.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("plates:", len(plates), "| portrait:", [p["no"] for p in plates if p["portrait"]], "| placed:", [p["no"] for p in plates if p["pages"]])
