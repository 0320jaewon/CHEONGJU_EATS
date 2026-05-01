-- 청주잇츠 restaurants 테이블
-- price_range: 프론트 가격대 필터(low/mid/high)와 1:1 매핑
-- rank_score : ML 랭킹 모델 출력값 (0.0 ~ 1.0)
-- is_franchise: 로컬 맛집 필터링용 프랜차이즈 여부

CREATE TABLE IF NOT EXISTS restaurants (
    id           BIGINT          AUTO_INCREMENT  PRIMARY KEY,
    kakao_id     VARCHAR(20)     NOT NULL        UNIQUE          COMMENT '카카오 장소 고유 ID',
    name         VARCHAR(100)    NOT NULL                        COMMENT '업소명',
    category     VARCHAR(50)                                     COMMENT '음식점 분류 (한식/중식 등)',
    address      VARCHAR(200)                                    COMMENT '도로명 주소',
    phone        VARCHAR(20)                                     COMMENT '전화번호',
    place_url    VARCHAR(300)                                    COMMENT '카카오맵 상세 링크',
    lat          DECIMAL(10, 7)  NOT NULL                        COMMENT '위도',
    lng          DECIMAL(10, 7)  NOT NULL                        COMMENT '경도',
    price_range  ENUM('low', 'mid', 'high')  DEFAULT NULL        COMMENT '가격대: low=~1만원 / mid=1~2만원 / high=2만원+',
    rank_score   DECIMAL(6, 4)               DEFAULT NULL        COMMENT '랭킹 모델 점수 (0.0000 ~ 1.0000)',
    is_franchise TINYINT(1)      NOT NULL    DEFAULT 0           COMMENT '프랜차이즈 여부 (0=로컬, 1=프랜차이즈)',
    created_at   DATETIME        NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME        NOT NULL    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_category    (category),
    INDEX idx_price_range (price_range),
    INDEX idx_rank_score  (rank_score DESC),
    INDEX idx_location    (lat, lng)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
