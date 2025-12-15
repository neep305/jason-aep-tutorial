# Schema Registry CLI (uv)

## 사전 준비
- Python 3.12 이상과 uv가 설치되어 있어야 합니다.
- 작업 루트: `api-integration`

## 의존성 설치
1. 루트로 이동: `cd api-integration`
2. uv로 패키지 설치: `uv sync` (잠금 파일을 고정하려면 `uv sync --frozen`)

## 실행 방법
1. 환경 변수 파일 준비: `schema-registry/schemas/.env` (필요 시 `SCHEMAS_ENV_FILE`로 다른 경로 지정 가능).
2. uv로 CLI 실행:
   - `uv run --env-file schema-registry/schemas/.env python schema-registry/schemas/main.py`

## 테스트
1. 실행 위치: 루트에서 `cd schema-registry/schemas`
2. 실행 명령
   - Linux/macOS (bash/zsh 등): `uv run python -m unittest discover -s test -t .`
   - Windows (PowerShell): `uv run python -m unittest discover -s test -t .`
   - 위 경로를 사용하는 이유: 테스트 시작 디렉터리가 import 가능한 패키지 루트여야 하므로, `schema-registry/schemas`에서 실행해야 `test` 모듈을 정상 인식합니다.
3. 참고: `schema-registry/schemas/test/__init__.py`를 추가해 `test` 디렉터리를 패키지로 인식하도록 했습니다.
