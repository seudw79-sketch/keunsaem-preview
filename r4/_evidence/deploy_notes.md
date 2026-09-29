# R4 라이브 배포 절차 (preview r4/ → ksmc31 루트) — 확정본

작성: worker · 2026-09-29 초안 → **2026-09-30 확정**(master [R4 리뷰 종결 → 배포 준비] ①~④ · R2 codex·gemini ACCEPT)
실행 도구: `r4/_evidence/deploy_to_live.sh` (기본 `--dry-run` · `--apply` 로만 실행 · **push 없음** — 오너 「올려」 승인 후 master 지시로 push)

## 0. 실측 전제 (2026-09-30 05:xx)
- 라이브 레포 `/Users/sdw79/SDWjavis/_레포/ksmc31` · main · HEAD fda2081 · 추적 변경 0(미추적 `_round/` 만) · 23MB(.git 12MB) · origin github.com/seudw79-sketch/ksmc31
- 라이브 루트: index.html(43KB, 인라인 CSS·OG·canonical·Church JSON-LD 보유) · jubo.html + jubo_2606xx~260927 7건 · latest.json · 주보목록.json · 칼럼목록.json · 통독_365.json · 통독_영상_덮어쓰기.json · robots.txt(Disallow /시안E_재정.html) · sitemap.xml(시안E_* 8 + / + jubo) · CNAME(ksmc31.kr) · google/naver 확인파일 2 · 2a6ca…txt · 시안E_* 9(+.bak) · 시안_새디자인.html · assets/(og-jubo-2026.jpg·youtube_qr.png) · 사진/web/
- **jubo*.html·jubo.html 이 시안E_* 를 링크한다**(교회소개 12·주보 3·아카데미 3·칼럼 2·재정 2·온라인예배 2·예배안내 2·홈 1) → 시안E_* 는 내부 링크 대상이므로 **보존**(삭제·수정 금지). 배포 후에도 주보에서 옛 디자인 페이지로 가는 경로가 남는다(→ §6 판단 3).
- **사진 충돌 17건**: r4/사진/web 의 about·c1a~c4c·hero·naver_map·pastor 가 라이브 사진/web 과 같은 이름·다른 내용(r4=축소·보정본). 라이브 것은 시안E_교회소개·시안E_홈·index·jubo 가 참조한다 → 덮어쓰면 시안E/jubo 렌더가 바뀐다. **해법: r4 사진은 `사진/r4/` 에 별도 배치**하고 9페이지의 `사진/web/` 경로를 `사진/r4/` 로 치환(경로 치환·문안 무관). 참조 사진 18장(약 1.3MB)만 복사, 미참조(hero.jpg·worship·academy·원본 c*.jpg)는 복사하지 않는다.
- r4 9페이지에 `href="시안E_…"` 는 0(근거 주석에만 문자열 존재) · 재정.html 잠금 스크립트 = 시안E_재정 과 byte-identical(재확인).

## 1. 배치 (스크립트 §1·§5)
| 라이브 경로 | 동작 | 출처 |
|---|---|---|
| index.html | **교체** | r4/index.html(+ 라이브 head 의 OG·canonical·JSON-LD 이식 완료 — r4 index 자체에 들어 있음) |
| 교회소개·예배안내·새가족·아카데미·온라인예배·재정·주보·칼럼.html | 신규(한글 파일명 그대로) | r4/ |
| assets/r4.css · assets/tokens.css | 신규(기존 assets/ 2파일과 이름 충돌 0) | r4/assets |
| 사진/r4/*.jpg (18장) | 신규 폴더 | r4/사진/web 중 참조분 |
| sitemap.xml | **교체** | r4/_evidence/sitemap.proposed.xml(§4) |
| robots.txt | **교체**(+1줄 `Disallow: /재정.html` · 기존 줄 삭제 0 — 스크립트가 기계 확인) | r4/_evidence/robots.proposed.txt(master 판단 1 · 2026-09-30) |
| 그 외 전부 | 무수정 | — |

## 2. 링크·경로 치환 (스크립트 §2 — 스테이지 사본에만 · SRC 무수정 · 문안 무변경)
| 패턴 | → | 대상 |
|---|---|---|
| `https://ksmc31.kr/jubo_` | `jubo_` | 주보.html 정적 카드 7 |
| `https://ksmc31.kr/'+esc(` | `'+esc(` | 주보.html 런타임 JS 템플릿(★plain sed 가 놓치는 자리) |
| `../jubo.html` | `jubo.html` | index·주보 이번 주 링크 |
| `fetch('../` | `fetch('` | index·아카데미·주보·칼럼 데이터 fetch 5종 |
| `'../'+d.` | `d.` | index·주보 latest.json 주보_링크 조립 |
| `사진/web/` | `사진/r4/` | 9페이지 src(§0 충돌 회피) |

## 3. 로컬 검증 (스크립트 §3 — 하나라도 실패하면 exit≠0 · apply 안 감)
1. 치환 잔여 0 — `https://ksmc31.kr/jubo_`·`../데이터`·`사진/web/` grep 0
2. 내부 링크·자원 전수 실존(스테이지 ∪ 라이브) — 깨짐 0
3. 문안 parity — `verify.py` 의 `text_parity` 를 스테이지 루트로 재사용(출처=라이브 시안E_*·대장·latest·주보목록) → 9/9 true
4. 재정.html 잠금 `<script>` = 시안E_재정 동일
5. index 메타 이식(og:url·canonical·Church JSON-LD) 존재

## 4. sitemap 갱신안 (`sitemap.proposed.xml`)
- 시안E_* 8항목 → R4 한글 파일명 7(교회소개·예배안내·새가족·아카데미·온라인예배·주보·칼럼) percent-encoding · `/` · `jubo.html` 유지 · **재정.html 미등재**(기존 sitemap 도 시안E_재정 미등재·robots Disallow 와 일관) · lastmod 2026-09-30.

## 5. 백업·되돌리기 (스크립트 §5)
- 백업: `--apply` 시 `rsync -a` 로 `~/SDWjavis/_레포/_레포밖_보관/ksmc31_pre_r4_<YYYYmmdd_HHMMSS>/` (.git 포함 전체 · 약 23MB).
- 되돌리기 A(로컬 커밋만·push 전): `git -C ksmc31 reset --hard <배포 전 HEAD>` + `git clean -fd -- 사진/r4 assets/r4.css assets/tokens.css`
- 되돌리기 B(백업 복원): `rsync -a --delete --exclude .git <백업>/ ksmc31/` 후 `git status` 확인
- push 이후 되돌리기는 master 지시(revert 커밋 → push) — 스크립트 범위 밖.

## 6. master 판단 4건 — 전부 확정 (master [판단·배포 4건] 2026-09-30)
1. **robots.txt** `Disallow: /재정.html` 1줄 추가 — **승인**(재정.html=시안E_재정과 동일 잠금 페이지·기존 패턴과 일관·저위험). → `robots.proposed.txt` 를 스크립트가 REPLACE, 기존 줄 보존을 기계 확인.
2. **사진 `사진/r4/` 별도 배치** — **승인**(시안E/jubo 렌더 보존이 사진/web 덮어쓰기보다 안전).
3. **시안E_* 잔존** — 이번 라운드 그대로, **후속 티켓으로 이관 승인**(jubo 생성기 템플릿의 시안E 링크 교체는 별도).
4. **preview index canonical `https://ksmc31.kr/` 유지** — **승인**.

`--apply`·push 는 오너 「올려」 확인 후 master 가 직접 지시한다(worker 자율 실행 금지).

## 7. 실행 순서 (오너 「올려」 승인 후)
1. `bash r4/_evidence/deploy_to_live.sh` (dry-run 재확인) → 2. `bash r4/_evidence/deploy_to_live.sh --apply` → 3. 보고(커밋 해시·백업 경로) → 4. master 지시로 `git -C ksmc31 push origin main` → 5. 라이브 9페이지 200·유튜브 임베드·주보 링크 실확인.
