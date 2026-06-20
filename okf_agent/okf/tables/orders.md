---
type: table
title: orders
description: 주문 마스터 헤더 테이블. 개별 주문의 상태 및 결제 일시 기록.
resource: bigquery://bigquery-public-data.thelook_ecommerce.orders
timestamp: 2024-05-22T00:00:00Z
tags: [table, sales, order]
---

# `orders` 테이블 명세

## 스키마 정보

| 컬럼명 | 데이터 타입 | 설명 |
| :--- | :--- | :--- |
| **`order_id`** | INT64 | 주문 고유 ID (기본 키) |
| `user_id` | INT64 | 주문한 사용자 ID |
| `status` | STRING | 주문 처리 상태 (Created, Processing, Shipped, Delivered, Cancelled, Returned 등) |
| `gender` | STRING | 주문자의 성별 |
| `created_at` | TIMESTAMP | 주문 결제/생성 일시 |
| `returned_at` | TIMESTAMP | 반품 접수 및 완료 일시 (반품이 아닐 경우 NULL) |
| `shipped_at` | TIMESTAMP | 물류 센터 출고 및 배송 시작 일시 |
| `delivered_at` | TIMESTAMP | 고객 수령 완료 일시 |
| `num_of_item` | INT64 | 해당 주문에 포함된 총 아이템 개수 |
