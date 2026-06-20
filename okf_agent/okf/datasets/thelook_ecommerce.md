---
type: dataset
title: The Look E-commerce Public Dataset
description: BigQuery 공개 데이터세트인 thelook_ecommerce의 메타데이터 명세입니다.
resource: bigquery://bigquery-public-data.thelook_ecommerce
timestamp: 2024-05-22T00:00:00Z
tags: [dataset, public-data, ecommerce]
---

# The Look E-commerce 공개 데이터세트 메타데이터

- **데이터셋 위치**: `bigquery-public-data.thelook_ecommerce`
- **설명**: 웹/앱 로그, 가상 사용자 프로필, 주문 내역, 재고 및 물류 센터 정보를 포함하는 가상의 의류 이커머스 데이터셋입니다. R2G 프로퍼티 그래프 구축의 기본 데이터 소스입니다.

## 포함 테이블 목록
-   [users](../tables/users.md) - 서비스에 가입된 가상 사용자 프로필 정보.
-   [products](../tables/products.md) - 판매 중인 상품 카탈로그 및 단가 정보.
-   [orders](../tables/orders.md) - 사용자가 발생시킨 주문 정보 (헤더).
-   [order_items](../tables/order_items.md) - 주문 상세 정보 (상품 매핑 및 판매가).
-   [distribution_centers](../tables/distribution_centers.md) - 전 세계 물류 센터 위치 정보.
-   [inventory_items](../tables/inventory_items.md) - 물류 센터에 입고된 개별 재고 아이템 내역.
-   [events](../tables/events.md) - 웹/앱 상에서 수집된 사용자 행동 로그.
