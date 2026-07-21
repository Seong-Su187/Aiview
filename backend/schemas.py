from pydantic import BaseModel
from typing import Optional

# --- [기존 모델 유지] ---
class BaselineRequest(BaseModel):
    user_id: str
    email: str
    baseline_jitter: float
    baseline_shimmer: float
    baseline_wpm: float

class SessionCreateRequest(BaseModel):
    user_id: str
    job_category: str

class QuestionGenerateRequest(BaseModel):
    job_category: str

# --- [신규 인증 관련 모델 추가] ---
class UserCreateRequest(BaseModel):
    username: str
    password: str
    full_name: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

# --- [🚀 신규 응답(Response) 모델 추가: 프론트엔드 데이터 전달용] ---
class QALogResponse(BaseModel):
    id: int
    session_id: str
    question: str
    transcribed_text: Optional[str] = None
    feedback: Optional[str] = None
    score: Optional[int] = None
    jitter_shaken_percentage: Optional[float] = None
    shimmer_shaken_percentage: Optional[float] = None
    speed_difference_wpm: Optional[float] = None
    gaze_percentage: Optional[float] = None
    emotion_percentage: Optional[float] = None
    
    # 💡 핵심: 프론트엔드 그래프 및 상세 카드에 표시될 누락되었던 2가지 데이터
    filler_word_count: Optional[int] = None
    gaze_loss_count: Optional[int] = None

    class Config:
        orm_mode = True  # Pydantic v1 호환 (SQLAlchemy 객체를 딕셔너리로 자동 변환)
        from_attributes = True  # Pydantic v2 호환