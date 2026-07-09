import { FormEvent, KeyboardEvent, useMemo, useRef, useState } from "react";
import { API_BASE_URL } from "./api";
import { DashboardPage } from "./pages/DashboardPage";
import { WikiPage } from "./pages/WikiPage";
import "./App.css";

const REQUIRED_SECTIONS = [
  "[오류 요약]",
  "[원인]",
  "[진단 방법]",
  "[해결 방법]",
  "[수정 코드 예시]",
  "[주의사항]",
] as const;

type Role = "user" | "bot";

type ChatMessage = {
  id: string;
  role: Role;
  content: string;
};

type AnswerSection = {
  title: string;
  body: string;
};

const INITIAL_MESSAGES: ChatMessage[] = [
  {
    id: "welcome",
    role: "bot",
    content:
      "[오류 요약]\n오류 메시지를 보내주시면 검색된 문서를 기준으로 분석합니다.\n\n[원인]\n아직 분석할 오류가 입력되지 않았습니다.\n\n[진단 방법]\n```powershell\npython --version\npip --version\n```\n\n[해결 방법]\n1단계: 오류 메시지 전체를 붙여넣어 주세요.\n2단계: 실행한 명령어와 파일 경로를 함께 알려 주세요.\n3단계: API Key, 비밀번호, 토큰은 가려서 보내 주세요.\n\n[수정 코드 예시]\n오류 내용을 받으면 필요한 경우 표시합니다.\n\n[주의사항]\n민감한 접속 정보는 그대로 입력하지 마세요.",
  },
];

function createSessionId(): string {
  const saved = window.localStorage.getItem("coding-error-chat-session");
  if (saved) {
    return saved;
  }

  const next = `web-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  window.localStorage.setItem("coding-error-chat-session", next);
  return next;
}

export function parseAnswerSections(answer: string): AnswerSection[] {
  const foundSections: AnswerSection[] = [];

  REQUIRED_SECTIONS.forEach((section, index) => {
    const start = answer.indexOf(section);
    if (start === -1) {
      return;
    }

    const nextStarts = REQUIRED_SECTIONS.slice(index + 1)
      .map((nextSection) => answer.indexOf(nextSection, start + section.length))
      .filter((nextStart) => nextStart !== -1);
    const end = nextStarts.length > 0 ? Math.min(...nextStarts) : answer.length;

    foundSections.push({
      title: section,
      body: answer.slice(start + section.length, end).trim(),
    });
  });

  if (foundSections.length === 0) {
    return [{ title: "[답변]", body: answer.trim() || "관련 정보를 찾지 못했습니다." }];
  }

  return foundSections;
}

function MessageBubble({ message }: { message: ChatMessage }) {
  const sections = useMemo(
    () =>
      message.role === "bot"
        ? parseAnswerSections(message.content).filter((section) => section.title !== "[진단 방법]")
        : [],
    [message.content, message.role],
  );

  return (
    <article className={`message ${message.role}`}>
      <div className="avatar" aria-hidden="true">
        {message.role === "bot" ? "AI" : "나"}
      </div>
      <div className="bubble">
        {message.role === "user" ? (
          <p>{message.content}</p>
        ) : (
          <div className="answer-sections">
            {sections.map((section) => (
              <section className="answer-section" key={section.title}>
                <h2>{section.title}</h2>
                <p>{section.body || "관련 정보를 찾지 못했습니다."}</p>
              </section>
            ))}
          </div>
        )}
      </div>
    </article>
  );
}

function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>(INITIAL_MESSAGES);
  const [question, setQuestion] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState("");
  const sessionId = useRef(createSessionId());

  async function sendQuestion(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmed = question.trim();
    if (!trimmed || isSending) {
      return;
    }

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: trimmed,
    };
    const loadingMessage: ChatMessage = {
      id: `bot-loading-${Date.now()}`,
      role: "bot",
      content:
        "[오류 요약]\n오류 내용을 분석 중입니다.\n\n[원인]\n검색된 문서를 확인하고 있습니다.\n\n[진단 방법]\n```powershell\n잠시만 기다려 주세요\n```\n\n[해결 방법]\n답변을 준비하고 있습니다.\n\n[수정 코드 예시]\n필요한 경우 함께 표시합니다.\n\n[주의사항]\n민감한 정보는 화면에 남지 않도록 주의해 주세요.",
    };

    setMessages((current) => [...current, userMessage, loadingMessage]);
    setQuestion("");
    setIsSending(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId.current,
          question: trimmed,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = (await response.json()) as { answer?: string };

      setMessages((current) =>
        current.map((message) =>
          message.id === loadingMessage.id
            ? {
                ...message,
                id: `bot-${Date.now()}`,
                content: data.answer ?? "관련 정보를 찾지 못했습니다.",
              }
            : message,
        ),
      );
    } catch {
      setError("서버 연결을 확인해 주세요.");
      setMessages((current) =>
        current.map((message) =>
          message.id === loadingMessage.id
            ? {
                ...message,
                id: `bot-error-${Date.now()}`,
                content:
                  "[오류 요약]\n서버에서 답변을 받아오지 못했습니다.\n\n[원인]\nFastAPI 서버가 꺼져 있거나 API 주소가 다를 수 있습니다.\n\n[진단 방법]\n```powershell\nuvicorn app.main:app --reload\n```\n\n[해결 방법]\n1단계: 백엔드 서버가 실행 중인지 확인하세요.\n2단계: 프론트엔드의 API 주소가 맞는지 확인하세요.\n3단계: 다시 질문을 전송해 주세요.\n\n[수정 코드 예시]\n관련 정보를 찾지 못했습니다.\n\n[주의사항]\n.env 파일의 API Key와 DB 접속 정보는 노출하지 마세요.",
              }
            : message,
        ),
      );
    } finally {
      setIsSending(false);
    }
  }

  function handleComposerKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      event.currentTarget.form?.requestSubmit();
    }
  }

  return (
    <main className="app-shell">
      <section className="chat-panel" aria-label="코딩 오류 분석 챗봇">
        <header className="chat-header">
          <div className="bot-mark">IT</div>
          <div>
            <h1>코딩 오류 분석 챗봇</h1>
          </div>
          <span className="status-dot">검색 문서 기반</span>
        </header>

        <div className="messages" aria-live="polite">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
        </div>

        {error ? <p className="error-text">{error}</p> : null}

        <form className="composer" onSubmit={sendQuestion}>
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            onKeyDown={handleComposerKeyDown}
            placeholder="오류 메시지를 붙여넣어 주세요"
            rows={2}
          />
          <button type="submit" disabled={isSending || !question.trim()} aria-label="질문 전송">
            전송
          </button>
        </form>
      </section>
    </main>
  );
}

function AppNavigation() {
  const links = [
    ["/", "챗봇"],
    ["/wiki", "오류 위키"],
    ["/dashboard", "대시보드"],
  ];

  return (
    <nav className="app-nav" aria-label="주요 화면">
      {links.map(([href, label]) => (
        <a className={window.location.pathname === href ? "active" : ""} href={href} key={href}>
          {label}
        </a>
      ))}
    </nav>
  );
}

function AppPage({ children }: { children: React.ReactNode }) {
  return (
    <>
      <AppNavigation />
      {children}
    </>
  );
}

export default function App() {
  const path = window.location.pathname;

  if (path === "/wiki") {
    return (
      <AppPage>
        <WikiPage />
      </AppPage>
    );
  }

  if (path === "/dashboard") {
    return (
      <AppPage>
        <DashboardPage />
      </AppPage>
    );
  }

  return <ChatPage />;
}
