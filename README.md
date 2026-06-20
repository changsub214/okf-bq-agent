# OKF 데이터 분석 에이전트 (OKF Data Analytics Agent)

이 프로젝트는 **[OKF (Open Knowledge Format)](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)**와 **[BigQuery Graph](https://cloud.google.com/bigquery/docs/graphs-intro)**를 활용하여 이커머스 데이터를 분석하고 비즈니스 인사이트를 도출하는 Google ADK 기반 AI 에이전트입니다.

## 🌟 주요 특징 (Why OKF & BigQuery Graph?)

### 1. [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
OKF는 지식을 Markdown 파일과 YAML Frontmatter 형식으로 표현하는 오픈 소스 표준 포맷입니다.
*   **인간 및 에이전트 친화적**: 복잡한 API나 SDK 없이도 사람이 직접 읽고 쓸 수 있으며, LLM(대형 언어 모델)이 컨텍스트로 쉽게 흡수할 수 있습니다.
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
루트 디렉토리에 `.env` 파일을 생성하고 다음 설정을 입력합니다.
```env
GOOGLE_CLOUD_PROJECT="<YOUR_PROJECT_ID>"
MODEL="gemini-3.5-flash"  # 사용할 모델명
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

1.  **배송 리드타임 및 병목 분석**
    *   *질문*: "최근 글로벌 배송 리드타임이 가장 긴 물류센터는 어디이며, 해당 물류센터에서 공급하는 주요 상품 카테고리의 주문 상태별 현황은 어떠한가요?"
2.  **카테고리별 구매자 분석**
    *   *질문*: "실제 상품을 구매한 고유 사용자 수 기준 가장 인기 있는 상품 카테고리는 무엇이며, 이들의 총 매출 기여도는 어떻게 되나요?"
3.  **물류센터 재고 매핑**
    *   *질문*: "각 물류센터별로 공급하는 상품과 실물 재고 현황을 요약해서 보여줘."
4.  **이탈 고객 및 행동 패턴 분석**
    *   *질문*: "장바구니에 상품을 담았으나 실제 구매까지 이어지지 않고 이탈한 세션들의 사용자 유입 채널별 현황을 분석해줘."
