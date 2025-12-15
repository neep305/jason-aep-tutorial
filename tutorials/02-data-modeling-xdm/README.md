# Data Modeling (XDM)

> 참고: [Adobe Experience Platform XDM](https://experienceleague.adobe.com/en/docs/experience-platform/xdm/home)
> Based on: XDM 정리 from PROJECT.md

## 문서 목적
- XDM 개념, 설계 원칙, 거버넌스 요구사항을 요약하고 기존 워크플로우(클래스/필드 그룹 선택, 아이덴티티 설정)에 적용합니다.
- 튜토리얼에서 다룰 프로필/이벤트/룩업 엔티티와 샘플 데이터셋 위치를 한눈에 정리합니다.

## XDM 개요
- XDM(Experience Data Model)은 디지털 경험 데이터를 일관된 구조로 정의하는 표준이며, 서비스 간 상호운용성과 거버넌스 자동화를 목표로 합니다.
- 스키마는 Class(행동 패턴: 프로필 vs 이벤트), Field Group(재사용 가능한 의미 단위), Data Type(구조형 타입)으로 구성되며, 확장은 `tenant.*` 네임스페이스를 사용합니다.
- Identity: 필수/보조 ID에 대해 Identity namespace와 primary 플래그를 설정하고, Relationship으로 엔티티 간 연결을 정의합니다.
- 거버넌스: PII, C1/C2/C3, L1/L2 등 Data Usage Label을 필드에 적용해 사용 제한을 표준화합니다.
- 스키마 변경은 비파괴적 확장(Non-breaking change)을 우선하며, 표준 필드 그룹을 기본으로 하고 커스텀 필드는 최소화합니다.

## XDM 엔티티 유형
- Profile entities: 개인/계정 단위 정적 또는 준정적 속성. 필수 ID(Identity namespace, primary)와 최신 업데이트(`lastUpdated`)를 포함. XDM Individual Profile Class 기반.
- Event entities: 시간 축에서 발생하는 행동 데이터. `timestamp` 필수, `eventType`으로 이벤트 분류. XDM ExperienceEvent Class 기반.
- Lookup entities: 참조/보강용 정적 마스터 데이터. 비즈니스 키(예: 호텔 id, 구독 id)로 식별. Profile/Enrichment용 Dataset.

## 모델링 절차
1) 비즈니스 목표/경험 여정 정의(누구/무엇/언제, 사용하는 채널)
2) XDM Class 선택(ExperienceEvent, Individual Profile 등)
3) Field Group 선택(Commerce/Web/Identity + 필요한 `tenant.*` 최소 추가)
4) Identity namespace 지정, primary ID 설정, Relationship 정의
5) 필수/중요 필드에 거버넌스 라벨(PII/C/L) 적용
6) Dataset 생성 후 수집 경로(Streaming/Batch/Sources)와 스키마 매핑 확인

## 데이터 구성 팁
- XDM 표준 Field Group을 우선 사용하고, Query Service 분석을 위해 `web.*`, `commerce.*`, `tenant.*` 등 주요 경로의 필드는 필수 속성들을 빠짐없이 채웁니다.
- 동일 개체에 중복/다의적 필드를 만들지 말고, 스키마 간 공유가 필요한 경우 Data Type 또는 공통 Field Group을 고려합니다.
- 이벤트 스키마에서는 시간(`timestamp`), 분류(`eventType`), 아이덴티티(장치/계정) 필드를 항상 포함합니다.

## 데이터 수집/활용
- 데이터셋은 Source 커넥터, Streaming/Batch Ingestion, Edge(Web SDK/App SDK) 등 채널에 맞춰 생성합니다.
- Query Service CTAS를 통해 샘플 CSV 로드를 테스트하고, 스키마 적합성과 거버넌스 라벨 적용 여부를 검증합니다.

## 샘플 엔티티 및 데이터셋(api/)
- Customer: `api/Customer/Customer.csv`
- LoyaltyAccount: `api/LoyaltyAccount/LoyaltyAccount.csv`
- ProductCartEvent: `api/ProductCartEvent/ProductCartEvent.csv`
- CartAbandon: `api/CartAbandon/CartAbandon.csv`
- CartCheckout: `api/CartCheckout/CartCheckout.csv`
- Hotel: `api/Hotel/Hotel.csv`
- Subscription: `api/Subscription/Subscription.csv`

샘플 CSV는 Query Service CTAS 등으로 로드해 10건 내외의 소량 데이터로 스키마/ID/라벨 적용을 점검합니다.

## 스키마 만들기
- Create schema
    - Select a class
        - Manual
        - ML-Assisted (Beta)
    - Name and review:
        - Schema details:
            - Individual profile: 예) 전화번호, 이메일, 이름
            - Experience Event: 예) 장바구니 담기, 전자상거래 활동
            - Other: 기존 클래스 사용 또는 커스텀 클래스 생성(예: Loan Details)

![Schema Detail](../02-data-modeling-xdm/resources/Schemas%20Create%20schema.png)

## XDM Schema가 denormalized인 이유
XDM schema는 denormalized(정규화 최소화) 구조를 선호하는데, 주요 이유는 다음과 같습니다:
- Streaming/Edge 저지연 수집: 이벤트/프로필을 JSON 형태로 바로 적재하며, join을 위해 보류하거나 재조회하는 비용을 줄여 ingestion 지연과 오류 가능성을 낮춥니다.
- Query Service에서 join 최소화: 데이터가 대규모일 때 병합/초벌 집계가 비싸므로, denormalized schema에 주요 lookup 정보(상태/카테고리/설명)를 포함시켜 반복 join을 줄입니다.
- 실시간 프로필 병합(Identity graph) 효율: identity graph가 이미 관계를 제공하므로, 스키마 자체에서 추가 join을 만들지 않아도 되게 필드를 함께 싣습니다.
- 거버넌스/버전 관리 단순화: Field Group 중심으로 확장하며, denormalized 구조는 필수 속성을 한 레코드에 모아 라벨 적용과 변경 추적을 단순화합니다.
- Activation/세그먼트 성능: 세그먼트 평가, Journey Orchestration 등 실행계에서 필요한 필드가 한 레코드에 있으면 계산·배달 성능과 안정성이 개선됩니다.
