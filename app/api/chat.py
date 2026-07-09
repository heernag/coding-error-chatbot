from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from time import perf_counter

from app.database.connection import get_db
from app.database.models import ChatHistory
from app.services.diagnostics import log_duration, log_event

from app.core.config import settings
router = APIRouter()

# 클라이언트가 보낼 요청 데이터 구조 정의
class ChatRequest(BaseModel):
    session_id: str
    question: str

@router.post('/chat')
async def chat_with_ai(payload: ChatRequest, db: Session = Depends(get_db)):
    from app.services.rag_service import get_rag_answer

    # TODO: 추후 이곳에 DB 대화기록 조회 및 RAG 서비스 호출 로직이 들어갑니다.
    user_question = payload.question
    session_id = payload.session_id
    request_started_at = perf_counter()
    log_event(f"/api/chat request start session_id={session_id} question_length={len(user_question)}")


    # RAG 서비스 함수를 호출하여 AI 답변 받아오기
    ai_answer = get_rag_answer(user_question, session_id)
    log_duration("/api/chat answer generation", perf_counter() - request_started_at)

    # 받아온 대화 내역 DB에 저장하기
    db_started_at = perf_counter()
    chat_log = ChatHistory(
        session_id=session_id,
        question=user_question,
        answer=ai_answer
    )
    db.add(chat_log)
    db.commit()
    db.refresh(chat_log)
    log_duration("/api/chat DB save", perf_counter() - db_started_at)
    log_duration("/api/chat total", perf_counter() - request_started_at)
    

    return {
        "session_id": session_id,
        "answer": ai_answer,
         
        #"saved_id": chat_log.id
    }
    
    # ✅ POST 함수가 끝난 후 새로 추가
@router.get('/history/{session_id}')
async def get_chat_history(session_id: str, db: Session = Depends(get_db)):


    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.session_id == session_id)
        .order_by(ChatHistory.created_at.asc())
        .all()
    )
    return{
        "session_id": session_id,
        "count": len(history),
        "history": [
            {
                "id": chat.id,
                "question": chat.question,
                "answer": chat.answer,
                "created_at": chat.created_at
            }
            for chat in history
        ]
    }
