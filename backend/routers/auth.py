from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from passlib.context import CryptContext
from schemas import UserCreateRequest, UserLoginRequest
from database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# 비밀번호 단방향 암호화를 위한 bcrypt 알고리즘 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """평문 비밀번호를 bcrypt 해시로 변환합니다."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """입력받은 비밀번호와 DB의 해시값이 일치하는지 검증합니다."""
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register")
def register_user(data: UserCreateRequest, db: Session = Depends(get_db)):
    """신규 유저 회원가입 API (비밀번호 암호화 저장)"""
    try:
        # 1. 아이디 중복 확인
        check_query = text("SELECT id FROM users WHERE username = :username")
        existing_user = db.execute(check_query, {"username": data.username}).fetchone()
        if existing_user:
            raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다.")

        # 2. 비밀번호 해싱 처리 (절대 평문으로 저장하지 않음)
        hashed_pw = get_password_hash(data.password)

        # 3. DB 안전 저장
        insert_query = text("""
            INSERT INTO users (username, password_hash, full_name)
            VALUES (:username, :password_hash, :full_name)
            RETURNING id, username, full_name;
        """)
        
        result = db.execute(insert_query, {
            "username": data.username,
            "password_hash": hashed_pw,
            "full_name": data.full_name
        }).fetchone()
        
        db.commit()
        
        return {
            "status": "success",
            "message": f"{data.full_name}님, 회원가입이 완료되었습니다.",
            "user_id": str(result[0])
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"회원가입 처리 중 오류 발생: {str(e)}")

@router.post("/login")
def login_user(data: UserLoginRequest, db: Session = Depends(get_db)):
    """유저 로그인 API (비밀번호 검증)"""
    try:
        # 1. 아이디로 유저 검색
        query = text("SELECT id, password_hash, full_name FROM users WHERE username = :username")
        user = db.execute(query, {"username": data.username}).fetchone()

        # 2. 유저가 없거나 비밀번호가 틀린 경우 차단
        # (보안상 '아이디가 없습니다'와 '비밀번호가 틀렸습니다'를 구분하지 않고 뭉뚱그려 에러를 냅니다)
        if not user or not verify_password(data.password, user[1]):
            raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 올바르지 않습니다.")

        return {
            "status": "success",
            "message": f"{user[2]}님, 환영합니다.",
            "user": {
                "user_id": str(user[0]),
                "username": data.username,
                "full_name": user[2]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"로그인 처리 중 오류 발생: {str(e)}")