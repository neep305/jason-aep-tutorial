# API 채널 샘플

- 목적: 서버/백엔드에서 스트리밍/배치 API로 XDM 데이터를 수집할 때 참고.
- 스키마: `schema.json` (ExperienceEvent 기반, commerce/web/identity + tenant.engagement 커스텀)
- 페이로드:
  - `payload-event.json`: 기본 이벤트 샘플
  - `payload-event-streaming.json`: `datasetId`/`inletId` 플레이스홀더 포함 스트리밍용
  - `payload-profile.json`: 프로필 업서트 샘플
- 배치 템플릿: `batch-events.csv`, `batch-profiles.csv`
- 사용: Streaming Ingestion API 또는 Batch Ingestion API 호출 시 본문/파일로 활용하며, Dataset은 스키마에 매핑되어 있어야 함.


## Dataset
> 아래 데이터는 Adobe Experience Platform Schema Behavior Type에 따라 구분되어 있다.
### Record Type
- batch-profile.csv
- product-master.csv
- membership-master.csv

### Time-series
