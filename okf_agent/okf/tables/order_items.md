---
type: table
title: order_items
description: 주문별 상세 품목 및 실제 판매가, 환불 상태 등을 저장하는 중간 매핑 테이블
resource: bigquery://bigquery-public-data.thelook_ecommerce.order_items
timestamp: 2024-05-22T00:00:00Z
tags: [table, sales, order-item]
---

# `order_items` 테이블 명세

## 스키마 정보

| 컬럼명 | 데이터 타입 | 설명 |
| :--- | :--- | :--- |
| **`id`** | INT64 | 주문 아이템 고유 ID (기본 키) |
| `order_id` | INT64 | 연관된 주문 ID (`orders.order_id` 외래 키) |
| `user_id` | INT64 | 구매한 사용자 ID (`users.id` 외래 키) |
| `product_id` | INT64 | 구매한 상품 ID (`products.id` 외래 키) |
| `inventory_item_id` | INT64 | 출고 처리된 개별 재고 물품 ID (`inventory_items.id` 외래 키) |
| `status` | STRING | 품목별 처리 상태 (Processing, Shipped, Delivered, Returned, Cancelled) |
| `created_at` | TIMESTAMP | 주문 품목 생성 일시 |
| `shipped_at` | TIMESTAMP | 품목 출고 일시 |
| `delivered_at` | TIMESTAMP | 품목 수령 일시 |
| `returned_at` | TIMESTAMP | 품목 반품/환불 일시 |
| `sale_price` | FLOAT64 | 실제 고객이 지불한 판매가 (할인 적용가) |
