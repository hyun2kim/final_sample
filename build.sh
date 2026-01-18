#!/usr/bin/env bash
# exit on error
set -o errexit

# pip 업그레이드 및 패키지 설치
python -m pip install --upgrade pip
pip install -r requirements.txt

# 정적 파일 모으기 (WhiteNoise용)
python manage.py collectstatic --no-input

# 데이터베이스 마이그레이션 적용
python manage.py migrate
