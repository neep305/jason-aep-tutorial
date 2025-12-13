# Web 채널 샘플

- 목적: Web SDK(Edge)로 이벤트를 전송할 때 참고.
- 스키마: `schema.json` (ExperienceEvent 기반, web/commerce/identity 포함)
- 페이로드: `payload-event.json`(기본), `payload-event-with-datastream.json`(datastreamId 플레이스홀더 포함)
- 사용: Web SDK `sendEvent({ xdm, datastreamId })` 또는 Edge Network 샌드박스 테스트에 활용.
