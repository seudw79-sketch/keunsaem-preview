#!/usr/bin/env bash
# deploy_cedar_to_live.sh — 시더 판(preview r4/drafts/cedar/) → ksmc31 라이브 루트 배포 준비 스크립트
# 근거: master [★배포 중단 — 배포 스크립트가 시더 판을 안 가리킨다] 2026-09-30 20:3x — 기존 deploy_to_live.sh(R4 판 · SRC=r4)는 손대지 않고 복사해 새로 만듦.
# ★기본은 --dry-run(라이브 무변경). --apply 로만 실행. ★git push 는 이 스크립트에 없다(오너 「올려」 승인 후 master 지시).
# 시더가 R4 와 다른 점(전수 재작성): ①SRC=r4/drafts/cedar(루트까지 세 단 ../../../ · 사진은 두 단 ../../사진/web/) ②CSS 는 페이지 안 인라인(외부 css 0)
#   ③자원 = 사진 3장(about.jpg 흑백은 CSS · pastor.jpg · naver_map.jpg)뿐 · 유튜브는 외부 ④데이터 fetch 는 루트 상대(latest.json·주보목록·칼럼목록·통독 2)
#   ⑤LATEST_URL 절대(https://ksmc31.kr/latest.json)→상대(latest.json · cedar/_src/site.json _latest_note) ⑥검증에 오늘 규칙 전부(꼬리·머리 결손·목적지 이탈·../ 4단·첫화면 maxres)
# 규칙(deploy_notes.md 정본 유지): 문안 창작 0 · 라이브의 jubo*·latest.json·주보목록.json·robots·CNAME·확인파일·시안E_* 무수정 ·
#      사진은 사진/cedar/ 에 별도 배치(라이브 사진/web 에 같은 이름 about.jpg·pastor.jpg·naver_map.jpg 가 있어 충돌 — 시안E/jubo 렌더 보존).
set -euo pipefail

MODE="dry-run"; case "${1:-}" in --apply) MODE="apply";; ""|--dry-run) ;; *) echo "사용: $0 [--dry-run|--apply]"; exit 2;; esac
PREVIEW="/Users/sdw79/SDWjavis/_레포/keunsaem-preview"
SRC="$PREVIEW/r4/drafts/cedar"
R4EV="$PREVIEW/r4/_evidence"
LIVE="/Users/sdw79/SDWjavis/_레포/ksmc31"
BK_ROOT="/Users/sdw79/SDWjavis/_레포/_레포밖_보관"
TS="$(date +%Y%m%d_%H%M%S)"
BK="$BK_ROOT/ksmc31_pre_cedar_$TS"
PAGES=(index.html 교회소개.html 예배안내.html 새가족.html 아카데미.html 온라인예배.html 재정.html 주보.html 칼럼.html)
STAGE_ROOT="$(mktemp -d /tmp/cedar_deploy_stage.XXXXXX)"; STAGE="$STAGE_ROOT/cedar"   # 폴더명 cedar = 검사기의 시더 전용 규칙 활성 조건(R4.name=="cedar")
mkdir -p "$STAGE"
trap 'rm -rf "$STAGE_ROOT"' EXIT
say(){ printf '%s\n' "$*"; }

say "== 시더 → 라이브 배포 [$MODE] $TS =="
say "SRC=$SRC"; say "LIVE=$LIVE"

# 0. 전제 조건 — 두 레포 모두 추적 파일 변경 0 (라이브의 미추적 _round/ 만 허용) · 생성기 산출이 최신인지(빌드 재실행 결과 = 커밋본)
LIVE_HEAD="$(git -C "$LIVE" rev-parse HEAD)"; LIVE_BR="$(git -C "$LIVE" rev-parse --abbrev-ref HEAD)"
SRC_HEAD="$(git -C "$PREVIEW" rev-parse HEAD)"
dirty_live="$(git -C "$LIVE" status --porcelain | grep -v '^?? _round/' || true)"
dirty_src="$(git -C "$PREVIEW" status --porcelain -- r4/drafts/cedar r4/drafts/c/_verify.py | grep -v '^?? ' || true)"
[[ -z "$dirty_live" ]] || { say "중단: 라이브 레포에 미커밋 변경이 있다:"; say "$dirty_live"; exit 3; }
[[ -z "$dirty_src" ]] || { say "중단: preview r4/drafts/cedar 에 미커밋 변경이 있다:"; say "$dirty_src"; exit 3; }
[[ "$LIVE_BR" == "main" ]] || { say "중단: 라이브 브랜치가 main 이 아니다($LIVE_BR)"; exit 3; }
say "라이브 HEAD(배포 전)=$LIVE_HEAD ($LIVE_BR) · preview HEAD=$SRC_HEAD"
# 생성기 재실행 → 커밋본과 동일해야 한다(손편집·미재생성 차단). 생성기는 라이브 latest.json 을 받아 사본을 갱신할 수 있어 preview 루트 latest.json 변경은 허용하고 되돌린다
( cd "$SRC" && python3 _build.py >/dev/null 2>"$STAGE_ROOT/build.err" && python3 _build.py --sub >/dev/null 2>>"$STAGE_ROOT/build.err" ) || { say "중단: 생성기 실행 실패"; cat "$STAGE_ROOT/build.err"; exit 3; }
regen="$(git -C "$PREVIEW" status --porcelain -- r4/drafts/cedar | grep -v '^?? ' || true)"
git -C "$PREVIEW" checkout -q -- latest.json 2>/dev/null || true
[[ -z "$regen" ]] || { say "중단: 생성기 재실행 결과가 커밋본과 다르다(재생성 후 커밋 필요):"; say "$regen"; git -C "$PREVIEW" checkout -q -- r4/drafts/cedar; exit 3; }
say "생성기 재실행 = 커밋본 동일 · 경고: $(grep -c '★경고' "$STAGE_ROOT/build.err" || true)건"; grep '★경고' "$STAGE_ROOT/build.err" || true

# 1. 스테이지 구성 (SRC 는 절대 수정하지 않는다 — 치환은 스테이지 사본에만)
mkdir -p "$STAGE/사진/cedar"
for p in "${PAGES[@]}"; do [[ -f "$SRC/$p" ]] || { say "중단: $SRC/$p 없음"; exit 4; }; cp "$SRC/$p" "$STAGE/$p"; done
# 참조 사진만 복사 (9페이지 src="../../사진/web/X" 전수 · 실존 검사)
photos="$(cat "${PAGES[@]/#/$SRC/}" | grep -o 'src="\.\./\.\./사진/web/[^"]*"' | sed 's#src="\.\./\.\./사진/web/##; s#"$##' | sort -u)"
n_photo=0; while IFS= read -r ph; do [[ -n "$ph" ]] || continue; [[ -f "$PREVIEW/r4/사진/web/$ph" ]] || { say "중단: 사진 없음 $ph"; exit 4; }; cp "$PREVIEW/r4/사진/web/$ph" "$STAGE/사진/cedar/$ph"; n_photo=$((n_photo+1)); done <<< "$photos"
# 외부 css 참조 0 이어야 한다(시더는 인라인)
if grep -l '<link rel="stylesheet" href="[^h]' "${PAGES[@]/#/$SRC/}" >/dev/null 2>&1; then say "중단: 시더 페이지에 로컬 외부 css 참조가 있다 — 치환표에 없음"; exit 4; fi
# sitemap: 9페이지 파일명이 R4 와 같으므로 R4 제안본을 lastmod 오늘로 갱신해 사용 · robots: R4 제안본(Disallow /재정.html · Sitemap 줄)
sed "s#<lastmod>[0-9-]*</lastmod>#<lastmod>$(date +%Y-%m-%d)</lastmod>#g" "$R4EV/sitemap.proposed.xml" > "$STAGE/sitemap.xml"
cp "$R4EV/robots.proposed.txt" "$STAGE/robots.txt"
grep -qx 'Disallow: /시안E_재정.html' "$STAGE/robots.txt" && grep -qx 'Disallow: /재정.html' "$STAGE/robots.txt" && grep -qx 'Sitemap: https://ksmc31.kr/sitemap.xml' "$STAGE/robots.txt" || { say "중단: robots.proposed.txt 에 필수 3줄이 없다"; exit 4; }
while IFS= read -r line; do [[ -z "$line" ]] || grep -qxF "$line" "$STAGE/robots.txt" || { say "중단: 라이브 robots 줄이 제안본에서 사라짐: $line"; exit 4; }; done < "$LIVE/robots.txt"

# 2. 경로 치환 — 시더 전용 표(루트까지 세 단 → 루트 · 사진 두 단 → 사진/cedar/ · LATEST_URL 절대→상대 · 주보 절대 링크 https://ksmc31.kr/jubo_→상대(R4 표와 동일 · 같은 도메인 안이라 상대가 정본)). 문안 무변경 · 경로만
for p in "${PAGES[@]}"; do
  sed -i '' \
    -e 's#https://ksmc31\.kr/jubo_#jubo_#g' \
    -e "s#https://ksmc31\.kr/'+esc(#'+esc(#g" \
    -e 's#\.\./\.\./\.\./jubo\.html#jubo.html#g' \
    -e "s#fetch('\.\./\.\./\.\./#fetch('#g" \
    -e "s#'\.\./\.\./\.\./'+d\.#d.#g" \
    -e 's#\.\./\.\./사진/web/#사진/cedar/#g' \
    -e 's#var LATEST_URL="https://ksmc31\.kr/latest\.json"#var LATEST_URL="latest.json"#g' \
    "$STAGE/$p"
done

# 3. 스테이지 검증 — 치환 잔여 0(../ 자체가 0) · 내부 링크 전수 실존(스테이지∪라이브) · 문안 parity+누락 0 · 시더 규칙 전부(꼬리·머리·목적지·../4단·maxres) · 넘침 0(390/1280) · 재정 스크립트 동일
say "-- 검증 --"
STAGE="$STAGE" LIVE="$LIVE" PREVIEW="$PREVIEW" python3 - <<'PY'
import os, re, sys, json, importlib.util
from pathlib import Path
STAGE=Path(os.environ["STAGE"]); LIVE=Path(os.environ["LIVE"]); PREVIEW=Path(os.environ["PREVIEW"])
pages=["index","교회소개","예배안내","새가족","아카데미","온라인예배","재정","주보","칼럼"]
def code_only(raw): return re.sub(r"(?m)^\s*//.*$","",re.sub(r"<!--.*?-->","",raw,flags=re.S))
# 3-0 치환 잔여 0 — 라이브 루트에서 ../ 는 어떤 것도 정당하지 않다(오늘 ../ 5단 사고 계열) · 사진/web · 절대 latest URL 도 0
residue={}
for pg in pages:
    code=code_only((STAGE/f"{pg}.html").read_text(encoding="utf-8"))
    hits=re.findall(r"\.\./|사진/web/|https://ksmc31\.kr/latest\.json|https://ksmc31\.kr/jubo_",code)
    if hits: residue[pg]=sorted(set(hits))
if residue: print("중단: 치환 잔여:", residue); sys.exit(5)
print("치환 잔여 0 (../ · 사진/web · 절대 latest/jubo — 코드 영역 기준)")
# 3-a 시더 검사기 재사용(R4=스테이지 · 폴더명 cedar 라 시더 규칙 활성): 창작 0 · 누락 0 · 시더 규칙 · 내부 링크(스테이지 없으면 라이브 실존으로 보완)
spec=importlib.util.spec_from_file_location("v", PREVIEW/"r4"/"drafts"/"c"/"_verify.py"); v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
v.R4=STAGE
rules=("목적지 이탈","저장소 밖 경로","꼬리 결손","머리 결손","첫 화면 썸네일","스크립트가 hqdefault")
broken={}; par={}; comp={}; ov={}
for pg in pages:
    lk=v.links(pg)
    keep=[b for b in lk["broken"] if b.startswith(rules) or not (LIVE/b.split("?")[0].split("#")[0]).exists()]
    if keep: broken[pg]=keep
    tp=v.text_parity(pg); par[pg]=tp["parity"]
    c=v.completeness(pg); comp[pg]=c["complete"]
    if not tp["parity"]: print(f"  창작 의심 {pg}: {tp['unmatched'][:3]}")
    if not c["complete"]: print(f"  누락 {pg}: {(c['missing_blocks']+c['missing_nodes'])[:3]}")
    ov[pg]={w: v.measure(pg,w).get("overflow") for w in (390,1280)}
print("창작 0:", all(par.values()), "· 누락 0:", all(comp.values()), "· 깨진/규칙 위반:", broken if broken else "0")
print("넘침(390/1280):", {k:vv for k,vv in ov.items() if any(vv.values())} or "0")
# 3-b 재정 잠금 스크립트 = 라이브 시안E_재정 과 동일(암호 로직 불변)
a=re.findall(r"<script>.*?</script>",(LIVE/"시안E_재정.html").read_text(encoding="utf-8"),flags=re.S)
b=[s for s in re.findall(r"<script>.*?</script>",(STAGE/"재정.html").read_text(encoding="utf-8"),flags=re.S) if "SALT=" in s]
print("재정 잠금 스크립트 동일:", a==b)
# 3-c 데이터 fetch 가 루트 상대인지(라이브 파일 실존)
need=["latest.json","주보목록.json","칼럼목록.json","통독_365.json","통독_영상_덮어쓰기.json","jubo.html"]
print("루트 데이터 실존:", {n:(LIVE/n).exists() for n in need})
ok = (not broken) and all(par.values()) and all(comp.values()) and (a==b) and not any(any(vv.values()) for vv in ov.values()) and all((LIVE/n).exists() for n in need)
sys.exit(0 if ok else 6)
PY

# 4. 배포 목록
say "-- 배포 목록 --"
for p in "${PAGES[@]}"; do if [[ -f "$LIVE/$p" ]]; then say "REPLACE  $p  ($(stat -f%z "$LIVE/$p") → $(stat -f%z "$STAGE/$p") bytes)"; else say "NEW      $p  ($(stat -f%z "$STAGE/$p") bytes)"; fi; done
say "NEW      사진/cedar/  ($n_photo 장 · $(du -sh "$STAGE/사진/cedar" | cut -f1)) — $(echo "$photos" | tr '\n' ' ')"
say "REPLACE  sitemap.xml  ($(stat -f%z "$LIVE/sitemap.xml") → $(stat -f%z "$STAGE/sitemap.xml") bytes)"
say "REPLACE  robots.txt  (Disallow: /재정.html 포함 제안본)"
say "무수정   jubo*.html · latest.json · 주보목록.json · 칼럼목록.json · 통독_*.json · CNAME · google*/naver* 확인파일 · 시안E_* · 사진/web/ · assets/ (r4.css·tokens.css 포함 — 시더는 안 씀)"
say "-- sitemap diff --"; diff "$LIVE/sitemap.xml" "$STAGE/sitemap.xml" || true
say "-- robots diff --"; diff "$LIVE/robots.txt" "$STAGE/robots.txt" || true

if [[ "$MODE" == "dry-run" ]]; then
  say "== DRY-RUN 종료 — 라이브 무변경 · 백업 미생성 · 커밋 없음 =="
  say "실행하려면: $0 --apply   (백업 $BK_ROOT/ksmc31_pre_cedar_<ts>/ 생성 후 복사·커밋 · push 없음)"
  exit 0
fi

# 5. --apply: 백업 → 복사 → 커밋 (push 없음)
mkdir -p "$BK_ROOT"
rsync -a "$LIVE/" "$BK/"
say "백업 완료: $BK ($(du -sh "$BK" | cut -f1))"
for p in "${PAGES[@]}"; do cp "$STAGE/$p" "$LIVE/$p"; done
mkdir -p "$LIVE/사진/cedar"; cp "$STAGE/사진/cedar/"* "$LIVE/사진/cedar/"
cp "$STAGE/sitemap.xml" "$LIVE/sitemap.xml"
cp "$STAGE/robots.txt" "$LIVE/robots.txt"
git -C "$LIVE" add -- "${PAGES[@]}" 사진/cedar sitemap.xml robots.txt
git -C "$LIVE" commit -q -m "시더 판 홈페이지 라이브 배포 — 9페이지(index 교체·한글 파일명 8)·사진/cedar(${n_photo}장)·sitemap 갱신·robots Disallow /재정.html. preview $SRC_HEAD 기준. 백업 $BK" -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
NEW_HEAD="$(git -C "$LIVE" rev-parse HEAD)"
say "== APPLY 완료 (push 없음) =="
say "라이브 커밋: $LIVE_HEAD → $NEW_HEAD"
say "되돌리기(로컬 커밋만 있을 때): git -C $LIVE reset --hard $LIVE_HEAD && git -C $LIVE clean -fd -- 사진/cedar"
say "되돌리기(백업 복원): rsync -a --delete --exclude .git $BK/ $LIVE/ && git -C $LIVE status"
