# 2026-01-16: Django 시작 시 Celery 앱이 자동 로드되도록 설정
# [Role: Django 프로젝트 패키지 초기화 및 Celery 앱 익스포트]
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
