"""
URL configuration for config project.

[Role: 프로젝트 전체의 URL 라우팅 및 API 엔드포인트 맵핑 관리]

https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# 2026-01-16: REST Framework Router를 활용한 API 엔드포인트 자동 라우팅 설정
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from core.views import ChapterViewSet, ProblemViewSet, SubmissionViewSet

router = DefaultRouter()
router.register(r'chapters', ChapterViewSet)
router.register(r'problems', ProblemViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # 2026-01-16: 메인 프론트엔드 페이지 서빙
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]
