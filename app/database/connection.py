from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# DB 엔진 생성(설정해둔 DATABASE_URL 사용)
# sqlite인 경우 동시성 처리를 위해 check_same_thread 옵션 필요
connect_args = {'check_same_thread':False} if 'sqlite' in settings.DATABASE_URL else {}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

# DB와 데이터를 주고받을 세션 공장 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 테이블 모델들이 상속받을 기본 클래스
Base = declarative_base()

# FastAPI에서 DB에 안전하게 접근하기 위한 의존성 함수
# API 요청이 들어올 때 세션을 열고, 처리가 끝나면 자동으로 닫아준다.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        