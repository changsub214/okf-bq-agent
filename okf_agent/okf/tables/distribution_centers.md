---
type: table
title: distribution_centers
description: 글로벌 물류 센터의 이름 및 지리적 위경도 좌표 정보를 저장하는 테이블
resource: bigquery://bigquery-public-data.thelook_ecommerce.distribution_centers
timestamp: 2024-05-22T00:00:00Z
tags: [table, logistics, distribution-center]
---

# `distribution_centers` 테이블 명세

## 스키마 정보

| 컬럼명 | 데이터 타입 | 설명 |
| :--- | :--- | :--- |
| **`id`** | INT64 | 물류 센터 고유 ID (기본 키) |
| `name` | STRING | 물류 센터명 |
| `latitude` | FLOAT64 | 위도 좌표 |
| `longitude` | FLOAT64 | 경도 좌표 |
