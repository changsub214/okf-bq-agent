# OKF 데이터 분석 에이전트 (OKF Data Analytics Agent)

이 프로젝트는 [OKF (Open Knowledge Format)](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)와 [BigQuery Graph](https://cloud.google.com/bigquery/docs/graphs-intro)를 활용하여 이커머스 데이터를 분석하고 비즈니스 인사이트를 도출하는 Google ADK 기반 데이터 분석 에이전트입니다.

## 🌟 주요 특징 (Why OKF & BigQuery Graph?)

### 1. [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
OKF는 지식을 Markdown 파일과 YAML Frontmatter 형식으로 표현하는 오픈 소스 표준 포맷입니다.
*   **인간 및 에이전트 친화적**: 사람과 AI가 쉽게 직접 읽고 쓸 수 있으며, LLM(대형 언어 모델)이 컨텍스트로 쉽게 흡수할 수 있습니다.
*   **버전 관리 용이성**: 모든 지식 문서가 Git으로 관리되므로 변경 이력 추적(blame), 코드 리뷰(PR) 등 소프트웨어 개발 워크플로우를 그대로 적용할 수 있습니다.
*   **구조화 + 비구조화 데이터 결합**: 필터링 및 인덱싱이 필요한 메타데이터는 YAML에, 상세 설명 및 예시 쿼리 등은 Markdown 본문에 자유롭게 작성할 수 있습니다.
*   **그래프 구조 표현**: 문서 간의 링크를 통해 단순 계층 구조를 넘어선 리치한 관계(Graph)를 표현합니다.

### 2. [BigQuery Graph](https://cloud.google.com/bigquery/docs/graphs-intro)
BigQuery Graph는 관계형 데이터와 그래프 모델을 통합하여 대규모 관계 분석을 수행할 수 있게 해주는 BigQuery의 네이티브 그래프 기능입니다.
*   **데이터 이동 없는 그래프 분석**: 별도의 그래프 데이터베이스로 데이터를 이관할 필요 없이, BigQuery 내에 존재하는 테이블을 그대로 활용하여 노드와 에지를 구성합니다.
*   **GQL (Graph Query Language) 지원**: ISO 표준 GQL을 사용하여 복잡한 다단계 관계(예: User -> Order -> InventoryItem -> Product)를 직관적이고 효율적으로 탐색할 수 있습니다.
*   **SQL+GQL 융합 분석**: `GRAPH_TABLE`을 통해 관계를 탐색(GQL)하고, 그 결과를 SQL의 집계 기능(`GROUP BY`, `SUM`, `AVG` 등)과 결합하여 고차원 인사이트를 도출합니다.

---

## ⚙️ 설치 및 설정 (Installation)

### 사전 준비 (Prerequisites)
1.  **Python 3.12+** 설치
2.  **Google Cloud Project** (결제가 활성화된 프로젝트)
3.  **gcloud CLI** 설치 및 인증
    ```bash
    gcloud auth login
    gcloud auth application-default login
    gcloud config set project <YOUR_PROJECT_ID>
    ```

### 설치 방법 (Setup)
1.  프로젝트 디렉토리로 이동합니다.
2.  가상 환경을 생성하고 활성화합니다.
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  필수 의존성을 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```

### 환경 변수 설정
루트 디렉토리 내 `.env` 파일에서 다음 설정을 입력합니다.
```env
GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
GOOGLE_CLOUD_LOCATION="YOUR_PROJECT_REGION" #global, us, eu ...
MODEL="gemini-3.5-flash"  # 사용할 모델명
```
4.  BigQuery에서 ecommerce 데이터세트(US 리전) 생성 후 다음 쿼리에서 PROJECT명 설정 후 실행합니다.
```sql
CREATE OR REPLACE PROPERTY GRAPH `YOUR_PROJECT.ecommerce.R2G`
NODE TABLES (

 `bigquery-public-data.thelook_ecommerce.users`
   KEY (id)
   LABEL User,

 `bigquery-public-data.thelook_ecommerce.products`
   KEY (id)
   LABEL Product,

 `bigquery-public-data.thelook_ecommerce.orders`
   KEY (order_id)
   LABEL `Order`,

 `bigquery-public-data.thelook_ecommerce.distribution_centers`
   KEY (id)
   LABEL DistributionCenter,

 `bigquery-public-data.thelook_ecommerce.inventory_items`
   KEY (id)
   LABEL InventoryItem,

 `bigquery-public-data.thelook_ecommerce.events`
   KEY (id)
   LABEL Event
)
EDGE TABLES (
 `bigquery-public-data.thelook_ecommerce.orders` AS `places`
   KEY (order_id)
   SOURCE KEY (user_id) REFERENCES `bigquery-public-data.thelook_ecommerce.users` (id)
   DESTINATION KEY (order_id) REFERENCES `bigquery-public-data.thelook_ecommerce.orders` (order_id)
   LABEL PLACES,

 `bigquery-public-data.thelook_ecommerce.order_items` AS contains_item
   KEY (id)
   SOURCE KEY (order_id) REFERENCES `bigquery-public-data.thelook_ecommerce.orders` (order_id)
   DESTINATION KEY (inventory_item_id) REFERENCES `bigquery-public-data.thelook_ecommerce.inventory_items` (id)
   LABEL CONTAINS_ITEM,

 `bigquery-public-data.thelook_ecommerce.inventory_items` AS is_product
   KEY (id)
   SOURCE KEY (id) REFERENCES `bigquery-public-data.thelook_ecommerce.inventory_items` (id)
   DESTINATION KEY (product_id) REFERENCES `bigquery-public-data.thelook_ecommerce.products` (id)
   LABEL IS_PRODUCT,

 `bigquery-public-data.thelook_ecommerce.inventory_items` AS stocked_at
   KEY (id)
   SOURCE KEY (id) REFERENCES `bigquery-public-data.thelook_ecommerce.inventory_items` (id)
   DESTINATION KEY (product_distribution_center_id) REFERENCES `bigquery-public-data.thelook_ecommerce.distribution_centers` (id)
   LABEL STOCKED_AT,

 `bigquery-public-data.thelook_ecommerce.products` AS supplied_by
   KEY (id)
   SOURCE KEY (id) REFERENCES `bigquery-public-data.thelook_ecommerce.products` (id)
   DESTINATION KEY (distribution_center_id) REFERENCES `bigquery-public-data.thelook_ecommerce.distribution_centers` (id)
   LABEL SUPPLIED_BY,

 `bigquery-public-data.thelook_ecommerce.events` AS performed_event
   KEY (id)
   SOURCE KEY (user_id) REFERENCES `bigquery-public-data.thelook_ecommerce.users` (id)
```


---

## 🏃 실행 방법 (How to Run)

ADK CLI를 사용하여 에이전트를 실행하거나 웹 플레이그라운드를 실행할 수 있습니다.

### CLI 실행
```bash
adk run agent.py
```

### 웹 플레이그라운드 실행
```bash
adk web
```
웹 브라우저에서 `http://127.0.0.1:8000`에 접속하여 대화형 UI를 통해 에이전트와 상호작용할 수 있습니다.

---

## 🗣️ 추천 자연어 쿼리 (Recommended Queries)

에이전트에게 다음과 같은 질문을 던져 BigQuery Graph 분석을 수행하고 인사이트를 얻을 수 있습니다.

1.  *질문1*: "골드 이상 등급 회원의 최근 6개월간 구매 및 반품 데이터를 R2G 그래프를 통해 조회하여 회원별 반품률을 산출해 주세요. 이들 중 어뷰징 의심 기준에 해당하는 대상자 수와 이들의 총 반품액을 집계해 주시고, 정책에 따른 제재 조치 제안 및 예상 물류비 절감 효과를 분석해 주세요."
2.  *질문2*: "각 물류 센터 별로 배송이 완료(Delivered)된 주문에 대해, 사용자의 거주 위치와 상품이 출고된 물류 센터 위치 간의 평균 지리적 거리를 계산하고, 이 거리가 평균 배송 소요 시간에 미치는 영향을 분석해주세요. 추가로, 사용자 거주 국가와 물류 센터 간 배송 중 지리적 거리는 멀지만 주문량이 많아 물류 재배치가 시급한 가장 비효율적인 상위 3개 노선(물류 센터 - 사용자 국가 조합) 을 도출하고 재고 분산 전략을 제안해주세요."
3.  *질문3*: "Facebook 채널을 통해 가입한 유저들이 동일한 주문 내에서 함께 가장 많이 구매한 서로 다른 상품 카테고리 쌍 TOP 5를 찾아주세요. 이 중 가장 많이 함께 구매된 카테고리 조합의 평균 결제 금액 합계는 얼마이며, 해당 카테고리 조합으로 이루어진 주문들의 취소(Cancelled) 및 반품(Returned) 비율은 타 상품군 대비 어떠한지 분석하여 마케팅 세일즈 패키지 제안서 형태로 요약해주세요."
