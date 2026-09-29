# [worker] R4 홈 1차 보고 — 2026-09-29 23:3x (worker surface:39)

## 결과 한 줄
디자인 토큰 + 공용 컴포넌트 + 홈(index.html) 완성 · git push 완료(**fb76ff2**, origin/main) · 라이브 **200**
https://seudw79-sketch.github.io/keunsaem-preview/r4/index.html

## 캡처 2장
- `~/SDWjavis/큰샘교회/홈페이지_리뉴얼_20260912/캡처_R4/index_1280.png` (1280×6067, 전체 페이지)
- `~/SDWjavis/큰샘교회/홈페이지_리뉴얼_20260912/캡처_R4/index_390.png` (390×9770, 전체 페이지)
- 참고: 같은 폴더 `_참고/hcbc_1280.png`(벤치마크 캡처)·`_참고/사진_컨택트시트.jpg`(보유 사진 41장 일람)

## 산출물
| 파일 | 내용 |
|---|---|
| r4/assets/tokens.css | 2-tier 토큰. hex 는 `--p-*` 줄만. 토큰마다 `/* 근거: */` 주석 |
| r4/assets/r4.css | 공용 컴포넌트 CSS 1개. `@layer tokens,base,components,pages`. hex 0 |
| r4/index.html | 문안 verbatim(대장·시안E·latest.json·jubo·주보목록). 블록마다 `<!-- 근거: -->` |
| r4/사진/web/ | hero.jpg·about.jpg·worship.jpg·academy.jpg (총 503KB, `_출처.json` 원본 대조) |
| r4/_evidence/ | verify.py · text_parity.json · links.json · overflow.json · css_check.json · contrast.json · design_decisions.md |

## 성공 기준 대비 실측 (홈 1페이지)
| 기준 | 결과 | 근거 파일 |
|---|---|---|
| ② 문안 = 원문 문자 일치 | **true** (미일치 0 / 텍스트 노드 전수) | text_parity.json |
| ③ 창작 문구 0 | 0건 (출처 밖 문구 없음) | text_parity.json |
| ④ 내부 링크 실존 | 깨짐 = **아직 안 만든 하위 8페이지 링크만**(교회소개·예배안내·아카데미·칼럼·재정·주보·온라인예배·새가족) — 2단계에서 해소 | links.json |
| ⑤ 공용 CSS 1개·hex 0 | r4.css hex 0 · index.html hex 0 · tokens.css 는 `--p-*` 줄만 · 주석 균형 17/17·32/32 | css_check.json |
| ⑥ 캡처·수평 넘침 | 390: scrollWidth 390 = clientWidth · 1280 동일 → 넘침 0 | overflow.json |
| ⑦ 라이브 200 | index.html 200 · assets/tokens.css 200 | curl 실측 |
| 대비(추가) | 12쌍 전부 PASS (본문 ≥4.5 · 금색은 대형·장식 전용 3.4) | contrast.json |

## 벤치마크 §5 반영 요약 (상세 = design_decisions.md)
채택: 명도비례 팔레트(남색·청록 계승) · 앤틱골드 #9C835A 1색 · 유동 clamp 타이포 7단 · 행간 1.22/1.35/1.68/1.85 · 자간 -0.025/0/0.08em · 컨테이너 1160/760 · 거터 clamp(16,4vw,32) · radius 2/4/알약 · saturate(.85) contrast(.95) 톤다운 · 섹션 순서(히어로→세기둥→예배+알약CTA→소개 2단→이번주+통독→최근설교→처음오신분 3단계→오시는길+문의→푸터 3열) · GNB 우측 알약 CTA "새가족 안내".
**와이어프레임의 헤드라인·성구·목회중심 설명·수요/새벽 시간·계좌 등은 한 글자도 쓰지 않음.**

## ★ master 판단 필요 3건
1. **섹션 여백**: 벤치마크 `clamp(56px, 8vh, 96px)` 채택(기준 격상 ② 120/72 은 보류 — "충돌 시 벤치마크 실측 우선" 지시대로). 120 으로 돌리려면 tokens.css `--section-y` 1줄: `clamp(4.5rem, 9.5vw, 8rem)`.
2. **히어로 오버레이**: 벤치마크 "페이퍼 틴트(밝은 배경+어두운 글자)" 대신 어두운 그라데이션 유지. 이유: hero.jpg(실내 단체사진)는 밀도가 높아 밝은 틴트로는 가독 확보 불가(hcbc 는 질감 벽면). 밝은 톤을 원하시면 히어로 사진을 about2(정자 앞 야외)로 교체하면 가능.
3. **문의 폼**: R3_B 의 "미연결" disabled 폼은 제거하고, 새가족 페이지의 실경로(카카오 오픈채팅 + 전화)로 대체. 폼 복원 원하시면 말씀 주십시오.

## 2단계(8페이지) 착수 전 확인 2건
1. **주보 페이지**: ksmc31 `주보목록.json` 7건 중 `jubo_260920.html`·`jubo_260927.html` 은 preview 레포에 없음 → 상대링크면 깨짐. 라이브 `https://ksmc31.kr/jubo_2609xx.html`(200 확인) 절대링크로 갈지, preview 에 있는 5건만 상대링크로 갈지.
2. **재정 페이지**: `시안E_재정.html` 은 암호 잠금(PBKDF2+AES-GCM) 단일 페이지 — 본문이 암호문이라 R4 디자인 이식 대상이 아님. (a) 그대로 복사 (b) 잠금 화면만 R4 스킨 적용 중 택일.

## 참고(결함 아님)
- preview 레포의 `latest.json`·`주보목록.json` 은 라이브(ksmc31)보다 오래됨(2026-09-13 vs 09-27). 홈 스냅샷은 라이브 값으로 박았고, 런타임 fetch 는 `../latest.json`(preview)이라 배포 전 preview 파일 갱신이 필요하면 별도 지시 바람(무수정 대상이라 손대지 않음).
- 부서3 워커 분담 시 필요한 것: `r4/assets/tokens.css`·`r4/assets/r4.css`·`r4/_evidence/verify.py`(페이지명 인자로 실행) 그대로 사용, 페이지 고유 CSS 는 `<style>@layer pages{…}</style>` 로만.
