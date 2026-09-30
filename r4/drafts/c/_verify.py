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
         "C안(도록형) 내부 검토용","(부분)","도판"}
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

# 홈에서 master 승인으로 뺀 r4 블록(2026-09-30): hero·times(첫 판면이 대신) · latest-sermon(첫 판면과 중복) · intro·gallery(성도 사진 — 명화 방향)
# · pillars 는 빈 칸이라 뺀 것이며 글을 채우면 복귀. footer 는 전 페이지 공통 꼬리로 대체(교회명·주소·전화·© 는 꼬리에 실림).
APPROVED_DROP={"index":{"hero","times","latest-sermon","pillars","intro","gallery","footer"}}
DROP_ALL={"page-head","footer"}   # page-head 는 첫 판면(spread)으로 옮겨져야 하므로 그 글자는 따로 검사

def _blocks(raw):
    raw=re.sub(r"<!--.*?-->","",raw,flags=re.S)
    out={}
    for m in re.finditer(r'<section\b[^>]*data-block="([^"]+)"[^>]*>.*?</section>',raw,re.S): out[m.group(1)]=m.group(0)
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
    drop=DROP_ALL|APPROVED_DROP.get(page,set())
    expected=[b for b in sb if b not in drop]
    missing_blocks=[b for b in expected if b not in gb]
    gen_nodes=set(_nodes(re.sub(r"<!--.*?-->","",gen,flags=re.S)))
    missing_nodes=[]
    for b in expected:
        if b in gb:
            for n in _nodes(sb[b]):
                if n not in gen_nodes: missing_nodes.append(f"{b}: {n}")
    if "page-head" in sb and page!="재정":   # 첫 판면으로 옮긴 글자(eyebrow·h1·lead)도 있어야 한다
        for n in _nodes(sb["page-head"]):
            if n not in gen_nodes: missing_nodes.append(f"page-head→spread: {n}")
    return {"page":page,"src_blocks":len(sb),"expected_blocks":len(expected),"gen_blocks":len(gb),
            "dropped_approved":sorted(b for b in sb if b in drop),"missing_blocks":missing_blocks,"missing_nodes":missing_nodes,
            "complete":not missing_blocks and not missing_nodes}

def links(page):
    f=R4/f"{page}.html"; raw=f.read_text(encoding="utf-8")
    raw=re.sub(r"<!--.*?-->","",raw,flags=re.S)
    out={"page":page,"internal":[],"external":[],"broken":[]}
    for m in re.finditer(r'(?:href|src)="([^"]+)"',raw):
        u=m.group(1)
        if u.startswith(("http://","https://","tel:","mailto:","data:")): out["external"].append(u); continue
        if u.startswith("#"):
            if not re.search(r'id="%s"'%re.escape(u[1:]),raw): out["broken"].append(u)
            continue
        path=u.split("?")[0].split("#")[0]
        target=(R4/path).resolve()
        if not target.exists(): out["broken"].append(u)
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
    base=[CHROME,"--headless=new","--disable-gpu","--hide-scrollbars","--allow-file-access-from-files","--virtual-time-budget=4000"]+args
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
