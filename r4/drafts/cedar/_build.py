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
WAVE = '<svg class="wave" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0,40 C240,80 480,0 720,40 C960,80 1200,0 1440,40 L1440,80 L0,80 Z"/></svg>'

CSS = r'''<style>
/* 규격(master 실측 · 그대로): 배경 #FFF · 본문 Open Sans/Helvetica Neue · 제목 56px/61.6px 700 lowercase #000 · 라벨 16px #47AB9D · 버튼 16px radius 1600px 1px solid #000 글자 #47AB9D
   · 헤더 흰 카드 radius 16px shadow rgba(0,0,0,.2) 0 0 16px padding 20px · 배너 12.8px 500 흰 글자 검은 알약 · 섹션 #404140/#B2AEAA/#47AB9D · 물결 SVG 1
   제목 글꼴: Poynter(상용) 대체 → 한글 Noto Serif KR 700 · 영문 Playfair Display 700(Poynter 의 굵은 세리프·높은 대비에 Lora 보다 가까움)
   ★대비 실측(WCAG): #47AB9D on #FFF = 2.77:1 — AA 4.5 미달·큰 글자 3:1 도 미달. 규격대로 두되 보고함. 대안 참고: #2A7D71 4.92 · #25705F 5.9 */
:root{--bg:#FFFFFF;--ink:#000;--teal:#47AB9D;--dark:#404140;--light:#B2AEAA;
  --sans:"Open Sans","Helvetica Neue",Helvetica,Arial,sans-serif;--serif:"Noto Serif KR","Playfair Display",serif}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.6;word-break:keep-all;overflow-wrap:break-word}
a{color:inherit}img{display:block;max-width:100%;height:auto}
.wrap{width:min(1200px,calc(100% - 40px));margin:0 auto}
/* 맨 위 배너 — 검은 알약 · 12.8px 500 흰 글자 */
.banner{display:flex;justify-content:center;padding:14px 20px 0}
.banner span{display:inline-block;background:#000;color:#fff;font-size:12.8px;font-weight:500;letter-spacing:.02em;padding:6px 16px;border-radius:1600px;white-space:nowrap;overflow-x:auto;max-width:100%}
/* 떠 있는 흰 카드 헤더 */
.hd{position:sticky;top:12px;z-index:10;margin:16px auto 0;width:min(1200px,calc(100% - 40px));background:#FFF;border-radius:16px;box-shadow:rgba(0,0,0,.2) 0 0 16px;padding:20px;display:flex;align-items:center;gap:24px;flex-wrap:wrap}
.logo{font-family:var(--serif);font-weight:700;font-size:22px;text-decoration:none;letter-spacing:-.01em}
.nav{display:flex;gap:22px;margin-left:auto;font-size:15px;font-weight:500}
.nav a{text-decoration:none}.nav a:hover{color:var(--teal)}
.tg{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);border:0}
.burger{display:none;margin-left:auto;width:44px;height:44px;position:relative;cursor:pointer}
.burger span,.burger::before,.burger::after{content:"";position:absolute;left:12px;width:20px;height:2px;background:#000}
.burger::before{top:15px}.burger span{top:21px}.burger::after{top:27px}
/* 첫 화면 — 왼쪽 큰 영상 · 오른쪽 라벨→제목→버튼→링크 */
.hero{padding:48px 0 0}
.hero .wrap{display:grid;grid-template-columns:7fr 5fr;gap:48px;align-items:center}
.media{position:relative;display:block;aspect-ratio:16/9;overflow:hidden;border-radius:16px;background:#000}
.media img{width:100%;height:100%;object-fit:cover}
.media::after{content:"";position:absolute;left:50%;top:50%;width:84px;height:84px;margin:-42px 0 0 -42px;border-radius:50%;background:rgba(255,255,255,.92)}
.media::before{content:"";position:absolute;left:50%;top:50%;z-index:1;margin:-13px 0 0 -9px;border-style:solid;border-width:13px 0 13px 24px;border-color:transparent transparent transparent #000}
.label{font-size:16px;font-weight:400;color:var(--teal)}
h1.title{font-family:var(--serif);font-weight:700;font-size:56px;line-height:61.6px;text-transform:lowercase;color:#000;margin-top:12px;letter-spacing:-.01em}
.verse{margin-top:14px;font-size:16px;color:var(--dark)}
.btn{display:inline-block;margin-top:24px;padding:12px 28px;font-size:16px;border-radius:1600px;background:transparent;border:1px solid #000;color:var(--teal);text-decoration:none}
.btn:hover{background:#000;color:#fff}
.more{display:inline-block;margin-left:18px;margin-top:24px;font-size:16px;color:var(--teal);text-decoration:none;border:0}
/* 물결 → 진회색 구역 */
.wave{display:block;width:100%;height:80px;margin-top:56px;fill:var(--dark)}
.dark{background:var(--dark);color:#fff;padding:56px 0 64px}
.dark .wrap{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
.dark h2{font-family:var(--serif);font-weight:700;font-size:36px;line-height:1.25;text-transform:lowercase}
.dark p{font-size:18px;line-height:1.7}
.dark .btn{border-color:#fff;color:#fff}.dark .btn:hover{background:#fff;color:var(--dark)}
.dark .muted{color:var(--light);font-size:14px;margin-top:12px}
.ft{padding:28px 0 40px;font-size:13px;color:var(--dark);text-align:center}
.ft a{text-decoration:none}
@media(max-width:900px){.hero .wrap{grid-template-columns:1fr;gap:28px}h1.title{font-size:40px;line-height:1.15}.dark .wrap{grid-template-columns:1fr}}
@media(max-width:640px){.burger{display:block}.nav{display:none;flex-basis:100%;flex-direction:column;gap:0;padding-top:12px;border-top:1px solid #eee}
  .tg:checked ~ .nav{display:flex}.nav a{padding:12px 0;border-bottom:1px solid #eee}.nav a:last-child{border:0}.hd{top:8px;padding:16px}}
</style>'''

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
<div class="banner"><span>{times}</span></div>
<header class="hd">
  <a class="logo" href="index.html">{esc(SITE["church"])}</a>
  <input type="checkbox" id="tg" class="tg" aria-label="메뉴" aria-controls="site-nav">
  <label for="tg" class="burger" aria-hidden="true"><span></span></label>
  <nav id="site-nav" class="nav" aria-label="주 메뉴">{nav}</nav>
</header>
<main>
<section class="hero"><div class="wrap">
  <a class="media" id="sm-thumb" href="{esc(LATEST["설교_링크"])}" target="_blank" rel="noopener" aria-label="설교 영상 보기"><img id="sm-thumb-img" src="https://i.ytimg.com/vi/{esc(vid)}/hqdefault.jpg" alt="" loading="eager"></a>
  <div>
    <p class="label" id="sm-label">{esc(label)}</p>
    <h1 class="title" id="sm-title">{esc(LATEST["설교_제목"])}</h1>
    <p class="verse" id="sm-verse">{esc(verse.strip())}</p>
    <a class="btn" id="sm-link" href="{esc(LATEST["설교_링크"])}" target="_blank" rel="noopener">설교 영상 보기</a><a class="more" href="../c/온라인예배.html">지난 설교</a>
  </div>
</div></section>
{WAVE}
<section class="dark"><div class="wrap">
  <div><h2>오시는 길</h2><p class="muted">{esc(SITE["church_full"])}</p></div>
  <div><p>{esc(SITE["address"])}<br><a href="tel:{esc(SITE["phone"])}">{esc(SITE["phone"])}</a></p>
    <a class="btn" href="https://map.kakao.com/link/search/경기%20광명시%20기아로%2023" target="_blank" rel="noopener">오시는 길 ↗</a></div>
</div></section>
</main>
<footer class="ft"><span>{esc(SITE["copyright"])}</span> · <span>T-HOME-CEDAR 비교 초안 · 내부 검토용</span></footer>
<script>
var LATEST_URL={json.dumps(SITE["latest_url"])};
if(location.protocol!=='file:')fetch(LATEST_URL,{{cache:'no-store'}}).then(function(r){{if(!r.ok)throw Error();return r.json()}}).then(function(d){{
  if(d.설교_제목&&d.설교_날짜&&/^https:\\/\\/www.youtube.com\\/watch\\?v=/.test(d.설교_링크)){{
    var p=d.설교_날짜.split('·'),ymd=p[0].trim().split('-');
    document.getElementById('sm-title').textContent=d.설교_제목;
    document.getElementById('sm-label').textContent='이번 주일 · '+parseInt(ymd[1],10)+'월 '+parseInt(ymd[2],10)+'일';
    document.getElementById('sm-verse').textContent=(p[1]||'').trim();
    ['sm-link','sm-thumb'].forEach(function(id){{document.getElementById(id).href=d.설교_링크}});
    var v=d.설교_링크.split('v=')[1].split('&')[0];document.getElementById('sm-thumb-img').src='https://i.ytimg.com/vi/'+v+'/hqdefault.jpg';
  }}
}}).catch(function(){{}});
</script>
</body>
</html>
'''
page = page.replace('__CSS__', CSS)
(D / "index.html").write_text(page, encoding="utf-8")
print("cedar/index.html", len(page), "B")
