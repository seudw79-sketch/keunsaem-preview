#!/usr/bin/env python3
"""R4 결정론 검증 하네스 — 문안 대조·링크 실존·hex 0·주석 균형·수평 넘침·캡처.
사용: python3 verify.py [페이지명 ...]   (생략=전 페이지)
산출: r4/_evidence/text_parity.json · links.json · css_check.json · overflow.json · 캡처_R4/<페이지>_{390,1280}.png
"""
import json, os, re, sys, html, subprocess, shutil, tempfile
from pathlib import Path

R4 = Path(__file__).resolve().parent.parent
PREVIEW = R4.parent
LIVE = Path("/Users/sdw79/SDWjavis/_레포/ksmc31")
CAP = Path("/Users/sdw79/SDWjavis/큰샘교회/홈페이지_리뉴얼_20260912/캡처_R4")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LEDGER = Path("/Users/sdw79/SDWjavis/큰샘교회/홈페이지_리뉴얼_20260912/조사/00_R3_실문구_대장.md")

# 페이지 → 출처 파일 목록(문안은 이 안에서만 나와야 한다 = 창작 0)
COMMON = [PREVIEW/"시안R3_B.html", LEDGER, LIVE/"시안E_홈.html", LIVE/"시안E_새가족.html", LIVE/"latest.json", LIVE/"주보목록.json"]
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
         "© 2026 큰샘교회"}
# 런타임 합성값(통독 회차 표기 — 시안E JS 가 r.일+'일차' 로 만든다) 허용 패턴
ALLOW_RE = [re.compile(r"^\d{1,3}일차$"), re.compile(r"^\d{1,3} / 365$")]

def norm(s):
    s = html.unescape(s).replace(" "," ")
    s = re.sub(r"\s+"," ",s).strip()
    return s

def source_text(paths):
    """출처 파일의 텍스트·alt·title·JSON 값을 정규화해 한 덩어리로."""
    buf=[]
    for p in paths:
        if not p.exists(): continue
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
    src_paths=PAGES[page]; f=R4/f"{page}.html"
    src_lines, src_flat = source_text(src_paths)
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
        pieces=[x.strip() for x in re.split(r"\s[·—/]\s|·|\s—\s",n) if x.strip()]
        if pieces and all((pc in hay) or (pc in ALLOW) or len(pc)<2 for pc in pieces): continue
        unmatched.append(n)
    return {"page":page,"nodes":total,"unmatched":unmatched,"parity":len(unmatched)==0}

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
    for css in sorted((R4/"assets").glob("*.css")):
        raw=css.read_text(encoding="utf-8")
        opens=raw.count("/*"); closes=raw.count("*/")
        body=re.sub(r"/\*.*?\*/","",raw,flags=re.S)
        if css.name=="tokens.css":
            # hex 는 primitive 선언 줄(--p-*)에만 허용
            hexes=[h for line in body.splitlines() if not re.match(r"\s*--p-",line) for h in re.findall(r"#[0-9A-Fa-f]{3,8}\b",line)]
        else:
            hexes=re.findall(r"#[0-9A-Fa-f]{3,8}\b",body)
        res[css.name]={"comment_open":opens,"comment_close":closes,"balanced":opens==closes,"hex_outside_tokens":hexes}
    for f in sorted(R4.glob("*.html")):
        raw=f.read_text(encoding="utf-8")
        raw=re.sub(r"<!--.*?-->","",raw,flags=re.S)
        raw=re.sub(r'href="[^"]*"',"",raw)
        hexes=re.findall(r"#[0-9A-Fa-f]{3,8}\b",raw)
        res[f.name]={"hex_in_html":hexes}
    return res

def chrome(args, timeout=90):
    return subprocess.run(["cys","run","--",CHROME,"--headless=new","--disable-gpu","--hide-scrollbars",
                           "--allow-file-access-from-files","--virtual-time-budget=4000"]+args,
                          capture_output=True,text=True,timeout=timeout)

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
        tp[pg]=text_parity(pg); lk[pg]=links(pg)
        ov[pg]={}
        for w in (390,1280):
            m=measure(pg,w); ov[pg][str(w)]=m
            h=min(max(m.get("scrollHeight",900)+40,900),16000)
            cp[f"{pg}_{w}"]=capture(pg,w,h)
        print(f"[{pg}] parity={tp[pg]['parity']} unmatched={tp[pg]['unmatched']} broken={lk[pg]['broken']} overflow={ {k:v.get('overflow') for k,v in ov[pg].items()} }")
    save("text_parity.json",tp); save("links.json",lk); save("overflow.json",ov); save("captures.json",cp)
    cc=css_check(); save("css_check.json",cc)
    print("css_check:",json.dumps(cc,ensure_ascii=False))
