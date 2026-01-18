"""
Django settings for config project.

[Role: 프로젝트의 전반적인 환경 설정 및 라이브러리 연동 관리]

For more information on this file, see
https://docs.djangoproject.com/en/6.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/6.0/ref/settings/
"""

from pathlib import Path
import os
import environ
import dj_database_url

# 2026-01-18: BASE_DIR 정의 (다른 설정에서 경로 참조를 위해 최상단에 위치해야 함)
BASE_DIR = Path(__file__).resolve().parent.parent

# 2026-01-18: 환경 변수 설정을 위한 django-environ 초기화
env = environ.Env(
    DEBUG=(bool, False)
)

# .env 파일이 존재하는 경우 읽어오기
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# 2026-01-18: 보안을 위해 SECRET_KEY를 환경 변수에서 가져옴
SECRET_KEY = env('SECRET_KEY', default='django-insecure-fallback-key-for-dev')

# 2026-01-18: 실시간 공유(ngrok)를 위해 DEBUG=True 및 모든 호스트 허용 설정
DEBUG = True
ALLOWED_HOSTS = ['*']

# 2026-01-17: ngrok 접속 시 CSRF 검증을 위해 모든 오리진을 신뢰 목록에 추가 (공유 세션용)
# 주의: 실제 배포 시에는 특정 도메인으로 제한해야 합니다.
CSRF_TRUSTED_ORIGINS = ['https://*.ngrok-free.dev', 'http://*.ngrok.io']
if env('RENDER_EXTERNAL_URL', default=None):
    CSRF_TRUSTED_ORIGINS.append(env('RENDER_EXTERNAL_URL'))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 2026-01-16: 외부 라이브러리 및 커스텀 앱 추가
    'rest_framework',
    'corsheaders',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 2026-01-18: WhiteNoise 미들웨어를 SecurityMiddleware 바로 다음에 추가 (정적 파일 서빙용)
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 2026-01-16: CORS 미들웨어 추가 (프론트엔드 연동을 위함)
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend'], # 2026-01-16: 프론트엔드 폴더를 템플릿 경로에 추가
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# 2026-01-18: DATABASE_URL 환경 변수를 사용하여 데이터베이스 설정 (Render 등의 클라우드 환경 최적화)
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
# 2026-01-16: 프론트엔드 정적 파일(JS, CSS, Image) 경로 지정
STATICFILES_DIRS = [
    BASE_DIR / 'frontend',
]

# 2026-01-18: 프로덕션 환경에서의 정적 파일 모음 경로 설정
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 2026-01-18: WhiteNoise 정적 파일 압축 및 캐싱 설정
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/6.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 2026-01-16: Celery & Redis 설정 (2026-01-18: 환경 변수 도입)
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul'

CORS_ALLOW_ALL_ORIGINS = True # 테스트 환경을 위해 모든 오리진 허용
