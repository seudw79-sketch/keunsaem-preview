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

## 2-B. 2차(v2) 방향 전환 기록 — 오너 「이게 최선이야?」→「고급스럽고 세련되게 현대식으로」
- 사진 진단(master, 컨택트시트 41장): 전부 폰 스냅·실내 형광등·저해상 → **타이포·질감 주도**로 전환. 1차(_v1_index.html)의 대형 회중 사진 히어로·사진 3곳 폐기.
- 팔레트 v2: 종이색 #F6F5F1 배경 + 먹색 #1E211E 글자, 남색 #1B3A47 은 버튼에만·청록 #2A5D69 은 라벨·링크·선에만, 금색 #9C835A 은 숫자·선·eyebrow 만 (master 2차 ④).
- 히어로: 사람 사진 금지 → 자체 십자가·벽 질감(r4/_evidence/photo_grade.py) + Nanum Brush Script 표어 록업 + 종이 그라데이션 마스크. 근거·대안 = r4/_evidence/images.md.
- 구조: hcbc.kr 문법(eyebrow 소형 자간 넓게 → 대형 세리프 제목 → 01/02/03 얇은 선 3열 → 골드 룰 태그라인) · 잡지형 2단(제목 좌·행 우) · 사진은 교회소개 1장 소형 + 「교회의 시간들」 6타일 duotone 만.

## 2-C. 수상작 차용 내역 (2026-09-29 실접속·캡처 = 캡처_R4/_참고/)
| 출처 (URL) | 접속 | 무엇을 차용했나 |
|---|---|---|
| Wright's Ferry Mansion — https://wrightsferrymansion.org (Awwwards SOTD 2024-04-30 https://www.awwwards.com/sites/wrights-ferry-mansion) · 벤치마크 §6-2 | 벤치마크 실측(200) | 린넨 종이 배경(#F6F5F1 계열) · clamp 초대형 출판 세리프(--text-display 상한 5.6rem, 캘리 --text-script 상한 7rem) · 정적 품격(JS 애니 0, CSS 스크롤 페이드 1종) · radius 0~2px |
| Passion City Church — https://passioncitychurch.com (Awwwards Nominee https://www.awwwards.com/sites/passion-city-church) | 직접 접속 403(봇 차단) → 벤치마크 §6-2 실측·Awwwards 갤러리 캡처로 대체 | 직각 카드(2px) + 알약 CTA 만(새가족 안내·온라인 예배·오픈채팅) · 따뜻한 앰버 톤은 갤러리 duotone 중간톤(warm)에만 반영 |
| The Obama Foundation — https://www.obama.org (Webby 2025 https://winners.webbyawards.com/2025/websites-and-mobile-sites/general-desktop-mobile-sites/charitable-organizationsnon-profit/289384/obama-foundation) | 벤치마크 실측(200) | 대담한 헤드라인 위계(title--display vs caption 라벨 12px) · 섹션 여백 분할 clamp(72px,10vw,128px) · 3열 모듈 |
| 기후솔루션 — https://forourclimate.org (웹어워드코리아 2024 http://www.i-awards.or.kr/Web/) | 벤치마크 실측(200) | 1px 라인 시스템(.cols/.rows/.strip/.footer 전부 hairline) · 원색 0 · Pretendard 본문 행간 1.7 |
| Awwwards 비영리 컬렉션 — https://www.awwwards.com/awwwards/collections/nonprofit-websites/ | 200 · 캡처 awwwards_nonprofit_1280.png (36건 썸네일) | 상위 5건 히어로 구조: ①Won Agency(암 지원) 전폭 인물 사진+좌하단 2줄 헤드라인+CTA 2 ②3D keypoints 다크 배경+소형 라벨 ③Ukraine events 다크 풀블리드+시계 타이포 1개 ④Nonprofit call to action 흑백 사진+중앙 단어 1개 ⑤Armenian Genocide 초대형 세리프 숫자 록업. 공통=한 화면에 록업 1개·요소 최소·사진은 모노/다크 톤으로 타이포에 종속 → 홈 히어로를 록업 1개(표어 캘리+부제+CTA)로 단순화, 사진은 duotone 으로 종속 |
| Awwwards Sites of the Day — https://www.awwwards.com/websites/sites_of_the_day/ | 200 · 캡처 awwwards_sotd_1280.png (최근 12건) | 최근 10건 공통: 세리프 이탤릭·대형 록업("The art OF THE SUBLIME"·"Elevating Life") · 흑/백/포인트 1색 · 큰 여백 · 제품/공간 이미지 1장 · 소형 대문자 라벨 |
| CSS Design Awards — https://www.cssdesignawards.com/ | 200 · 캡처 cssda_1280.png (WOTD 2026-09-29 ZIRKA Interceptor·Newest Nominees 3·Previous WOTDs 3) | 자간 넓은 소형 대문자 라벨("AWARDED 2026 SEP 29"·"NEWEST NOMINEES") · 얇은 밑줄 강조 · 점수판식 숫자 라벨 → .num/.eyebrow 자간 0.18em·금색 숫자 |
| CSS Design Awards WOTD 갤러리 — https://www.cssdesignawards.com/website-gallery?feature=wotd | 302 리다이렉트(갤러리 직접 열람 불가) → 홈의 WOTD/Previous WOTDs 6건으로 대체 | (위와 동일) |

## 2-D. 오너 지정 5곳에서 차용한 것 (2026-09-30 실접속 200 · 캡처 = 캡처_R4/_참고/owner_*_1280.png) — 벤치마크 8곳보다 우선
| 사이트 (URL) | 관찰(히어로·타이포·섹션 리듬·CTA) | 차용 → 홈 v2 | 차용 안 함(이유) |
|---|---|---|---|
| Cedarcrest Church — https://cedarcrestchurch.com/ | 상단 좌측 "SUNDAYS 8 AM \| 9:30 AM \| 11 AM" 칩 · 떠 있는 둥근 내비 바 · 히어로 = **최신 설교 영상 썸네일(둥근) + 소문자 세리프 대형 제목("philippians: choosing Jesus is choosing joy") + WATCH NOW 알약 + PREVIOUS MESSAGES 링크** · 웜 토프 밴드 "we'd love to meet you" + PLAN YOUR VISIT 알약 · 큰 둥근 사진 카드 | ①예배 시간 유틸 라인을 히어로 위 최상단에 ②**최신 설교 2단 피처**(썸네일 좌·대형 세리프 제목 우·알약 CTA) 를 히어로 바로 아래 ③알약 CTA 2개 조합(설교 영상 보기 ↗ + 온라인 예배 ↗) | 큰 둥근 사진 카드·웨이브 구분(master: 둥근 큰 카드 금지) |
| Passion City Church — https://passioncitychurch.com/ | 인셋 둥근 전폭 비디오 프레임 · 좌하단 초대형 볼드 산세리프 3줄("For God. / For People. / For the City.") · 우상단 알약 1개(UPCOMING EVENTS) | ①히어로 **인셋 둥근 프레임**(--radius-media 12px) ②록업 2~3줄 짧게 ③상단 우측 알약 1개(새가족 안내) | 비디오 배경(사진·영상 자산 없음)·볼드 산세리프(한국어 세리프 편집 톤 유지) |
| One Church — https://one.church/ | 중앙 브랜드 록업 "ONE CHURCH" 초대형 + 위에 주소 소형 자간 넓게 · WATCH/VISIT 버튼 2개 · 남색 밴드 "JOIN US FOR SERVICE"+시간 + 큰 베이지 VISIT | ①중앙 정렬 록업(히어로) ②소형 자간 넓은 안내줄(예배 시간 유틸) ③CTA 2~3개 통일 | 검색바·남색 대면적 밴드(master: 남색은 버튼만) |
| Elevation Church — https://elevationchurch.org/ | 다크 테마 · 비디오 히어로 + 소형 환영 문구 + 알약 2개 · 4열 아이콘 피처 · 카드 캐러셀 | 알약 2개 조합 규칙만 | 다크 테마·아이콘·캐러셀(종이색·정적 원칙) |
| Transformation Church — https://transformchurch.us/ | 흰 배경 · 비디오 히어로(헤드리스 미렌더) · "WATCH **LATEST** SERMON" 초대형 산세리프 + 자간 넓은 대문자 메타 3줄(SERMON/SERIES/SPEAKER) | ①**최신 설교를 첫 섹션으로**(피처) ②메타를 소형 자간 넓은 라벨로(.meta·.num) | 비디오 히어로·전면 대문자 산세리프 |

공통 문법(5곳): 예배 시간이 첫 화면 최상단 · 최신 설교(영상)가 히어로 다음 · 알약 CTA 2개 이하 · 인셋 둥근 미디어 프레임 · 록업은 2~3줄 짧게. → 홈 v2 는 이 다섯을 전부 반영했고, 색·서체·정적 원칙은 master 2차 방침을 유지했다.

### 수상작 공통 문법 5줄 (홈 v2 반영)
1. 한 화면 = 한 메시지: 히어로에 대형 타이포 록업 1개 + CTA 1~2개, 그 외 요소 제거. → 히어로 = 표어 캘리 + 부제 + 알약 3개.
2. 사진은 톤 통일(모노·듀오톤·저채도)로 타이포에 종속 — 배경이지 주인공이 아님. → 히어로 질감 블러, 갤러리 duotone.
3. 라벨은 소형·자간 넓게(0.15~0.25em), 제목은 세리프(캘리/이탤릭 혼용)로 크기 대비를 극적으로. → --tracking-wide 0.18em · --text-display/--text-script.
4. 색은 2~3색(종이·먹·포인트 1) + 1px 라인 구획, 그림자·둥근 큰 카드 없음. → 종이·먹·금 + 남/청 소량, 전 구획 hairline.
5. 모션은 스크롤 등장·호버 밑줄/색 전환 정도로 절제(0.2~0.3s). → .reveal 1종 + 버튼 hover 250ms.

## 3. 대비 실측 (WCAG2 ratio · sRGB relative luminance 계산)
r4/_evidence/contrast.json 에 스크립트로 산출·기록(본문 ≥4.5 · 대형/UI ≥3). v2 팔레트 12쌍 전부 기준 통과.
- 알려진 트레이드오프: 금색 #9C835A 은 종이 위 3.3:1 — 소형 본문 기준(4.5) 미달이므로 **정보를 담지 않는 장식 숫자(01/02/03)·룰 선에만** 쓴다(정보는 제목이 담음). 라벨 본문은 청록 #2A5D69(6.7:1).
- 히어로 질감 위 먹색 글자: 질감 최밝 영역 14.9:1 · 중간톤 근사 7.5:1 — 종이 그라데이션 마스크(상 60%·하 86%)로 록업 구간을 추가로 밝힘.

## 4. 검증 하네스 메모 (실측에서 배운 것)
- 헤드리스 Chrome 은 500px 미만 창을 만들지 못한다(시안E 주석 실측 재확인: window-size=390 → clientWidth 500). 390 측정·캡처는 iframe 래퍼(폭 390)를 520px 창에 렌더해 얻는다(verify.py).
- body{overflow-x:hidden} 은 scrollWidth 로 넘침을 숨긴다 → 요소 우측 끝 최대값(maxRight, 스크롤 컨테이너 자손 제외)으로 판정한다.
