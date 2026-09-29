# R4 라이브 배포 치환 규칙 (preview → ksmc31 라이브)

작성: worker · 2026-09-29 · master 회신(주보 링크 정책) 근거

## 1. 주보 링크 (master 회신 ①)
- preview 의 r4/주보.html 은 `주보목록.json` 7건 전부를 **라이브 절대링크** `https://ksmc31.kr/jubo_YYMMDD.html?v=YYYYMMDD` 로 건다(preview 레포에 없는 260920·260927 파일은 복사하지 않는다).
- 라이브(ksmc31 레포 루트)로 옮길 때 치환: `https://ksmc31.kr/jubo_` → `jubo_` (상대링크). 홈의 `../jubo.html?v=…` 도 `jubo.html?v=…` 로.
  ```
  sed -i '' 's#https://ksmc31\.kr/jubo_#jubo_#g; s#\.\./jubo\.html#jubo.html#g' r4/*.html
  ```

## 2. 데이터 파일 경로
- r4/ 는 preview 루트의 하위 폴더라 `latest.json`·`통독_365.json`·`통독_영상_덮어쓰기.json`·`주보목록.json`·`칼럼목록.json` 을 `../` 로 읽는다.
- 라이브 루트에 r4 파일들을 그대로 두면 `../` → `./` 로 치환:
  ```
  sed -i '' "s#fetch('\.\./#fetch('#g" r4/*.html
  ```
- preview 의 latest.json·주보목록.json 은 라이브보다 오래됨(2026-09-13 vs 09-27). preview 에서 런타임 값이 옛날로 보이는 것은 데이터 파일 차이이지 페이지 결함이 아니다.

## 3. 사진
- r4/사진/web/ 은 ksmc31/사진/web 의 축소본(원본 무수정). 라이브에서는 그대로 `사진/web/` 하위로 옮겨 쓰거나 원본 폴더 파일명으로 되돌린다(대조표 `r4/사진/web/_출처.json`).

## 4. 무수정 대상(preview·라이브 공통)
- 기존 index.html·jubo*.html·latest.json·시안R3_*·시안E_* 는 손대지 않는다. R4 는 r4/ 폴더 안에서만 완결된다.
