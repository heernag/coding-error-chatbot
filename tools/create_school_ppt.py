from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from create_project_ppt import (
    app_props,
    bullet_card,
    content_types,
    core_props,
    footer,
    package_rels,
    presentation_rels,
    presentation_xml,
    slide_xml,
    text_box,
    title,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "coding_error_chatbot_school_presentation.pptx"


def school_slides() -> list[list[str]]:
    return [
        [
            title(2, "코딩 오류 분석 챗봇", "학교 프로젝트 발표"),
            text_box(
                3,
                "Intro",
                0.8,
                1.75,
                11.6,
                2.0,
                [
                    "개발 중 발생하는 오류 메시지를 입력하면",
                    "원인, 해결 방법, 주의사항을 보기 쉽게 정리해주는 챗봇입니다.",
                ],
                26,
                "0B2240",
                fill="EAF3FF",
                line="B9D2F0",
            ),
            bullet_card(4, 0.85, 4.55, 3.7, 1.6, "프로젝트 주제", ["개발자 보조 챗봇", "오류 분석 자동화"]),
            bullet_card(5, 4.85, 4.55, 3.7, 1.6, "사용 기술", ["FastAPI", "React", "Chroma DB"]),
            bullet_card(6, 8.85, 4.55, 3.7, 1.6, "핵심 결과", ["빠른 검색", "구조화된 답변"]),
        ],
        [
            title(2, "개발 배경"),
            bullet_card(
                3,
                0.75,
                1.45,
                5.75,
                3.6,
                "문제 상황",
                [
                    "오류 메시지는 초보자에게 이해하기 어렵다",
                    "검색 결과가 많아도 무엇을 적용해야 할지 헷갈린다",
                    "API Key, DB 비밀번호 같은 민감 정보 노출 위험이 있다",
                ],
            ),
            bullet_card(
                4,
                6.85,
                1.45,
                5.75,
                3.6,
                "필요성",
                [
                    "오류 원인을 한눈에 파악할 수 있어야 한다",
                    "해결 방법이 단계별로 정리되어야 한다",
                    "답변 형식이 항상 일정해야 한다",
                ],
            ),
            text_box(
                5,
                "Message",
                0.9,
                5.7,
                11.4,
                0.7,
                ["이 프로젝트는 오류 해결 과정을 더 빠르고 쉽게 만들기 위해 시작했습니다."],
                20,
                "16643B",
            ),
        ],
        [
            title(2, "프로젝트 목표"),
            bullet_card(
                3,
                0.85,
                1.45,
                3.65,
                3.8,
                "목표 1",
                ["사용자가 오류 메시지를 입력한다", "챗봇이 핵심 원인을 요약한다"],
            ),
            bullet_card(
                4,
                4.85,
                1.45,
                3.65,
                3.8,
                "목표 2",
                ["검색된 문서 기반으로 답변한다", "없는 내용은 추측하지 않는다"],
            ),
            bullet_card(
                5,
                8.85,
                1.45,
                3.65,
                3.8,
                "목표 3",
                ["초보자도 따라할 수 있게 설명한다", "주의사항과 코드 예시를 함께 보여준다"],
            ),
            text_box(6, "Summary", 0.9, 5.85, 11.4, 0.65, ["결론적으로, 오류 해결 과정을 안내하는 학습형 챗봇을 만드는 것이 목표입니다."], 20, "0B2240"),
        ],
        [
            title(2, "주요 기능"),
            bullet_card(
                3,
                0.75,
                1.35,
                5.75,
                2.0,
                "오류 분석 답변",
                ["오류 요약", "원인", "해결 방법", "수정 코드 예시", "주의사항"],
            ),
            bullet_card(
                4,
                6.85,
                1.35,
                5.75,
                2.0,
                "채팅 UI",
                ["DM 또는 카카오톡처럼 대화형 구성", "Enter로 질문 전송", "AI 답변은 오른쪽 표시"],
            ),
            bullet_card(
                5,
                0.75,
                4.05,
                5.75,
                1.75,
                "문서 검색",
                ["오류 문서 JSON 데이터 검색", "비슷한 오류 문서를 찾아 답변 생성"],
            ),
            bullet_card(
                6,
                6.85,
                4.05,
                5.75,
                1.75,
                "대화 저장",
                ["session_id 기준 대화 관리", "Oracle DB 연결 가능"],
            ),
        ],
        [
            title(2, "시스템 구성"),
            bullet_card(3, 0.65, 1.5, 3.5, 3.85, "Frontend", ["React", "TypeScript", "Vite", "챗봇 화면"]),
            bullet_card(4, 4.85, 1.5, 3.5, 3.85, "Backend", ["FastAPI", "채팅 API", "답변 생성", "대화 저장"]),
            bullet_card(5, 9.05, 1.5, 3.5, 3.85, "Data", ["오류 문서 JSON", "Chroma Vector DB", "Oracle DB"]),
            text_box(
                6,
                "Flow",
                0.9,
                5.95,
                11.4,
                0.6,
                ["사용자 질문 → 백엔드 API → 문서 검색 → 답변 생성 → 프론트 화면 표시"],
                20,
                "185FBA",
            ),
        ],
        [
            title(2, "챗봇 동작 과정"),
            bullet_card(3, 0.75, 1.25, 11.8, 1.0, "1단계: 질문 입력", ["예: 리눅스 권한 없음"]),
            bullet_card(4, 0.75, 2.65, 11.8, 1.0, "2단계: 관련 문서 검색", ["Linux, Oracle, Python, Git 등 카테고리 기준 검색"]),
            bullet_card(5, 0.75, 4.05, 11.8, 1.0, "3단계: 답변 생성", ["검색된 문서의 원인, 해결 방법, 예시를 정해진 형식으로 구성"]),
            bullet_card(6, 0.75, 5.45, 11.8, 1.0, "4단계: 화면 출력", ["카드 대신 점선 구분으로 읽기 쉽게 표시"]),
        ],
        [
            title(2, "화면 구성"),
            bullet_card(
                3,
                0.75,
                1.45,
                5.75,
                3.8,
                "사용자 화면",
                [
                    "왼쪽에 사용자 질문 표시",
                    "오른쪽에 AI 답변 표시",
                    "모바일과 데스크톱에서 모두 사용 가능",
                ],
            ),
            bullet_card(
                4,
                6.85,
                1.45,
                5.75,
                3.8,
                "답변 구조",
                [
                    "부제목 글자를 크게 표시",
                    "각 영역은 점선으로 구분",
                    "수정 코드 예시는 코드 블록으로 표시",
                ],
            ),
            text_box(5, "UX", 0.9, 5.85, 11.4, 0.65, ["목표는 복잡한 오류 정보를 채팅 화면 안에서 쉽게 읽도록 만드는 것입니다."], 20, "0B2240"),
        ],
        [
            title(2, "오류 분석 예시"),
            text_box(
                3,
                "Example",
                0.85,
                1.35,
                11.7,
                4.7,
                [
                    "입력: 리눅스 권한 없음",
                    "",
                    "[오류 요약] Permission denied: 권한 부족",
                    "[원인] 실행 권한 또는 디렉터리 접근 권한 없음",
                    "[해결 방법] chmod 명령어로 실행 권한 부여",
                    "[수정 코드 예시] chmod +x deploy.sh && ./deploy.sh",
                    "[주의사항] 중요한 파일 권한은 신중하게 변경",
                ],
                20,
                "17202A",
                fill="F5F8FC",
                line="D8E1EC",
            ),
        ],
        [
            title(2, "구현 결과"),
            bullet_card(
                3,
                0.75,
                1.45,
                5.75,
                3.8,
                "완성된 기능",
                [
                    "React 챗봇 UI 구현",
                    "FastAPI 채팅 API 구현",
                    "문서 기반 오류 답변 생성",
                    "수정 코드 예시 표시",
                ],
            ),
            bullet_card(
                4,
                6.85,
                1.45,
                5.75,
                3.8,
                "개선한 점",
                [
                    "LLM 지연 문제를 줄이기 위해 문서 기반 답변 사용",
                    "OpenRouter fallback 모델 설정",
                    "프론트 UI 가독성 개선",
                    "테스트와 빌드 검증 완료",
                ],
            ),
            text_box(5, "Verification", 0.9, 5.85, 11.4, 0.65, ["테스트와 프론트 빌드를 통해 주요 기능이 정상 동작하는지 확인했습니다."], 20, "16643B"),
        ],
        [
            title(2, "한계점 및 개선 방향"),
            bullet_card(
                3,
                0.75,
                1.45,
                5.75,
                3.8,
                "현재 한계",
                [
                    "검색 문서에 없는 오류는 답변이 제한적이다",
                    "임베딩 모델 로딩 시간이 처음에 걸린다",
                    "무료 LLM 모델은 속도와 제한 문제가 있다",
                ],
            ),
            bullet_card(
                4,
                6.85,
                1.45,
                5.75,
                3.8,
                "개선 방향",
                [
                    "오류 문서 데이터 추가",
                    "검색 정확도 개선",
                    "복사 버튼과 피드백 버튼 추가",
                    "관리자용 문서 등록 기능 개발",
                ],
            ),
            text_box(5, "Closing", 0.9, 5.85, 11.4, 0.65, ["앞으로 더 많은 오류 데이터를 추가하면 실무와 학습에 모두 도움이 되는 챗봇으로 발전시킬 수 있습니다."], 20, "0B2240"),
        ],
        [
            title(2, "마무리"),
            text_box(
                3,
                "End",
                0.85,
                1.65,
                11.7,
                3.3,
                [
                    "이번 프로젝트를 통해 FastAPI, React, 벡터 검색, 챗봇 UI를 함께 구현해 보았습니다.",
                    "",
                    "단순히 AI에게 질문하는 방식이 아니라, 검색된 문서를 기반으로 안정적인 답변을 만드는 구조를 경험했습니다.",
                ],
                24,
                "0B2240",
                fill="EAF3FF",
                line="B9D2F0",
            ),
            text_box(4, "Thanks", 4.55, 5.6, 4.4, 0.65, ["감사합니다"], 30, "185FBA"),
        ],
    ]


def build() -> None:
    deck = school_slides()
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
