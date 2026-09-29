#!/usr/bin/env bash
# deploy_to_live.sh — R4(preview r4/) → ksmc31 라이브 루트 배포 준비 스크립트
# 근거: master [R4 리뷰 종결 → 배포 준비] 2026-09-30 ③ — 백업→복사→링크 치환→로컬 검증→git add/commit 까지만.
# ★기본은 --dry-run(라이브 무변경). --apply 로만 실행. ★git push 는 이 스크립트에 없다(오너 「올려」 승인 후 master 지시).
# 규칙(deploy_notes.md 정본): 문안 창작 0 · 라이브의 jubo*·latest.json·주보목록.json·robots·CNAME·확인파일·시안E_* 무수정 ·
#      사진은 사진/r4/ 에 별도 배치(라이브 사진/web 의 같은 이름 17개와 충돌 — 시안E/jubo 렌더 보존).
set -euo pipefail

MODE="dry-run"; case "${1:-}" in --apply) MODE="apply";; ""|--dry-run) ;; *) echo "사용: $0 [--dry-run|--apply]"; exit 2;; esac
SRC="/Users/sdw79/SDWjavis/_레포/keunsaem-preview/r4"
LIVE="/Users/sdw79/SDWjavis/_레포/ksmc31"
BK_ROOT="/Users/sdw79/SDWjavis/_레포/_레포밖_보관"
TS="$(date +%Y%m%d_%H%M%S)"
BK="$BK_ROOT/ksmc31_pre_r4_$TS"
PAGES=(index.html 교회소개.html 예배안내.html 새가족.html 아카데미.html 온라인예배.html 재정.html 주보.html 칼럼.html)
STAGE="$(mktemp -d /tmp/r4_deploy_stage.XXXXXX)"
trap 'rm -rf "$STAGE"' EXIT
say(){ printf '%s\n' "$*"; }

say "== R4 → 라이브 배포 [$MODE] $TS =="
say "SRC=$SRC"; say "LIVE=$LIVE"

# 0. 전제 조건 — 두 레포 모두 추적 파일 변경 0 (라이브의 미추적 _round/ 만 허용)
LIVE_HEAD="$(git -C "$LIVE" rev-parse HEAD)"; LIVE_BR="$(git -C "$LIVE" rev-parse --abbrev-ref HEAD)"
SRC_HEAD="$(git -C "$SRC" rev-parse HEAD)"
dirty_live="$(git -C "$LIVE" status --porcelain | grep -v '^?? _round/' || true)"
dirty_src="$(git -C "$SRC" status --porcelain -- r4 | grep -v '^?? ' || true)"
[[ -z "$dirty_live" ]] || { say "중단: 라이브 레포에 미커밋 변경이 있다:"; say "$dirty_live"; exit 3; }
[[ -z "$dirty_src" ]] || { say "중단: preview r4/ 에 미커밋 변경이 있다:"; say "$dirty_src"; exit 3; }
[[ "$LIVE_BR" == "main" ]] || { say "중단: 라이브 브랜치가 main 이 아니다($LIVE_BR)"; exit 3; }
say "라이브 HEAD(배포 전)=$LIVE_HEAD ($LIVE_BR) · preview HEAD=$SRC_HEAD"

# 1. 스테이지 구성 (SRC 는 절대 수정하지 않는다 — 치환은 스테이지 사본에만)
mkdir -p "$STAGE/assets" "$STAGE/사진/r4"
for p in "${PAGES[@]}"; do [[ -f "$SRC/$p" ]] || { say "중단: $SRC/$p 없음"; exit 4; }; cp "$SRC/$p" "$STAGE/$p"; done
cp "$SRC/assets/r4.css" "$SRC/assets/tokens.css" "$STAGE/assets/"
# 참조 사진만 복사 (9페이지 src="사진/web/X" 전수)
photos="$(cat "${PAGES[@]/#/$SRC/}" | grep -o 'src="사진/web/[^"]*"' | sed 's#src="사진/web/##; s#"$##' | sort -u)"
n_photo=0; while IFS= read -r ph; do [[ -n "$ph" ]] || continue; [[ -f "$SRC/사진/web/$ph" ]] || { say "중단: 사진 없음 $ph"; exit 4; }; cp "$SRC/사진/web/$ph" "$STAGE/사진/r4/$ph"; n_photo=$((n_photo+1)); done <<< "$photos"
cp "$SRC/_evidence/sitemap.proposed.xml" "$STAGE/sitemap.xml"

# 2. 링크·경로 치환 (deploy_notes.md §1~§3 — 문안 무변경 · 경로만)
for p in "${PAGES[@]}"; do
  sed -i '' \
    -e 's#https://ksmc31\.kr/jubo_#jubo_#g' \
    -e "s#https://ksmc31\.kr/'+esc(#'+esc(#g" \
    -e 's#\.\./jubo\.html#jubo.html#g' \
    -e "s#fetch('\.\./#fetch('#g" \
    -e "s#'\.\./'+d\.#d.#g" \
    -e 's#사진/web/#사진/r4/#g' \
    "$STAGE/$p"
done

# 3. 스테이지 검증 — 잔여 경로 0 · 내부 링크 전수 실존(스테이지∪라이브) · 문안 parity(verify.py 재사용) · 재정 스크립트 동일
say "-- 검증 --"
STAGE="$STAGE" LIVE="$LIVE" SRC="$SRC" python3 - <<'PY'
import os, re, sys, json, importlib.util
from pathlib import Path
STAGE=Path(os.environ["STAGE"]); LIVE=Path(os.environ["LIVE"]); SRC=Path(os.environ["SRC"])
pages=["index","교회소개","예배안내","새가족","아카데미","온라인예배","재정","주보","칼럼"]
def code_only(raw):
    # HTML 주석과 줄머리 // JS 주석은 코드가 아니다(근거 주석에 ../·사진/web 문자열이 남는 것은 정상)
    raw=re.sub(r"<!--.*?-->","",raw,flags=re.S)
    return re.sub(r"(?m)^\s*//.*$","",raw)
# 3-0 치환 잔여 0 (코드 영역만)
residue={}
for pg in pages:
    code=code_only((STAGE/f"{pg}.html").read_text(encoding="utf-8"))
    hits=re.findall(r"https://ksmc31\.kr/jubo_|\.\./(?:jubo|latest|주보목록|칼럼목록|통독)|사진/web/",code)
    if hits: residue[pg]=hits
if residue:
    print("중단: 치환 잔여(코드 영역):", residue); sys.exit(5)
print("치환 잔여 0 (절대 jubo 링크·../데이터·사진/web — 코드 영역 기준)")
# 3-a 내부 링크·자원 실존 (스테이지 우선, 없으면 라이브) — <script> 안의 JS 문자열 템플릿('+esc(…)+')은 href 가 아니므로 제외
broken=[]; n=0
for pg in pages:
    raw=code_only((STAGE/f"{pg}.html").read_text(encoding="utf-8")); raw=re.sub(r"<script.*?</script>","",raw,flags=re.S)
    for m in re.finditer(r'(?:href|src)="([^"]+)"',raw):
        u=m.group(1)
        if u.startswith(("http://","https://","tel:","mailto:","data:")): continue
        if u.startswith("#"):
            n+=1
            if not re.search(r'id="%s"'%re.escape(u[1:]),raw): broken.append((pg,u))
            continue
        path=u.split("?")[0].split("#")[0]; n+=1
        if not ((STAGE/path).exists() or (LIVE/path).exists()): broken.append((pg,u))
print(f"내부 링크·자원 {n}건 검사 · 깨짐 {len(broken)}건", broken if broken else "")
# 3-b 문안 parity — r4 verify.py 의 text_parity 를 스테이지 루트로 재사용(출처 파일은 verify.py 안의 라이브 절대경로)
spec=importlib.util.spec_from_file_location("verify", SRC/"_evidence"/"verify.py"); v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
v.R4=STAGE
par={pg:v.text_parity(pg) for pg in pages}
bad={k:r["unmatched"] for k,r in par.items() if not r["parity"]}
print("문안 parity:", {k:r["parity"] for k,r in par.items()});
if bad: print("불일치:", bad)
# 3-c 재정 잠금 스크립트 = 라이브 시안E_재정 과 동일
a=re.findall(r"<script.*?</script>",(LIVE/"시안E_재정.html").read_text(encoding="utf-8"),flags=re.S)
b=re.findall(r"<script.*?</script>",(STAGE/"재정.html").read_text(encoding="utf-8"),flags=re.S)
print("재정 잠금 스크립트 동일:", a==b)
# 3-d index 메타 이식 확인
idx=(STAGE/"index.html").read_text(encoding="utf-8")
print("index 메타:", {"og:url":'og:url" content="https://ksmc31.kr/"' in idx, "canonical":'rel="canonical" href="https://ksmc31.kr/"' in idx, "ld+json Church":'"@type":"Church"' in idx})
ok = (not broken) and (not bad) and (a==b)
sys.exit(0 if ok else 6)
PY

# 4. 배포 목록 (무엇이 라이브에 어떻게 들어가는가)
say "-- 배포 목록 --"
for p in "${PAGES[@]}"; do if [[ -f "$LIVE/$p" ]]; then say "REPLACE  $p  ($(stat -f%z "$LIVE/$p") → $(stat -f%z "$STAGE/$p") bytes)"; else say "NEW      $p  ($(stat -f%z "$STAGE/$p") bytes)"; fi; done
for f in assets/r4.css assets/tokens.css; do [[ -f "$LIVE/$f" ]] && say "REPLACE  $f" || say "NEW      $f"; done
say "NEW      사진/r4/  ($n_photo 장 · $(du -sh "$STAGE/사진/r4" | cut -f1))"
say "REPLACE  sitemap.xml  ($(stat -f%z "$LIVE/sitemap.xml") → $(stat -f%z "$STAGE/sitemap.xml") bytes)"
say "무수정   jubo*.html · latest.json · 주보목록.json · 칼럼목록.json · 통독_*.json · robots.txt · CNAME · google*/naver* 확인파일 · 시안E_* · 사진/web/ · assets/og-jubo-2026.jpg·youtube_qr.png"
say "-- sitemap diff --"; diff "$LIVE/sitemap.xml" "$STAGE/sitemap.xml" || true

if [[ "$MODE" == "dry-run" ]]; then
  say "== DRY-RUN 종료 — 라이브 무변경 · 백업 미생성 · 커밋 없음 =="
  say "실행하려면: $0 --apply   (백업 $BK_ROOT/ksmc31_pre_r4_<ts>/ 생성 후 복사·커밋 · push 없음)"
  exit 0
fi

# 5. --apply: 백업 → 복사 → 커밋 (push 없음)
mkdir -p "$BK_ROOT"
rsync -a "$LIVE/" "$BK/"
say "백업 완료: $BK ($(du -sh "$BK" | cut -f1))"
for p in "${PAGES[@]}"; do cp "$STAGE/$p" "$LIVE/$p"; done
cp "$STAGE/assets/r4.css" "$STAGE/assets/tokens.css" "$LIVE/assets/"
mkdir -p "$LIVE/사진/r4"; cp "$STAGE/사진/r4/"* "$LIVE/사진/r4/"
cp "$STAGE/sitemap.xml" "$LIVE/sitemap.xml"
git -C "$LIVE" add -- "${PAGES[@]}" assets/r4.css assets/tokens.css 사진/r4 sitemap.xml
git -C "$LIVE" commit -q -m "R4 홈페이지 리뉴얼 라이브 배포 — 9페이지(index 교체·한글 파일명 8)·assets/r4.css·tokens.css·사진/r4(${n_photo}장)·sitemap 갱신. preview $SRC_HEAD 기준. 백업 $BK" -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
NEW_HEAD="$(git -C "$LIVE" rev-parse HEAD)"
say "== APPLY 완료 (push 없음) =="
say "라이브 커밋: $LIVE_HEAD → $NEW_HEAD"
say "되돌리기(로컬 커밋만 있을 때): git -C $LIVE reset --hard $LIVE_HEAD && git -C $LIVE clean -fd -- 사진/r4 assets/r4.css assets/tokens.css"
say "되돌리기(백업 복원): rsync -a --delete --exclude .git $BK/ $LIVE/ && git -C $LIVE status"
