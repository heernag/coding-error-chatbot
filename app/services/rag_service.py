import re
from time import perf_counter

from app.core.config import settings
from app.services.diagnostics import log_duration, log_event, log_llm_settings
from app.services.llm_service import invoke_with_fallback
from app.services.vector_db import data
# Chroma Vector DB를 불러오기 위한 import
# vector_db.py에서 이미 JSON 로드, 임베딩 생성, Chroma DB 생성/로드를 끝낸 상태
from app.services.vector_db import vectorstore


def _as_text(value):
    if isinstance(value, list):
        return " / ".join(str(item) for item in value if item)
    return value or ""


def _lookup_source_item(item: dict) -> dict:
    item_id = item.get("id")
    error_code = item.get("error_code")
    for source_item in data:
        if item_id and source_item.get("id") == item_id:
            return source_item
        if error_code and source_item.get("error_code") == error_code:
            return source_item
    return {}


def _metadata_value(item: dict, key: str):
    value = item.get(key)
    if value:
        return value
    return _lookup_source_item(item).get(key, "")


def _code_examples(item: dict) -> str:
    examples = _as_text(_metadata_value(item, "examples"))
    command_examples = _as_text(_metadata_value(item, "command_example"))
    combined = "\n".join(part for part in [command_examples, examples] if part)
    if not combined:
        return "검색 문서에 수정 코드 예시는 없습니다."
    return f"```text\n{combined}\n```"


def build_context_from_item(item: dict) -> str:
    return f"""
오류명: {item.get('title', '')}
설명: {item.get('description', '')}
분류: {item.get('category', '')} / {item.get('subcategory', '')}
오류 코드: {item.get('error_code') or item.get('id', '')}
발생 원인: {_as_text(item.get('cause', ''))}
진단 방법: {_as_text(item.get('diagnosis', ''))}
해결 방법: {_as_text(item.get('solution', ''))}
주의사항: {item.get('caution', '')}
출처: {item.get('source_url', '')}
""".strip()


def build_answer_prompt(question: str, context: str) -> str:
    return f"""
당신은 개발자를 도와주는 코딩 오류 분석 챗봇입니다.

사용자는 Python, JavaScript, HTML/CSS, Flask, FastAPI, Oracle SQL, Pandas, LangChain, FAISS, Git, Linux 명령어 등에서 발생한 오류를 질문합니다.

당신은 아래 [검색된 문서]와 사용자가 입력한 [사용자 오류 내용]을 바탕으로만 답변해야 합니다.

답변 규칙:

검색된 문서에 근거가 있는 내용만 답변하세요.
문서에 없는 내용은 추측하지 말고 "관련 정보를 찾지 못했습니다"라고 답하세요.
사용자가 오류 메시지를 붙여넣으면 가장 먼저 핵심 오류 원인을 요약하세요.
답변은 반드시 다음 순서로 작성하세요.

[오류 요약]

사용자가 겪는 문제를 한 줄로 설명합니다.

[원인]

오류가 발생한 가능성이 높은 원인을 설명합니다.
코드, 경로, 패키지, 환경설정, DB 연결, 문법 오류 등으로 구분해서 설명합니다.

[진단 방법]

사용자가 직접 확인할 수 있는 명령어 또는 체크리스트를 제시합니다.
명령어는 반드시 코드 블록으로 작성합니다.

[해결 방법]

단계별로 해결 방법을 제시합니다.
초보자도 따라할 수 있도록 1단계, 2단계, 3단계로 나눕니다.

[수정 코드 예시]

필요한 경우 수정된 코드 예시를 제공합니다.
코드가 확실하지 않거나 문서에 없으면 코드를 임의로 만들지 않습니다.

[주의사항]

버전 충돌, 가상환경, 파일 경로, API Key 노출, DB 접속 정보 등 주의할 점이 있으면 마지막에 경고로 표시합니다.

추가 규칙:

답변은 한국어로 작성하세요.
너무 어려운 용어는 쉽게 풀어서 설명하세요.
사용자가 초보자라고 가정하고 설명하세요.
단순히 정답만 말하지 말고 "왜 이런 오류가 났는지"를 설명하세요.
명령어는 Windows 기준을 우선으로 하되, 필요하면 Linux/Mac 명령어도 함께 제공합니다.
API Key, 비밀번호, 토큰이 보이면 그대로 출력하지 말고 보안상 가려야 한다고 안내하세요.

[검색된 문서]
{context}

[사용자 오류 내용]
{question}
""".strip()


def build_no_context_response(question: str) -> str:
    return f"""
[오류 요약]
입력하신 오류 내용과 관련된 정보를 검색된 문서에서 찾지 못했습니다.

[원인]
관련 정보를 찾지 못했습니다.

[진단 방법]
아래 내용을 다시 확인해 주세요.

```powershell
python --version
pip --version
```

오류 메시지 전체, 실행한 명령어, 사용한 파일 경로, 패키지 이름, 실행 환경을 함께 입력해 주세요.

[해결 방법]
1단계: 오류 메시지 원문을 생략하지 말고 다시 입력해 주세요.
2단계: Python, FastAPI, Oracle, Git처럼 어떤 기술에서 난 오류인지 함께 적어 주세요.
3단계: API Key, 비밀번호, 토큰이 포함되어 있다면 보안상 가린 뒤 다시 질문해 주세요.

[수정 코드 예시]
관련 정보를 찾지 못했습니다.

[주의사항]
입력하신 내용: {question}
API Key, 비밀번호, 토큰, DB 접속 정보가 포함되어 있다면 그대로 공유하지 말고 반드시 가려 주세요.
""".strip()


def build_llm_error_response(error: Exception) -> str:
    return f"""
[?ㅻ쪟 ?붿빟]
OpenRouter LLM 호출 중 응답 지연 또는 비정상 응답이 발생했습니다.

[?먯씤]
OpenRouter API 키와 기본 설정은 로드되었지만, 선택한 무료 모델이 제한되었거나 응답을 정상 JSON 형식으로 돌려주지 못했을 가능성이 있습니다.
오류 종류: {type(error).__name__}

[吏꾨떒 諛⑸쾿]
```powershell
# 백엔드 실행 터미널에서 [CHAT DIAG] 로그를 확인하세요.
# OpenRouter LLM call start 이후 완료 로그가 늦거나 failed 로그가 나오면 모델 응답 구간 문제입니다.
```

[?닿껐 諛⑸쾿]
1단계: 백엔드 터미널의 [CHAT DIAG] 로그에서 OpenRouter LLM call elapsed 값을 확인하세요.
2단계: 무료 모델이 계속 지연되면 OPENROUTER_MODEL 값을 다른 free 모델로 바꿔 테스트하세요.
3단계: 프론트가 오래 기다리지 않도록 현재 백엔드는 60초 후 실패 응답을 반환합니다.

[?섏젙 肄붾뱶 ?덉떆]
관련 정보를 찾지 못했습니다.

[二쇱쓽?ы빆]
API Key, 비밀번호, 토큰, DB 접속 정보는 로그나 화면에 그대로 공유하지 말고 가려 주세요.
""".strip()


def build_direct_answer_from_item(item: dict) -> str:
    return f"""
[오류 요약]
{item.get('title', '')}: {item.get('description', '')}

[원인]
{_as_text(item.get('cause', '')) or '관련 정보를 찾지 못했습니다.'}

[진단 방법]
```powershell
{_as_text(item.get('diagnosis', '')) or '관련 정보를 찾지 못했습니다.'}
```

[해결 방법]
1단계: 검색된 문서의 오류 코드와 현재 오류 메시지가 같은지 확인하세요.
2단계: 문서의 원인 항목에 해당하는 코드, 경로, 패키지, 환경설정을 확인하세요.
3단계: 아래 해결 방법을 순서대로 적용하세요.

{_as_text(item.get('solution', '')) or '관련 정보를 찾지 못했습니다.'}

[수정 코드 예시]
{_code_examples(item)}

[주의사항]
{item.get('caution', '') or 'API Key, 비밀번호, 토큰, DB 접속 정보는 그대로 공유하지 마세요.'}
""".strip()


def build_document_answer_from_item(item: dict) -> str:
    return f"""
[오류 요약]
{item.get('title', '')}: {item.get('description', '')}

[원인]
{_as_text(item.get('cause', '')) or '관련 정보를 찾지 못했습니다.'}

[진단 방법]
```powershell
{_as_text(item.get('diagnosis', '')) or '관련 정보를 찾지 못했습니다.'}
```

[해결 방법]
1단계: 검색된 문서의 오류 이름과 현재 오류 메시지가 같은지 확인하세요.
2단계: 문서에 있는 원인 항목 중 코드, 경로, 패키지, 환경설정, 권한 문제에 해당하는 부분을 확인하세요.
3단계: 아래 해결 내용을 순서대로 적용하세요.

{_as_text(item.get('solution', '')) or '관련 정보를 찾지 못했습니다.'}

[수정 코드 예시]
{_code_examples(item)}

[주의사항]
{item.get('caution', '') or 'API Key, 비밀번호, 토큰, DB 접속 정보는 그대로 공유하지 말고 가려 주세요.'}
""".strip()




def get_rag_answer(question: str, session_id: str) -> str:
    """
    사용자 질문을 받아서 Chroma Vector DB에서 관련 오류 문서를 검색하고,
    검색된 metadata를 이용해 답변 문자열을 만들어 반환하는 함수
    """
     # 1. 질문 안에 ORA-00942 같은 에러 코드가 있는지 먼저 확인
    log_event(f"RAG start session_id={session_id} question_length={len(question)}")
    log_llm_settings(settings)

    error_code_match = re.search(r"([A-Z]+-\d{3,10})", question.upper())
    if error_code_match:
        error_code = error_code_match.group().lower()

        for item in data:
            item_error_code = (item.get("error_code") or "").lower()
            item_id = (item.get("id") or "").lower()

            if item_error_code == error_code or item_id == error_code:
                log_event(f"RAG direct match error_code={error_code}")
                return build_direct_answer_from_item(item)
    

    

    # Chroma Vector DB를 검색기(retriever) 형태로 변환
    # similarity_score_threshold:
    #   유사도가 일정 기준 이상인 문서만 가져오는 검색 방식

    q_lower = question.lower()

    filter_condition = None
    if "linux" in q_lower or "리눅스" in q_lower:
        filter_condition = {"category": "Linux"}

    elif "oracle" in q_lower or "ora-" in q_lower or "오라클" in q_lower or "오라" in q_lower:
        filter_condition = {"category": "Oracle"}

    elif "git" in q_lower:
        filter_condition = {"category": "Git"}

    elif "python" in q_lower or "pip" in q_lower or "파이썬" in q_lower:
        filter_condition = {"category": "Python"}



    
    search_kwargs={
        "k": 3,                 # 가장 유사한 문서 3개만 가져옴
        "score_threshold": 0.3  # 유사도 기준값, 낮추면 더 많이 잡히고 높이면 더 엄격해짐
    }

    if filter_condition:
        search_kwargs["filter"] = filter_condition

    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs = search_kwargs
    )
    
    

    # 사용자의 질문을 벡터로 변환한 뒤,
    # Chroma DB 안의 문서 벡터들과 비교해서 가장 비슷한 문서를 가져옴
    search_started_at = perf_counter()
    try:
        docs = retriever.invoke(question)
    except Exception as e:
        print("=" * 50)
        print("검색 중 오류 발생")
        print("질문:", question)
        print("에러:", e)
        print("=" * 50)
        return f"검색 중 오류가 발생했습니다: {e}"

    # 검색 결과가 있는 경우
    log_duration("RAG retrieval", perf_counter() - search_started_at)

    if docs:
        log_event(f"RAG docs_found={len(docs)}")
        # 가장 유사한 문서 1개 선택
        doc = docs[0]

        # vector_db.py에서 Chroma에 저장했던 metadata 꺼내기
        item = doc.metadata
        log_event("RAG document answer returned without LLM")
        return build_document_answer_from_item(item)

    log_event("RAG docs_found=0")
    return build_no_context_response(question)
