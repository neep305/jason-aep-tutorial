# App 채널 샘플

- 목적: Mobile SDK(Edge)로 앱 이벤트를 전송할 때 참고.
- 스키마: `schema.json` (ExperienceEvent 기반, 앱/commerce/identity 포함)
- 페이로드: `payload-event.json`(기본), `payload-event-with-datastream.json`(datastreamId 플레이스홀더 포함)
- 사용: 모바일 SDK `sendEvent` 호출 시 XDM 페이로드로 전달하거나 Assurance/Debugger로 검증.
