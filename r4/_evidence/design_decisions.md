# R4 디자인 결정 기록 — 채택 / 보류 (근거 URL 동반)

작성: worker(surface:39) · 2026-09-29 · 대상: r4/assets/tokens.css · r4/assets/r4.css · r4/index.html
우선순위(master 지시): ①조사/02_프리미엄_벤치마크_20260929.md §5 토큰·사진 배치·섹션 순서 → ②master 기준 격상 8항 → 충돌 시 벤치마크 실측 우선.
불변: 색 계열=남색·청록 계승+금색 포인트 1색 · 문안=시안E_*.html·latest.json·jubo_*.html·실문구 대장만(벤치마크 §5(5) 와이어프레임 문안은 제미나이 예시 — 한 글자도 미사용).

## 1. 채택 (벤치마크 §5 → 토큰)

| 항목 | 벤치마크 값(§5) | R4 토큰 | 근거 URL |
|---|---|---|---|
| 바탕/표면 명도 비례 | paper #F8F7F3(L97)·surface #FFFEFB·surface-sub #F0EEE6(L93) | --p-paper-050 #F6F8F8 · --p-paper-000 #FCFDFD · --p-tint-100 #EBF1F2 (같은 명도, 남색·청록 계열) | https://hcbc.kr/ (--paper #f8f7f3 실측) · https://wrightsferrymansion.org (#eeece8) |
| 글자 3단(ink/body/muted) | #1E211E · #383D37 · #6B7068 | --p-ink-900 #1A2429 · --p-ink-700 #33414A · --p-ink-500 #5D6A71(대비 실측 후 조정: tint 위 4.5:1) | https://hcbc.kr/ (--ink #20231f·--muted #666a63) |
| 1px 선 2단 | #DAD7CD · #E8E6DF | --p-line-200 #D9DFE1 · --p-line-100 #E7ECED | https://hcbc.kr/ (--line #d9d8d1) |
| 악센트 채도·명도 비례 | --color-accent #364336 (L25·저채도 올리브) | --p-navy-700 #1B3A47(제목) · --p-teal-600 #2A5D69(링크·버튼) — 계열만 남색·청록으로 | https://hcbc.kr/ (--accent #39463b) · https://passioncitychurch.com (#32373c) |
| 금색 포인트 1색 | --color-accent-gold #9C835A | --p-gold-500 #9C835A 그대로 (넘버링·아이브로우 선 전용, 소형 본문 금지) | 벤치마크 §4-6 앤틱 골드 |
| 유동 타이포 clamp | display clamp(2.2rem,5.5vw,4.2rem) · h1 clamp(1.75rem,3.2vw,2.75rem) · h2 clamp(1.35rem,2.2vw,1.85rem) · h3 1.15rem · body 1rem · sm .875rem · caption .75rem | --text-display/--text-h1/--text-h2/--text-h3/--text-body/--text-body-sm/--text-caption 동일값 | https://hcbc.kr/ (clamp(2.4rem,7vw,5.6rem)) · https://wrightsferrymansion.org (clamp 8단계) |
| 행간·자간 | 1.22/1.35/1.68/1.85 · -0.025em/0/0.08em | --lh-tight/--lh-heading/--lh-body/--lh-loose · --tracking-tight/normal/wide 동일값 | https://forourclimate.org (본문 1.65) · https://hcbc.kr/ (제목 1.25~1.34·본문 1.55~1.6) |
| 컨테이너·거터 | 1160px · 760px · clamp(16px,4vw,32px) | --wrap 1160 · --wrap-narrow 760 · --gutter 동일 | https://hcbc.kr/ (--content 1180px) · https://saddleback.com (1200) |
| 섹션 상하 여백 | clamp(56px,8vh,96px) | --section-y 동일값 (**master ② 120/72 보류** — 충돌 시 벤치마크 우선 지시에 따름. 되돌리려면 토큰 1줄: clamp(4.5rem,9.5vw,8rem)) | https://www.obama.org (64~128) · https://passioncitychurch.com (80) |
| 모서리 | 2px 카드 · 4px 버튼 · 9999px 알약 CTA | --radius-sm/md/pill 동일 · 알약=히어로 링크·온라인 예배·오픈채팅·GNB 새가족 안내 | https://www.awwwards.com/sites/passion-city-church · https://hcbc.kr/ (radius 0) |
| 카드 그림자 | --box-shadow-subtle 0 4px 20px rgba(30,33,30,.04) | --shadow-subtle 정의만, **카드 미사용**(master ⑧ 얇은 선·큰 여백 + 벤치마크 §4-6 1px 디바이더가 같은 결론) | https://hcbc.kr/ |
| 사진 톤다운 | filter saturate(0.85) contrast(0.95) | --photo-filter 동일 (히어로·섹션 사진 전부) | 벤치마크 §5(4)-1 |
| 섹션 순서 | 히어로 → 비전·핵심가치 3칼럼 → 예배·모임(+알약 CTA) → 2단 사진·소개 → 처음 오신 분 3단계 → 오시는 길·연락 → 푸터 | 홈: 히어로 → 세 기둥(표어) → 예배 시간표(+온라인 예배 알약) → 교회소개 2단 → 이번 주(카드+통독) → 최근 설교 → 처음 오신 분 3단계(새가족 4항) → 오시는 길+문의 → 푸터 3열 | 벤치마크 §5(5) · https://hcbc.kr/ (3칼럼 핵심가치) |
| GNB 우측 알약 CTA | [처음 오신 분] | "새가족 안내"(시안E_새가족.html 제목) → 새가족.html | 벤치마크 §3(4) Passion City |
| 3단계 스테퍼 | 1·2·3단계 카드 | 새가족 4항 중 3문항(언제/어디로/물어볼 것)에 01·02·03 넘버링 — 문안은 시안E_새가족.html 그대로 | 벤치마크 §5(5) SECTION 5 |
| 모션 | transition .2~.25s · 정적 우선 | --dur-fast 250ms · 스크롤 등장 페이드 1종(CSS animation-timeline: view(), 미지원=정적) | https://hcbc.kr/ · master ⑥ |

## 2. 보류 (근거와 이유)

| 항목 | 벤치마크 제안 | 보류 이유 |
|---|---|---|
| 올리브/세이지·린넨 웜톤 팔레트 | #364336·#F8F7F3 등 | master 불변 조건: 남색·청록 계승. 명도·채도 비례만 이식(위 표). |
| Nanum Brush Script 캘리 성구 | --font-script | 성구 문안이 원천 자료에 없음(창작 0) + 폰트 링크는 시안R3_B 와 동일 2종만(범위 조건). |
| 히어로 페이퍼 틴트 오버레이(밝은 배경+어두운 글자) | 어두운 오버레이 대신 --color-paper 틴트 | 보유 히어로 사진(hero.jpg 실내 단체사진)은 hcbc 의 질감 벽면과 달리 밀도가 높아 밝은 틴트+어두운 글자로는 가독 확보 불가. master ③ 어두운 그라데이션 유지 + 벤치마크 톤다운 필터 병용. |
| 섹션 여백 master ② 120px/72px | — | 벤치마크 clamp(56px,8vh,96px) 채택(충돌 시 벤치마크 우선). 토큰 1줄로 복귀 가능. |
| 담임목사 4:5 프로필·목회자 인사 섹션(홈) | SECTION 4 | 인사말 문안 없음(창작 0). 담임목사 학력·활동 블록은 교회소개 페이지에서 시안E_교회소개.html 그대로 이식 예정(master 보충 ③). |
| 푸터 담임목사·고유번호·계좌 | 벤치마크 푸터 | 원천 자료에 없음(계좌는 재정 페이지 암호 잠금). 3열(교회·예배·바로가기)만. |
| 예배 시간 "수요성경공부·새벽기도회" | 와이어프레임 예시 | 제미나이 예시 문안 — 미사용. 실값은 대장(주일 11시·성경공부 주일 오후 1시·아침예배 오전 7시). |
| 사진 15장 배치 전략의 3대 가치 3장·교제 3장·다음세대 2장 | §5(4) | 홈은 히어로 1 + 섹션 3(예배·소개·아카데미)로 절제(master ③ "2~3곳"). 갤러리는 교회소개 페이지 「교회의 시간들」 12장으로 이식 예정. |

## 3. 대비 실측 (WCAG2 ratio · sRGB relative luminance 계산)
아래는 r4/_evidence/contrast.json 에 스크립트로 산출·기록(본문 ≥4.5 · 대형/UI ≥3).
