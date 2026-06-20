---
type: table
title: products
description: 판매 대상 상품 목록 및 제조사, 카테고리, 소비자가 정보 테이블
resource: bigquery://bigquery-public-data.thelook_ecommerce.products
timestamp: 2024-05-22T00:00:00Z
tags: [table, catalog, product]
---

# `products` 테이블 명세

## 스키마 정보

| 컬럼명 | 데이터 타입 | 설명 |
| :--- | :--- | :--- |
| **`id`** | INT64 | 상품 고유 ID (기본 키) |
| `cost` | FLOAT64 | 원가 |
| `category` | STRING | 상품 카테고리 (Jeans, Sweaters, Swim 등) |
| `name` | STRING | 상품명 |
| `brand` | STRING | 브랜드명 |
| `retail_price` | FLOAT64 | 정가 (소비자 판매가) |
| `department` | STRING | 대상 부서 (Men / Women) |
| `sku` | STRING | 재고 관리 코드 (SKU) |
| `distribution_center_id` | INT64 | 상품이 속해있는 기본 물류 센터 ID |
