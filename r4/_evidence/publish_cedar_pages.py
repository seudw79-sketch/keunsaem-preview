#!/usr/bin/env python3
"""publish_cedar_pages.py — cedar 생성본(preview r4/drafts/cedar/<페이지>.html) → ksmc31 라이브 루트 1페이지 단위 발행.
deploy_cedar_to_live.sh §2(경로 치환·noindex/내부검토 제거)·§2-b(GA4) 와 그 뒤 라이브에 손으로 얹힌 3층
(2485766 ga4-conversion-events.js · e5ee514 꼬리 법인명 · d3aaf5c Open Graph)을 한 함수로 재현한다.
검증: 같은 변환을 cedar/새가족.html 에 걸면 라이브 새가족.html 과 바이트 동일(2026-10-13 실측) — 이 parity 가 깨지면 발행을 중단한다.
사용: python3 publish_cedar_pages.py --check 새가족   (parity 만)  ·  python3 publish_cedar_pages.py 기도 힘들때말씀  (라이브 루트에 쓴다 · 커밋/푸시 없음)
"""
import re, sys, urllib.parse
from pathlib import Path
PREVIEW = Path("/Users/sdw79/SDWjavis/_레포/keunsaem-preview"); SRC = PREVIEW/"r4"/"drafts"/"cedar"; LIVE = Path("/Users/sdw79/SDWjavis/_레포/ksmc31")
GA4 = "G-HBE29Z8PJJ"
GA4_SNIPPET = ('<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
               '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}\n'
               "gtag('js',new Date());gtag('config','%s');gtag('config','AW-18487103627');</script>\n"
               '<script src="assets/ga4-conversion-events.js" defer></script>\n') % (GA4, GA4)
OG = ('<meta property="og:type" content="website">\n<meta property="og:site_name" content="큰샘감리교회">\n<meta property="og:title" content="{title}">\n'
      '<meta property="og:description" content="광명 소하동 큰샘감리교회 · 하나님의 마음을 시원케 하는 교회 · 주일예배 오전 11시">\n'
      '<meta property="og:image" content="https://ksmc31.kr/assets/og.jpg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
      '<meta property="og:url" content="https://ksmc31.kr/{path}">\n<meta property="og:locale" content="ko_KR">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="https://ksmc31.kr/assets/og.jpg">\n')
FOOT_OLD = '<footer class="ft"><span>© 2026 큰샘교회</span></footer>'
FOOT_NEW = '<footer class="ft"><span>© 2026 큰샘감리교회</span> · <span>고유번호 140-82-77161</span> · <a href="mailto:office@ksmc31.kr">office@ksmc31.kr</a> · <a href="https://www.youtube.com/channel/UC6kFMamsryfHU6mB61vtttw" target="_blank" rel="noopener">큰샘감리교회 유튜브 채널</a></footer>'

def transform(page):
    raw = (SRC/f"{page}.html").read_text(encoding="utf-8")
    s = raw
    # §2 경로 치환 (deploy_cedar_to_live.sh 와 같은 표)
    s = s.replace("https://ksmc31.kr/jubo_", "jubo_").replace("https://ksmc31.kr/'+esc(", "'+esc(")
    s = s.replace("../../../jubo.html", "jubo.html").replace("fetch('../../../", "fetch('").replace("'../../../'+d.", "d.")
    s = s.replace("../../사진/web/", "사진/cedar/").replace('var LATEST_URL="https://ksmc31.kr/latest.json"', 'var LATEST_URL="latest.json"')
    s = s.replace('<meta name="robots" content="noindex, nofollow">\n', "").replace('<meta name="robots" content="noindex, nofollow">', "").replace(" · <span>T-HOME-CEDAR 비교 초안 · 내부 검토용</span>", "")
    # d3aaf5c Open Graph — <title> 바로 뒤
    title = re.search(r"<title>(.*?)</title>", s).group(1)
    path = urllib.parse.quote(f"{page}.html") if page != "index" else ""
    # SEO-SIGNALS(130837f) 이후 라이브 머리 순서: title → canonical → meta description → OG. 생성본(856880c)은 title 뒤에 canonical 을 이미 두므로
    # 그 줄 뒤에 r4 원본의 description 과 OG 를 넣는다(ADS-D3 2026-10-15 · 교회처음 parity 로 검증). canonical 이 없으면 종전대로 title 뒤.
    canon = f'<link rel="canonical" href="https://ksmc31.kr/{path}">\n'
    r4raw = (SRC.parent.parent / f"{page}.html").read_text(encoding="utf-8")
    dm = re.search(r'<meta name="description" content="([^"]*)">', r4raw)
    desc = (f'<meta name="description" content="{dm.group(1)}">\n' if dm else "")
    if f"<title>{title}</title>\n" + canon in s:
        s = s.replace(f"<title>{title}</title>\n" + canon, f"<title>{title}</title>\n" + canon + desc + OG.format(title=title, path=path), 1)
    else:
        s = s.replace(f"<title>{title}</title>\n", f"<title>{title}</title>\n" + OG.format(title=title, path=path), 1)
    # §2-b GA4 + 2485766 conversion js — </head> 앞
    assert GA4 not in s and "</head>" in s
    s = s.replace("</head>", GA4_SNIPPET + "</head>", 1)
    # e5ee514 꼬리
    assert FOOT_OLD in s, "footer 원형이 다르다"
    s = s.replace(FOOT_OLD, FOOT_NEW, 1)
    code = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    assert not re.search(r"\.\./|사진/web/|noindex|내부 검토용", code), "치환 잔여"
    return s

if __name__ == "__main__":
    args = sys.argv[1:]; check = "--check" in args; pages = [a for a in args if not a.startswith("--")]
    for pg in pages:
        out = transform(pg)
        if check:
            live = (LIVE/f"{pg}.html").read_text(encoding="utf-8")
            print(f"{pg}: parity {'OK' if out == live else 'MISMATCH'} ({len(out)} vs {len(live)} B)")
            if out != live:
                import difflib; print("".join(list(difflib.unified_diff(live.splitlines(1), out.splitlines(1), "live", "transform", n=0))[:40]))
                sys.exit(1)
        else:
            (LIVE/f"{pg}.html").write_text(out, encoding="utf-8"); print(f"{pg}.html → {LIVE} ({len(out):,} B)")
