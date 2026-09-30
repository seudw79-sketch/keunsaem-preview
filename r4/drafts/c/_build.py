#!/usr/bin/env python3
"""C안(도록형) 9페이지 생성기 — 손복사 0.
입력: _src/plates.json(도판 대장) · _src/site.json(설정) · ../../<페이지>.html(r4 본편 · 문안 정본 · 읽기만) · 라이브 latest.json
출력: ./<페이지>.html 9개 (정적 · 외부 JS 0 · 공용 CSS c.css 1파일)
근거: r4/drafts/시안C_확장방안.md · plates_스키마.md · master 티켓 T-HOME-C-EXPAND(2026-09-30)
원칙: 본문 문안은 r4 <main> 섹션을 그대로 이식한다(문안 parity) — 여기서 새 문장을 만들지 않는다.
      캡션·alt 는 plates.json 에서만 만든다. 첫 판면(spread)은 r4 page-head(eyebrow·h1·lead)를 옮겨 채운다.
사용: python3 _build.py            → 9페이지 생성 + 검사
      python3 _build.py --timetable hero   → site.json 값을 잠시 덮어 생성(시안C 대조용)
"""
import json, re, sys, html
from pathlib import Path

C = Path(__file__).resolve().parent          # r4/drafts/c
R4 = C.parent.parent                          # r4 (본편 · 읽기만)
SRC = C / "_src"
SITE = json.load(open(SRC / "site.json", encoding="utf-8"))
PLATES = json.load(open(SRC / "plates.json", encoding="utf-8"))
LATEST = json.load(open(SITE["latest_json"], encoding="utf-8"))

if "--timetable" in sys.argv:
    SITE["hero_timetable"] = sys.argv[sys.argv.index("--timetable") + 1]
if "--nav" in sys.argv:
    SITE["nav_mode"] = sys.argv[sys.argv.index("--nav") + 1]
# --out <폴더> : 형제 폴더(예: c-menu)에 찍는다 — css·도판·하위 페이지 링크는 ../c/ 를 가리켜 두 판이 파일까지 같게(메뉴 비교용 · master 순서 변경 2026-09-30)
OUT = C; ASSET = ""
if "--out" in sys.argv:
    OUT = C.parent / sys.argv[sys.argv.index("--out") + 1]; OUT.mkdir(exist_ok=True); ASSET = "../c/"
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None

esc = lambda s: html.escape(str(s), quote=True)

# ── 도판 대장 ─────────────────────────────────────────────
BY_NO = {p["no"]: p for p in PLATES["plates"]}
PREFIX_KO = PLATES["_meta"]["prefix_ko"]

def artist_ko(p):
    """캡션 작가 표기 — Met artistPrefix 가 있으면 대응표로만 옮긴다(단정형 금지). 대장 artist_ko 에 이미 한정어가 들어 있으면 그대로."""
    pre = p["artist_prefix"]
    if pre and pre not in PREFIX_KO:
        raise SystemExit(f"{p['no']}: 대응표에 없는 artistPrefix {pre!r} — master 에게 물을 것")
    return p["artist_ko"]

def caption(p, n, spread):
    a = artist_ko(p); t = f"『{p['title_ko']}』"
    if p["title_suffix"]: t += f" ({p['title_suffix']})"
    parts = [f"{a}, {t}"]
    if p["date_ko"]: parts[0] += f", {p['date_ko']}"
    s = parts[0] + (" (부분)" if (spread and p["crop"]["partial"]) else "")
    num = f"도판 {n:02d} · " if spread else f'<span class="n">{n:02d}</span> · '
    return num + esc(s)

def alt(p):
    a = artist_ko(p); s = f"{a}, {p['title_ko']}"
    if p["date_ko"]: s += f", {p['date_ko']}"
    return esc(s)

def img_tag(p, spread):
    w1200, w2400 = f"{ASSET}assets/plates/{p['file']}_1200.jpg", f"{ASSET}assets/plates/{p['file']}_2400.jpg"
    W, H = p["src_px"]; h2400 = round(H * 2400 / W)
    sizes = "(max-width:820px) 100vw, 63vw" if spread else "(max-width:640px) 50vw, 25vw"
    cls = "plate" + (" is-crop" if (spread and p["crop"]["partial"]) else "")
    style = f' style="object-position:{esc(p["crop"]["focus"])}"' if (spread and p["crop"]["partial"]) else ""
    pri = ' fetchpriority="high"' if spread else ' loading="lazy"'
    return (f'<img class="{cls}" src="{w2400}" srcset="{w1200} 1200w, {w2400} 2400w" sizes="{sizes}" '
            f'width="2400" height="{h2400}" alt="{alt(p)}"{style}{pri}>')

def plates_for(page):
    spread = [p for p in PLATES["plates"] for u in p["pages"] if u["page"] == page and u["slot"] == "spread"]
    grid = sorted([(u.get("order", 99), p) for p in PLATES["plates"] for u in p["pages"] if u["page"] == page and u["slot"] == "grid"], key=lambda x: x[0])
    # 생성기 검사 규칙(스키마 §3) — ①spread 정확히 1 ②세로 그림은 부분 크롭 표시가 있어야 spread 가능 ③가로 <2400 spread 금지 ④중복 금지
    if page != "재정":
        assert len(spread) == 1, f"{page}: spread 도판이 {len(spread)}점 (정확히 1점이어야)"
        s = spread[0]
        assert not (s["portrait"] and not s["crop"]["partial"]), f"{page}: 세로 그림 {s['no']} 을 부분 크롭 없이 spread 에 둘 수 없음"
        assert s["src_px"][0] >= 2400, f"{page}: {s['no']} 가로 {s['src_px'][0]} < 2400 — spread 불가"
    nos = [p["no"] for p in spread] + [p["no"] for _, p in grid]
    assert len(nos) == len(set(nos)), f"{page}: 같은 그림 중복 {nos}"
    return (spread[0] if spread else None), [p for _, p in grid]

# ── r4 본편 읽기(문안 정본) ────────────────────────────────
def read_r4(page):
    raw = (R4 / f"{page}.html").read_text(encoding="utf-8")
    title = re.search(r"<title>(.*?)</title>", raw, re.S).group(1).strip()
    main = re.search(r"<main.*?</main>", raw, re.S).group(0)
    scripts = re.findall(r"<script>.*?</script>", raw[raw.index("</main>"):], re.S)
    return title, main, scripts

def repath(frag):
    """r4/ 기준 상대경로 → r4/drafts/c/ 기준. 사진/→../../사진/ · ../→../../../ (속성·스크립트 문자열 모두)."""
    # 순서 중요: 상위(../) 먼저 바꾸고 그 다음 사진/ — 반대로 하면 방금 만든 ../../사진/ 이 또 잡혀 4단이 된다(첫 실행에서 실측)
    frag = re.sub(r'(src|href)="\.\./', r'\1="../../../', frag)
    frag = frag.replace("'../", "'../../../").replace('"../"', '"../../../"')
    frag = re.sub(r'(src|href)="사진/', r'\1="../../사진/', frag)
    return frag

def sections(main, drop=(), keep=None):
    """main 안 <section ...> 블록을 data-block 기준으로 고른다(주석 포함 원문 그대로)."""
    out = []
    for m in re.finditer(r"(?:<!--[^\n]*?-->\s*)*<section\b[^>]*data-block=\"([^\"]+)\"[^>]*>.*?</section>", main, re.S):
        blk = m.group(1)
        if keep is not None and blk not in keep: continue
        if blk in drop: continue
        out.append((blk, m.group(0)))
    if keep is not None:
        order = {k: i for i, k in enumerate(keep)}
        out.sort(key=lambda x: order[x[0]])
    return out

def page_head(main):
    m = re.search(r'<section class="section page-top"[^>]*data-block="page-head".*?</section>', main, re.S).group(0)
    eyebrow = re.search(r'<span class="eyebrow">(.*?)</span>', m, re.S).group(1)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", m, re.S).group(1)
    lead = re.search(r'<p class="lead"[^>]*>(.*?)</p>', m, re.S)
    return eyebrow.strip(), h1.strip(), (lead.group(1).strip() if lead else "")

# ── 공통 조각 ─────────────────────────────────────────────
def head(title, page):
    noindex = '<meta name="robots" content="noindex, nofollow">'   # 초안 — 본편 아님
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{noindex}
<title>{esc(title)}</title>
<!-- C안(도록형) · 생성: r4/drafts/c/_build.py — 손으로 고치지 말 것(다음 생성에서 덮인다). 문안=r4/{page}.html 검증분 · 캡션=_src/plates.json · 설정=_src/site.json -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-dynamic-subset.css">
<link rel="stylesheet" href="{ASSET}c.css">
</head>
<body data-nav="{esc(SITE["nav_mode"])}">
'''

def header(page):
    links = "".join(f'<a href="{ASSET if n["file"] != "index.html" else ""}{esc(n["file"])}"{" aria-current=\"page\"" if n["file"] == f"{page}.html" else ""}>{esc(n["label"])}</a>' for n in SITE["nav"])
    return f'''<header class="hd" data-place="{esc(SITE["nav_placement"])}">
  <a class="logo" href="index.html">{esc(SITE["church"])}</a>
  <input type="checkbox" id="nav-toggle" class="nav-toggle" aria-label="메뉴" aria-controls="site-nav">
  <label for="nav-toggle" class="nav-btn">메뉴</label>
  <nav id="site-nav" class="nav" aria-label="주 메뉴">{links}</nav>
</header>
'''

def footer(used):
    """꼬리 — 교회 사실 표기(r4 푸터 문자 그대로) + 도판 출처 줄(그 페이지 도판의 소장처에서 자동)."""
    colls = sorted({p["collection"] for p in used})
    credit = f'<span>도판: {esc(" · ".join(colls))} 공개 소장품(Public Domain)</span>' if colls else ""
    return f'''<footer class="ft">
  <span>{esc(SITE["church_full"])} · {esc(SITE["address"])} · <a href="tel:{esc(SITE["phone"])}">{esc(SITE["phone"])}</a></span>
  {credit}
  <span>{esc(SITE["copyright"])}</span>
  <span>C안(도록형) 내부 검토용</span>
</footer>
</body>
</html>
'''

def spread_block(plate, right, n=1):
    return f'''<section class="spread">
  <figure class="plateL">
    {img_tag(plate, True)}
    <figcaption>{caption(plate, n, True)}</figcaption>
  </figure>
  <div class="plateR">
{right}
  </div>
</section>
'''

def plates_grid(grid, start):
    if not grid: return ""
    figs = "\n".join(f'    <figure>\n      {img_tag(p, False)}\n      <figcaption>{caption(p, start + i, False)}</figcaption>\n    </figure>' for i, p in enumerate(grid))
    return f'''<section class="plates">
  <h2>도판 목록</h2>
  <div class="grid">
{figs}
  </div>
</section>
'''

# ── 홈 ────────────────────────────────────────────────────
def sermon_parts(d):
    """latest.json 설교_날짜 '2026-09-27 · 민수기 14장 8-9절' → ('이번 주일 · 9월 27일', '민수기 14장 8-9절')"""
    date, _, verse = d["설교_날짜"].partition("·")
    y, m, dd = date.strip().split("-")
    return f"이번 주일 · {int(m)}월 {int(dd)}일", verse.strip()

def build_index():
    title, main, scripts = read_r4("index")
    spread, grid = plates_for("index")
    label, verse = sermon_parts(LATEST)
    meta_rows = ([f'      <div><dt>{esc(w["dt"])}</dt><dd>{esc(w["dd"])}</dd></div>' for w in SITE["worship"]] if SITE["hero_timetable"] == "hero" else [])
    meta_rows.append(f'      <div><dt>오시는 길</dt><dd>{esc(SITE["address"])}</dd></div>')
    right = f'''    <p class="no">No. 01</p>
    <p class="label" id="sm-label">{esc(label)}</p>
    <h1 class="title" id="sm-title">{esc(LATEST["설교_제목"])}</h1>
    <p class="verse" id="sm-verse">{esc(verse)}</p>
    <div class="actions">
      <a class="btn" id="sm-link" href="{esc(LATEST["설교_링크"])}" target="_blank" rel="noopener">설교 영상 보기</a>
      <a class="more" href="#sermons">지난 설교</a>
    </div>
    <dl class="meta">
{chr(10).join(meta_rows)}
    </dl>'''
    # 홈에 싣는 r4 섹션(순서 고정) — 뺀 것: hero(첫 판면이 대신) · latest-sermon(첫 판면과 중복) · pillars(빈 줄 · 오너 답 대기) · intro·gallery(사진 · 명화 방향)
    keep = ["today", "sermons", "worship", "visitors", "location"]
    body = [s for _, s in sections(main, keep=keep)]
    # 통독 스크립트는 r4 원문 그대로(IIFE) · latest.json 갱신은 첫 판면 id 에 맞춰 여기서 씀
    iife = next(s for s in scripts if "오늘회차" in s)
    iife = re.search(r"\(function\(\)\{.*?\}\)\(\);", iife, re.S).group(0)
    latest_js = """// latest.json 정본으로 첫 판면·최근 설교·주보만 갱신(빌드 값이 먼저 보이고, 열 때 최신값으로 덮는다). 경로는 r4/drafts/c/ 기준 상위 3단(../../../).
if(location.protocol!=='file:')fetch('../../../latest.json',{cache:'no-store'}).then(function(r){if(!r.ok)throw Error();return r.json()}).then(function(d){
  if(d.설교_제목&&d.설교_날짜&&/^https:\\/\\/www.youtube.com\\/watch\\?v=/.test(d.설교_링크)){
    var parts=d.설교_날짜.split('·'),ymd=parts[0].trim().split('-');
    document.getElementById('sm-title').textContent=d.설교_제목;
    document.getElementById('sm-label').textContent='이번 주일 · '+parseInt(ymd[1],10)+'월 '+parseInt(ymd[2],10)+'일';
    document.getElementById('sm-verse').textContent=(parts[1]||'').trim();
    document.getElementById('sm-link').href=d.설교_링크;
    var st=document.getElementById('sermon-title'),sd=document.getElementById('sermon-date'),sl=document.getElementById('sermon-link');
    if(st)st.textContent=d.설교_제목;if(sd){sd.textContent=d.설교_날짜;sd.dateTime=d.설교_날짜.slice(0,10);}if(sl)sl.href=d.설교_링크;
  }
  var jt=document.getElementById('jb-title'),jl=document.getElementById('jb-link');
  if(d.주보_제목&&jt)jt.textContent=d.주보_제목;
  if(d.주보_링크&&jl)jl.href='../../../'+d.주보_링크;
}).catch(function(){});"""
    out = head(title, "index") + header("index") + spread_block(spread, right)
    out += plates_grid(grid, 2)
    out += "<main>\n" + repath("\n".join(body)) + "\n</main>\n"
    out += "<script>\n" + latest_js + "\n" + repath(iife) + "\n</script>\n"
    out += footer([spread] + grid)
    return out

# ── 하위 페이지 ───────────────────────────────────────────
def build_page(page, n):
    title, main, scripts = read_r4(page)
    spread, grid = plates_for(page)
    eyebrow, h1, lead = page_head(main)
    right = f'''    <p class="no">No. {n:02d}</p>
    <p class="label">{eyebrow}</p>
    <h1 class="title">{h1}</h1>''' + (f'\n    <p class="lead">{lead}</p>' if lead else "")
    body = [s for _, s in sections(main, drop=("page-head",))]
    out = head(title, page) + header(page) + spread_block(spread, right)
    out += "<main>\n" + repath("\n".join(body)) + "\n</main>\n"
    for s in scripts: out += repath(s) + "\n"
    out += footer([spread] + grid)
    return out

def build_finance():
    """재정: 잠금 카드(시안E 원본 · 암호 로직·SALT·IV·CT·id 불변) — 토큰 파일만 c.css 로 바꾼다. 본문 한 글자도 안 건드림."""
    raw = (R4 / "재정.html").read_text(encoding="utf-8")
    assert 'href="assets/tokens.css"' in raw
    return raw.replace('href="assets/tokens.css"', 'href="c.css"', 1)

if __name__ == "__main__":
    n = 0
    for page in SITE["pages"]:
        n += 1
        if page == "index": html_out = build_index()
        elif page == "재정": html_out = build_finance()
        else: html_out = build_page(page, n)
        if ONLY and page not in ONLY: continue
        (OUT / f"{page}.html").write_text(html_out, encoding="utf-8")
        print(f"[{OUT.name}/{page}] {len(html_out):,}B  hero_timetable={SITE['hero_timetable']} nav_mode={SITE['nav_mode']}")
