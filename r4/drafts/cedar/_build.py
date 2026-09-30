#!/usr/bin/env python3
"""T-HOME-CEDAR — cedarcrestchurch.com 의 틀(수치·배치)만 따르고 내용은 큰샘교회 것으로 채운 홈 1장 생성.
입력: ../c/_src/site.json(메뉴 8·예배 시간·주소 — c/ 와 같은 정본) · 미리보기 루트 latest.json(이번 주 설교 · c/ 빌드가 라이브와 동기화)
출력: ./index.html · 규격은 master 실측 computed style(2026-09-30) 그대로 — 남의 로고·사진·영상·문구·SVG 파일은 쓰지 않는다(물결은 우리가 그림).
"""
import json, html, re
from pathlib import Path
D = Path(__file__).resolve().parent
PREVIEW = D.parent.parent.parent
SITE = json.load(open(D.parent / "c" / "_src" / "site.json", encoding="utf-8"))
LATEST = json.load(open(PREVIEW / "latest.json", encoding="utf-8"))
esc = lambda s: html.escape(str(s), quote=True)

date, _, verse = LATEST["설교_날짜"].partition("·")
y, m, d = date.strip().split("-")
label = f"이번 주일 · {int(m)}월 {int(d)}일"
vid = LATEST["설교_링크"].split("v=")[1].split("&")[0]
nav = "".join(f'<a href="../c/{esc(n["file"])}">{esc(n["label"])}</a>' for n in SITE["nav"])   # 하위 8페이지는 아직 c/ 것을 가리킨다(cedar 하위는 오너 확인 뒤)
times = " · ".join(f'{esc(w["dt"])} {esc(w["dd"])}' for w in SITE["worship"])

# 물결 곡선 — 우리가 그린 것(외부 SVG 파일 사용 0)
WAVE = '<svg class="wave" viewBox="0 0 1000 100" preserveAspectRatio="none" aria-hidden="true"><path d="M0,100 L0,58 C250,30 500,30 750,58 C830,68 920,84 1000,92 L1000,100 Z"/></svg>'  # 우리가 그린 곡선 · viewBox 만 원판과 같음

CSS = r'''<style>
/* 규격 = master 실측(§1) + CSS 선언값(§7 · 선택자 근거) — 근사치 금지 · 값 그대로. html 16px 기준 em→px.
   제목 글꼴: Poynter(상용) 대체 → 한글 Noto Serif KR 700 · 영문 Playfair Display 700 · lowercase 는 한글 무효.
   ★색 두 토큰(master 판정): 읽는 글자 --teal-text #2A7D71(흰 위 4.92:1) · 장식 면 --teal-surface #47AB9D(원판). 오너가 원판 색 그대로를 원하면 --teal-text 만 #47AB9D 로 되돌린다. */
:root{--bg:#FFFFFF;--ink:#000;--teal-text:#2A7D71;--teal-surface:#47AB9D;--dark:#404140;--light:#B2AEAA;
  --sans:"Open Sans","Helvetica Neue",Helvetica,Arial,sans-serif;--serif:"Noto Serif KR","Playfair Display",serif}
*{box-sizing:border-box;margin:0;padding:0}
html{font-size:16px}
/* 배경 옅은 질감 — CSS 만(이미지 0 · master 7 · 거의 안 보일 정도): 원판은 wood-texture.png + 흰 85% */
body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.6;word-break:keep-all;overflow-wrap:break-word;
  background-image:repeating-linear-gradient(0deg,rgba(0,0,0,.018) 0 1px,transparent 1px 3px),repeating-linear-gradient(90deg,rgba(0,0,0,.012) 0 1px,transparent 1px 5px)}
a{color:inherit}img{display:block;max-width:100%;height:auto}
.wrap{width:min(1200px,calc(100% - 40px));margin:0 auto}
/* 맨 위 배너 — 왼쪽 정렬(master 1) · §7: .mo-9 12.8px 500 자간 .075em 흰 · 띠 .mo-4 padding 7px(바탕은 §1 검정 vs 선언 #404140 — master 답 전 §1) */
.banner{width:min(1200px,calc(100% - 40px));margin:14px auto 0;display:flex;justify-content:flex-start}
.banner span{display:inline-block;background:var(--dark);color:#fff;font-size:12.8px;font-weight:500;letter-spacing:.075em;line-height:1.2;padding:7px 16px;white-space:nowrap;overflow-x:auto;max-width:100%}  /* 바탕 #404140 띠 = master 판정(선언 .mo-4) · 모서리 선언 없음 */
/* 떠 있는 흰 카드 헤더 — §1: #FFF · radius 16px · shadow rgba(0,0,0,.2) 0 0 16px · padding 20px (§7 .mo-5 일치) */
.hd{position:sticky;top:12px;z-index:10;margin:16px auto 0;width:min(1200px,calc(100% - 40px));background:#FFF;border-radius:16px;box-shadow:rgba(0,0,0,.2) 0 0 16px;padding:20px;display:flex;align-items:center;gap:16px;flex-wrap:wrap;transition:box-shadow .2s ease,padding .2s ease}
.hd.is-stuck{box-shadow:rgba(0,0,0,.3) 0 4px 20px;padding:14px 20px}  /* A3 ② 스크롤 내리면 그림자 진해지고 살짝 줄어듦 */
.sentinel{height:1px}
.logo{font-family:var(--serif);font-weight:700;font-size:22px;text-decoration:none;letter-spacing:-.01em;margin-right:auto}
/* 메뉴 — §7 ①②: 12.8px · 400 · lh 1 · 자간 .1em · 안쪽 여백 .75em(12px) · 대문자화 없음(한글) · hover 청록 */
.nav{display:flex;gap:0;align-items:center}
.nav a{font-size:12.8px;font-weight:400;line-height:1;letter-spacing:.1em;padding:12px;text-decoration:none}
.nav a{transition:color .2s ease}
.nav a:hover{color:var(--teal-surface)}  /* .mo-1f hover #47ab9d (원판 선언 · 장식적 순간색) */
/* VISIT 자리 알약 = 「새가족 안내」 — §7: .9em(14.4px) · 600 · 자간 .075em · padding .575em 1.15em · 1px solid 청록 · radius 100em */
.pill{font-size:14.4px;font-weight:600;letter-spacing:.075em;padding:.575em 1.15em;border:1px solid var(--teal-surface);border-radius:100em;color:var(--teal-text);text-decoration:none;white-space:nowrap;margin-left:8px}
.pill:hover{background:var(--teal-surface);color:#fff}
/* 네모 테두리 햄버거 — 상시 표시(master 2) · 드로어(전체 메뉴) */
.tg{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);border:0}
.burger{display:block;width:44px;height:44px;position:relative;cursor:pointer;border:1px solid #000;border-radius:8px;margin-left:8px}
.burger span,.burger::before,.burger::after{content:"";position:absolute;left:12px;width:18px;height:2px;background:#000}
.burger::before{top:14px}.burger span{top:20px}.burger::after{top:26px}
.tg:focus-visible ~ .burger{outline:2px solid var(--teal-text);outline-offset:2px}
.drawer{display:none;flex-basis:100%;flex-direction:column;padding-top:12px;border-top:1px solid #eee}
.tg:checked ~ .drawer{display:flex}
.drawer a{padding:12px 0;border-bottom:1px solid #eee;text-decoration:none;font-size:15px}.drawer a:last-child{border:0}
/* 첫 화면 — §7 .mu-1: 위 calc(8rem+80px) 아래 calc(8rem+40px) · 왼쪽 영상 16:9 모서리 2em · 오른쪽 라벨→제목→버튼 둘(성구 줄 없음 · master 4) */
.hero{position:relative;padding:calc(8rem + 80px - 96px) 0 calc(8rem + 40px);overflow:hidden}
.hero .wrap{display:grid;grid-template-columns:7fr 5fr;gap:48px;align-items:center}
.media{position:relative;display:block;width:100%;padding-top:56.25%;height:0;overflow:hidden;border-radius:2em;background:#000;transition:transform .3s ease,box-shadow .3s ease}
.media:hover{transform:scale(1.02);box-shadow:rgba(0,0,0,.25) 0 12px 32px}  /* A3 ④ */
.media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.media::after{content:"";position:absolute;left:50%;top:50%;width:84px;height:84px;margin:-42px 0 0 -42px;border-radius:50%;background:rgba(255,255,255,.92)}
.media::before{content:"";position:absolute;left:50%;top:50%;z-index:1;margin:-13px 0 0 -9px;border-style:solid;border-width:13px 0 13px 24px;border-color:transparent transparent transparent #000}
.label{font-size:16px;font-weight:400;color:var(--teal-text)}
h1.title{font-family:var(--serif);font-weight:700;font-size:56px;line-height:61.6px;text-transform:lowercase;color:#000;margin-top:12px;letter-spacing:-.01em}
/* 버튼 — §1: 16px · radius 1600px · 투명 · 1px solid #000 · 글자 청록(§7 선언은 #000 — master 답 전 §1) · 자간 §7 .075em · 굵기 600 */
.btn{display:inline-block;margin-top:24px;padding:.575em 1.15em;font-size:16px;font-weight:600;letter-spacing:.075em;border-radius:1600px;background:transparent;border:1px solid #000;color:#000;text-decoration:none;transition:background .2s ease,color .2s ease}  /* 글자 #000 = master 판정(선언 .mu-2x) · hover .mu-2y */
.btn:hover{background:#000;color:#fff}
.more{display:inline-block;margin-left:18px;margin-top:24px;font-size:16px;font-weight:600;letter-spacing:.075em;color:var(--teal-text);text-decoration:none;border:0;transition:color .2s ease}
.more:hover{color:var(--dark)}  /* .mu-30 hover #404140 */
/* 물결 — §7 ⑥: 150px · 첫 구역 하단 · 연회색 · 곡선은 우리가 그림 */
.wave{position:absolute;left:0;right:0;bottom:-1px;width:100%;height:150px;display:block;fill:var(--light)}
/* 연회색 구역(master 6 · §7 ⑤: #b2aeaa + linear-gradient(to bottom,#b2aeaa 0% 2%,#b2aeaa8c) · padding 6rem) — 성구 줄이 여기로 옮겨짐(내용 손실 0) */
.light{background-color:var(--light);background-image:linear-gradient(to bottom,#b2aeaa 0% 2%,#b2aeaa8c);padding:6rem 0;color:#000}
.light .wrap{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
.light h2{font-family:var(--serif);font-weight:700;font-size:36px;line-height:1.25;text-transform:lowercase}
.light .verse{font-size:18px;line-height:1.7;margin-top:8px}
.light .wrap.light--verse{display:block;text-align:center}
.light--verse .verse{font-family:var(--serif);font-weight:700;font-size:clamp(26px,3.2vw,40px);line-height:1.4;margin:0 auto;max-width:24ch}  /* 성구 = 구역의 주인공(master 보강1) */
.light .muted{font-size:14px;margin-top:12px;color:#000}
/* 진회색 구역 — 다음 구역으로 내림(master 6) */
.dark{background:var(--dark);color:#fff;padding:6rem 0}
.dark .wrap{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
.dark h2{font-family:var(--serif);font-weight:700;font-size:36px;line-height:1.25;text-transform:lowercase}
.dark p{font-size:18px;line-height:1.7}
.dark .btn{border-color:#fff;color:#fff}.dark .btn:hover{background:#fff;color:var(--dark)}
/* A3 ① 스크롤 진입 등장 — 20px 아래서 .55s ease-out · 1회(JS IntersectionObserver 가 .in 부여 · JS 없으면 그냥 보임) */
.js .reveal{opacity:0;transform:translateY(20px);transition:opacity .55s ease-out,transform .55s ease-out}
.js .reveal.in{opacity:1;transform:none}
/* A3 ⑥ 움직임 줄이기 — 전부 끔 */
@media (prefers-reduced-motion: reduce){.js .reveal{opacity:1;transform:none;transition:none}.hd,.btn,.more,.nav a,.media{transition:none}.media:hover{transform:none}}
.ft{padding:28px 0 40px;font-size:13px;color:var(--dark);text-align:center}
.ft a{text-decoration:none}
@media(max-width:960px){.nav{display:none}.hero .wrap{grid-template-columns:1fr;gap:28px}h1.title{font-size:40px;line-height:1.15}.light .wrap,.dark .wrap{grid-template-columns:1fr}.hero{padding-top:56px}}
@media(max-width:640px){.pill{display:none}.hd{top:8px;padding:16px}.banner span{font-size:11px}}


/* ── 하위 8페이지: r4 본문 부품의 시더 스킨(c/c.css 도록 스킨을 시더 토큰으로 치환 · 마크업·문안은 r4 그대로) ── */
:root{--line:#E5E2DF}
.subhero{padding:56px 0 calc(6rem + 40px);position:relative;overflow:hidden}
.subhero .label{font-size:16px;color:var(--teal-text)}
.subhero h1.title{font-size:56px;line-height:61.6px}
.subhero .lead{font-size:18px;line-height:1.7;margin-top:16px;max-width:36ch;color:var(--dark)}
.body{background-color:var(--light);background-image:linear-gradient(to bottom,#b2aeaa 0% 2%,#b2aeaa8c);padding:3rem 0 4rem}
.body .section{background:#fff;border-radius:16px;box-shadow:rgba(0,0,0,.2) 0 0 16px;margin:0 auto 24px;width:min(1200px,calc(100% - 40px));border:0;padding:clamp(28px,4vw,48px)}
.body .section--tint{background:#fff}
.body .title{font-family:var(--serif);font-weight:700;color:#000}
.body .eyebrow{color:var(--teal-text);letter-spacing:.1em;font-size:12.8px;font-weight:600}
.body .btn{margin-top:12px}
.body .cols .go,.body .text-link{color:var(--teal-text);border-color:var(--line);transition:color .2s ease}
.body .cols .go:hover,.body .text-link:hover{color:var(--dark)}
.body .num{color:var(--dark)}
.body .btn--primary{background:#000;color:#fff;border-color:#000}.body .btn--primary:hover{background:#fff;color:#000}
/* ── r4 본문 부품의 도록 스킨 (마크업·문안은 r4 검증분 그대로 · 여기서는 보기만 바꾼다) ── */
.section{padding:clamp(30px,5vh,64px) 20px;border-bottom:1px solid var(--line)}

.wrap{max-width:1180px;margin:0 auto}
.eyebrow{display:block;font-family:var(--sans);font-size:12.5px;letter-spacing:.14em;font-weight:500;color:var(--dark);margin-bottom:14px}
.title{font-family:var(--serif);font-weight:400;font-size:clamp(22px,2.6vw,32px);line-height:1.35;letter-spacing:-.02em;color:var(--ink);max-width:22ch}
.title--display{font-size:clamp(25px,3.1vw,40px)}
.lead{font-size:16px;line-height:1.75;color:var(--ink);max-width:36ch}
.note{font-size:13px;color:var(--dark);line-height:1.7}
.head{margin-bottom:28px}
.head .lead{margin-top:12px}
p{max-width:60ch}

.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(18px,3vw,40px)}
.cols>*{border-top:1px solid var(--line);padding-top:14px;min-width:0}
.num{display:block;font-family:var(--serif);font-size:12.5px;letter-spacing:.12em;color:var(--dark);margin-bottom:12px}
.cols h3{font-family:var(--serif);font-size:19px;line-height:1.4;margin-bottom:8px}
.cols .big{display:block;font-family:var(--serif);font-size:clamp(22px,2.4vw,30px);line-height:1.2;color:var(--ink);letter-spacing:-.02em;margin-bottom:8px}
.cols p{font-size:13.5px;color:var(--dark)}
.cols .go,.text-link{display:inline-block;margin-top:12px;font-size:13.5px;color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line);padding-bottom:2px}
.cols .go:hover,.text-link:hover{border-color:var(--ink)}
.empty-line{display:none}
.rule{display:flex;align-items:center;gap:14px;margin-top:28px;font-family:var(--serif);font-size:19px;color:var(--ink)}
.rule::before{content:"";width:64px;height:1px;background:var(--ink);flex:0 0 auto}

.two{display:grid;grid-template-columns:5fr 7fr;gap:clamp(18px,3vw,40px);align-items:start}
.two>*{min-width:0}
.two--photo{grid-template-columns:4fr 8fr;align-items:center}
.prose{display:grid;gap:14px}
.prose p{line-height:1.85}
.rows{border-top:1px solid var(--line)}
.row{display:grid;grid-template-columns:3.5em 1fr;gap:14px;padding:16px 0;border-bottom:1px solid var(--line);align-items:baseline}
.row .num{margin:0}
.row h3{font-family:var(--serif);font-size:18px;margin-bottom:6px}
.row p{font-size:13.5px;color:var(--dark);max-width:52ch}
.row .note a{color:var(--ink)}
.row .actions{margin-top:10px}

.photo{position:relative;overflow:hidden;border:1px solid var(--line)}
.photo img{width:100%;height:100%;object-fit:cover;filter:none}
.photo--43{aspect-ratio:4/3}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.tiles>*{min-width:0}
.tiles .photo{aspect-ratio:4/3}
.feature{display:grid;grid-template-columns:1fr 1fr;gap:clamp(18px,3vw,40px);align-items:center}
.feature>*{min-width:0}
.media{position:relative;display:block;aspect-ratio:16/9;overflow:hidden;border:1px solid var(--line)}
.media img{width:100%;height:100%;object-fit:cover;filter:none}
.feature .meta{margin-top:12px;font-size:13.5px;color:var(--dark);border:0;padding:0}

.reading{display:grid;grid-template-columns:5fr 7fr;gap:clamp(18px,3vw,40px);align-items:start;margin-top:28px;padding-top:28px;border-top:1px solid var(--line)}
.reading>*{min-width:0}
.reading h3{font-family:var(--serif);font-size:clamp(20px,2.2vw,26px)}
.reading__now{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:10px}
.reading__now>div{border-top:1px solid var(--line);padding-top:10px}
.reading__now span{display:block;font-size:12.5px;letter-spacing:.12em;color:var(--dark);margin-bottom:6px}
.reading__now b{font-family:var(--serif);font-weight:500;font-size:clamp(22px,2.4vw,30px);color:var(--ink);letter-spacing:-.02em}
.reading__nav{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:18px}
.reading__nav button{background:transparent;border:1px solid var(--line);color:var(--ink);padding:9px 16px;border-radius:9999px;font-size:13.5px}
.reading__nav button:hover{border-color:var(--ink)}
.reading__nav span{font-size:13.5px;color:var(--dark);letter-spacing:.06em}
.reading__links{margin-top:18px;display:flex;gap:16px;flex-wrap:wrap}

.address{font-family:var(--serif);font-size:clamp(20px,2.2vw,26px);line-height:1.4;color:var(--ink);max-width:22ch}
.phone{display:inline-block;font-size:16px;margin-top:12px;color:var(--ink)}

/* ── 재정 잠금 카드(시안E 원본 마크업 · 로직 불변) — 공통 머리/꼬리 안 본문 자리 ── */
.lock{min-height:52vh;display:flex;align-items:center}
.lock .card{margin:0 auto;max-width:340px;width:100%;text-align:center;border:1px solid var(--line);padding:28px 24px}
.lock h1{font-family:var(--serif);font-weight:500;font-size:22px;margin-bottom:8px}
.lock p{color:var(--dark);font-size:14px;margin:0 auto 18px}
.lock input{width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:0;font-size:16px;font-family:var(--sans);background:#fff;color:var(--ink)}
.lock button{margin-top:10px;width:100%;padding:11px;border:1px solid var(--ink);border-radius:9999px;background:var(--ink);color:#fff;font-size:16px;font-family:var(--sans)}
.lock #err{color:var(--ink);font-size:13px;min-height:1.2em;margin-top:8px}
.lock a{display:inline-block;margin-top:14px;font-size:13px;text-decoration:none;border-bottom:1px solid var(--line)}


/* 하위 페이지 반응형 — c/c.css 의 반응형 규칙(도록 스킨 블록 밖에 있어 처음 복사에서 빠짐 · 2026-09-30 주보 390 캡처에서 3열 유지로 낱말 중간 끊김 실측) */
@media(max-width:960px){.body .two,.body .two--photo,.body .reading,.body .feature{grid-template-columns:1fr}}
@media(max-width:640px){.body .cols{grid-template-columns:1fr}.body .cols--4{grid-template-columns:1fr}.body .tiles{grid-template-columns:repeat(2,1fr)}.body .reading__now{grid-template-columns:1fr}.body .times .row{grid-template-columns:1fr}.body .section{padding:24px 18px}.subhero h1.title{font-size:40px;line-height:1.15}}
</style>'''

A3JS = r'''// A3 — 라이브러리 0 · IntersectionObserver 하나: ①구역 등장(1회) ②헤더 카드 스크롤 반응(센티널 이탈) · reduced-motion 이면 아무것도 안 함
(function(){if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches)return;document.documentElement.classList.add('js');
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.target.id==='top-sentinel'){document.querySelector('.hd').classList.toggle('is-stuck',!e.isIntersecting);return;}if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:0.12});
document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});io.observe(document.getElementById('top-sentinel'));})();'''

# ── 하위 8페이지 — 본문은 r4 <main> 섹션을 그대로 이식(창작 0·누락 0 · c/_build.py 와 같은 방식) · 머리·첫 화면·꼬리만 시더 틀 · 홈 토큰 공유(master 2026-09-30) ──
import re as _re
R4 = PREVIEW / "r4"

def repath(frag):
    frag = _re.sub(r'(src|href|srcset)=(["\'])\.\./', r'\1=\2../../../', frag)
    frag = frag.replace("'../", "'../../../").replace('"../"', '"../../../"')
    frag = _re.sub(r'(src|href|srcset)=(["\'])사진/', r'\1=\2../../사진/', frag)
    return frag

def read_r4(page):
    raw = (R4 / f"{page}.html").read_text(encoding="utf-8")
    title = _re.search(r"<title>(.*?)</title>", raw, _re.S).group(1).strip()
    main = _re.search(r"<main.*?</main>", raw, _re.S).group(0)
    scripts = _re.findall(r"<script>.*?</script>", raw[raw.index("</main>"):], _re.S)
    return title, main, scripts

# r4 페이지 머리의 페이지 전용 <style>(영상 임베드 16:9 · 4열 그리드 · 시간표 행 등) — 본문 부품이 기대하는 규칙이라 같이 옮긴다(2026-09-30 예배안내 390 넘침 실측: iframe 폭 고정이 원인).
# r4 토큰 이름은 시더 토큰으로 매핑 · page-top(첫 화면 여백)은 subhero 가 대신하므로 제외
R4_TOKEN_MAP = {"var(--radius-media)": "16px", "var(--line-light)": "var(--line)", "var(--line)": "var(--line)", "var(--surface-tint)": "#fff",
                "var(--s-3)": "16px", "var(--s-6)": "40px", "var(--s-2)": "12px", "var(--s-4)": "24px", "var(--muted)": "var(--dark)", "var(--ink)": "#000",
                "var(--accent)": "var(--teal-text)", "var(--text-body-sm)": "14px", "var(--font-serif)": "var(--serif)", "var(--gap-md)": "24px", "var(--gap-sm)": "16px",
                "var(--fs-3)": "clamp(22px,2.4vw,30px)", "var(--text-h2)": "19px", "var(--tracking-tight)": "-.02em", "var(--lh-body)": "1.6", "var(--text-caption)": "12.8px", "var(--tracking-wide)": ".1em", "var(--s-8)": "56px", "var(--text-h1)": "clamp(22px,2.6vw,32px)", "var(--s-5)": "32px", "var(--s-1)": "8px"}
def page_css(page):
    raw = (R4 / f"{page}.html").read_text(encoding="utf-8"); head = raw[:raw.find("<body")]
    css = " ".join(_re.findall(r"<style[^>]*>(.*?)</style>", head, _re.S))
    css = _re.sub(r"@layer pages\s*\{(.*)\}\s*$", r"\1", css.strip(), flags=_re.S)   # 레이어 껍질 제거(시더 CSS 는 레이어 없음)
    css = _re.sub(r"\.page-top\{[^}]*\}", "", css); css = _re.sub(r"@media\([^)]*\)\{\s*\.page-top\{[^}]*\}\s*\}", "", css)
    for k, v in R4_TOKEN_MAP.items(): css = css.replace(k, v)
    left = [x for x in _re.findall(r"var\(--[a-z0-9-]+\)", css) if x not in ("var(--serif)","var(--sans)","var(--line)","var(--teal-text)","var(--dark)","var(--light)")]
    assert not left, f"{page}: 시더 토큰에 없는 r4 변수 {sorted(set(left))} — R4_TOKEN_MAP 에 추가"
    return "<style>/* r4/" + page + ".html 페이지 전용 규칙(토큰 매핑) */" + css + "</style>"

def sections(main, drop=()):
    out = []
    for m in _re.finditer(r"(?:<!--[^\n]*?-->\s*)*<section\b[^>]*data-block=\"([^\"]+)\"[^>]*>.*?</section>", main, _re.S):
        if m.group(1) in drop: continue
        out.append(m.group(0))
    return out

def page_head(main):
    m = _re.search(r'<section class="section page-top"[^>]*data-block="page-head".*?</section>', main, _re.S).group(0)
    eyebrow = _re.search(r'<span class="eyebrow">(.*?)</span>', m, _re.S).group(1).strip()
    h1 = _re.search(r"<h1[^>]*>(.*?)</h1>", m, _re.S).group(1).strip()
    lead = _re.search(r'<p class="lead"[^>]*>(.*?)</p>', m, _re.S)
    return eyebrow, h1, (lead.group(1).strip() if lead else "")

# 홈 안내 구역 — r4/index.html 의 섹션을 그대로 이식(master 보강2 · 창작 0). 순서 고정.
# 뺀 것: hero·times(첫 화면이 대신) · latest-sermon(첫 화면과 중복) · gallery(성도 사진 — 앞선 판정) · location(진회색 오시는 길 구역이 대신) · footer
# pillars(세 기둥)는 r4 그대로(제목 3 · 빈 줄은 r4 규칙대로 숨김 · 오너 글이 오면 r4 에서 채움)
HOME_KEEP = ["pillars", "intro", "worship", "today", "sermons", "visitors"]
def home_guide():
    _, main, scripts = read_r4("index")
    blocks = {}
    for m in _re.finditer(r"(?:<!--[^\n]*?-->\s*)*<section\b[^>]*data-block=\"([^\"]+)\"[^>]*>.*?</section>", main, _re.S):
        blocks[m.group(1)] = m.group(0)
    body = "\n".join(repath(blocks[k]) for k in HOME_KEEP)
    body = _re.sub(r'<section\b([^>]*?)class="', r'<section\1class="reveal ', body)   # id 가 class 앞에 오는 태그도 처리(첫 판에서 class 중복 생성 실측)
    iife = next(s for s in scripts if "오늘회차" in s)
    iife = _re.search(r"\(function\(\)\{.*?\}\)\(\);", iife, _re.S).group(0)
    return '<section class="body">\n' + body + '\n</section>\n', repath(iife)

page = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{esc(SITE["church"])}</title>
<!-- T-HOME-CEDAR · 생성: r4/drafts/cedar/_build.py — 손으로 고치지 말 것. 규격=master 실측(cedarcrestchurch.com computed style 2026-09-30) · 내용=site.json·latest.json -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500;600&family=Noto+Serif+KR:wght@700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
__CSS__
</head>
<body>
<div class="sentinel" id="top-sentinel"></div>
<div class="banner"><span>{times}</span></div>
<header class="hd">
  <a class="logo" href="index.html">{esc(SITE["church"])}</a>
  <input type="checkbox" id="tg" class="tg" aria-label="메뉴" aria-controls="drawer">
  <nav id="site-nav" class="nav" aria-label="주 메뉴">{nav}</nav>
  <a class="pill" href="../c/새가족.html">새가족 안내</a>
  <label for="tg" class="burger" aria-hidden="true"><span></span></label>
  <nav id="drawer" class="drawer" aria-label="전체 메뉴">{nav}</nav>
</header>
<main>
<section class="hero"><div class="wrap reveal">
  <a class="media" id="sm-thumb" href="{esc(LATEST["설교_링크"])}" target="_blank" rel="noopener" aria-label="설교 영상 보기"><img id="sm-thumb-img" src="https://i.ytimg.com/vi/{esc(vid)}/hqdefault.jpg" alt="" loading="eager"></a>
  <div>
    <p class="label" id="sm-label">{esc(label)}</p>
    <h1 class="title" id="sm-title">{esc(LATEST["설교_제목"])}</h1>
    <a class="btn" id="sm-link" href="{esc(LATEST["설교_링크"])}" target="_blank" rel="noopener">설교 영상 보기</a><a class="more" href="../c/온라인예배.html">지난 설교</a>
  </div>
</div>
{WAVE}</section>
<section class="light"><div class="wrap reveal light--verse">
  <p class="verse" id="sm-verse">{esc(verse.strip())}</p>
</div></section>
__HOME_GUIDE__
<section class="dark"><div class="wrap reveal">
  <div><h2>오시는 길</h2><p class="muted">{esc(SITE["church_full"])}</p></div>
  <div><p>{esc(SITE["address"])}<br><a href="tel:{esc(SITE["phone"])}">{esc(SITE["phone"])}</a></p>
    <a class="btn" href="https://map.kakao.com/link/search/경기%20광명시%20기아로%2023" target="_blank" rel="noopener">오시는 길 ↗</a></div>
</div></section>
</main>
<footer class="ft"><span>{esc(SITE["copyright"])}</span> · <span>T-HOME-CEDAR 비교 초안 · 내부 검토용</span></footer>
<script>
__A3JS__
var LATEST_URL={json.dumps(SITE["latest_url"])};
if(location.protocol!=='file:')fetch(LATEST_URL,{{cache:'no-store'}}).then(function(r){{if(!r.ok)throw Error();return r.json()}}).then(function(d){{
  if(d.설교_제목&&d.설교_날짜&&/^https:\\/\\/www.youtube.com\\/watch\\?v=/.test(d.설교_링크)){{
    var p=d.설교_날짜.split('·'),ymd=p[0].trim().split('-');
    document.getElementById('sm-title').textContent=d.설교_제목;
    document.getElementById('sm-label').textContent='이번 주일 · '+parseInt(ymd[1],10)+'월 '+parseInt(ymd[2],10)+'일';
    document.getElementById('sm-verse').textContent=(p[1]||'').trim();
    ['sm-link','sm-thumb'].forEach(function(id){{document.getElementById(id).href=d.설교_링크}});
    var st=document.getElementById('sermon-title'),sd=document.getElementById('sermon-date'),sl=document.getElementById('sermon-link');if(st)st.textContent=d.설교_제목;if(sd){{sd.textContent=d.설교_날짜;sd.dateTime=d.설교_날짜.slice(0,10);}}if(sl)sl.href=d.설교_링크;
    var v=d.설교_링크.split('v=')[1].split('&')[0];document.getElementById('sm-thumb-img').src='https://i.ytimg.com/vi/'+v+'/hqdefault.jpg';
  }}
  var jt=document.getElementById('jb-title'),jl=document.getElementById('jb-link');if(d.주보_제목&&jt)jt.textContent=d.주보_제목;if(d.주보_링크&&jl)jl.href='../../../'+d.주보_링크;
}}).catch(function(){{}});
__TONGDOK__
</script>
</body>
</html>
'''
_guide, _iife = home_guide()
page = page.replace('__CSS__', CSS).replace('__A3JS__', A3JS).replace('__HOME_GUIDE__', _guide).replace('__TONGDOK__', _iife)
(D / "index.html").write_text(page, encoding="utf-8")
print("cedar/index.html", len(page), "B")


# 홈 page 문자열에서 공통 조각을 잘라 쓴다(같은 문자열 → 9페이지 한 몸)
_head_html = page[:page.index("<body>")]                                   # <!DOCTYPE …</head>
_banner_header = page[page.index("<body>")+len("<body>"):page.index("<main>")]  # 센티널·배너·헤더 카드
_dark_footer = page[page.index('<section class="dark">'):page.index("<script>")]  # 진회색 오시는 길 + 꼬리
_a3 = A3JS



SUBPAGES = ["교회소개", "예배안내", "새가족", "아카데미", "온라인예배", "재정", "주보", "칼럼"]

def build_sub(pg, n):
    if pg == "재정":
        raw = (R4 / "재정.html").read_text(encoding="utf-8")
        title = _re.search(r"<title>(.*?)</title>", raw, _re.S).group(1).strip()
        card = _re.search(r'<div class="card">.*?</div>\s*(?=<script>)', raw, _re.S).group(0).strip()
        script = _re.search(r"<script>.*?</script>", raw, _re.S).group(0)
        assert 'id="pw"' in card and "SALT=" in script
        body_html = f'<main>\n<section class="subhero"><div class="wrap reveal"><p class="label">No. {n:02d}</p><h1 class="title">교회 재정</h1></div>{WAVE}</section>\n<section class="body"><div class="section lock reveal">{card}</div></section>\n</main>\n{script}\n'
    else:
        title, main, scripts = read_r4(pg)
        eyebrow, h1, lead = page_head(main)
        body = repath("\n".join(sections(main, drop=("page-head",))))
        body = _re.sub(r'<section\b([^>]*?)class="', r'<section\1class="reveal ', body)
        body_html = (f'<main>\n<section class="subhero"><div class="wrap reveal"><p class="label">{eyebrow}</p><h1 class="title">{h1}</h1>'
                     + (f'<p class="lead">{lead}</p>' if lead else "") + f'</div>{WAVE}</section>\n<section class="body">\n{body}\n</section>\n</main>\n'
                     + "".join(repath(s) + "\n" for s in scripts))
    html_out = _head_html.replace(f"<title>{esc(SITE['church'])}</title>", f"<title>{esc(title)}</title>", 1)
    if pg != "재정": html_out = html_out.replace("</head>", page_css(pg) + "\n</head>", 1)
    html_out += "<body>" + _banner_header + body_html + _dark_footer + "<script>\n" + _a3 + "\n</script>\n</body>\n</html>\n"
    return html_out

if "--sub" in __import__("sys").argv:
    for i, pg in enumerate(SUBPAGES, 2):
        out = build_sub(pg, i)
        (D / f"{pg}.html").write_text(out, encoding="utf-8")
        print(f"cedar/{pg}.html {len(out):,}B")
