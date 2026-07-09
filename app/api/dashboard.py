from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services import dashboard_service


router = APIRouter()


@router.get("/dashboard/summary")
async def dashboard_summary(db: Session = Depends(get_db)):
    return dashboard_service.get_summary(db)


@router.get("/dashboard/daily-questions")
async def dashboard_daily_questions(db: Session = Depends(get_db)):
    return dashboard_service.get_daily_questions(db)


@router.get("/dashboard/monthly-questions")
async def dashboard_monthly_questions(db: Session = Depends(get_db)):
    return dashboard_service.get_monthly_questions(db)


@router.get("/dashboard/top-keywords")
async def dashboard_top_keywords(db: Session = Depends(get_db)):
    return dashboard_service.get_top_keywords(db)


@router.get("/dashboard/recent-logs")
async def dashboard_recent_logs(db: Session = Depends(get_db)):
    return dashboard_service.get_recent_logs(db)


@router.get("/dashboard/category-stats")
async def dashboard_category_stats(db: Session = Depends(get_db)):
    return dashboard_service.get_category_stats(db)
