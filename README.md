# 🏗️ Architecture Gym 실행 가이드

안녕하세요! **Architecture Gym** 프로젝트에 오신 것을 환영합니다. 이 문서는 시스템을 설치하고 실행하는 방법을 아주 쉽고 친절하게 안내해 드립니다. 🚀

---

## 1. 사전 준비 사항 (Prerequisites)

시작하기 전에 아래 소프트웨어가 설치되어 있는지 확인해 주세요.
*   **Python 3.11+**: 시스템의 핵심 언어입니다.
*   **Redis**: Celery 비동기 작업을 위한 메시지 브로커입니다. (Windows라면 [Redis-x64](https://github.com/tporadowski/redis/releases) 또는 WSL을 권장합니다.)

---

## 2. 환경 설정 및 설치

이제 **Conda**를 통해 가상환경이 구축되었습니다. 아래 명령어로 바로 활성화하실 수 있습니다.

### 가상환경 활성화 (Conda)
```bash
conda activate final
```

이미 모든 라이브러리가 설치되어 있으므로 바로 실행이 가능합니다. 추가 라이브러리가 필요한 경우에만 설치해 주세요:
```bash
pip install -r requirements.txt
```

---

## 3. 시스템 실행 방법

Architecture Gym은 **백엔드, 셀러리(비동기 작업), 프론트엔드** 세 가지 파트로 구성됩니다. 각 파트를 개별 터미널에서 실행해 주세요.

### 🏁 Step 1: 데이터베이스 준비
처음 실행하거나 모델이 변경되었을 때 실행합니다.
```bash
python manage.py makemigrations
python manage.py migrate
```

### 🏁 Step 2: Django 백엔드 서버 실행
```bash
# 터미널 1
python manage.py runserver
```
*   서버 주소: `http://127.0.0.1:8000/`

### 🏁 Step 3: Celery 워커 서버 실행 (비동기 채점용)
**주의:** 먼저 Redis 서버가 실행 중이어야 합니다!
```bash
# 터미널 2
celery -A config worker -l info
```

### 🏁 Step 4: 프론트엔드 접속
현재 프론트엔드는 가볍고 빠른 실행을 위해 **Vue.js CDN** 방식을 사용하고 있습니다.
*   `frontend/index.html` 파일을 마우스 오른쪽 버튼으로 클릭하여 **'Open with Live Server'**로 열거나, 브라우저에 파일을 끌어다 놓으세요.

---

## 4. 프로젝트 구조 안내

*   📂 `config/`: Django 전체 설정 및 Celery 설정
*   📂 `core/`: 챕터 관리 및 사용자 데이터를 처리하는 백엔드 로직
*   📂 `frontend/`: Vue.js 기반의 예쁜 대시보드 화면
*   📂 `doc/`: 아키텍처 설계와 설치 계획서
*   📂 `old/`: 이전에 작업했던 소중한 파일들이 보관된 곳

---

## 💡 팁
*   로그인 및 관리자 기능을 사용하고 싶으시면 `python manage.py createsuperuser`로 관리자 계정을 만드세요.
*   `image/sports_gym.mp4` 파일이 배경으로 나오는지 확인해 보세요. 운동하는 느낌 물씬!

즐거운 엔지니어링 훈련 되세요! 🏋️‍♀️✨
