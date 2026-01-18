# Architecture Gym 환경설정 세팅 계획 (Setting Plan)
<!-- Created by Antigravity on 2026-01-16: Architecture Gym 프로젝트 로드맵 및 초기 설정 계획서 -->

## 1. 프로젝트 개요
- **프로젝트 명**: Architecture Gym (모의 면접 시스템)
- **컨셉**: 면접의 딱딱함 대신 'Playground' 느낌의 재미와 성취감을 주는 엔지니어링 훈련 플랫폼
- **주요 기능**: 5가지 엔지니어링 챕터 실습, 토큰 보상, 리더보드 경쟁, 각각 개별 체험 가능

## 2. 기술 스택 (Tech Stack)
### Backend
- **Framework**: Django (REST Framework)
- **Task Queue**: Celery (비동기 채점 및 AI 에이전트 실행 관리)
- **Broker**: Redis (Celery를 위한 브로커 및 캐시 서버)
- **Database**: SQLite (개발용) 또는 PostgreSQL

### Frontend
- **Framework**: Vue.js (Vite 기반)
- **Styling**: Vanilla CSS (Premium Design), Lucide Icons
- **Background**: `image/sports_gym.mp4`를 활용한 동적 메인 화면

### Virtual Environment
- **Name**: `final` (Python 3.11+)

## 3. 챕터 구성 (5 Chapters)
1. **Code Practice**: 실무형 코딩 테스트 (Rate Limiter, Log Aggregator 등)
2. **Debug Practice**: 버그 수정(Bug Hunt) 및 리팩토링(Cleanup)
3. **System Practice**: 시스템 아키텍처 설계 (Mermaid 다이어그램 활용)
4. **Ops Practice**: 장애 대응 시뮬레이션 (Incident Response)
5. **Agent Practice**: AI 에이전트 최적화 (Prompt, RAG, Tool Calling 디버깅)

## 4. 환경 구성 단계 및 일정
### 1단계: 가상환경 및 백엔드 기초 세팅
- [ ] `final` 가상환경 생성 및 활성화
- [ ] Django 프로젝트 및 앱 생성 (`api`, `chapters`)
- [ ] Celery 및 Redis 연동 설정
- [ ] 기본 DB 모델링 (User, Score, Token, Leaderboard)

### 2단계: 프론트엔드 기초 세팅
- [ ] Vite를 이용한 Vue.js 프로젝트 생성
- [ ] 메인 레이아웃 구성 (`sports_gym.mp4` 배경 적용)
- [ ] 5개 챕터 진입 카드 UI 구현

### 3단계: 챕터별 기능 구현
- [ ] 각 챕터별 API 엔드포인트 개발
- [ ] Celery를 이용한 비동기 평가 로직 구현
- [ ] Mermaid.js를 이용한 시스템 설계 툴 연동

### 4단계: 게임화 요소 적용
- [ ] 토큰 지급 로직 및 리더보드 기능 구현
- [ ] 사용자 대시보드 (성취도 시각화)

### 5단계: 최종 폴리싱 및 배포 준비
- [ ] UI/UX 고도화 (프리미엄 디자인 적용)
- [ ] 통합 테스트 및 버그 수정

## 5. 초기 실행 가이드 (Draft)
```bash
# 가상환경 생성
python -m venv final

# 가상환경 활성화 (Windows)
.\final\Scripts\activate

# 패키지 설치
pip install django djangorestframework celery redis django-cors-headers

# 프론트엔드 세팅
npx -y create-vite@latest frontend --template vue
cd frontend
npm install
```
