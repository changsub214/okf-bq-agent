---
type: queries
title: Recommended GQL & Hybrid Queries for R2G Graph
description: R2G 그래프 상에서 비즈니스 인사이트를 추출하기 위한 GQL 쿼리 및 SQL-GQL 융합 분석 템플릿입니다.
resource: bigquery://YOUR_PROJECT_ID.ecommerce.R2G
timestamp: 2024-05-23T00:00:00Z
tags: [queries, gql, hybrid-analysis]
---

# R2G 그래프 추천 GQL 및 SQL+GQL 융합 쿼리

본 문서는 R2G 프로퍼티 그래프 상에서 관계 데이터 네트워크를 빠르게 탐색하기 위해 사용하는 GQL(Graph Query Language) 문 및 SQL과의 하이브리드(융합) 분석 쿼리 템플릿입니다.

---

## 1. 표준 GQL 패턴 (Standard GQL Patterns)

### 패턴 A: 특정 사용자의 전체 구매 상품 추적
사용자 노드(`User`)에서 생성한 주문(`Order`)을 거쳐 개별 재고 실물(`InventoryItem`)과 최종 상품 카탈로그(`Product`) 정보까지 도달하는 그래프 트래버설 쿼리입니다.

```sql
SELECT * FROM GRAPH_TABLE(
  `YOUR_PROJECT_ID.ecommerce.R2G`
  MATCH (u:User)-[:PLACES]->(o:`Order`)-[:CONTAINS_ITEM]->(i:InventoryItem)-[:IS_PRODUCT]->(p:Product)
  WHERE u.id = @target_user_id
  COLUMNS (
    u.id AS user_id,
    o.order_id AS order_id,
    o.status AS order_status,
    p.name AS product_name,
    p.retail_price AS price
  )
);
```

### 패턴 B: 물류센터별 공급 상품 및 실물 재고 현황 매핑
특정 물류센터(`DistributionCenter`)에 입고 보관되어 있는 재고 실물(`InventoryItem`)을 통해 해당 상품(`Product`) 정보와 물류센터 매핑 관계를 확인합니다.

```sql
SELECT * FROM GRAPH_TABLE(
  `YOUR_PROJECT_ID.ecommerce.R2G`
  MATCH (p:Product)-[:SUPPLIED_BY]->(d:DistributionCenter),
        (i:InventoryItem)-[:STOCKED_AT]->(d)
  COLUMNS (
    p.id AS product_id,
    p.name AS product_name,
    d.name AS dc_name,
    i.id AS inventory_item_id
  )
)
LIMIT 100;
```

---

## 2. SQL + GQL 융합 분석 예제 (Hybrid Insight Queries)

`GRAPH_TABLE`을 통해 다대다(M:N) 경로와 다단계 조인을 선형 그래프 탐색(GQL)으로 가볍게 연결하고, 그 추출 결과에 SQL의 강력한 그룹화(`GROUP BY`) 및 집계 기능을 접목하여 고차원 비즈니스 인사이트를 확보합니다.

### 융합 예제 1: 카테고리별 실질 구매 고유 사용자 수 및 매출 비중 (이커머스 핵심 성장 지표)
-   **목적**: 단순 주문 건수 위주 분석을 탈피하여, 실제 고유 활성 구매자(`User`) 분포와 카테고리별 기여도를 평가합니다.
-   **GQL 역할**: `User - Order - Order_Item - Product` 간 복잡한 4단계 조인을 선형 탐색으로 통합.
-   **SQL 역할**: 카테고리별 고유 구매자 집계 및 내림차순 정렬.

```sql
SELECT
  product_category,
  COUNT(DISTINCT user_id) AS unique_buyers,
  COUNT(order_id) AS total_orders,
  ROUND(SUM(sale_price), 2) AS gross_revenue
FROM GRAPH_TABLE(
  `YOUR_PROJECT_ID.ecommerce.R2G`
  MATCH (u:User)-[:PLACES]->(o:`Order`)-[:CONTAINS_ITEM]->(i:InventoryItem)-[:IS_PRODUCT]->(p:Product)
  -- 주문이 정상 배송 완료되거나 처리 중인 거래만 분석 대상
  WHERE o.status IN ('Shipped', 'Delivered', 'Complete', 'Processing')
  COLUMNS (
    u.id AS user_id,
    o.order_id AS order_id,
    p.category AS product_category,
    p.retail_price AS sale_price
  )
)
GROUP BY product_category
ORDER BY unique_buyers DESC;
```

### 융합 예제 2: 글로벌 물류 센터별 평균 배송 소요 시간 (Logistics Lead Time)
-   **목적**: 상품 공급 물류센터(`DistributionCenter`) 위치 및 주문 상태별 실제 배송 소요일수(배송 시작 ~ 수령 완료)의 실비를 계산하여 물류 병목 현상을 파악합니다.
-   **GQL 역할**: 주문(`Order`)에 묶인 품목(`InventoryItem`)이 실제 보관된 물류센터(`DistributionCenter`) 추적.
-   **SQL 역할**: 날짜 시간 차이(DATEDIFF) 계산 및 물류센터별 평균 리드타임 집계.

```sql
SELECT
  dc_name,
  COUNT(DISTINCT order_id) AS delivered_orders_count,
  ROUND(AVG(TIMESTAMP_DIFF(delivered_at, shipped_at, HOUR) / 24.0), 2) AS avg_delivery_lead_time_days
FROM GRAPH_TABLE(
  `YOUR_PROJECT_ID.ecommerce.R2G`
  MATCH (o:`Order`)-[:CONTAINS_ITEM]->(i:InventoryItem)-[:STOCKED_AT]->(d:DistributionCenter)
  WHERE o.status = 'Delivered' 
    AND o.shipped_at IS NOT NULL 
    AND o.delivered_at IS NOT NULL
  COLUMNS (
    o.order_id AS order_id,
    d.name AS dc_name,
    o.shipped_at AS shipped_at,
    o.delivered_at AS delivered_at
  )
)
GROUP BY dc_name
ORDER BY avg_delivery_lead_time_days ASC;
```

### 융합 예제 3: 이탈 고객 분석 - 장바구니 담기 후 구매 미완료 세션 패턴
-   **목적**: 웹 로그(`Event`) 데이터 상에서 '장바구니 담기'는 했으나 실제 '구매 완료'로 전환되지 않고 이탈한 세션들의 사용자 유입 채널 분석.
-   **GQL 역할**: 사용자가 수행한 웹 이벤트(`Event`) 경로 확인.
-   **SQL 역할**: 세션 기준 분석 및 마케팅 채널(Traffic Source)별 이탈 카운트 집계.

```sql
SELECT
  traffic_source,
  COUNT(DISTINCT session_id) AS abandoned_sessions_count
FROM GRAPH_TABLE(
  `YOUR_PROJECT_ID.ecommerce.R2G`
  MATCH (u:User)-[:PERFORMED_EVENT]->(e:Event)
  WHERE e.event_type = 'cart'
  COLUMNS (
    u.id AS user_id,
    u.traffic_source AS traffic_source,
    e.session_id AS session_id
  )
)
-- 동일 세션에서 구매(purchase) 이벤트가 발생하지 않은 세션만 필터링
WHERE session_id NOT IN (
  SELECT DISTINCT session_id
  FROM GRAPH_TABLE(
    `YOUR_PROJECT_ID.ecommerce.R2G`
    MATCH (u:User)-[:PERFORMED_EVENT]->(e:Event)
    WHERE e.event_type = 'purchase'
    COLUMNS (e.session_id AS session_id)
  )
)
GROUP BY traffic_source
ORDER BY abandoned_sessions_count DESC;
```
