export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export type WikiDocument = {
  id: string;
  category: string;
  subcategory?: string;
  error_code: string;
  title: string;
  error_message?: string;
  description: string;
  cause: string[];
  diagnosis: string[];
  solution: string[];
  examples: string[];
  keywords: string[];
  caution?: string;
  source_title?: string;
  source_url?: string;
  updated_at?: string;
};

export type DashboardSummary = {
  total_questions: number;
  today_questions: number;
  month_questions: number;
  active_users: number;
  wiki_documents: number;
};

export type CountPoint = {
  date?: string;
  month?: string;
  count: number;
};

export type TopKeyword = {
  keyword: string;
  count: number;
};

export type RecentLog = {
  id: number;
  time: string;
  user: string;
  question: string;
  answer_summary: string;
  category: string;
  response_time: number | null;
};

export type CategoryStat = {
  category: string;
  count: number;
};

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function fetchWikiDocuments() {
  return request<{ count: number; categories: string[]; documents: WikiDocument[] }>("/api/wiki");
}

export async function searchWikiDocuments(keyword: string) {
  return request<{ keyword: string; count: number; documents: WikiDocument[] }>(
    `/api/wiki/search?keyword=${encodeURIComponent(keyword)}`,
  );
}

export async function fetchDashboardSummary() {
  return request<DashboardSummary>("/api/dashboard/summary");
}

export async function fetchDailyQuestions() {
  return request<CountPoint[]>("/api/dashboard/daily-questions");
}

export async function fetchMonthlyQuestions() {
  return request<CountPoint[]>("/api/dashboard/monthly-questions");
}

export async function fetchTopKeywords() {
  return request<TopKeyword[]>("/api/dashboard/top-keywords");
}

export async function fetchRecentLogs() {
  return request<RecentLog[]>("/api/dashboard/recent-logs");
}

export async function fetchCategoryStats() {
  return request<CategoryStat[]>("/api/dashboard/category-stats");
}
