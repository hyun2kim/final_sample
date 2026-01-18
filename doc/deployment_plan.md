# ngrok 실시간 공유 구현 계획서 (2026-01-18 업데이트)

Render 배포 대신 ngrok 터널링을 사용하여 현재 개발 중인 시스템을 팀원들이 즉시 접속할 수 있도록 공유하는 계획입니다.

## 주요 단계

### 1. `settings.py` 호스트 설정
- `ALLOWED_HOSTS`에 모든 호스트(`*`)를 허용하도록 설정하여 ngrok 도메인 접속을 허용합니다.
- `CSRF_TRUSTED_ORIGINS`에 `https://*.ngrok-free.dev`를 추가하여 보안 오류를 방지합니다.

### 2. 서버 실행
- `final` 가상환경 활성화: `conda activate final`
- Django 서버 구동: `python manage.py runserver`

### 3. ngrok 인증 설정
- ngrok 대시보드([dashboard.ngrok.com](https://dashboard.ngrok.com))에서 `Authtoken`을 발급받습니다.
- 터미널에 인증 토큰 등록: `ngrok config add-authtoken <YOUR_TOKEN>`

### 4. ngrok 터널링 및 공유
- 별도 터미널에서 터널 열기: `ngrok http 8000`
- 화면에 표시된 `Forwarding` URL을 복사하여 팀원들에게 공유합니다.

## 검증 계획
- 외부 기기(모바일 등)에서 공유된 URL로 접속하여 시스템이 정상 작동하는지 확인합니다.
