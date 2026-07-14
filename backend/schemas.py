from pydantic import BaseModel

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