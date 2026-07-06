from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import chat
from app.database.connection import Base, engine
from app.database import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description='IT 엔지니어를 위한 오픈소스/오라클 SQL 에러 트러블슈팅 및 사내 위키 챗봇',
    version='0.138.0'
)

# 프런트엔드와 원활한 통신을 위한 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], # 개발 단계에서는 모두 허용, 배포 시 프런트 주소만 지정
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# API 라우터 등록
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=['Chat'])


@app.get('/')
def read_root():
    return {'message': f'Welcome to {settings.PROJECT_NAME} API Server!'}