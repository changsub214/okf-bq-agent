---
type: table
title: users
description: 이커머스 서비스 가입 고객의 데모그래픽 및 지리 정보 테이블
resource: bigquery://bigquery-public-data.thelook_ecommerce.users
timestamp: 2024-05-22T00:00:00Z
tags: [table, demographics, customer]
---

# `users` 테이블 명세

## 스키마 정보

| 컬럼명 | 데이터 타입 | 설명 |
| :--- | :--- | :--- |
| **`id`** | INT64 | 사용자 고유 ID (기본 키) |
| `first_name` | STRING | 이름 |
| `last_name` | STRING | 성 |
| `email` | STRING | 이메일 주소 |
| `age` | INT64 | 나이 |
| `gender` | STRING | 성별 (M / F) |
| `state` | STRING | 거주 주 (State) |
| `street_address` | STRING | 도로명 주소 |
| `postal_code` | STRING | 우편번호 |
| `city` | STRING | 거주 도시 |
| `country` | STRING | 거주 국가 |
| `latitude` | FLOAT64 | 위도 좌표 |
| `longitude` | FLOAT64 | 경도 좌표 |
| `traffic_source` | STRING | 가입 유입 채널 (Search, Organic, Facebook, Email 등) |
| `created_at` | TIMESTAMP | 계정 생성 일시 |
