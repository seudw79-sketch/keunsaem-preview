# [worker] R4 홈 3차 보고 — 2026-09-30 03:xx (worker surface:45 · 39 후임)

## 결과 한 줄
master 검수 4건(a~d) + codex R1 3건 + gemini R1 8건(+푸터 © 허용)을 한 번에 반영해 홈 3차를 만들었다. 결정론 검증(문안 대조·링크·hex·넘침·캡처) 전부 통과, 드로어 열림 상태까지 실측 캡처로 확인.
라이브: https://seudw79-sketch.github.io/keunsaem-preview/r4/index.html — **push ab44788 · 라이브 200 · 3차 마크업 반영 확인**(nav-toggle·hero__script·「세 기둥」 grep, push 후 4번째 폴링 ≈40초)

## 반영 내역 (지적 → 무엇을 어떻게 바꿨나)
| 출처 | 지적 | 반영 | 파일:위치 |
|---|---|---|---|
| master (a) · codex ③ · gemini ① blocking | 모바일 상단 내비 잘림 · 가로스크롤 발견성 약함 | **CSS-only 체크박스 드로어**(외부 JS 0). `#nav-toggle` 체크박스(시각 숨김·포커스 가능) + `label.nav__burger`(햄버거 3선 → 체크 시 X) + `nav#site-nav` 를 ≤640px 에서 헤더 아래 고정 패널로. 닫힘=`max-height:0; visibility:hidden`(탭 순서·보조기기 트리에서 제외), 열림=`:checked ~ nav` 로 `visibility:visible; max-height:calc(100svh - 64px); overflow-y:auto`. 641px 이상은 기존 가로 내비 그대로 | index.html 헤더 3줄 · r4.css `.nav__toggle`/`.nav__burger` 기본 + `@media(max-width:640px)` 블록 |
| master (b) | 모바일 예배시간 유틸 2줄 꺾임 | ≤640px 에서 `.util` 을 nowrap·11px·자간 .06em·gap 16px 로 축약, 넘칠 때만 가로 스크롤(스크롤바 숨김 · `justify-content:safe center`, 미지원 브라우저는 좌정렬 폴백). **390 실측: 3항목이 한 줄에 다 들어감(스크롤 불필요)** | r4.css ≤640 `.util` 4줄 |
| master (c) · codex ② · gemini ② blocking | 세 기둥 빈 줄 렌더 금지 · 임시 문안 불허 | `.empty-line{display:none}` — 빈 `<p>` 는 HTML 에 남겨 오너 답 오면 문안만 넣으면 되게 함(임시 문안 0 · 행 높이=실콘텐츠). 세 기둥 열은 번호·제목만 보임 | r4.css `.empty-line` · index.html 주석 |
| master (d) · gemini ④ | 세 기둥 제목이 히어로 표어와 중복 | eyebrow 「성경 아카데미」→**「세 기둥」**(master 지정 문구) · 제목 `title--display`→`title`(--text-h1, 한 단계↓) · 표어 문안은 그대로(변경 0) | index.html #vision · verify.py ALLOW 에 「세 기둥」 등재(출처 주석) |
| codex ① · gemini ③ major | 캘리(112px)가 H1 전체 차지 → H1 세리프 | H1 「말씀을 읽고 배우고 가르치자」= Noto Serif KR 500 · 자간 -0.025em · **clamp(2.2rem,5.5vw,4.2rem)**(토큰 `--text-hero`). 캘리는 짧은 보조 라벨 `.hero__script` 「큰샘교회」clamp(1.9rem,4vw,2.75rem) 로 축소 | tokens.css `--text-hero`·`--text-script` · r4.css `.hero h1`·`.hero__script` · index.html 히어로 록업 |
| gemini ⑤ major | 섹션 제목 크기 --text-h1 통일 · 디스플레이는 히어로만 | `.feature .title`(주일 설교) display→h1 · #visitors `title--display` 제거 · #vision 위 (d) 로 제거 → 홈에서 `title--display` 사용 0 | r4.css `.feature .title` · index.html #latest·#visitors |
| gemini ⑥ major | 배경 단일 종이색 · 틴트는 강조 블록 1개 | 틴트 3곳(#intro·#week·#visitors) → **#visitors(처음 오신 분 안내) 1곳만** 유지. #intro 는 종이색, #week 는 `section--line`(hairline) 으로 | index.html 3섹션 class |
| gemini ⑦ minor | 앵커 화살표: 페이지 내 ↓/없음 · 서브페이지 → | 히어로 「예배안내 ↓」「오시는 길 ↓」「새가족 안내 →」 · 서브페이지 링크 5곳 ↗→「→」(온라인 예배·주보 보기·예배 참여하기·성경 아카데미×2) · 외부(유튜브·카카오맵) ↗ 유지 | index.html · verify.py 화살표 strip 정규식에 ↓ 추가 |
| gemini ⑧ minor | 갤러리 타일 3×2 로 크게(360px+) | `.tiles` 6열→**3열**(1160 wrap 에서 타일 폭 ≈376px) · ≤640 2열 유지 · 중복이던 ≤960 3열 규칙 제거 | r4.css `.tiles` |
| gemini 허용 | 푸터 '© 2026 큰샘교회' 한 줄 | `footer__copy` 둘째 줄 추가 · verify.py ALLOW 등재(사실 표기·master 허용 출처 주석) | index.html 푸터 · verify.py |
| gemini 불채택 | '성도들의 삶과…' 안내문 · 임시 기둥 문구 · 제목 문구 변경 | **반영하지 않음**(창작 문구) — 이번 3차에 새 문안 0 | — |

## 병합 판단 3건 (리뷰어 간 차이 · 내가 정한 것 — master 검수 대상)
1. **H1 크기**: codex clamp(2.2rem,5.5vw,4.2rem) vs gemini clamp(2.4rem,5.2vw,5.2rem). → **codex 값 채택.** 근거: 조사/02_프리미엄_벤치마크_20260929.md **235행** `--text-hero-display: clamp(2.2rem, 5.5vw, 4.2rem)` 이 우리 벤치마크의 자체 토큰(codex 가 인용한 233행 근처 실측). gemini 5.2rem 상한은 벤치마크에 근거 없음 + ⑤(섹션 제목 3rem 상한)와의 대비는 4.2rem 으로 충분. 바꾸려면 tokens.css `--text-hero` 1줄.
2. **캘리 라벨 문구**: 리뷰어는 "부제/성구 라벨"을 권했으나 **대장(00_R3_실문구_대장.md)에 성구 표기가 없다**(grep: 표어 1건만, 에스라·성구 0건). 창작 금지라 성구를 지어 넣지 않고 대장 교회명 **「큰샘교회」** 를 캘리 라벨로 썼다(영문 라벨 KEUNSAEM METHODIST CHURCH 아래 한글 서명 록업). 다른 문구로 바꾸려면 index.html `.hero__script` 1줄. 오너가 성구를 주면 그걸로 교체 권장.
3. **틴트 1개 = 처음 오신 분 안내**: 전환 목적(새가족)이 가장 강한 블록이고 hcbc 'NEW HERE?' 도 강조 블록. 「이번 주 큰샘교회」로 바꾸려면 class 2곳 교환.

## 실측 중 발견·수정 1건
- 드로어 열림 상태 첫 캡처에서 **패널 배경(nav-glass 86% 알파)** 뒤로 히어로 문구·예배시간 줄이 비쳐 메뉴 가독성이 떨어졌다(헤드리스는 backdrop blur 를 약하게 그림 — 실기기도 안전하지 않다). → 패널 배경을 **종이색 불투명(var(--bg))** 으로 바꾸고 재캡처로 확인. 헤더 바 자체는 glass 유지.

## 성공 기준 대비 실측 (verify.py index · 2026-09-30 03:2x)
| 기준 | 결과 | 근거 파일 |
|---|---|---|
| ② 문안 = 원문 문자 일치 | **parity true · unmatched 0** | _evidence/text_parity.json |
| ③ 창작 0 | 0건 — 신규 노드는 「세 기둥」(master 지정)·「© 2026 큰샘교회」(master 허용)·체크박스 이름 「메뉴」(구조 라벨, aria-label) 뿐 | text_parity.json · verify.py ALLOW 주석 |
| ④ 내부 링크 | 깨짐 11건 = 전부 **미제작 4페이지**(교회소개·예배안내·새가족·주보) 링크 — 2차와 동일, 다음 단계에서 해소 | links.json |
| ⑤ 공용 CSS 1개 · hex 0 | r4.css hex 0 · tokens.css --p-* 밖 hex 0 · html hex 0 · 주석 균형 r4 20/20 · tokens 21/21 | css_check.json |
| ⑥ 수평 넘침 | **390: 0 · 1280: 0**(maxRight 판정) | overflow.json |
| ⑥ 캡처 | index_1280.png 1280×7964 · index_390.png 390×9745 · **+ index_390_drawer_open.png 390×900(드로어 열림)** | 캡처_R4/ |
| ⑦ 라이브 200 | push 후 확인 → 보고 메시지에 기재 | — |

## 접근성 — 무엇을 실측했고 무엇은 못 했나 (환각 금지)
- 실측함: 드로어 열림/닫힘 렌더(캡처), 햄버거→X 전환, 닫힘 상태 `visibility:hidden`(CSS 규칙 존재).
- **실측 못 함(헤드리스 한계)**: Tab→Space 토글, 스크린리더 읽기. 설계상 근거: 체크박스는 `display:none`/`hidden` 이 아니라 sr-only(1px clip) 라 포커스 가능 · `aria-label="메뉴"`·`aria-controls="site-nav"` · `:focus-visible ~ .nav__burger` 포커스 링. **실기기 확인 필요 — 미검증 항목으로 표기.**

## 타 페이지 영향 (공용 CSS 변경의 파급)
- 부서3 페이지(아카데미·칼럼·온라인예배)는 `section--tint`·`title--display` 각 1회 사용 — 두 규칙은 **삭제하지 않았으므로 영향 0**. `.hero h1`·`.hero__script`·`.util`·`.tiles`·`.feature`·`.empty-line` 은 부서3 4페이지에서 사용 0(grep 실측). 재정.html 은 해당 클래스 0.
- gemini ⑤(섹션 제목 통일)를 부서3 페이지에도 적용할지는 master 판단(그 페이지들의 `title--display` 1회씩).

## 캡처 3장
- `~/SDWjavis/큰샘교회/홈페이지_리뉴얼_20260912/캡처_R4/index_1280.png`
- `~/SDWjavis/큰샘교회/홈페이지_리뉴얼_20260912/캡처_R4/index_390.png`
- `~/SDWjavis/큰샘교회/홈페이지_리뉴얼_20260912/캡처_R4/index_390_drawer_open.png`

## master 판단 필요
1. 병합 판단 3건(위) 승인 여부.
2. 부서3 페이지에 gemini ⑤ 적용 여부.
3. 오너 답 대기 그대로: 세 기둥 2줄×3 문구 · 캘리 라벨 문구(성구가 있으면 교체).

## ★재개 포인터
- 홈 3차 완료·push 후 → **교회소개.html(v2 재조립·`_wip_교회소개.html` 문안 재사용) → 예배안내 → 새가족 → 주보**(WORKER_TODO 다음 액션 2~5). 드로어·유틸·화살표 규칙은 공용 CSS 에 있으므로 하위 페이지는 헤더 마크업 3줄(체크박스·라벨·nav id)만 홈과 동일하게 복사하면 된다.
