# 트러블슈팅 일지

## 1. Node.js 명령어 인식 문제

### 상황

VSCode 터미널에서 `node`, `npm` 명령어가 인식되지 않았습니다.

```powershell
npm : 'npm' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는 프로그램 이름으로 인식되지 않습니다.
```

### 원인

- Node.js가 `D:\Program Files\nodejs`에 설치되어 있었습니다.
- 일반 PowerShell에서는 `node`가 인식됐지만, VSCode 터미널의 PATH에는 Node 경로가 반영되지 않았습니다.
- Git Bash와 PowerShell은 환경변수 설정 문법이 달라 같은 명령어를 사용할 수 없었습니다.

### 해결

PowerShell에서 현재 터미널 세션에 Node 경로를 직접 추가했습니다.

```powershell
$env:Path = 'D:\Program Files\nodejs;' + $env:Path
```

npm 실행은 명시 경로로 처리했습니다.

```powershell
& 'D:\Program Files\nodejs\npm.cmd' run build
```

### 결과

Vite React TypeScript 프론트엔드 프로젝트에서 `npm install`, `npm run build`, `npm run dev` 실행이 가능해졌습니다.

## 2. React 프론트엔드 재구성

### 상황

기존 `frontend` 프로젝트 구성이 너무 빈약했고, Vite React TypeScript 기반으로 다시 구성할 필요가 있었습니다.

### 해결

- Vite + React + TypeScript 구조로 프론트엔드를 재구성했습니다.
- 사용하지 않는 Vite 기본 assets를 제거했습니다.
- DM 또는 카카오톡처럼 질문과 답변이 말풍선으로 보이는 챗봇 UI를 구현했습니다.
- Enter는 전송, Shift+Enter는 줄바꿈으로 동작하도록 변경했습니다.
- 사용자 메시지와 AI 메시지 위치를 요구사항에 맞게 조정했습니다.

### 결과

프론트엔드 빌드가 정상 통과했습니다.

```powershell
npm run build
```

## 3. AI 답변 섹션 표시 문제

### 상황

AI 답변에서 `[진단 방법]` 카드를 제거하고, 나머지 답변은 섹션별로 보기 좋게 표시해야 했습니다.

### 원인

- 백엔드 답변은 텍스트 섹션 형태였지만 프론트엔드에서 단순 문자열처럼 표시되고 있었습니다.
- 섹션별 박스가 많아 화면이 복잡해 보였습니다.

### 해결

- 프론트엔드에서 답변 문자열을 섹션 단위로 파싱하는 `parseAnswerSections()` 로직을 구현했습니다.
- `[진단 방법]`은 표시 대상에서 제외했습니다.
- 섹션 제목 글자 크기를 키웠습니다.
- 섹션마다 박스로 감싸던 스타일을 제거하고 점선 구분선으로 변경했습니다.

### 결과

답변은 다음 섹션 중심으로 정리되어 보입니다.

```text
[오류 요약]
[원인]
[해결 방법]
[수정 코드 예시]
[주의사항]
```

## 4. OpenRouter 무료 모델 rate limit 문제

### 상황

OpenRouter의 `google/gemma-4-26b-a4b-it:free` 모델을 사용했을 때 `/api/chat` 요청이 오래 pending 상태로 보였습니다.

### 진단

백엔드 로그를 통해 LLM 호출 구간에서 지연이 발생하는 것을 확인했습니다. 테스트 중 다음과 같은 429 오류도 확인했습니다.

```text
RateLimitError: 429
google/gemma-4-26b-a4b-it:free is temporarily rate-limited upstream
```

### 원인

- API Key 로드 문제는 아니었습니다.
- OpenRouter 무료 모델 upstream에서 rate limit이 발생했습니다.
- 무료 모델 특성상 트래픽이 몰리면 응답이 느리거나 실패할 수 있습니다.

### 해결

- OpenRouter fallback 모델 목록을 추가했습니다.
- `timeout=60`, `max_retries=0`, `max_tokens=700`을 설정했습니다.
- 빈 응답은 실패로 처리해 다음 모델로 넘어가게 했습니다.
- 최종적으로 문서가 검색되면 LLM 호출 없이 metadata 기반으로 답변을 생성하도록 변경했습니다.

### 결과

무료 모델 지연과 rate limit에 덜 의존하는 구조가 되었습니다.

## 5. `/api/chat` 응답 속도 문제

### 상황

프론트엔드에서 질문을 보내면 답변이 너무 늦게 오거나 pending 상태가 오래 유지됐습니다.

### 진단

백엔드에 구간별 로그를 추가했습니다.

```text
[CHAT DIAG] RAG retrieval elapsed=...
[CHAT DIAG] OpenRouter LLM call start
[CHAT DIAG] OpenRouter LLM call elapsed=...
[CHAT DIAG] /api/chat DB save elapsed=...
```

### 원인

- RAG 검색은 약 0.3~0.5초 수준으로 빠르게 동작했습니다.
- 병목은 OpenRouter LLM 호출 구간이었습니다.

### 해결

- 검색 문서가 있으면 LLM 호출 없이 답변을 생성하도록 변경했습니다.
- `cause`, `diagnosis`, `solution`, `examples`, `command_example`, `caution` metadata를 바로 답변 섹션에 매핑했습니다.

### 결과

예시 질문 `리눅스 권한 없음`에서 RAG 검색은 약 0.355초로 측정됐고, 답변 섹션도 정상 표시되었습니다.

```text
RAG retrieval elapsed=0.355s
sections=[오류 요약, 원인, 진단 방법, 해결 방법, 수정 코드 예시, 주의사항]
```

## 6. 수정 코드 예시가 표시되지 않는 문제

### 상황

프론트엔드에 `[수정 코드 예시]` 섹션은 있었지만 실제 코드 예시가 나오지 않았습니다.

### 원인

원본 JSON에는 `examples`, `command_example` 필드가 있었지만, ChromaDB metadata 생성 과정에서 해당 필드가 빠져 있었습니다.

### 해결

`app/services/vector_db.py`에서 metadata에 예시 필드를 추가했습니다.

```python
"examples": " / ".join(item.get("examples", [])),
"command_example": " / ".join(item.get("command_example", [])),
```

이미 생성된 ChromaDB metadata에 예시가 없을 수 있으므로, `rag_service.py`에서 원본 JSON을 다시 조회해 예시를 보강하는 fallback도 추가했습니다.

### 결과

`리눅스 권한 없음` 질문에서 다음과 같은 코드 예시가 표시되도록 개선했습니다.

```text
id / ls -l <path> / namei -l <path>
./deploy.sh -> bash: ./deploy.sh: Permission denied
해결: chmod +x deploy.sh && ./deploy.sh
```

## 7. 한글 인코딩 출력 문제

### 상황

PowerShell에서 일부 한글 출력이 깨져 보였습니다.

### 원인

- 파일 내용은 UTF-8이지만 콘솔 출력 인코딩이 맞지 않아 글자가 깨져 보일 수 있었습니다.
- Python 실행 시 출력 인코딩을 명시하지 않으면 한글 로그 확인이 어려울 수 있었습니다.

### 해결

한글 출력 확인이 필요한 경우 다음 환경변수를 사용했습니다.

```powershell
$env:PYTHONIOENCODING='utf-8'
```

### 결과

테스트와 로그 확인 시 한글 내용을 더 안정적으로 확인할 수 있었습니다.

## 8. GitHub 업로드와 `.env` 제외

### 상황

프로젝트를 GitHub에 올리되 `.env` 파일은 제외해야 했습니다.

### 원인

- `.env`에는 OpenRouter API Key 같은 민감 정보가 들어 있습니다.
- GitHub에 노출되면 API Key 유출과 비용 발생 위험이 있습니다.

### 해결

- `.gitignore`를 정리했습니다.
- `.env`, DB 파일, ChromaDB, `node_modules`, 가상환경 폴더, 빌드 결과물을 제외했습니다.
- 안전한 예시 설정은 `.env.example`로 관리했습니다.
- GitHub 원격 저장소에 push했습니다.

### 결과

GitHub 저장소에 민감 정보 없이 프로젝트를 업로드했습니다.

```text
https://github.com/heernag/coding-error-chatbot
```

## 9. 트러블슈팅 요약

| 문제 | 원인 | 해결 |
|---|---|---|
| npm 인식 실패 | VSCode PATH 문제 | Node 경로를 PowerShell 세션에 직접 추가 |
| `/api/chat` pending | LLM 호출 지연 | 문서 metadata 기반 답변 생성으로 변경 |
| Gemma free 실패 | OpenRouter upstream 429 | fallback 모델과 timeout 설정 |
| 수정 코드 예시 미표시 | ChromaDB metadata 누락 | `examples`, `command_example` 추가 |
| 한글 깨짐 | 콘솔 인코딩 문제 | UTF-8 출력 환경변수 사용 |
| `.env` 보안 | API Key 노출 위험 | `.gitignore`와 `.env.example` 분리 |

## 10. 배운 점

- AI API는 외부 서비스 상태에 영향을 받으므로 timeout, fallback, 로그가 필요합니다.
- RAG 시스템에서는 LLM보다 데이터 구조와 metadata 설계가 답변 품질에 더 큰 영향을 줄 수 있습니다.
- 문제를 추측으로 고치기보다 구간별 로그를 추가하면 병목 지점을 빠르게 찾을 수 있습니다.
- GitHub 업로드 전에는 `.env`, DB, `node_modules`, 가상환경이 제외됐는지 반드시 확인해야 합니다.
