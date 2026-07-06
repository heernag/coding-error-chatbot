# 코드 리뷰 문서

## 1. 프로젝트 개요

이 프로젝트는 개발자가 Python, Oracle SQL, Linux, Git, Docker 등에서 만나는 오류 메시지를 입력하면, 사전에 구축한 오류 문서 데이터와 벡터 검색을 기반으로 원인, 해결 방법, 수정 코드 예시, 주의사항을 제공하는 코딩 오류 분석 챗봇입니다.

전체 구조는 React 프론트엔드, FastAPI 백엔드, ChromaDB 벡터 검색, Oracle DB 채팅 이력 저장으로 구성되어 있습니다.

```text
React Frontend
  -> FastAPI Backend
  -> RAG Service
  -> ChromaDB + JSON Error Documents
  -> Structured Answer
  -> Oracle DB Chat History
```

## 2. 백엔드 코드 리뷰

관련 파일:

- `app/main.py`
- `app/api/chat.py`

좋았던 점:

- FastAPI 앱 설정과 API 라우터가 분리되어 있어 구조가 단순하고 이해하기 쉽습니다.
- `/api/chat`은 질문 처리, `/api/history/{session_id}`는 세션별 채팅 이력 조회로 역할이 분리되어 있습니다.
- React 프론트엔드와 연동하기 위해 CORS 설정이 적용되어 있습니다.
- 요청 처리 시간, RAG 검색 시간, DB 저장 시간 등을 로그로 확인할 수 있도록 진단 로그를 추가했습니다.

개선한 점:

- 초기에는 프론트엔드에서 `/api/chat` 요청이 오래 pending 상태로 보였습니다.
- 원인을 찾기 위해 RAG 검색, LLM 호출, DB 저장 구간별 로그를 추가했습니다.
- 확인 결과 병목은 RAG 검색이 아니라 OpenRouter 무료 모델 호출 구간이었습니다.
- 이후 검색된 문서가 있으면 LLM을 거치지 않고 문서 metadata 기반으로 바로 답변을 생성하도록 개선했습니다.

추가 개선 제안:

- 운영 환경에서는 CORS `allow_origins=['*']` 대신 실제 프론트엔드 주소만 허용하는 것이 좋습니다.
- DB 저장 실패 시 사용자에게도 명확한 오류 응답을 주도록 예외 처리를 더 세분화할 수 있습니다.
- API 응답에 `source`, `confidence`, `elapsed_ms` 같은 진단용 필드를 선택적으로 추가하면 운영 분석에 도움이 됩니다.

## 3. DB 계층 코드 리뷰

관련 파일:

- `app/database/connection.py`
- `app/database/models.py`

현재 모델:

```python
class ChatHistory(Base):
    __tablename__ = 'chat_history'

    id = Column(Integer, Identity(start=1), primary_key=True)
    session_id = Column(String(50), index=True, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

좋았던 점:

- SQLAlchemy ORM을 사용해 DB 모델을 명확하게 정의했습니다.
- `session_id`에 index를 설정해 세션별 이력 조회 성능을 고려했습니다.
- `DATABASE_URL` 환경변수를 기반으로 Oracle DB와 개발용 SQLite 환경을 모두 다룰 수 있게 구성했습니다.
- `get_db()` 의존성 함수로 요청마다 DB 세션을 열고 닫는 구조를 만들었습니다.

추가 개선 제안:

- 향후에는 `users`, `error_documents`, `feedback`, `chat_references` 테이블을 추가해 서비스형 구조로 확장할 수 있습니다.
- `created_at`은 timezone-aware datetime으로 바꾸면 서버 지역 설정에 덜 영향을 받습니다.
- 답변이 길어질 수 있으므로 Oracle 환경에서는 `Text` 타입이 실제로 CLOB에 맞게 생성되는지 확인이 필요합니다.

## 4. RAG 서비스 코드 리뷰

관련 파일:

- `app/services/rag_service.py`
- `app/services/vector_db.py`

좋았던 점:

- 오류 문서 JSON을 LangChain `Document` 객체로 변환하고, 검색용 본문과 답변용 metadata를 분리했습니다.
- `title`, `error_message`, `error_code`, `keywords`, `examples`를 검색 대상에 포함했습니다.
- `cause`, `diagnosis`, `solution`, `examples`, `command_example`, `caution`을 답변 생성에 활용하도록 구성했습니다.
- 오류 코드가 질문에 포함된 경우 직접 매칭을 우선 적용해 검색 정확도를 높였습니다.
- Linux, Oracle, Git, Python 등 키워드에 따라 category filter를 적용하도록 개선했습니다.

중요 개선 사항:

- 초기에는 검색된 문서를 LLM에 전달해 답변을 생성했습니다.
- OpenRouter 무료 모델에서 rate limit, 응답 지연, 빈 응답 문제가 발생했습니다.
- 이후 검색된 문서 metadata를 기반으로 직접 구조화 답변을 생성하도록 변경했습니다.
- 이 변경으로 답변 속도와 형식 안정성이 크게 좋아졌습니다.

추가 개선 제안:

- 현재 `score_threshold`는 0.3 기준입니다. 실제 질문 로그가 쌓이면 도메인별로 임계값을 조정할 수 있습니다.
- 질문 의도 분류를 강화하면 category filter를 더 정확하게 적용할 수 있습니다.
- 현재 오류 문서는 JSON + ChromaDB 기반이지만, 향후 관리자 페이지에서 DB 기반으로 관리할 수 있습니다.

## 5. LLM 연동 코드 리뷰

관련 파일:

- `app/services/llm_service.py`

좋았던 점:

- OpenRouter API를 OpenAI 호환 방식으로 연결했습니다.
- 무료 모델의 rate limit에 대비해 fallback 모델 목록을 구성했습니다.
- `timeout=60`, `max_retries=0`, `max_tokens=700`을 설정해 무한 대기와 과도한 응답 생성을 줄였습니다.
- 빈 응답은 실패로 처리해 다음 모델로 넘어갈 수 있게 했습니다.

현재 역할:

- 현재 주요 답변 생성은 문서 metadata 기반으로 처리합니다.
- LLM은 향후 문장 개선, 추가 요약, 검색 문서가 없을 때의 보조 기능으로 사용할 수 있습니다.

주의할 점:

- 무료 모델은 트래픽 상황에 따라 응답 속도와 성공률이 불안정할 수 있습니다.
- API Key는 `.env`에만 저장하고 GitHub에는 올리지 않아야 합니다.
- OpenRouter 모델명은 자주 바뀔 수 있으므로 실제 사용 전 모델 목록 확인이 필요합니다.

## 6. 프론트엔드 코드 리뷰

관련 파일:

- `frontend/src/App.tsx`
- `frontend/src/App.css`

좋았던 점:

- React + TypeScript 기반으로 챗봇 UI를 구현했습니다.
- 사용자가 질문하면 메신저처럼 말풍선 형태로 대화가 쌓이도록 구성했습니다.
- 사용자 메시지는 왼쪽, AI 답변은 오른쪽에 배치했습니다.
- Enter는 전송, Shift+Enter는 줄바꿈으로 동작하도록 구현했습니다.
- AI 답변은 `[오류 요약]`, `[원인]`, `[해결 방법]`, `[수정 코드 예시]`, `[주의사항]` 섹션으로 파싱해 보여줍니다.
- 사용자가 요청한 대로 `[진단 방법]` 섹션은 프론트엔드에서 표시하지 않도록 처리했습니다.
- 각 섹션 내부 박스를 줄이고 점선 구분선으로 정리해 시각적으로 더 가볍게 만들었습니다.

개선한 점:

- 초기 답변 카드가 섹션마다 박스로 감싸져 답답해 보이는 문제가 있었습니다.
- 섹션 제목 글자 크기를 키우고, 섹션 사이를 선으로 구분해 가독성을 높였습니다.
- 수정 코드 예시가 나오지 않던 문제는 백엔드 metadata 보강으로 해결했습니다.

추가 개선 제안:

- 코드 블록 복사 버튼을 추가하면 사용성이 좋아집니다.
- 답변 만족도 버튼을 추가하면 이후 검색 품질 개선 데이터로 활용할 수 있습니다.
- 로딩 상태를 더 명확히 보여주면 사용자가 응답 지연을 오류로 오해하지 않게 할 수 있습니다.

## 7. 테스트 코드 리뷰

관련 파일:

- `tests/test_rag_service_format.py`
- `tests/test_llm_service_config.py`
- `tests/test_frontend_structure.py`
- `tests/test_diagnostics.py`

좋았던 점:

- RAG 답변에 필수 섹션이 포함되는지 검증했습니다.
- 문서가 검색되면 LLM 호출 없이 답변이 생성되는지 검증했습니다.
- OpenRouter fallback 동작과 빈 응답 처리 로직을 검증했습니다.
- 프론트엔드 구조, Enter 전송, 섹션 스타일, 점선 구분 스타일을 테스트했습니다.
- 민감한 API Key가 로그에 그대로 출력되지 않는지 확인하는 테스트를 추가했습니다.

추가 개선 제안:

- 실제 API 서버를 띄운 상태에서 `/api/chat` 통합 테스트를 추가할 수 있습니다.
- Oracle DB 연결 테스트는 환경 의존성이 크므로 별도 profile로 분리하는 것이 좋습니다.
- 프론트엔드는 Playwright를 이용해 실제 화면 렌더링 테스트를 추가하면 더 안정적입니다.

## 8. 종합 평가

이 프로젝트의 핵심 강점은 단순 챗봇 UI를 넘어서, 오류 문서 데이터, 벡터 검색, API 서버, DB 저장, 프론트엔드 렌더링까지 하나의 서비스 흐름으로 연결했다는 점입니다.

특히 OpenRouter 무료 모델 지연 문제를 직접 겪고, 로그 기반으로 병목을 분리한 뒤, LLM 의존도를 낮추는 구조로 바꾼 과정은 백엔드와 AI 서비스 개발 역량을 보여주기 좋습니다.

포트폴리오에서는 다음 포인트를 강조하면 좋습니다.

- FastAPI 기반 API 설계
- RAG 검색 구조 설계
- ChromaDB metadata 설계
- Oracle DB 채팅 이력 저장
- React TypeScript 챗봇 UI 구현
- OpenRouter API 연동과 fallback 처리
- 로그 기반 트러블슈팅
- `.env` 보안 관리와 GitHub 배포 정리
