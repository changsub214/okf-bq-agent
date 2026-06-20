---
type: table
title: inventory_items
description: 개별 상품의 고유 일련번호(Serial Number) 성격의 재고 실물 정보 테이블
resource: bigquery://bigquery-public-data.thelook_ecommerce.inventory_items
timestamp: 2024-05-22T00:00:00Z
tags: [table, logistics, inventory]
---

# `inventory_items` 테이블 명세

## 스키마 정보

| 컬럼명 | 데이터 타입 | 설명 |
| :--- | :--- | :--- |
| **`id`** | INT64 | 개별 재고 실물 고유 ID (기본 키) |
| `product_id` | INT64 | 해당 재고가 해당하는 상품 ID (`products.id` 외래 키) |
| `created_at` | TIMESTAMP | 물류 센터에 입고된 시각 |
| `sold_at` | TIMESTAMP | 해당 재고가 판매 출고된 시각 (미판매 재고는 NULL) |
| `cost` | FLOAT64 | 입고 원가 |
| `product_category` | STRING | 상품 대분류 |
| `product_name` | STRING | 상품명 |
| `product_brand` | STRING | 브랜드명 |
| `product_retail_price` | FLOAT64 | 정가 |
| `product_department` | STRING | 대상 부서 |
| `product_sku` | STRING | SKU 코드 |
| `product_distribution_center_id` | INT64 | 보관되어 있는 물류 센터 ID (`distribution_centers.id` 외래 키) |
