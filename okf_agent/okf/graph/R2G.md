---
type: graph
title: R2G Property Graph Schema Specification
description: thelook_ecommerce 공개 데이터셋을 원천으로 하여 구성된 R2G 프로퍼티 그래프 스키마 사양서입니다.
resource: bigquery://YOUR_PROJECT_ID.ecommerce.R2G
timestamp: 2024-05-23T00:00:00Z
tags: [graph, schema, r2g]
---

# R2G 프로퍼티 그래프 스키마 명세

- **그래프 식별자 (Graph Name)**: `YOUR_PROJECT_ID.ecommerce.R2G`
- **데이터 소스**: [The Look E-commerce 공개 데이터세트](../datasets/thelook_ecommerce.md)

R2G 프로퍼티 그래프는 사용자 행동(Events), 구매 내역(Orders, Products, Inventory), 그리고 공급망(Distribution Centers) 간의 관계형 데이터를 그래프 네트워크 형태로 추상화한 데이터 모델입니다.

---

## 1. 노드 스키마 (Node Schema)

R2G 그래프에 정의된 노드는 총 6가지 유형입니다. 상세 데이터 스키마는 각 테이블 정의서를 참조하십시오.

| 노드 레이블 (Label) | 식별 키 (Key) | 연동 데이터 테이블 (Table Metadata) |
| :--- | :--- | :--- |
| **`User`** | `id` | [users](../tables/users.md) |
| **`Product`** | `id` | [products](../tables/products.md) |
| **`Order`** | `order_id` | [orders](../tables/orders.md) |
| **`DistributionCenter`** | `id` | [distribution_centers](../tables/distribution_centers.md) |
| **`InventoryItem`** | `id` | [inventory_items](../tables/inventory_items.md) |
| **`Event`** | `id` | [events](../tables/events.md) |

---

## 2. 에지 스키마 (Edge Schema)

관계형 스키마의 조인 키(Foreign Key) 및 중간 테이블을 에지 데이터 테이블로 변환하여 관계를 정의했습니다.

| 에지 레이블 (Label) | 출발 노드 (`SOURCE`) | 도착 노드 (`DESTINATION`) | 매핑 데이터 소스 |
| :--- | :--- | :--- | :--- |
| **`places`** | `User` (`id`) | `Order` (`order_id`) | [orders](../tables/orders.md) |
| **`contains_item`** | `Order` (`order_id`) | `InventoryItem` (`id`) | [order_items](../tables/order_items.md) |
| **`is_product`** | `InventoryItem` (`id`) | `Product` (`id`) | [inventory_items](../tables/inventory_items.md) |
| **`stocked_at`** | `InventoryItem` (`id`) | `DistributionCenter` (`id`) | [inventory_items](../tables/inventory_items.md) |
| **`supplied_by`** | `Product` (`id`) | `DistributionCenter` (`id`) | [products](../tables/products.md) |
| **`performed_event`** | `User` (`id`) | `Event` (`id`) | [events](../tables/events.md) |

---

## 3. 추천 GQL 및 분석 패턴
R2G 프로퍼티 그래프 분석을 위한 최적화된 추천 GQL 쿼리 및 SQL 융합 분석 예제는 아래 링크에 정의되어 있습니다.

-   [R2G 추천 GQL 및 SQL+GQL 융합 분석 예제](R2G_queries.md)
