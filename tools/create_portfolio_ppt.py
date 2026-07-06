from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from create_project_ppt import (
    app_props,
    bullet_card,
    content_types,
    core_props,
    package_rels,
    presentation_rels,
    presentation_xml,
    slide_xml,
    text_box,
    title,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "coding_error_chatbot_portfolio_presentation.pptx"


def ribbon(text: str, y: float = 1.28) -> str:
    return text_box(80, "Ribbon", 0.72, y, 11.85, 0.48, [text], 15, "185FBA", fill="EAF3FF", line="B9D2F0")


def insight(text: str) -> str:
    return text_box(88, "Insight", 0.85, 6.05, 11.65, 0.55, [text], 17, "16643B", fill="F6FAF7", line="CFE5D6")


def slides() -> list[list[str]]:
    return [
        [
            title(2, "IT 코딩 오류 분석 챗봇", "취업 포트폴리오 발표 자료"),
            text_box(3, "Hero", 0.8, 1.85, 11.7, 2.15, [
                "개발 오류 메시지를 입력하면 검색 문서 기반으로 원인, 해결 방법, 코드 예시를 제공하는 RAG 챗봇",
                "FastAPI, React, Chroma Vector DB, Oracle DB를 연결한 실전형 풀스택 프로젝트",
            ], 24, "0B2240", fill="EAF3FF", line="B9D2F0"),
            bullet_card(4, 0.85, 4.85, 3.7, 1.35, "Keyword", ["RAG", "Vector Search", "FastAPI"]),
            bullet_card(5, 4.85, 4.85, 3.7, 1.35, "Frontend", ["React", "TypeScript", "Chat UI"]),
            bullet_card(6, 8.85, 4.85, 3.7, 1.35, "Backend/Data", ["Oracle", "SQLAlchemy", "ETL"]),
        ],
        [
            title(2, "목차"),
            bullet_card(3, 0.75, 1.35, 5.75, 2.3, "프로젝트 이해", ["프로젝트 소개", "문제 정의", "목표와 기대 효과", "사용 기술"]),
            bullet_card(4, 6.85, 1.35, 5.75, 2.3, "구현 과정", ["데이터 수집", "ETL", "Oracle DB", "아키텍처와 ERD"]),
            bullet_card(5, 0.75, 4.15, 5.75, 2.0, "기술 설명", ["코드 리뷰", "AI 기능", "Skill/Agent/Artifact", "검증"]),
            bullet_card(6, 6.85, 4.15, 5.75, 2.0, "결과 정리", ["데이터 분석", "결과 인사이트", "역할분담", "향후 개선"]),
        ],
        [
            title(2, "프로젝트 소개"),
            bullet_card(3, 0.75, 1.35, 5.75, 3.7, "프로젝트 한 줄 설명", ["개발자가 오류 메시지를 입력하면", "문서 기반으로 원인과 해결 방법을 정리", "초보자도 따라할 수 있는 단계형 답변 제공"]),
            bullet_card(4, 6.85, 1.35, 5.75, 3.7, "핵심 차별점", ["검색 문서에 근거한 답변", "정해진 섹션 구조", "수정 코드 예시 제공", "민감 정보 노출 주의"]),
            insight("면접 포인트: 단순 챗봇이 아니라 검색, DB, 프론트 UX, 운영 안정성까지 연결한 프로젝트입니다."),
        ],
        [
            title(2, "문제 정의"),
            bullet_card(3, 0.75, 1.35, 5.75, 3.75, "사용자 불편", ["오류 메시지가 길고 어렵다", "검색 결과가 많아도 적용 방법이 불명확하다", "실행 환경, 경로, 권한, 패키지 문제가 섞여 있다"]),
            bullet_card(4, 6.85, 1.35, 5.75, 3.75, "해결해야 할 과제", ["원인 요약", "진단 방법", "해결 순서", "코드 예시", "주의사항을 한 화면에 제공"]),
            insight("문제 해결의 핵심은 답변 품질뿐 아니라, 사용자가 바로 행동할 수 있는 구조화입니다."),
        ],
        [
            title(2, "프로젝트 목표와 요구사항"),
            bullet_card(3, 0.75, 1.35, 3.75, 4.3, "Functional", ["오류 메시지 입력", "관련 문서 검색", "섹션별 답변 생성", "대화 기록 저장"]),
            bullet_card(4, 4.85, 1.35, 3.75, 4.3, "UX", ["DM형 챗봇 화면", "Enter 전송", "카드/점선 구분", "코드 예시 표시"]),
            bullet_card(5, 8.95, 1.35, 3.75, 4.3, "Quality", ["문서 근거 기반", "민감정보 보호", "빠른 응답", "테스트 검증"]),
            insight("요구사항을 기능, 사용자 경험, 품질 기준으로 나누어 구현 범위를 관리했습니다."),
        ],
        [
            title(2, "기술 스택"),
            bullet_card(3, 0.65, 1.35, 3.6, 4.4, "Frontend", ["Vite", "React", "TypeScript", "CSS", "Fetch API"]),
            bullet_card(4, 4.85, 1.35, 3.6, 4.4, "Backend", ["FastAPI", "Pydantic", "SQLAlchemy", "Uvicorn", "Python"]),
            bullet_card(5, 9.05, 1.35, 3.6, 4.4, "AI/Data", ["Chroma", "HuggingFace Embeddings", "BAAI/bge-m3", "OpenRouter fallback", "Oracle DB"]),
            insight("풀스택 구조와 AI 검색 구조를 한 프로젝트 안에서 연결했습니다."),
        ],
        [
            title(2, "데이터 수집 과정"),
            bullet_card(3, 0.75, 1.35, 5.75, 3.85, "데이터 구성", ["총 151건의 오류 문서", "Oracle, Linux, Spring Boot, Git, Docker, Python", "공식 문서 기반 source_url 포함"]),
            bullet_card(4, 6.85, 1.35, 5.75, 3.85, "문서 필드", ["title", "error_message", "cause", "diagnosis", "solution", "examples", "command_example", "caution"]),
            insight("단순 Q&A가 아니라 오류 분석에 필요한 원인, 진단, 해결, 예시를 분리해 수집했습니다."),
        ],
        [
            title(2, "데이터 분석"),
            bullet_card(3, 0.75, 1.3, 5.75, 4.05, "카테고리 분포", ["Oracle: 40건", "Linux: 30건", "Spring Boot: 30건", "Git: 25건", "Docker: 25건", "Python: 1건"]),
            bullet_card(4, 6.85, 1.3, 5.75, 4.05, "데이터 인사이트", ["DB와 인프라 오류 비중이 높음", "명령어 기반 오류는 진단/예시가 중요", "Python 데이터는 추가 보강 필요"]),
            insight("데이터 분포 분석을 통해 향후 보강해야 할 기술 영역을 확인했습니다."),
        ],
        [
            title(2, "ETL 과정"),
            text_box(3, "ETL", 0.85, 1.3, 11.6, 4.4, [
                "Extract: JSON 오류 문서 로드",
                "Transform: 검색용 page_content와 metadata로 변환",
                "Load: HuggingFace 임베딩 생성 후 Chroma Vector DB에 저장",
                "",
                "검색 대상: title, error_message, error_code, keywords, examples",
                "답변 대상: cause, diagnosis, solution, examples, command_example, caution",
            ], 21, "17202A", fill="F5F8FC", line="D8E1EC"),
            insight("검색에 필요한 텍스트와 답변에 필요한 metadata를 분리해 RAG 품질을 높였습니다."),
        ],
        [
            title(2, "Oracle DB 구축 과정"),
            bullet_card(3, 0.75, 1.35, 5.75, 3.85, "DB 연결", ["DATABASE_URL 환경변수 기반", "SQLAlchemy create_engine", "Oracle 연결 지원", "SQLite fallback 가능"]),
            bullet_card(4, 6.85, 1.35, 5.75, 3.85, "테이블 생성", ["Base.metadata.create_all", "ChatHistory 모델", "session_id 기준 대화 기록", "created_at 자동 저장"]),
            insight("Oracle DB는 운영 대화 이력 저장소 역할을 하며, ORM 모델로 테이블 구조를 관리했습니다."),
        ],
        [
            title(2, "ERD"),
            text_box(3, "ChatHistory", 0.85, 1.35, 5.8, 4.5, [
                "chat_history",
                "",
                "PK id: Integer Identity",
                "session_id: String(50), index",
                "question: Text",
                "answer: Text",
                "created_at: DateTime",
            ], 21, "17202A", fill="EAF3FF", line="B9D2F0"),
            text_box(4, "Future", 7.05, 1.35, 5.1, 4.5, [
                "향후 확장 후보",
                "",
                "error_documents",
                "feedback",
                "users",
                "model_usage_logs",
            ], 21, "17202A", fill="F6FAF7", line="CFE5D6"),
            insight("현재 ERD는 대화 기록 중심이며, 사용자/피드백/문서 관리 테이블로 확장할 수 있습니다."),
        ],
        [
            title(2, "시스템 아키텍처"),
            bullet_card(3, 0.65, 1.35, 3.6, 4.3, "Client", ["React UI", "질문 입력", "답변 섹션 렌더링"]),
            bullet_card(4, 4.85, 1.35, 3.6, 4.3, "API", ["FastAPI", "/api/chat", "/api/history", "CORS 설정"]),
            bullet_card(5, 9.05, 1.35, 3.6, 4.3, "Data/AI", ["Chroma 검색", "JSON 문서", "Oracle 저장", "OpenRouter fallback"]),
            insight("프론트, API, 검색/저장 계층을 분리해 유지보수성과 설명 가능성을 높였습니다."),
        ],
        [
            title(2, "API 설계"),
            bullet_card(3, 0.75, 1.35, 5.75, 3.85, "POST /api/chat", ["입력: session_id, question", "처리: RAG 답변 생성", "저장: ChatHistory", "출력: session_id, answer"]),
            bullet_card(4, 6.85, 1.35, 5.75, 3.85, "GET /api/history/{session_id}", ["세션별 대화 조회", "created_at 기준 정렬", "질문/답변/시간 반환"]),
            insight("API는 채팅 생성과 이력 조회로 나누어 프론트에서 단순하게 사용할 수 있도록 구성했습니다."),
        ],
        [
            title(2, "AI 기능: RAG 검색"),
            bullet_card(3, 0.75, 1.25, 5.75, 4.15, "검색 전략", ["오류 코드 직접 매칭", "카테고리 필터", "similarity_score_threshold", "상위 문서 3개 검색"]),
            bullet_card(4, 6.85, 1.25, 5.75, 4.15, "답변 전략", ["문서 metadata 기반 답변", "정해진 6개 섹션", "수정 코드 예시 포함", "문서에 없는 내용은 제한"]),
            insight("초기에는 LLM 생성 중심이었지만, 속도와 안정성을 위해 문서 기반 답변 생성으로 개선했습니다."),
        ],
        [
            title(2, "AI 기능: OpenRouter fallback"),
            bullet_card(3, 0.75, 1.35, 5.75, 3.9, "문제", ["Gemma free 모델 rate limit", "긴 프롬프트 지연", "빈 응답", "프론트 pending 현상"]),
            bullet_card(4, 6.85, 1.35, 5.75, 3.9, "해결", ["poolside free 모델 1순위", "nvidia/openai/cohere/gemma fallback", "timeout=60", "max_tokens=700", "빈 응답 실패 처리"]),
            insight("외부 AI 모델은 불안정할 수 있으므로 fallback과 timeout 전략을 코드에 반영했습니다."),
        ],
        [
            title(2, "코드 리뷰: Backend"),
            bullet_card(3, 0.75, 1.3, 5.75, 4.15, "좋은 점", ["라우터와 서비스 분리", "DB 세션 의존성 사용", "응답 시간 로그 추가", "환경변수 기반 설정"]),
            bullet_card(4, 6.85, 1.3, 5.75, 4.15, "개선한 점", ["LLM 호출 제거로 응답 지연 감소", "예시 metadata 보강", "민감정보 로그 미출력", "테스트 추가"]),
            insight("백엔드는 API, DB, RAG 서비스가 분리되어 있어 기능별 테스트와 개선이 가능했습니다."),
        ],
        [
            title(2, "코드 리뷰: RAG/ETL"),
            bullet_card(3, 0.75, 1.3, 5.75, 4.15, "핵심 코드", ["build_document", "get_embedding_model", "get_rag_answer", "build_document_answer_from_item"]),
            bullet_card(4, 6.85, 1.3, 5.75, 4.15, "리뷰 포인트", ["검색용 content와 답변 metadata 분리", "기존 Chroma DB metadata 보강", "문서 기반 답변으로 형식 안정화", "검색 실패 응답 별도 처리"]),
            insight("RAG 품질은 모델보다 데이터 구조와 검색/metadata 설계에 크게 좌우된다는 점을 반영했습니다."),
        ],
        [
            title(2, "코드 리뷰: Frontend"),
            bullet_card(3, 0.75, 1.3, 5.75, 4.15, "핵심 구현", ["parseAnswerSections", "MessageBubble", "sendQuestion", "Enter 전송 처리"]),
            bullet_card(4, 6.85, 1.3, 5.75, 4.15, "UI 개선", ["AI 오른쪽/사용자 왼쪽 배치", "부제목 글자 확대", "내부 박스 제거", "점선 구분선", "수정 코드 예시 표시"]),
            insight("프론트는 단순 표시가 아니라 답변 구조를 파싱해 가독성 좋은 문서형 UI로 렌더링합니다."),
        ],
        [
            title(2, "Skill, Agent, Artifact"),
            bullet_card(3, 0.65, 1.35, 3.7, 4.35, "Skill", ["체계적 디버깅", "테스트 주도 수정", "검증 후 완료", "브레인스토밍"]),
            bullet_card(4, 4.85, 1.35, 3.7, 4.35, "Agent", ["Codex 활용", "코드 탐색", "수정 제안", "테스트 실행", "문서/PPT 생성"]),
            bullet_card(5, 9.05, 1.35, 3.7, 4.35, "Artifact", ["React 프론트", "FastAPI 백엔드", "Chroma DB", "테스트 코드", "PPT 산출물"]),
            insight("단순 구현 결과뿐 아니라, 문제 해결 과정과 산출물 관리까지 포트폴리오에 포함했습니다."),
        ],
        [
            title(2, "역할분담"),
            bullet_card(3, 0.75, 1.25, 5.75, 4.35, "구현 역할", ["기획: 문제 정의와 발표 흐름", "데이터: 오류 문서 구조화", "백엔드: FastAPI, DB, RAG", "프론트: React 챗봇 UI"]),
            bullet_card(4, 6.85, 1.25, 5.75, 4.35, "품질 역할", ["AI 연동: OpenRouter fallback", "QA: 테스트와 빌드 검증", "문서화: README/PPT", "발표: 시연 시나리오 정리"]),
            insight("발표 시 실제 팀원명이 있다면 각 역할 옆에 이름을 매핑하면 됩니다."),
        ],
        [
            title(2, "검증과 테스트"),
            bullet_card(3, 0.75, 1.35, 5.75, 3.85, "테스트 항목", ["RAG 응답 섹션", "LLM fallback", "프론트 구조", "수정 코드 예시", "문법 컴파일"]),
            bullet_card(4, 6.85, 1.35, 5.75, 3.85, "검증 명령", ["python -m unittest", "py_compile", "npm run build", "실제 검색 시간 측정"]),
            insight("기능 수정 후에는 테스트와 빌드를 반복해 UI/백엔드 변경의 안정성을 확인했습니다."),
        ],
        [
            title(2, "결과 인사이트"),
            bullet_card(3, 0.75, 1.3, 5.75, 4.15, "기술 인사이트", ["LLM만으로 답변하면 느리고 불안정할 수 있음", "문서 기반 생성은 빠르고 예측 가능", "metadata 설계가 답변 품질을 좌우"]),
            bullet_card(4, 6.85, 1.3, 5.75, 4.15, "사용자 인사이트", ["초보자는 원인보다 다음 행동이 중요", "코드 예시가 있어야 바로 적용 가능", "섹션 구조가 이해 속도를 높임"]),
            insight("프로젝트의 핵심 성과는 AI 모델 사용보다, 문제 해결 경험을 안정적으로 설계한 점입니다."),
        ],
        [
            title(2, "성과 요약"),
            bullet_card(3, 0.75, 1.35, 3.75, 4.3, "기능 완성", ["채팅 UI", "RAG 검색", "DB 저장", "코드 예시"]),
            bullet_card(4, 4.85, 1.35, 3.75, 4.3, "성능 개선", ["LLM 의존도 감소", "검색 후 즉시 답변", "실측 0.3~0.5초대 검색"]),
            bullet_card(5, 8.95, 1.35, 3.75, 4.3, "포트폴리오 가치", ["풀스택", "AI 검색", "DB/ETL", "테스트", "문서화"]),
            insight("한 프로젝트 안에서 데이터, 백엔드, 프론트, AI 기능을 모두 설명할 수 있는 구조를 만들었습니다."),
        ],
        [
            title(2, "향후 개선 방향"),
            bullet_card(3, 0.75, 1.25, 5.75, 4.35, "기능 개선", ["관리자 문서 등록 화면", "사용자 피드백 버튼", "답변 복사 기능", "코드 하이라이팅", "로그 대시보드"]),
            bullet_card(4, 6.85, 1.25, 5.75, 4.35, "기술 개선", ["문서 자동 수집 파이프라인", "Oracle ERD 확장", "검색 랭킹 개선", "모델 사용량 모니터링", "배포 환경 구성"]),
            insight("향후에는 운영 관점의 문서 관리와 피드백 루프를 추가해 실제 서비스 수준으로 확장할 수 있습니다."),
        ],
        [
            title(2, "마무리"),
            text_box(3, "Closing", 0.85, 1.55, 11.7, 3.85, [
                "이 프로젝트는 코딩 오류 해결 과정을 빠르고 구조화된 경험으로 바꾸는 것을 목표로 했습니다.",
                "",
                "데이터 수집, ETL, 벡터 검색, FastAPI, Oracle DB, React UI, 테스트와 문서화까지 연결하며",
                "취업 포트폴리오에서 설명 가능한 풀스택 AI 프로젝트로 발전시켰습니다.",
            ], 23, "0B2240", fill="EAF3FF", line="B9D2F0"),
            text_box(4, "Thanks", 4.25, 5.75, 4.9, 0.7, ["감사합니다"], 30, "185FBA"),
        ],
    ]


def build() -> None:
    deck = slides()
    with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types(len(deck)))
        z.writestr("_rels/.rels", package_rels())
        z.writestr("docProps/core.xml", core_props())
        z.writestr("docProps/app.xml", app_props(len(deck)))
        z.writestr("ppt/presentation.xml", presentation_xml(len(deck)))
        z.writestr("ppt/_rels/presentation.xml.rels", presentation_rels(len(deck)))
        for index, shapes in enumerate(deck, start=1):
            z.writestr(f"ppt/slides/slide{index}.xml", slide_xml(index, shapes))
    print(OUT)


if __name__ == "__main__":
    build()
