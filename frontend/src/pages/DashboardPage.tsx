import { useEffect, useMemo, useState } from "react";
import {
  CategoryStat,
  CountPoint,
  DashboardSummary,
  fetchCategoryStats,
  fetchDailyQuestions,
  fetchDashboardSummary,
  fetchMonthlyQuestions,
  fetchRecentLogs,
  fetchTopKeywords,
  RecentLog,
  TopKeyword,
} from "../api";

const initialSummary: DashboardSummary = {
  total_questions: 0,
  today_questions: 0,
  month_questions: 0,
  active_users: 0,
  wiki_documents: 0,
};

export function SummaryCards({ summary }: { summary: DashboardSummary }) {
  const cards = [
    ["총 질문 수", summary.total_questions],
    ["오늘 질문 수", summary.today_questions],
    ["이번 달 질문 수", summary.month_questions],
    ["활성 사용자 수", summary.active_users],
    ["전체 위키 문서 수", summary.wiki_documents],
  ];

  return (
    <section className="summary-grid" aria-label="대시보드 핵심 지표">
      {cards.map(([label, value]) => (
        <article className="metric-card" key={label}>
          <span>{label}</span>
          <strong>{Number(value).toLocaleString()}</strong>
        </article>
      ))}
    </section>
  );
}

function BarChart({ title, points, labelKey }: { title: string; points: CountPoint[]; labelKey: "date" | "month" }) {
  const max = Math.max(1, ...points.map((point) => point.count));
  const visiblePoints = points.slice(-12);

  return (
    <section className="chart-card">
      <h2>{title}</h2>
      <div className="bar-chart">
        {visiblePoints.map((point) => (
          <div className="bar-item" key={point[labelKey]}>
            <div className="bar-track">
              <span style={{ height: `${Math.max(6, (point.count / max) * 100)}%` }} />
            </div>
            <small>{String(point[labelKey] ?? "").slice(labelKey === "date" ? 5 : 0)}</small>
            <strong>{point.count}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}

export function DailyQuestionChart({ points }: { points: CountPoint[] }) {
  return <BarChart title="일별 질문 수" points={points} labelKey="date" />;
}

export function MonthlyQuestionChart({ points }: { points: CountPoint[] }) {
  return <BarChart title="월별 질문 수" points={points} labelKey="month" />;
}

export function TopKeywordList({ keywords }: { keywords: TopKeyword[] }) {
  return (
    <section className="panel-card">
      <h2>많이 질문한 내용 Top 10</h2>
      <ol className="top-keywords">
        {keywords.map((item) => (
          <li key={item.keyword}>
            <span>{item.keyword}</span>
            <strong>{item.count}</strong>
          </li>
        ))}
      </ol>
      {keywords.length === 0 ? <p className="empty-state">아직 질문 데이터가 없습니다.</p> : null}
    </section>
  );
}

export function CategoryStatsChart({ stats }: { stats: CategoryStat[] }) {
  const total = useMemo(() => stats.reduce((sum, item) => sum + item.count, 0), [stats]);

  return (
    <section className="panel-card">
      <h2>카테고리별 질문 비율</h2>
      <div className="ratio-list">
        {stats.map((item) => {
          const percent = total ? Math.round((item.count / total) * 100) : 0;
          return (
            <div className="ratio-row" key={item.category}>
              <div>
                <span>{item.category}</span>
                <strong>{percent}%</strong>
              </div>
              <em><i style={{ width: `${percent}%` }} /></em>
            </div>
          );
        })}
      </div>
      {stats.length === 0 ? <p className="empty-state">카테고리 통계가 없습니다.</p> : null}
    </section>
  );
}

export function RecentChatLogs({ logs }: { logs: RecentLog[] }) {
  return (
    <section className="panel-card recent-log-card">
      <h2>최근 대화 로그</h2>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>시간</th>
              <th>사용자</th>
              <th>질문 내용</th>
              <th>AI 답변 요약</th>
              <th>카테고리</th>
              <th>응답 시간</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id}>
                <td>{log.time ? new Date(log.time).toLocaleString() : "-"}</td>
                <td>{log.user}</td>
                <td>{log.question}</td>
                <td>{log.answer_summary}</td>
                <td>{log.category}</td>
                <td>{log.response_time ? `${log.response_time}ms` : "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {logs.length === 0 ? <p className="empty-state">최근 대화 기록이 없습니다.</p> : null}
    </section>
  );
}

export function DashboardPage() {
  const [summary, setSummary] = useState(initialSummary);
  const [daily, setDaily] = useState<CountPoint[]>([]);
  const [monthly, setMonthly] = useState<CountPoint[]>([]);
  const [topKeywords, setTopKeywords] = useState<TopKeyword[]>([]);
  const [recentLogs, setRecentLogs] = useState<RecentLog[]>([]);
  const [categoryStats, setCategoryStats] = useState<CategoryStat[]>([]);
  const [status, setStatus] = useState("대시보드 데이터를 불러오는 중입니다.");

  useEffect(() => {
    Promise.all([
      fetchDashboardSummary(),
      fetchDailyQuestions(),
      fetchMonthlyQuestions(),
      fetchTopKeywords(),
      fetchRecentLogs(),
      fetchCategoryStats(),
    ])
      .then(([summaryData, dailyData, monthlyData, keywordData, logData, categoryData]) => {
        setSummary(summaryData);
        setDaily(dailyData);
        setMonthly(monthlyData);
        setTopKeywords(keywordData);
        setRecentLogs(logData);
        setCategoryStats(categoryData);
        setStatus("");
      })
      .catch(() => setStatus("백엔드 대시보드 API 연결을 확인해 주세요."));
  }, []);

  return (
    <main className="page-shell dashboard-page">
      <header className="page-title">
        <div>
          <span>Admin Dashboard</span>
          <h1>관리자 대시보드</h1>
        </div>
        <p>챗봇 사용 기록과 위키 문서 현황을 한 화면에서 확인합니다.</p>
      </header>

      <SummaryCards summary={summary} />
      <div className="dashboard-grid">
        <DailyQuestionChart points={daily} />
        <MonthlyQuestionChart points={monthly} />
        <TopKeywordList keywords={topKeywords} />
        <CategoryStatsChart stats={categoryStats} />
      </div>
      <RecentChatLogs logs={recentLogs} />
      {status ? <p className="notice-text">{status}</p> : null}
    </main>
  );
}

