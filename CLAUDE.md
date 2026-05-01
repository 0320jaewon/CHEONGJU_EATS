# 📍 청주잇츠 (Cheongju Eats) - 프로젝트 가이드북

본 문서는 충북대학교 개신프론티어 Ⅱ 과제인 '청주 지역 맛집 데이터 시각화 및 랭킹 서비스' **청주잇츠** 프로젝트의 인수인계 및 개발 컨텍스트 유지를 위한 문서입니다.

---

## 🚀 1. 프로젝트 개요 (Project Overview)
- **목표**: 청주 지역의 맛집 데이터를 수집, 정제하여 지도 기반으로 시각화하고 사용자에게 최적화된 맛집 랭킹 정보를 제공하는 웹 서비스.
- **주요 가치**: 단순 정보 제공을 넘어, 프랜차이즈를 제외한 '로컬 맛집' 중심의 랭킹 모델 적용.

## 👥 2. 팀 구성 및 역할 (Team & Roles)
- **박재원 (Data Engineer)**: 데이터 수집 및 정제, DB 적재 프로세스 구축. *(로컬 MySQL 환경 세팅 완료)*
- **김상민 (Frontend & ML)**: UI/UX 디자인, 카카오 지도 API 연동, 맛집 랭킹 알고리즘 및 모델 개발.
- **이재빈 (Backend)**: Spring Boot 기반 REST API 서버 구축 및 DB 아키텍처 설계.

## 🛠️ 3. 기술 스택 (Tech Stack)
- **Backend**: ~~Spring Boot~~ → **FastAPI + Uvicorn** (Python), SQLAlchemy, PyMySQL, MySQL
- **Frontend**: HTML5, Tailwind CSS CDN, Vanilla JavaScript (fetch API), Kakao Maps SDK
- **Data Engineering**: Python 3.x, Kakao Local API (REST API), mysql-connector-python
- **DB 스키마**: `schema.sql` — `restaurants` 테이블 설계 완료 (price_range / rank_score / is_franchise 포함)
- **DB 적재**: `db_loader.py` — insert 모드(카카오 JSON) / rank 모드(랭킹 CSV) 지원
- **Repository**: [GitHub Link](https://github.com/jabsbin/project.git)

## ✅ 4. 현재 진행 현황 (Current Status)
### 🔹 Backend (FastAPI) — 2026-04-29 완성
- [x] **FastAPI 서버 구축 완료**: `main.py` — SQLAlchemy + PyMySQL로 MySQL 직접 연결.
- [x] **`GET /restaurants`** 엔드포인트 구현 완료 — DB 전체 목록 JSON 반환, API 응답 확인 완료.
- [x] **`GET /`** 루트 경로 → `static/index.html` FileResponse 반환 설정 완료.
- [x] **정적 파일 서빙**: `/static` 경로에 StaticFiles 마운트 완료.
- [x] **절대 경로 처리**: `BASE_DIR = Path(__file__).parent` 적용 — 실행 위치 무관하게 동작.
- [x] **포트 8080으로 서버 정상 구동 확인** (`uvicorn main:app --reload --port 8080`).
- [x] MySQL `restaurants` 초기 테이블 설계 완료.

### 🔹 Frontend (`static/index.html`) — 2026-04-29 완성
- [x] **프론트엔드 완성**: `static/index.html` 신규 생성, `/restaurants` API fetch 연동.
- [x] **디자인**: Tailwind CSS CDN + 크림/앰버 톤 따뜻한 푸드 감성 카드 UI.
- [x] **카드 레이아웃**: 식당 이름, 카테고리 배지(색상 구분), 주소(핀 아이콘), 전화번호(클릭 통화), 카카오맵 링크.
- [x] **카테고리 필터**: 전체/한식/중식/일식/양식/카페/치킨/분식 버튼 필터링.
- [x] **실시간 검색**: 가게명·주소 검색 (200ms 디바운스).
- [x] **UX**: 카드 호버 애니메이션, 스켈레톤 로딩, 빈 결과 안내, 로딩 바.
- [x] **반응형**: 1열(모바일) → 2열(태블릿) → 3~4열(데스크톱) 그리드.
- [x] **기존 `homepage.html`**: 카카오 지도+클러스터링+길찾기 포함 고급 UI — 별도 보존.

### 🔹 Data & DB 환경
- [x] `collect_restaurants.py`: 카카오 로컬 API 기반 데이터 수집 스크립트 완성.
- [x] `test_kakao.py`: API 호출 테스트 완료.
- [x] `schema.sql`: `restaurants` 테이블에 `price_range`, `rank_score`, `is_franchise` 컬럼 추가 및 확정.
- [x] `db_loader.py`: INSERT_SQL 및 파이썬 로직을 확장하여 신규 3개 필드 일괄 적재(INSERT/UPDATE) 지원. `.env` 파일 기반 비밀번호 관리 적용.
- [x] `dummy_restaurants.json`: 충북대 근처 가상 식당 5건 — 로컬 테스트용 더미 데이터 생성 완료.
- [x] **MySQL 8.0 설치 완료**: root 비밀번호 설정, `cjeats` 데이터베이스 생성, `utf8mb4` 인코딩 설정 완료.
- [x] **DB 테이블 생성 완료**: `restaurants` 테이블 (14개 컬럼) 생성 완료.
- [x] **더미 데이터 적재 성공**: `dummy_restaurants.json` 5건(충대 순대국밥 등) DB INSERT 검증 완료.
- [ ] 랭킹 모델 연동을 위한 9,700개 음식점 데이터 필터링 진행 중 (상위 30% 선정 중).

## 🖥️ 5. 서버 실행 방법
```bash
# cjeats 폴더에서 실행
cd C:\Users\박재원\Desktop\cjeats
uvicorn main:app --reload --port 8080

# 접속 주소
# 프론트엔드: http://127.0.0.1:8080/
# API:        http://127.0.0.1:8080/restaurants
```
> **주의**: 8000번 포트는 이전 프로세스가 점유할 수 있으므로 8080 포트 사용.

## 📋 6. 향후 과제 (Upcoming Tasks)
### 1순위: 실제 카카오 수집 데이터 적재
- `collect_restaurants.py`로 수집한 실제 카카오 데이터를 `db_loader.py --mode insert`로 DB에 적재.
- `/restaurants` API로 실데이터 카드 렌더링 확인.

### 2순위: 백엔드 API 고도화
- 필터링(카테고리, 가격대), 정렬(거리순, 랭킹순), 페이지네이션 쿼리 파라미터 처리.
- `homepage.html`의 `/api/restaurants` 엔드포인트(bbox, page, limit 등) 구현 및 연동.

### 3순위: 기능 고도화
- **상세 팝업**: 카드 클릭 시 상세 정보 모달 연동.
- **카카오 지도**: `homepage.html` 지도 뷰와 `index.html` 카드 뷰 통합 또는 탭 전환.
- **랭킹 모델 연동**: ML 모델 출력 CSV → `db_loader.py --mode rank` 파이프라인 실제 실행.

## 🗄️ 6. 데이터베이스 구조 (Database Schema)
`schema.sql` 기준 `restaurants` 테이블 확정 컬럼:

| 컬럼 | 타입 | 설명 |
|---|---|---|
| `kakao_id` | VARCHAR(20) UNIQUE | 카카오 장소 고유 ID |
| `name` | VARCHAR(100) | 업소명 |
| `category` | VARCHAR(50) | 음식점 분류 (한식/중식 등) |
| `address` | VARCHAR(200) | 도로명 주소 |
| `phone` | VARCHAR(20) | 전화번호 |
| `place_url` | VARCHAR(300) | 카카오맵 상세 링크 |
| `lat` / `lng` | DECIMAL(10,7) | 위경도 좌표 |
| `price_range` | ENUM('low','mid','high') | 가격대 (low=~1만원 / mid=1~2만원 / high=2만원+) |
| `rank_score` | DECIMAL(6,4) | 랭킹 모델 점수 (0.0000~1.0000) |
| `is_franchise` | TINYINT(1) | 프랜차이즈 여부 (0=로컬, 1=프랜차이즈) |

## 🔧 7. 주요 파일 구조
```
cjeats/
├── main.py                 # FastAPI 서버 (루트→index.html, /restaurants API)
├── static/
│   └── index.html          # 프론트엔드 메인 UI (Tailwind 카드 뷰)
├── homepage.html           # 카카오 지도+길찾기 고급 UI (별도 보존)
├── schema.sql              # DB 테이블 정의
├── db_loader.py            # 데이터 적재 스크립트
└── dummy_restaurants.json  # 로컬 테스트용 더미 데이터
```

## 🔧 8. 주요 스크립트 사용법

```bash
# 카카오 JSON 데이터 DB 적재 (insert 모드)
python db_loader.py --mode insert --json data/restaurants.json

# 랭킹 모델 CSV upsert (rank 모드)
python db_loader.py --mode rank --csv data/rank_scores.csv

# 더미 데이터로 로컬 테스트
python db_loader.py --mode insert --json dummy_restaurants.json
```

---
## 🔐 9. 환경 변수 및 보안 설정

- DB 비밀번호는 `.env` 파일로 관리. `db_loader.py`에서 `python-dotenv`로 로드.
- `.env` 파일은 `.gitignore`에 추가하여 GitHub에 커밋되지 않도록 관리.
- `.env` 예시:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=****
DB_NAME=cjeats
```

---
*마지막 업데이트: 2026-04-29 — FastAPI 서버 + 프론트엔드 카드 UI 완성*
