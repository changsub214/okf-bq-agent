---
type: table
title: events
description: 서비스 플랫폼(웹/앱) 내에서 발생하는 행동 로그 및 유입 경로 테이블
resource: bigquery://bigquery-public-data.thelook_ecommerce.events
timestamp: 2024-05-22T00:00:00Z
tags: [table, log, web-event]
---

# `events` 테이블 명세

## 스키마 정보

| 컬럼명 | 데이터 타입 | 설명 |
| :--- | :--- | :--- |
| **`id`** | INT64 | 이벤트 고유 ID (기본 키) |
| `user_id` | INT64 | 행동을 유발한 가입 회원 ID (`users.id` 외래 키. 비회원일 경우 NULL) |
| `sequence_number` | INT64 | 세션 내 이벤트 발생 순서 |
| `session_id` | STRING | 브라우징 세션 ID |
| `created_at` | TIMESTAMP | 이벤트 발생 시각 |
| `ip_address` | STRING | 접속 IP 주소 |
| `city` | STRING | 접속 도시 |
| `state` | STRING | 접속 주 (State) |
| `postal_code` | STRING | 우편번호 |
| `browser` | STRING | 접속 브라우저 (Chrome, Safari, IE, Firefox 등) |
| `traffic_source` | STRING | 유입 마케팅 채널 |
| `uri` | STRING | 요청 대상 URI |
| `event_type` | STRING | 이벤트 성격 (home, department, product, cart, purchase, cancel 등) |
