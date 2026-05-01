"""
청주잇츠 DB 적재 스크립트

사용 시나리오
  1) 카카오 API 수집 결과를 restaurants 테이블에 bulk insert
     : python db_loader.py --mode insert --json data/restaurants.json

  2) 랭킹 모델 CSV(kakao_id + rank_score + is_franchise)로 점수만 upsert
     : python db_loader.py --mode rank --csv data/rank_scores.csv

CSV 포맷 (rank 모드):
  kakao_id,rank_score,is_franchise
  12345678,0.8321,0
  ...
"""

import argparse
import csv
import json
import sys
import mysql.connector
from mysql.connector import Error

# ──────────────────────────────────────────────
# DB 접속 정보 (운영 시 환경변수로 분리 권장)
# ──────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "0320",
    "database": "cjeats",
    "charset":  "utf8mb4",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ──────────────────────────────────────────────
# 1. 카카오 API 수집 데이터 → restaurants 테이블 적재
# ──────────────────────────────────────────────
INSERT_SQL = """
INSERT INTO restaurants
    (kakao_id, name, category, address, phone, place_url, lat, lng,
     price_range, rank_score, is_franchise)
VALUES
    (%(kakao_id)s, %(name)s, %(category)s, %(address)s,
     %(phone)s, %(place_url)s, %(lat)s, %(lng)s,
     %(price_range)s, %(rank_score)s, %(is_franchise)s)
ON DUPLICATE KEY UPDATE
    name         = VALUES(name),
    category     = VALUES(category),
    address      = VALUES(address),
    phone        = VALUES(phone),
    place_url    = VALUES(place_url),
    lat          = VALUES(lat),
    lng          = VALUES(lng),
    price_range  = VALUES(price_range),
    rank_score   = COALESCE(VALUES(rank_score), rank_score),
    is_franchise = VALUES(is_franchise)
"""

def insert_restaurants(rows: list[dict]) -> None:
    """카카오 API 결과 리스트를 DB에 bulk insert (중복 kakao_id는 정보 갱신)."""
    required = {"kakao_id", "name", "lat", "lng"}
    for row in rows:
        row.setdefault("category",    None)
        row.setdefault("address",     None)
        row.setdefault("phone",       None)
        row.setdefault("place_url",   None)
        row.setdefault("price_range", None)
        row.setdefault("rank_score",  None)
        row.setdefault("is_franchise", 0)
        if not required.issubset(row):
            raise ValueError(f"필수 필드 누락: {required - row.keys()}")

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.executemany(INSERT_SQL, rows)
        conn.commit()
        print(f"[insert] {cursor.rowcount}건 처리 완료 (신규 삽입 + 갱신 합산)")
    except Error as e:
        conn.rollback()
        print(f"[insert] 오류 발생, 롤백: {e}", file=sys.stderr)
        raise
    finally:
        cursor.close()
        conn.close()


# ──────────────────────────────────────────────
# 2. 랭킹 CSV → rank_score / is_franchise Upsert
# ──────────────────────────────────────────────
RANK_UPSERT_SQL = """
INSERT INTO restaurants (kakao_id, name, lat, lng, rank_score, is_franchise)
VALUES (%(kakao_id)s, '', 0, 0, %(rank_score)s, %(is_franchise)s)
ON DUPLICATE KEY UPDATE
    rank_score   = VALUES(rank_score),
    is_franchise = VALUES(is_franchise)
"""
# name/lat/lng에 더미값을 넣지만, ON DUPLICATE KEY이므로 kakao_id가 이미
# 존재하는 행에 한해 rank_score·is_franchise만 실제로 업데이트된다.

def upsert_rank_scores_from_csv(csv_path: str) -> None:
    """
    랭킹 모델 CSV를 읽어 rank_score와 is_franchise를 upsert.

    CSV 필수 컬럼: kakao_id, rank_score
    CSV 선택 컬럼: is_franchise (없으면 0으로 처리)
    """
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line in reader:
            rows.append({
                "kakao_id":     line["kakao_id"].strip(),
                "rank_score":   float(line["rank_score"]),
                "is_franchise": int(line.get("is_franchise", 0)),
            })

    if not rows:
        print("[rank] CSV가 비어 있습니다.")
        return

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.executemany(RANK_UPSERT_SQL, rows)
        conn.commit()
        updated = cursor.rowcount
        print(f"[rank] {len(rows)}건 읽음 → {updated}건 upsert 완료")
    except Error as e:
        conn.rollback()
        print(f"[rank] 오류 발생, 롤백: {e}", file=sys.stderr)
        raise
    finally:
        cursor.close()
        conn.close()


# ──────────────────────────────────────────────
# CLI 진입점
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="청주잇츠 DB 적재 도구")
    parser.add_argument("--mode", choices=["insert", "rank"], required=True,
                        help="insert: 카카오 JSON 적재 | rank: 랭킹 CSV upsert")
    parser.add_argument("--json", help="카카오 API 수집 결과 JSON 파일 경로 (insert 모드)")
    parser.add_argument("--csv",  help="랭킹 점수 CSV 파일 경로 (rank 모드)")
    args = parser.parse_args()

    if args.mode == "insert":
        if not args.json:
            parser.error("--json 파일 경로를 지정하세요.")
        with open(args.json, encoding="utf-8") as f:
            data = json.load(f)
        insert_restaurants(data)

    elif args.mode == "rank":
        if not args.csv:
            parser.error("--csv 파일 경로를 지정하세요.")
        upsert_rank_scores_from_csv(args.csv)


if __name__ == "__main__":
    main()
