from collections import Counter, defaultdict
from datetime import datetime, timedelta
import re

from sqlalchemy.orm import Session

from app.database.models import ChatHistory
from app.services.wiki_service import find_category_for_text, get_wiki_documents


def _now():
    return datetime.utcnow()


def _answer_summary(answer: str, limit: int = 90):
    compact = " ".join((answer or "").split())
    if len(compact) <= limit:
        return compact
    return f"{compact[:limit]}..."


def _keyword_candidates(question: str):
    text = question or ""
    error_codes = re.findall(r"[A-Za-z]+-\d{3,10}", text)
    words = re.findall(r"[A-Za-z][A-Za-z0-9_+-]{2,}|[가-힣]{2,}", text)
    stopwords = {
        "error",
        "failed",
        "exception",
        "오류",
        "에러",
        "발생",
        "해결",
        "방법",
        "질문",
        "안됨",
        "없음",
    }
    filtered_words = [word for word in words if word.lower() not in stopwords]
    return [code.upper() for code in error_codes] + filtered_words[:4]


def get_summary(db: Session):
    now = _now()
    today_start = datetime(now.year, now.month, now.day)
    month_start = datetime(now.year, now.month, 1)

    return {
        "total_questions": db.query(ChatHistory).count(),
        "today_questions": db.query(ChatHistory).filter(ChatHistory.created_at >= today_start).count(),
        "month_questions": db.query(ChatHistory).filter(ChatHistory.created_at >= month_start).count(),
        "active_users": db.query(ChatHistory.session_id).distinct().count(),
        "wiki_documents": len(get_wiki_documents()),
    }


def get_daily_questions(db: Session, days: int = 30):
    now = _now()
    start = datetime(now.year, now.month, now.day) - timedelta(days=days - 1)
    rows = db.query(ChatHistory).filter(ChatHistory.created_at >= start).all()
    counts = Counter(row.created_at.strftime("%Y-%m-%d") for row in rows if row.created_at)

    result = []
    for offset in range(days):
        date = (start + timedelta(days=offset)).strftime("%Y-%m-%d")
        result.append({"date": date, "count": counts.get(date, 0)})
    return result


def get_monthly_questions(db: Session):
    rows = db.query(ChatHistory).all()
    counts = Counter(row.created_at.strftime("%Y-%m") for row in rows if row.created_at)
    return [{"month": month, "count": count} for month, count in sorted(counts.items())]


def get_top_keywords(db: Session, limit: int = 10):
    rows = db.query(ChatHistory).all()
    counter = Counter()
    for row in rows:
        counter.update(_keyword_candidates(row.question))
    return [{"keyword": keyword, "count": count} for keyword, count in counter.most_common(limit)]


def get_recent_logs(db: Session, limit: int = 20):
    rows = db.query(ChatHistory).order_by(ChatHistory.created_at.desc()).limit(limit).all()
    return [
        {
            "id": row.id,
            "time": row.created_at.isoformat() if row.created_at else "",
            "user": row.session_id,
            "question": row.question,
            "answer_summary": _answer_summary(row.answer),
            "category": find_category_for_text(row.question),
            "response_time": None,
        }
        for row in rows
    ]


def get_category_stats(db: Session):
    rows = db.query(ChatHistory).all()
    counts = defaultdict(int)
    for row in rows:
        counts[find_category_for_text(row.question)] += 1
    return [{"category": category, "count": count} for category, count in sorted(counts.items())]
