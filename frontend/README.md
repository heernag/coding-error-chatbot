# 코딩 오류 분석 챗봇 프론트엔드

Vite, React, TypeScript로 구성한 프론트엔드입니다. Vite 기본 보일러플레이트를 바탕으로 만들었고, 초기 예제 로고나 사용하지 않는 리소스는 제거했습니다.

## 실행 준비

프론트엔드 폴더로 이동합니다.

```powershell
cd D:\1jo_test\frontend
```

의존성을 설치합니다.

```powershell
npm install
```

## 개발 서버 실행

```powershell
npm run dev
```

기본 주소는 아래와 같습니다.

```text
http://127.0.0.1:5173
```

## 백엔드 실행

프론트엔드는 FastAPI의 `/api/chat`으로 질문을 보냅니다. 다른 터미널에서 백엔드도 실행해 주세요.

```powershell
cd D:\1jo_test
uvicorn app.main:app --reload
```

## Git Bash에서 실행할 때

VSCode 터미널이 Git Bash라면 Node 경로가 안 잡힐 수 있습니다. 그때는 아래처럼 PATH를 먼저 추가합니다.

```bash
export PATH="/d/Program Files/nodejs:$PATH"
npm install
npm run dev
```

## 빌드 확인

```powershell
npm run build
```

## 구성

```text
frontend/
  index.html
  package.json
  vite.config.ts
  tsconfig.json
  tsconfig.app.json
  tsconfig.node.json
  src/
    App.tsx
    App.css
    index.css
    main.tsx
    vite-env.d.ts
```
