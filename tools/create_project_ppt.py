from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "coding_error_chatbot_presentation.pptx"

SLIDE_W = 12192000
SLIDE_H = 6858000


def emu(inches: float) -> int:
    return int(inches * 914400)


def text_runs(lines: list[str], font_size: int = 24, color: str = "17202A") -> str:
    paragraphs = []
    for line in lines:
        line = line.strip()
        if not line:
            paragraphs.append("<a:p/>")
            continue
        paragraphs.append(
            "<a:p>"
            f"<a:r><a:rPr lang=\"ko-KR\" sz=\"{font_size * 100}\" dirty=\"0\">"
            f"<a:solidFill><a:srgbClr val=\"{color}\"/></a:solidFill>"
            "</a:rPr>"
            f"<a:t>{escape(line)}</a:t>"
            "</a:r>"
            "</a:p>"
        )
    return "".join(paragraphs)


def text_box(
    shape_id: int,
    name: str,
    x: float,
    y: float,
    w: float,
    h: float,
    lines: list[str],
    font_size: int = 24,
    color: str = "17202A",
    fill: str | None = None,
    line: str | None = None,
) -> str:
    fill_xml = (
        f"<a:solidFill><a:srgbClr val=\"{fill}\"/></a:solidFill>"
        if fill
        else "<a:noFill/>"
    )
    line_xml = (
        f"<a:ln w=\"12700\"><a:solidFill><a:srgbClr val=\"{line}\"/></a:solidFill></a:ln>"
        if line
        else "<a:ln><a:noFill/></a:ln>"
    )
    return f"""
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{shape_id}" name="{escape(name)}"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
    <a:prstGeom prst="roundRect"><a:avLst/></a:prstGeom>
    {fill_xml}
    {line_xml}
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" lIns="91440" tIns="91440" rIns="91440" bIns="91440"/>
    <a:lstStyle/>
    {text_runs(lines, font_size, color)}
  </p:txBody>
</p:sp>
"""


def title(shape_id: int, text: str, subtitle: str = "") -> str:
    lines = [text]
    if subtitle:
        lines.extend(["", subtitle])
    return text_box(shape_id, "Title", 0.55, 0.35, 12.2, 1.05, lines, 30, "0B2240")


def footer(slide_no: int) -> str:
    return text_box(
        900,
        "Footer",
        0.55,
        7.05,
        12.2,
        0.25,
        [f"IT 코딩 오류 분석 챗봇 | {slide_no}"],
        9,
        "6B7785",
    )


def bullet_card(shape_id: int, x: float, y: float, w: float, h: float, header: str, bullets: list[str]) -> str:
    return text_box(
        shape_id,
        header,
        x,
        y,
        w,
        h,
        [header, "", *[f"- {bullet}" for bullet in bullets]],
        18,
        "17202A",
        fill="F5F8FC",
        line="D8E1EC",
    )


def slide_xml(slide_no: int, shapes: list[str]) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      {''.join(shapes)}
      {footer(slide_no)}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>
"""


def slides() -> list[list[str]]:
    return [
        [
            title(2, "IT 코딩 오류 분석 챗봇", "검색 문서 기반으로 오류 원인과 해결 방법을 안내하는 RAG 챗봇"),
            text_box(3, "Hero", 0.75, 2.0, 11.85, 2.7, [
                "Python, Oracle SQL, Git, Linux 등 개발 중 만나는 오류를 입력하면",
                "검색된 문서의 근거를 바탕으로 원인, 해결 방법, 주의사항을 구조화해서 보여줍니다.",
            ], 24, "0B2240", fill="EAF3FF", line="B9D2F0"),
            bullet_card(4, 0.85, 5.05, 3.7, 1.35, "핵심 가치", ["초보자도 따라갈 수 있는 설명", "API 키와 DB 정보 노출 방지"]),
            bullet_card(5, 4.85, 5.05, 3.7, 1.35, "현재 상태", ["FastAPI 백엔드", "React 챗봇 UI"]),
            bullet_card(6, 8.85, 5.05, 3.7, 1.35, "발표 포인트", ["검색 기반 답변", "빠른 응답 구조"]),
        ],
        [
            title(2, "문제 정의"),
            bullet_card(3, 0.75, 1.55, 5.8, 2.0, "사용자 문제", ["오류 메시지가 길고 낯설다", "무엇부터 확인해야 할지 모른다", "검색 결과가 너무 흩어져 있다"]),
            bullet_card(4, 6.85, 1.55, 5.8, 2.0, "기존 방식의 한계", ["질문마다 설명 품질이 들쭉날쭉하다", "민감 정보가 그대로 공유될 수 있다", "무료 LLM 모델은 지연과 제한이 잦다"]),
            text_box(5, "Goal", 0.75, 4.15, 11.9, 1.45, [
                "목표: 검색된 문서에 근거한 답변을 고정된 카드 형식으로 제공해",
                "빠르고 예측 가능한 오류 분석 경험을 만든다.",
            ], 24, "17202A", fill="F6FAF7", line="CFE5D6"),
        ],
        [
            title(2, "전체 아키텍처"),
            bullet_card(3, 0.65, 1.55, 3.6, 3.9, "Frontend", ["Vite", "React", "TypeScript", "DM형 챗봇 UI"]),
            bullet_card(4, 4.85, 1.55, 3.6, 3.9, "Backend", ["FastAPI", "/api/chat", "SQLAlchemy", "Oracle DB 저장"]),
            bullet_card(5, 9.05, 1.55, 3.6, 3.9, "Search/RAG", ["JSON 오류 문서", "BAAI/bge-m3 임베딩", "Chroma Vector DB", "문서 기반 답변 생성"]),
            text_box(6, "Flow", 1.2, 5.95, 11.0, 0.55, ["질문 입력 → 문서 검색 → 섹션별 답변 생성 → 대화 기록 저장 → 프론트 렌더링"], 19, "185FBA"),
        ],
        [
            title(2, "백엔드 흐름"),
            bullet_card(3, 0.75, 1.55, 3.65, 4.25, "1. 요청 수신", ["session_id", "question", "FastAPI 라우터"]),
            bullet_card(4, 4.85, 1.55, 3.65, 4.25, "2. 문서 검색", ["오류 코드 직접 매칭", "카테고리 필터", "유사도 검색"]),
            bullet_card(5, 8.95, 1.55, 3.65, 4.25, "3. 답변 생성", ["오류 요약", "원인", "해결 방법", "수정 코드 예시", "주의사항"]),
            text_box(6, "Note", 0.9, 6.15, 11.65, 0.55, ["검색 문서가 있으면 LLM 호출 없이 답변을 만들어 속도와 안정성을 확보했습니다."], 18, "16643B"),
        ],
        [
            title(2, "프론트엔드 UX"),
            bullet_card(3, 0.75, 1.45, 5.75, 2.25, "대화형 UI", ["사용자 질문은 왼쪽", "AI 답변은 오른쪽", "Enter로 바로 전송", "Shift+Enter는 줄바꿈"]),
            bullet_card(4, 6.85, 1.45, 5.75, 2.25, "답변 표현", ["섹션 제목을 크게 표시", "섹션 사이 점선 구분", "진단 방법 카드는 숨김", "수정 코드 예시는 코드 블록 표시"]),
            text_box(5, "Sample", 1.1, 4.25, 11.0, 1.55, [
                "[오류 요약] Permission denied: 권한 부족",
                "[원인] 실행 권한 또는 디렉터리 접근 권한 없음",
                "[수정 코드 예시] chmod +x deploy.sh && ./deploy.sh",
            ], 18, "17202A", fill="F5F8FC", line="D8E1EC"),
        ],
        [
            title(2, "데이터와 검색"),
            bullet_card(3, 0.75, 1.45, 5.75, 3.8, "문서 데이터", ["150개 이상의 오류 문서", "category/subcategory", "cause/diagnosis/solution", "examples/command_example"]),
            bullet_card(4, 6.85, 1.45, 5.75, 3.8, "검색 전략", ["오류 코드 우선 매칭", "기술 키워드로 카테고리 필터", "Chroma similarity 검색", "상위 문서 metadata 활용"]),
            text_box(5, "Why", 0.95, 5.85, 11.4, 0.75, ["LLM 추론보다 검색 문서 기반 생성이 빠르고, 답변 형식도 안정적입니다."], 20, "0B2240"),
        ],
        [
            title(2, "LLM과 OpenRouter 처리"),
            bullet_card(3, 0.75, 1.45, 5.75, 3.65, "초기 이슈", ["Gemma free 모델 rate limit", "긴 프롬프트 지연", "빈 응답 또는 JSON 오류", "프론트 pending처럼 보임"]),
            bullet_card(4, 6.85, 1.45, 5.75, 3.65, "개선 방식", ["무료 fallback 모델 구성", "timeout/max_tokens 설정", "빈 응답은 실패 처리", "문서 매칭 시 LLM 생략"]),
            text_box(5, "Result", 0.9, 5.85, 11.5, 0.7, ["결과: 일반 질문 처리 경로는 문서 검색 중심으로 바뀌어 응답 시간이 크게 줄었습니다."], 20, "16643B"),
        ],
        [
            title(2, "시연 시나리오"),
            bullet_card(3, 0.75, 1.35, 11.85, 1.2, "1. Linux 권한 오류", ["입력: 리눅스 권한 없음", "출력: Permission denied 원인과 chmod 예시"]),
            bullet_card(4, 0.75, 2.95, 11.85, 1.2, "2. Oracle 오류", ["입력: ORA-00942", "출력: 테이블/권한/스키마 관련 원인"]),
            bullet_card(5, 0.75, 4.55, 11.85, 1.2, "3. Python 패키지 오류", ["입력: ModuleNotFoundError", "출력: 가상환경과 pip 설치 확인"]),
            text_box(6, "Tip", 0.9, 6.25, 11.5, 0.45, ["발표에서는 답변 카드의 섹션 구조와 수정 코드 예시 표시를 강조하면 좋습니다."], 17, "185FBA"),
        ],
        [
            title(2, "검증 결과"),
            bullet_card(3, 0.75, 1.45, 5.75, 3.8, "자동 검증", ["백엔드 단위 테스트", "프론트 구조 테스트", "TypeScript/Vite build", "문법 컴파일 확인"]),
            bullet_card(4, 6.85, 1.45, 5.75, 3.8, "실측 예시", ["리눅스 권한 없음 검색", "RAG retrieval 약 0.3~0.5초", "6개 섹션 생성 확인", "수정 코드 예시 출력 확인"]),
            text_box(5, "Quality", 0.9, 5.85, 11.5, 0.65, ["API Key, 비밀번호, 토큰, DB 접속 정보는 답변과 로그에서 직접 노출하지 않도록 주의합니다."], 18, "C0392B"),
        ],
        [
            title(2, "개선 방향"),
            bullet_card(3, 0.75, 1.45, 3.65, 3.8, "검색 품질", ["문서 수 확장", "동의어/오타 보정", "카테고리 자동 분류"]),
            bullet_card(4, 4.85, 1.45, 3.65, 3.8, "운영 안정성", ["모델 상태 모니터링", "검색 로그 대시보드", "Oracle 권한 정책 정리"]),
            bullet_card(5, 8.95, 1.45, 3.65, 3.8, "UX 개선", ["대화 히스토리 보기", "복사 버튼", "코드 블록 강조", "피드백 버튼"]),
            text_box(6, "Closing", 0.95, 5.95, 11.35, 0.7, ["검색 문서 기반 챗봇으로 빠르고 일관된 코딩 오류 분석 경험을 제공합니다."], 22, "0B2240"),
        ],
    ]


def content_types(slide_count: int) -> str:
    overrides = "\n".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, slide_count + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  {overrides}
</Types>
"""


def presentation_xml(slide_count: int) -> str:
    ids = "\n".join(
        f'<p:sldId id="{255 + i}" r:id="rId{i}"/>' for i in range(1, slide_count + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldIdLst>{ids}</p:sldIdLst>
  <p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>
"""


def presentation_rels(slide_count: int) -> str:
    rels = "\n".join(
        f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        for i in range(1, slide_count + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {rels}
</Relationships>
"""


def package_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""


def core_props() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:dcmitype="http://purl.org/dc/dcmitype/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>IT 코딩 오류 분석 챗봇</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
"""


def app_props(slide_count: int) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
            xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
  <PresentationFormat>Widescreen</PresentationFormat>
  <Slides>{slide_count}</Slides>
</Properties>
"""


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
