# [worker] R4 홈 2차 보고 — 2026-09-30 00:xx (worker surface:39)

## 결과 한 줄
오너 기준 「고급스럽고 세련되게 현대식으로」·master 2차 방침(타이포·질감 주도·hcbc 구조·수상작 문법)으로 홈을 다시 만들어 push. 1차는 `r4/_v1_index.html` 로 보존.
라이브: https://seudw79-sketch.github.io/keunsaem-preview/r4/index.html

## 무엇이 바뀌었나 (1차 → 2차)
| 항목 | 1차 | 2차 |
|---|---|---|
| 히어로 | 실내 회중 사진 전폭 + 어두운 스크림 + 흰 세리프 | **사람 없는 십자가·흰 벽돌 벽 질감**(우리 사진 pastor_full 크롭·블러·저채도, 1920×1080 48KB) 위에 **표어 캘리 록업**(Nanum Brush Script, 상한 7rem) + 세리프 부제 + 알약 CTA 3 · 종이 그라데이션 마스크 · 인셋 프레임 |
| 팔레트 | 청록 계열 오프화이트 + 남색 히어로/푸터/카드 | **종이색 #F6F5F1 + 먹색 #1E211E** · 남색은 버튼만·청록은 라벨·선만 · **금색 #9C835A 숫자·룰만** (master 2차 ④) |
| 타이포 | display 상한 4.2rem | display 상한 **5.6rem**(hcbc 실측) · 캘리 7rem · 라벨 0.72rem 자간 **0.18em** — 극적 대비 |
| 구조 | 카드 3열 나열·사진 3곳 | hcbc 문법: eyebrow → 대형 세리프 → **01/02/03 얇은 선 3열** → 골드 룰 태그라인 · **잡지형 2단**(제목 좌·행/본문 우) · 사진은 교회소개 1장 소형 + 「교회의 시간들」 **6타일 duotone** 만 |
| 카드 | 테두리 박스·남색 카드 | 박스 없음 — 상단 hairline 열만(그림자 0·둥근 카드 0) |
| 푸터 | 남색 3열 | 종이 위 hairline 3열(교회·예배·바로가기) |
| 섹션 여백 | clamp(56px,8vh,96px) | clamp(72px,10vw,128px) — 여백 크게(master 2차 ③) |

## 캡처 2장 (진짜 390 = iframe 래퍼 · 하네스 개선)
- `~/SDWjavis/큰샘교회/홈페이지_리뉴얼_20260912/캡처_R4/index_1280.png` (1280×7146 전체)
- `~/SDWjavis/큰샘교회/홈페이지_리뉴얼_20260912/캡처_R4/index_390.png` (390×9447 전체 — 헤드리스 500px 하한을 iframe 래퍼로 우회, 시안E 주석 실측 재확인)
- 참고 캡처: `_참고/awwwards_nonprofit_1280.png`·`awwwards_sotd_1280.png`·`cssda_1280.png`·`hcbc_full_1280.png`·`bridgetown_1280.png`·`_hero_texture_preview.jpg`·`_tiles_preview.jpg`

## 성공 기준 대비 실측
| 기준 | 결과 | 근거 |
|---|---|---|
| ② 문안 = 원문 문자 일치 | **true** (미일치 0) — 수상작·벤치마크 와이어프레임 문안 0 사용 | text_parity.json |
| ③ 창작 0 | 0건 | text_parity.json |
| ④ 내부 링크 | 깨짐 = 하위 8페이지(미제작·master 중지) 링크만 | links.json |
| ⑤ 공용 CSS 1개·hex 0 | r4.css hex 0 · html hex 0 · tokens.css --p-* 줄만 · 주석 균형 13/13·19/19 | css_check.json |
| ⑥ 수평 넘침 | **390(진짜): 0 · 1280: 0** (maxRight 판정·스크롤 컨테이너 제외) | overflow.json |
| ⑦ 라이브 200 | push 후 확인(아래 해시) | — |
| 대비 | v2 12쌍 전부 PASS(금색은 장식 숫자 전용 3.3:1 트레이드오프 기록) | contrast.json |
| 사진 | 히어로 48KB·about 161KB·타일 6장 407KB — 페이지 사진 합계 ≈ 0.6MB(3MB 이하) | 사진/web/_grade.json |

## 히어로 결정 근거 (캔바/스톡 vs 자체 질감)
자체 질감 채택 — hcbc 히어로 문법(질감 벽면 + 캘리)과 동형, 라이선스·AI 기믹 위험 0, 캔바 커넥터는 200×200 만 내려받힘(1920 은 디자인 변환+export 추가 단계). 상세·대안 = `r4/_evidence/images.md`.

## 수상작 참고 (오너 지목) — 실접속 결과
- Awwwards 비영리 컬렉션 200(36건) · Sites of the Day 200(최근 12건) · CSS Design Awards 홈 200(WOTD 2026-09-29 + 노미네이트/이전 WOTD 6건) · CSSDA WOTD 갤러리 **302(직접 열람 불가 → 홈 6건으로 대체)** · passioncitychurch.com **403(봇 차단 → 벤치마크 실측·갤러리 캡처로 대체)**.
- 차용 내역·URL·공통 문법 5줄 = `r4/_evidence/design_decisions.md` §2-C.

## master 판단 필요
1. 표어 캘리(Nanum Brush Script) vs 대형 세리프 — 캘리로 갔음(hcbc 동형·서명성). 세리프로 바꾸려면 `.hero h1{font-family:var(--font-serif)}` 1줄.
2. 「교회의 시간들」 6타일 duotone 톤(세피아 약) — 원색 22% 만 남김. 더 흑백/더 컬러는 photo_grade.py 의 blend 값 1개.
3. 하위 페이지: 교회소개 초안(`_wip_교회소개.html`, 1차 컴포넌트 기준)은 v2 컴포넌트로 재조립 필요 — 재개 지시 시 v2 기준으로 4페이지(교회소개·예배안내·새가족·주보) 진행.

## ★재개 포인터 (2026-09-30 · master 검수 통과 수준 · 컨텍스트 사이클 전 저장)
- 확정: 캘리 유지(세리프 전환 1줄 대기) · 6타일 톤 유지 · 하위 페이지 v2 컴포넌트 재조립.
- 홈 3차 4건: (a) 모바일 햄버거/드로어 CSS only(checkbox) (b) 모바일 예배시간 유틸 1줄(균등 축약 또는 가로 스크롤) (c) 세 기둥 빈 줄 숨김(오너 답 전) (d) 세 기둥 제목 한 단계↓ + eyebrow 「세 기둥」(master 지정 문구).
- 리뷰어 verdict 2건 수령 후 합쳐 3차 → push → 보고 → 교회소개·예배안내·새가족·주보(v2 재조립, 주보=ksmc31.kr 절대링크).
- 상세 = ~/.cys/pack/round/WORKER_TODO.md 「★재개 포인터」.

- CYCLE 저장 2026-09-30 01:0x: WORKER_TODO.md 전면 재기록(배정 출처·미해결 게이트·다음 액션 6단계). 복구 후 첫 일 = 홈 3차(a~d + 리뷰어 verdict 2건).

- CYCLE 재요구 2026-09-30 01:1x: WORKER_TODO.md 재기록(변동 없음). 다음 액션 1=홈 3차(a~d+리뷰어 2건, 출처 master 00:5x) → 2~5=교회소개·예배안내·새가족·주보(v2 재조립).

- CYCLE 재기록 2026-09-30 00:10:13(3회째): WORKER_TODO.md 물리 재기록 완료. 다음 액션 1=홈 3차(a~d+리뷰어 2건 · 출처 master 2026-09-30 00:5x 검수 회신) → 2~5=교회소개·예배안내·새가족·주보(v2 재조립 · 출처 원티켓+master 00:5x).

- CYCLE 재기록 2026-09-30 00:12:31(4회째): WORKER_TODO.md 물리 재기록 완료. 다음 액션 1=홈 3차(a~d+리뷰어 2건 · 출처 master 2026-09-30 00:5x 검수 회신) → 2~5=교회소개·예배안내·새가족·주보(v2 재조립 · 출처 원티켓+master 00:5x). SESSION_STATE.md 는 쓰기 금지 대상 — worker 절은 00:5x 에 이미 append 됨.
