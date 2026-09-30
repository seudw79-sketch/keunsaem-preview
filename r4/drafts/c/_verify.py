#!/usr/bin/env python3
"""C안 결정론 검증 하네스 — r4/_evidence/verify.py 를 r4/drafts/c/ 에 맞게 경로·출처만 바꾼 사본(검사 로직 동일 · 캡션 조각 대조 1줄 추가).
원본: R4 결정론 검증 하네스 — 문안 대조·링크 실존·hex 0·주석 균형·수평 넘침·캡처.
사용: python3 verify.py [페이지명 ...]   (생략=전 페이지)
산출: r4/_evidence/text_parity.json · links.json · css_check.json · overflow.json · 캡처_R4/<페이지>_{390,1280}.png
"""
import json, os, re, sys, html, subprocess, shutil, tempfile
from pathlib import Path

R4 = Path(__file__).resolve().parent            # r4/drafts/c (검사 대상 폴더 · 이름은 원본 그대로 둠)
PREVIEW = R4.parent.parent.parent                 # keunsaem-preview
CSRC = R4 / "_src"
LIVE = Path("/Users/sdw79/SDWjavis/_레포/ksmc31")
CAP = Path("/Users/sdw79/SDWjavis/큰샘교회/홈페이지_리뉴얼_20260912/캡처_R4/c")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LEDGER = Path("/Users/sdw79/SDWjavis/큰샘교회/홈페이지_리뉴얼_20260912/조사/00_R3_실문구_대장.md")

# 페이지 → 출처 파일 목록(문안은 이 안에서만 나와야 한다 = 창작 0)
COMMON = [PREVIEW/"시안R3_B.html", LEDGER, CSRC/"plates.json", CSRC/"site.json", PREVIEW/"r4"/"drafts"/"시안C"/"index.html", LIVE/"시안E_홈.html", LIVE/"시안E_새가족.html", LIVE/"latest.json", LIVE/"주보목록.json"]
PAGES = {
    "index": COMMON + [LIVE/"시안E_교회소개.html", LIVE/"시안E_새가족.html", LIVE/"시안E_예배안내.html",
                       LIVE/"jubo_260920.html", LIVE/"jubo_260913.html", LIVE/"통독_365.json", LIVE/"통독_영상_덮어쓰기.json"],
    "교회소개": COMMON + [LIVE/"시안E_교회소개.html"],
    "예배안내": COMMON + [LIVE/"시안E_예배안내.html"],
    "새가족": COMMON + [LIVE/"시안E_새가족.html"],
    "아카데미": COMMON + [LIVE/"시안E_아카데미.html", LIVE/"통독_365.json"],
    "온라인예배": COMMON + [LIVE/"시안E_온라인예배.html"],
    "재정": COMMON + [LIVE/"시안E_재정.html"],
    "주보": COMMON + [LIVE/"시안E_주보.html"],
    "칼럼": COMMON + [LIVE/"시안E_칼럼.html", LIVE/"칼럼목록.json"],
}
# 이번 주 주보(latest.json 주보_링크 → jubo_<yymmdd>.html)를 홈 출처에 추가 — 성경 봉독 본문의 유일한 대장(2026-09-30)
try:
    _m=re.search(r"v=(\d{4})(\d{2})(\d{2})", json.loads((LIVE/"latest.json").read_text(encoding="utf-8")).get("주보_링크",""))
    if _m: PAGES["index"]=PAGES["index"]+[LIVE/f"jubo_{_m.group(1)[2:]}{_m.group(2)}{_m.group(3)}.html"]
except Exception: pass
# 구조 라벨·기호(문안 아님) 허용목록 — 여기 있는 것만 출처 없이 허용
# 04=교회소개 네 가지 4열 번호(구조 라벨 · 01~03 과 동급) — ★주석은 반드시 별도 줄에(세트 리터럴 줄 끝 주석이 뒤 항목을 삼킨 사고 2026-09-30)
ALLOW = {"↗","→","←","↓","·","—","/","01","02","03","04","365","오늘의 통독 강의 ↗","처음 오시는 분께",
         "← 이전 회차","다음 회차 →","바로가기","주 메뉴","새가족 안내 ↗","예배안내 ↗","오시는 길 ↗","성경 아카데미 ↗",
         # master 지정 문구(2026-09-30 3차 (d)·gemini R1 ④) — 세 기둥 섹션 eyebrow
         "세 기둥",
         # master 허용(2026-09-30 gemini R1 전달) — 푸터 사실 표기 한 줄
         "© 2026 큰샘교회",
         # C안 도록 구조 라벨(문안 아님) — 시안C(master 제작)·생성기 고정 문자열
         "도판 목록","메뉴","지난 설교","이번 주일","No. 01","No. 02","No. 03","No. 04","No. 05","No. 06","No. 07","No. 08","No. 09",
         "C안(도록형) 내부 검토용","(부분)","도판",
         # 시더 판 구조 라벨
         "T-HOME-CEDAR 비교 초안 · 내부 검토용","No. 02","No. 03","No. 04","No. 05","No. 06","No. 07","No. 08","No. 09"}
# 런타임 합성값(통독 회차 표기 — 시안E JS 가 r.일+'일차' 로 만든다) 허용 패턴
ALLOW_RE = [re.compile(r"^\d{1,3}일차$"), re.compile(r"^\d{1,3} / 365$"), re.compile(r"^도판 \d\d$"), re.compile(r"^\d\d$"), re.compile(r"^이번 주일 · \d{1,2}월 \d{1,2}일$"), re.compile(r"^도판: .+ 공개 소장품\(Public Domain\)$")]

def norm(s):
    s = html.unescape(s).replace(" "," ")
    s = re.sub(r"\s+"," ",s).strip()
    return s

def source_text(paths):
    """출처 파일의 텍스트·alt·title·JSON 값을 정규화해 한 덩어리로."""
    buf=[]
    missing=[str(p) for p in paths if not p.exists()]
    if missing:   # codex r1: 출처가 없으면 조용히 건너뛰지 않는다 — 실패로 올린다
        raise FileNotFoundError("출처 파일 없음: "+", ".join(missing))
    for p in paths:
        raw=p.read_text(encoding="utf-8",errors="replace")
        if p.suffix==".json":
            def walk(o):
                if isinstance(o,dict): [walk(v) for v in o.values()]
                elif isinstance(o,list): [walk(v) for v in o]
                else: buf.append(str(o))
            walk(json.loads(raw)); continue
        raw=re.sub(r"<script.*?</script>","",raw,flags=re.S)
        raw=re.sub(r"<style.*?</style>","",raw,flags=re.S)
        raw=re.sub(r"<!--.*?-->","",raw,flags=re.S)
        for m in re.finditer(r'(?:alt|title|content|href)="([^"]*)"',raw): buf.append(m.group(1))
        for m in re.finditer(r"(?:alt|title|content|href)='([^']*)'",raw): buf.append(m.group(1))
        raw=re.sub(r"<br\s*/?>","\n",raw)
        buf.append(re.sub(r"<[^>]+>","\n",raw))
    return norm("\n".join(buf)), norm(" ".join(buf))

def page_text_nodes(p):
    raw=p.read_text(encoding="utf-8")
    raw=re.sub(r"<script.*?</script>","",raw,flags=re.S)
    raw=re.sub(r"<style.*?</style>","",raw,flags=re.S)
    raw=re.sub(r"<!--.*?-->","",raw,flags=re.S)
    nodes=[]
    for m in re.finditer(r'alt="([^"]*)"',raw): nodes.append(("alt",m.group(1)))
    raw=re.sub(r"<br\s*/?>","\n",raw)
    for t in re.split(r"<[^>]+>",raw):
        for line in t.split("\n"):
            n=norm(line)
            if n: nodes.append(("text",n))
    return nodes

def text_parity(page):
    """방향 1(창작 0): 생성 페이지의 글자가 전부 출처에 있는가. ※ 누락은 못 잡는다 — 그것은 completeness() 가 본다(codex r1 2026-09-30)."""
    src_paths=PAGES[page]; f=R4/f"{page}.html"
    try:
        src_lines, src_flat = source_text(src_paths)
    except FileNotFoundError as e:
        return {"page":page,"nodes":0,"unmatched":[str(e)],"parity":False}
    hay = src_flat
    unmatched=[]; total=0
    for kind,n in page_text_nodes(f):
        if not n or n in ALLOW or any(rx.match(n) for rx in ALLOW_RE): continue
        total+=1
        if n in hay: continue
        # 화살표 기호(↗ → ← ↓)는 링크 장식 — 떼고 본문만 대조 (↓=gemini R1 ⑦ 페이지 내 이동)
        base=re.sub(r"\s*[↗→←↓]\s*$","",n).strip()
        if base and base in hay: continue
        # 구분자로 쪼개 조각 단위 대조(조각마다 출처 존재해야 함)
        # C안 캡션 「작가, 『제목』 (덧말), 연도 (부분)」 — 『』() 를 떼고 쉼표로도 쪼개 plates.json 값과 조각 대조
        n2=n.replace("『","").replace("』","").replace(" (부분)","").rstrip(" ·")
        pieces=[x.strip() for x in re.split(r"\s[·—/]\s|·|\s—\s|,\s",n2) if x.strip()]
        if pieces and all((pc in hay) or (pc in ALLOW) or len(pc)<2 for pc in pieces): continue
        unmatched.append(n)
    return {"page":page,"nodes":total,"unmatched":unmatched,"parity":len(unmatched)==0}

# 홈에서 뺀 r4 블록 — master 승인(2026-09-30): hero(첫 판면이 대신) · latest-sermon(첫 판면과 중복) · intro·gallery(성도 사진 — 명화 방향).
# ★pillars(세 기둥 = 오너 목회 3축)는 빈 칸이라 뺀 것이지 없애기로 한 것이 아님 — 오너가 글을 채우면 복귀(_build.py keep 에 "pillars" 추가 + 여기 APPROVED_DROP 에서 제거).
# footer 는 전 페이지 공통 꼬리로 대체(교회명·주소·전화·© 는 꼬리에 실림). times 는 hero 안 예배 시간 줄(같은 값이 worship 블록에 있음).
# 이 목록과 _build.py build_index() 의 주석·keep 은 같은 사실을 적는다 — 한쪽을 바꾸면 다른 쪽도.
APPROVED_DROP={"index":{"hero","times","latest-sermon","pillars","intro","gallery","footer"}}
# 문안이 아닌 요소(사진)를 뺄 때 사라지는 alt 문구 — 선언된 것만 누락 검사에서 제외(조용한 건너뛰기 금지 · 시더 홈 사람 사진 0 · 2026-09-30)
APPROVED_NODE_DROP={}
# 시더(cedar) 판 전용 승인 제외 — 사유: 사람 사진 0(오너 방향) · gallery 는 사진 0 이면 존재 이유 없음(master 판정 2026-09-30). 검사 호출부가 R4.name=="cedar" 일 때 이 값을 쓴다
CEDAR_APPROVED_DROP={"index":{"hero","times","latest-sermon","gallery","location","footer"},"교회소개":{"gallery"}}
CEDAR_APPROVED_NODE_DROP={"index":{"정자 앞에 함께 선 큰샘교회 가족들"}}   # 교회소개 about.jpg 는 오너 수정 2 로 복귀(흑백) → 제외 해제
# 선언된 문장 결합(오너 수정 3 · <br> 제거로 두 노드가 한 노드가 됨 · 문구 불변): (페이지, (원문 연속 노드…), 생성 노드)
CEDAR_TEXT_JOIN={"새가족":[(("처음 오신","분 안내"),"처음 오신 분 안내")],"index":[(("처음 오신","분 안내"),"처음 오신 분 안내")]}
DROP_ALL={"page-head","footer"}   # page-head 는 첫 판면(spread)으로 옮겨져야 하므로 그 글자는 따로 검사

def _blocks(raw):
    """data-block → 원문. 같은 이름이 두 번 나오면 덮어쓰지 않고 '이름#2' 로 따로 보관한다(codex r2: 덮어쓰기면 한쪽 누락이 가려진다)."""
    raw=re.sub(r"<!--.*?-->","",raw,flags=re.S)
    out={}
    for m in re.finditer(r'<section\b[^>]*data-block="([^"]+)"[^>]*>.*?</section>',raw,re.S):
        k=m.group(1); i=2
        while k in out: k=f"{m.group(1)}#{i}"; i+=1
        out[k]=m.group(0)
    return out
def _nodes(frag):
    frag=re.sub(r"<script.*?</script>","",frag,flags=re.S); frag=re.sub(r"<br\s*/?>","\n",frag)
    ns=[]
    for m in re.finditer(r'alt="([^"]*)"',frag):
        n=norm(m.group(1));
        if n: ns.append(n)
    for t in re.split(r"<[^>]+>",frag):
        for line in t.split("\n"):
            n=norm(line)
            if n: ns.append(n)
    return ns

def completeness(page):
    """방향 2(누락 0): r4 본편의 블록·글자가 생성 페이지에 다 들어갔는가 — 출처 없는 것을 건너뛰지 않고, 빠진 블록·문장의 이름을 찍는다(codex r1 수용)."""
    src=(PREVIEW/"r4"/f"{page}.html"); f=R4/f"{page}.html"
    if not src.exists(): return {"page":page,"complete":False,"missing_blocks":["r4 원문 없음: "+str(src)],"missing_nodes":[]}
    sb=_blocks(src.read_text(encoding="utf-8")); gen=f.read_text(encoding="utf-8"); gb=_blocks(gen)
    _ad = CEDAR_APPROVED_DROP if R4.name=="cedar" else APPROVED_DROP
    drop=DROP_ALL|_ad.get(page,set())
    expected=[b for b in sb if b not in drop]
    missing_blocks=[b for b in expected if b not in gb]
    # 블록 단위 · 문장 순서·개수까지 같아야 한다(페이지 전체 set 비교는 중복 문장·순서·개수를 무시해 통째로 빠진 문단을 놓칠 수 있다 — codex r2 수용).
    # 이식은 원문 그대로이므로 '같은 블록의 문장 열이 완전히 같다'가 기준. 다르면 첫 어긋난 자리(위치·원문·생성)를 찍는다.
    missing_nodes=[]
    dup=[k for k in list(sb)+list(gb) if "#" in k]
    if dup: missing_nodes.append("같은 data-block 이름이 두 번: "+", ".join(sorted(set(dup))))
    for b in expected:
        if b in gb:
            _nd = CEDAR_APPROVED_NODE_DROP if R4.name=="cedar" else APPROVED_NODE_DROP
            sn=[n for n in _nodes(sb[b]) if n not in _nd.get(page,set())]; gn=_nodes(gb[b])
            if R4.name=="cedar":
                for parts,joined in CEDAR_TEXT_JOIN.get(page,[]):
                    for i in range(len(sn)-len(parts)+1):
                        if tuple(sn[i:i+len(parts)])==parts: sn[i:i+len(parts)]=[joined]; break
            if sn!=gn:
                i=next((i for i in range(max(len(sn),len(gn))) if i>=len(sn) or i>=len(gn) or sn[i]!=gn[i]),0)
                missing_nodes.append(f"{b}: 원문 {len(sn)}문장 vs 생성 {len(gn)}문장 · 첫 어긋남 #{i+1} 원문={sn[i] if i<len(sn) else '(없음)'!r} 생성={gn[i] if i<len(gn) else '(없음)'!r}")
    if "page-head" in sb and page!="재정":   # 첫 판면으로 옮긴 글자(eyebrow·h1·lead) — 순서는 바뀌어도 되나 전부 있어야 한다
        spread=re.search(r'<section class="(?:spread|subhero)">.*?</section>',gen,re.S)   # subhero = 시더 틀 첫 화면(같은 역할)
        sp_nodes=_nodes(spread.group(0)) if spread else []
        for n in _nodes(sb["page-head"]):
            if n not in sp_nodes: missing_nodes.append(f"page-head→spread: {n}")
    return {"page":page,"src_blocks":len(sb),"expected_blocks":len(expected),"gen_blocks":len(gb),
            "dropped_approved":sorted(b for b in sb if b in drop),"missing_blocks":missing_blocks,"missing_nodes":missing_nodes,
            "complete":not missing_blocks and not missing_nodes}

def links(page):
    f=R4/f"{page}.html"; raw=f.read_text(encoding="utf-8")
    raw=re.sub(r"<!--.*?-->","",raw,flags=re.S)
    out={"page":page,"internal":[],"external":[],"broken":[]}
    # 저장소 밖 경로 금지(codex R1 · master 2026-09-30): 산출물 어디에도(속성·JS 문자열 포함) ../ 가 4단 이상 연속이면 실패 — 미리보기 루트는 r4/drafts/<판>/ 에서 3단
    for m in re.finditer(r'(?:\.\./){4,}[^"\'\s)]*',raw): out["broken"].append("저장소 밖 경로: "+m.group(0))
    # 첫 화면 큰 카드 썸네일은 maxresdefault 여야 한다(오너 수정 5 · 480px hqdefault 를 560~1120px 로 늘려 뿌옇게 보임). 스크립트 교체 경로에 hqdefault 직접 지정도 금지
    if R4.name=="cedar" and page=="index":
        big=re.search(r'<img id="sm-thumb-img"[^>]*src="([^"]+)"',raw)
        if big and "maxresdefault" not in big.group(1): out["broken"].append("첫 화면 썸네일 저해상: "+big.group(1))
        if re.search(r"src='https://i\.ytimg\.com/vi/'\+[^;]*hqdefault",raw): out["broken"].append("스크립트가 hqdefault 를 직접 지정")
    # 있어야 할 것이 그대로 있는가(master 2026-09-30 · 하위 8페이지 꼬리 소실 회귀를 검사기가 못 잡음): 시더 9페이지 전부 — 진회색 꼬리 섹션 1 · 주소 ≥1 · 전화 ≥1 · 「오시는 길 ↗」 버튼 1. 값으로 판정
    if R4.name=="cedar":
        need={"dark섹션":len(re.findall(r'<section class="dark">',raw)),"주소":raw.count("경기 광명시 기아로 23"),"전화":raw.count("010-2534-0407"),"오시는길버튼":len(re.findall(r'<a class="btn"[^>]*>오시는 길 ↗</a>',raw))}
        if need["dark섹션"]!=1 or need["주소"]<1 or need["전화"]<1 or need["오시는길버튼"]!=1: out["broken"].append("꼬리 결손: "+json.dumps(need,ensure_ascii=False))
    for m in re.finditer(r'(?:href|src)="([^"]+)"',raw):
        u=m.group(1)
        if u.startswith(("http://","https://","tel:","mailto:","data:")): out["external"].append(u); continue
        if u.startswith("#"):
            if not re.search(r'id="%s"'%re.escape(u[1:]),raw): out["broken"].append(u)
            continue
        path=u.split("?")[0].split("#")[0]
        target=(R4/path).resolve()
        if not target.exists(): out["broken"].append(u)
        # 목적지 규칙(2026-09-30 master 지적 · 200 만 보면 목적지가 틀려도 통과): 시더(cedar) 폴더 안 페이지의 내부 링크는 다른 시안 폴더(../c/ 등)로 나가면 안 된다
        if R4.name == "cedar" and re.match(r"\.\./(c|시안C|c-menu|c-color)/", u): out["broken"].append("목적지 이탈: " + u)
        out["internal"].append(u)
    return out

def css_check():
    res={}
    for css in sorted(R4.glob("*.css")):
        raw=css.read_text(encoding="utf-8")
        opens=raw.count("/*"); closes=raw.count("*/")
        body=re.sub(r"/\*.*?\*/","",raw,flags=re.S)
        if css.name=="c.css":
            # hex 는 primitive 선언 줄(--p-*)에만 허용
            # C안: hex 는 :root 블록 안에만 허용
            root=re.search(r":root\{.*?\}",body,re.S); rootspan=root.span() if root else (0,0)
            hexes=[m.group(0) for m in re.finditer(r"#[0-9A-Fa-f]{3,8}\b",body) if not (rootspan[0]<=m.start()<rootspan[1])]
        else:
            hexes=re.findall(r"#[0-9A-Fa-f]{3,8}\b",body)
        res[css.name]={"comment_open":opens,"comment_close":closes,"balanced":opens==closes,"hex_outside_tokens":hexes}
    for f in sorted(R4.glob("*.html")):
        if f.name.startswith("_"): continue
        raw=f.read_text(encoding="utf-8")
        raw=re.sub(r"<!--.*?-->","",raw,flags=re.S)
        raw=re.sub(r'href="[^"]*"',"",raw)
        hexes=re.findall(r"#[0-9A-Fa-f]{3,8}\b",raw)
        res[f.name]={"hex_in_html":hexes}
    return res

def chrome(args, timeout=90):
    """cys run(스코프 실행)이 기본 · 리뷰어 좌석처럼 cys 가 없거나 거부되면 로컬 크롬 직접 실행으로 폴백(gemini r1 지적 · master 수용 2026-09-30 —
    폴백 없이는 overflow.json 이 전부 에러로 기록돼 넘침 판정이 무효였다)."""
    # --force-prefers-reduced-motion: 캡처·측정이 등장 전환(0.55s 페이드) 도중을 잡지 않게 — 페이지의 reduced-motion 분기가 전환을 끈다(gemini R1 G · master: 페이드 중간 캡처는 판정 근거가 못 된다). 실측: 플래그 유무로 matchMedia true/false 확인 2026-09-30
    base=[CHROME,"--headless=new","--disable-gpu","--hide-scrollbars","--allow-file-access-from-files","--force-prefers-reduced-motion","--virtual-time-budget=4000"]+args
    if shutil.which("cys"):
        r=subprocess.run(["cys","run","--"]+base,capture_output=True,text=True,timeout=timeout)
        if r.returncode==0 and r.stdout.strip(): return r
    return subprocess.run(base,capture_output=True,text=True,timeout=timeout)

def measure(page, width):
    """넘침 측정. 헤드리스 Chrome 은 500px 미만 창을 못 만들므로(시안E 실측) 500 미만 폭은 iframe 래퍼로 진짜 폭을 만든다.
    maxRight 는 overflow-x:auto/scroll 조상 안의 요소(내비 스크롤 행)는 제외한다."""
    f=R4/f"{page}.html"; raw=f.read_text(encoding="utf-8")
    probe=("<script>window.addEventListener('load',function(){var d=document.documentElement;var mr=0;"
           "function inScroll(e){for(var p=e.parentElement;p&&p!==document.body;p=p.parentElement){var o=getComputedStyle(p).overflowX;if(o==='auto'||o==='scroll')return true;}return false;}"
           "document.querySelectorAll('body *').forEach(function(e){if(inScroll(e))return;var r=e.getBoundingClientRect();if(r.width>0&&r.right>mr)mr=r.right;});"
           "var msg='PROBE sw='+Math.max(d.scrollWidth,document.body.scrollWidth,Math.ceil(mr))+' cw='+d.clientWidth+' sh='+Math.max(d.scrollHeight,document.body.scrollHeight)+' mr='+Math.ceil(mr);"
           "document.title=msg;if(window.parent!==window)window.parent.postMessage(msg,'*');});</script></body>")
    tmp=R4/f"_probe_{page}.html"; tmp.write_text(raw.replace("</body>",probe,1),encoding="utf-8")
    wrap=R4/f"_wrap_{page}_{width}.html"
    try:
        if width<500:
            wrap.write_text(f"<!doctype html><html><head><meta charset='utf-8'><title>WRAP</title><style>body{{margin:0}}iframe{{border:0;display:block}}</style></head><body><iframe id='f' src='_probe_{page}.html' width='{width}' height='900'></iframe><script>window.addEventListener('message',function(e){{document.title=String(e.data)}});</script></body></html>",encoding="utf-8")
            r=chrome(["--window-size=520,900","--dump-dom",f"file://{wrap}"])
        else:
            r=chrome([f"--window-size={width},900","--dump-dom",f"file://{tmp}"])
        m=re.search(r"PROBE sw=(\d+) cw=(\d+) sh=(\d+) mr=(\d+)",r.stdout)
        if not m: return {"error":"probe not found","stderr":r.stderr[-300:]}
        sw,cw,sh,mr=map(int,m.groups())
        return {"scrollWidth":sw,"clientWidth":cw,"scrollHeight":sh,"maxRight":mr,"overflow":sw>cw,"method":"iframe-wrapper" if width<500 else "window"}
    finally:
        tmp.unlink(missing_ok=True); wrap.unlink(missing_ok=True)

def capture(page, width, height):
    """캡처. 500px 미만은 iframe 래퍼(폭 width·높이 height)를 520px 창에 렌더한 뒤 왼쪽 width 만 잘라 저장."""
    CAP.mkdir(parents=True,exist_ok=True)
    out=CAP/f"{page}_{width}.png"
    if width<500:
        wrap=R4/f"_cap_{page}_{width}.html"
        wrap.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>body{{margin:0;background:transparent}}iframe{{border:0;display:block}}</style></head><body><iframe src='{page}.html' width='{width}' height='{height}'></iframe></body></html>",encoding="utf-8")
        try:
            r=chrome([f"--window-size=520,{height}",f"--screenshot={out}",f"file://{wrap}"],timeout=180)
        finally:
            wrap.unlink(missing_ok=True)
        try:
            from PIL import Image
            im=Image.open(out); im.crop((0,0,width,im.height)).save(out)
        except Exception as e:
            return {"file":str(out),"exists":False,"error":str(e)}
    else:
        r=chrome([f"--window-size={width},{height}",f"--screenshot={out}",f"file://{R4/(page+'.html')}"],timeout=180)
    return {"file":str(out),"exists":out.exists() and out.stat().st_size>0,"bytes":out.stat().st_size if out.exists() else 0,"method":"iframe-wrapper" if width<500 else "window"}

def load(name):
    p=R4/"_evidence"/name
    return json.loads(p.read_text()) if p.exists() else {}
def save(name,obj):
    (R4/"_evidence"/name).write_text(json.dumps(obj,ensure_ascii=False,indent=1),encoding="utf-8")

if __name__=="__main__":
    pages=[a for a in sys.argv[1:] if a in PAGES] or [p for p in PAGES if (R4/f"{p}.html").exists()]
    tp=load("text_parity.json"); lk=load("links.json"); ov=load("overflow.json"); cp=load("captures.json")
    for pg in pages:
        tp[pg]=text_parity(pg); lk[pg]=links(pg); tp[pg]["completeness"]=completeness(pg)
        ov[pg]={}
        for w in (390,1280):
            m=measure(pg,w); ov[pg][str(w)]=m
            h=min(max(m.get("scrollHeight",900)+40,900),16000)
            cp[f"{pg}_{w}"]=capture(pg,w,h)
        c=tp[pg]["completeness"]
        print(f"[{pg}] parity={tp[pg]['parity']} unmatched={tp[pg]['unmatched']} complete={c['complete']} blocks={c.get('expected_blocks')}/{c.get('gen_blocks')} missing_blocks={c['missing_blocks']} missing_nodes={c['missing_nodes'][:5]} broken={lk[pg]['broken']} overflow={ {k:v.get('overflow') for k,v in ov[pg].items()} }")
    save("text_parity.json",tp); save("links.json",lk); save("overflow.json",ov); save("captures.json",cp)
    cc=css_check(); save("css_check.json",cc)
    print("css_check:",json.dumps(cc,ensure_ascii=False))
