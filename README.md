# 🎬 AI 면접 도우미 (AI Interview Assistant)

> **당신의 목소리를 기억하는 초개인화 AI 실시간 오디오-아바타 모의 면접 플랫폼**
> 사용자의 평소 목소리(Baseline) 데이터를 기준으로 긴장도(목소리 떨림, 발화 속도)를 실시간 물리 분석하고, AI-Hub 공공 데이터와 고용노동부 표준 지침을 기반으로 환각(Hallucination) 없는 고정밀 면접 피드백을 데스크톱 웹 환경에서 제공합니다.

---

## 📌 Project Overview

*   **프로젝트명:** AI 면접 도우미 (AI Interview Assistant)
*   **개발 환경:** Visual Studio Code (VS Code) + Google Colab (A100/L4 원격 GPU 가속)
*   **타겟 플랫폼:** 데스크톱 웹 환경 (Desktop Web Browser - Chrome 최적화)
*   **핵심 목표:**
    *   가입 시 평온 상태 음성(Baseline) 수집을 통한 개인화 대조군 데이터 축적
    *   OpenSMILE 및 WavLM/Wav2Vec2 오픈소스 감정 모델을 결합한 실시간 목소리 떨림 지표 연산
    *   Supabase (pgvector)와 AI-Hub 채용면접 인터뷰 데이터를 활용한 RAG 기반 답변 타당성 검증
    *   TencentGameMate MuseTalk 엔진을 이용한 초저지연 오디오 동기화 면접관 아바타 구동 (Web 웹소켓 스트리밍)
    *   실시간 2인 이상 다대다 경쟁 매칭을 통한 실전 고사장 분위기 재현

---

## 🛠 Tech Stack

### Frontend / Web
*   **Framework:** React (Web), HTML5 Video / Web Audio API
*   **Communication:** WebSockets (실시간 오디오 스트리밍 및 동시성 방 제어용)

### Backend & Database
*   **Framework:** FastAPI (Python 기반 고속 비동기 서버)
*   **Database:** Supabase (PostgreSQL)
*   **Vector DB:** Supabase pgvector 확장 모듈
*   **Auth:** Supabase Authentication

### AI / RAG Pipeline & Audio Analytics
*   **Acoustic Feature Extraction:** OpenSMILE (audEERING) - Jitter, Shimmer 물리 지표 추출
*   **Voice Emotion Recognition:** WavLM (`jihedjabnoun/wavlm-base-emotion`), Wav2Vec2 (`speechbrain/emotion-recognition-wav2vec2-IEMOCAP`)
*   **STT (Speech-to-Text):** OpenAI Whisper Large v3 (Faster-Whisper 로컬 가속 서빙)
*   **TTS (Text-to-Speech):** Edge TTS (로컬 가중치 구동 레이어)
*   **Digital Avatar Engine:** TencentGameMate MuseTalk (LivePortrait 이미지 모션 결합형)
*   **Orchestration & LLM:** LangChain / GPT-4o-mini (RAG 및 프롬프트 제어)

---

## 💡 Key Features

### 1. 가입 시 평온 상태 음성(Baseline) 분석 및 개인화 대조
*   회원가입 온보딩 시 사용자가 제공된 일상 텍스트를 30초~1분간 낭독합니다.
*   이때 추출된 주파수 변동률(Jitter), 진폭 변동률(Shimmer), 발화 속도(WPM)를 유저 고유의 '안정 상태 레퍼런스'로 Supabase DB에 적재합니다.
*   실제 면접 진행 시 이 Baseline 대비 긴장도 상승률을 연산하여 정밀 피드백을 제공합니다.

### 2. MuseTalk 기반 실시간 면접관 아바타 구동
*   고정된 면접관의 스틸 이미지 파일이 로컬 GPU(A100) 환경에서 연산되는 MuseTalk 엔진을 거쳐, TTS로 생성된 질문 오디오 청크에 맞추어 실시간으로 정밀한 립싱크 비디오로 합성됩니다.
*   브라우저 이탈이나 별도 플러그인 없이 데스크톱 웹 화면 내에서 면접관의 자연스러운 발화 리액션을 감상할 수 있습니다.

### 3. AI-Hub RAG 기반 답변 타당성 검증 및 5단계 평가 (BARS)
*   사용자가 업로드한 이력서를 LLM이 분석하여 맞춤 질문 5개를 생성합니다.
*   사용자의 음성 답변이 변환되면, **AI-Hub 채용면접 인터뷰 데이터셋**을 임베딩한 Vector DB에서 유사 맥락군을 쿼리해 옵니다.
*   고용노동부 표준 가이드라인 및 STAR(Situation, Task, Action, Result) 구조 정합성을 대조하여 내용의 적절성을 5단계 계량 평정표(BARS) 기준으로 냉철하게 채점합니다.
*   개인정보 보호를 위해 음성 데이터 원본은 자질 추출 및 전사 완료 즉시 시스템 메모리에서 영구 삭제(비식별화 보장) 처리합니다.

### 4. 실시간 웹소켓 다대다 서바이벌 매칭
*   동일 직무 지원자 2~3명을 하나의 가상 웹 면접장에 매칭합니다.
*   공통 질문에 대해 참가자들이 순서대로 발화하는 다대다 압박 환경을 제어합니다.
*   면접 종료 후, 참가자들의 음성 안정도와 답변 내용 점수를 상호 비교형 웹 대시보드로 시각화하여 강력한 모의 트레이닝 환경을 선사합니다.

---

## 🏗 System Architecture

### User Flow (Web Browser)
```
[웹 접속 및 로그인] ──► [평온 스크립트 녹음 (Baseline 데이터셋 구축)] ──► [이력서 업로드 및 직무 선택] ──► [AI 면접관 아바타 구동 및 5문항 인터뷰 진행] ──► [종합 대시보드 리포트 확인]
```

### RAG & Audio Pipeline 아키텍처
```
[유저 마이크 입력] ──► [FastAPI WebSocket 수신] ──► 1. OpenSMILE / WavLM ──► 평음 대조 긴장도 분석
                            │
                            └──► 2. Whisper STT ──► 텍스트화 ──► Supabase Vector DB (RAG)
                                                                       ▲
[AI-Hub 면접 데이터] ──► [임베딩 변환] ──► [Supabase pgvector] ◄───────┼─────► [유사도 매칭 및 채점]
[고용노동부 표준 가이드]                                                        │
[BARS 5단계 평가 적용]                                                          │
                                                                               ▼
[Web UI 리포트 출력] ◄── [MuseTalk 아바타 스트리밍] ◄── [Edge TTS] ◄── [LLM 피드백 및 다음 질문 생성]
```

---

## 👨‍💻 Team Roles

| 역할 (Role) | 담당 업무 (Responsibilities) | 담당자 (Members) |
| :--- | :--- | :--- |
| **PM / 기획** | 도메인 분석, AI-Hub 데이터 가이드라인 파싱, 고용노동부 BARS 평가 지표 설계 및 기획서 총괄 | 공동 |
| **Data Engineer** | AI-Hub 채용면접 인터뷰 데이터 정제 및 청킹, Supabase pgvector 기반 벡터 데이터베이스 인프라 구축, 오디오 데이터 비식별화 아키텍처 구현 | 팀원 A |
| **AI Engineer** | OpenSMILE, WavLM, Wav2Vec2 긴장도/감정 임베딩 파이프라인 구축, Faster-Whisper 최적화, MuseTalk-LivePortrait 실시간 립싱크 디퓨전 체인 제어 | 팀원 B, 팀원 C |
| **Backend** | FastAPI 비동기 웹소켓 서버 아키텍처 설계, 실시간 다인 매칭 룸 제어 프로토콜 구현, Supabase Auth 및 DB 연동 | 팀원 A, 팀원 D |
| **Frontend** | React 데스크톱 웹 어플리케이션 인터페이스 구현, Web Audio API 마이크 캡처 엔진 제어, 실시간 오디오/비디오 스트리밍 뷰어 및 결과 분석 웹 대시보드 시각화 | 팀원 D, 팀원 C |

---

## 🚀 Getting Started

### Prerequisites
*   Node.js (v18 이상) & npm / yarn
*   Python (v3.10 이상)
*   Visual Studio Code (VS Code)
*   CUDA Toolkit 11.8 이상 및 cuDNN (로컬 오픈소스 GPU 가속 추론 인프라용)
*   Supabase Account & OpenAI API Key

### Installation & Setup (통합 환경 구축)
```bash
# 1. 저장소 클론 및 프로젝트 루트 진입
git clone https://github.com/your-repo/AI-Interview-Assistant.git
cd AI-Interview-Assistant

# 2. 백엔드(FastAPI) 가상환경 설정 및 필수 패키지 일괄 설치
cd backend
python -m venv venv
source venv/bin/activate  # Windows 환경인 경우: venv\Scripts\activate
pip install -r requirements.txt

# [참고] backend/.env 파일을 생성하여 Supabase URL, Anon Key, OpenAI API Key를 입력해야 합니다.

# 3. 프론트엔드(React) 의존성 패키지 일괄 설치
cd ../frontend
npm install
```

### Running the App (터미널 실행 명령어)
```bash
# [터미널 1] 원격 GPU 가속 비동기 백엔드 서버 가동 (FastAPI)
cd backend
source venv/bin/activate  # Windows 환경인 경우: venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# [터미널 2] 데스크톱 웹 클라이언트 서버 가동 (React)
# 새 터미널 창을 열고 프로젝트 루트 폴더에서 아래를 실행합니다.
cd frontend
npm start
```
*   두 서버가 모두 정상 정상 구동되면 데스크톱 웹 브라우저를 열고 `http://localhost:3000` 주소로 접속하여 모의 면접 세션을 즉시 시작할 수 있습니다.

---

## 🔗 References & Academic Sources

*   **모의 면접 실효성 연구 근거:** [ORISE - Five Reasons Everybody Should Do a Mock Interview](https://orise.orau.gov/internships-fellowships/blog/five-reasons-everybody-should-do-a-mock-interview.html)
*   **실시간 오디오 대화 실현 가능성 벤치마킹:** [GeekNews - 실시간 AI 음성 인터랙션 선행 사례](https://news.hada.io/topic?id=27442)
*   **RAG 기준점 매칭 공공 데이터셋:** [AI-Hub 채용면접 인터뷰 데이터 공식 표준 저장소](https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=71592)
*   **음성 물리 자질 추출 오픈소스:** [audEERING openSMILE 공식 저장소](https://github.com/audeering/opensmile)
```