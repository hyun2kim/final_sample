# 2026-01-16: Agent Practice 및 기본 기능을 위한 API ViewSet 구현
# [Role: API 요청 처리(Request) 및 비즈니스 로직(Action) 수행]
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Chapter, Problem, Submission
from .serializers import ChapterSerializer, ProblemSerializer, SubmissionSerializer

class ChapterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Chapter.objects.all().order_by('order')
    serializer_class = ChapterSerializer

class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        # 2026-01-16: 실제 환경에서는 request.user를 사용해야 함
        from django.contrib.auth.models import User
        user = User.objects.first()
        serializer.save(user=user)

    @action(detail=False, methods=['post'], url_path='agent')
    def submit_agent(self, request):
        problem_id = request.data.get('problem_id')
        code = request.data.get('code')
        
        print(f"[DEBUG] Submitting agent for problem: {problem_id}")
        
        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            return Response({'error': 'Problem not found'}, status=status.HTTP_404_NOT_FOUND)

        from django.contrib.auth.models import User
        user = User.objects.first()
        
        # 2026-01-16: 사용자가 없는 경우 임시로 생성하여 진행 (연습 환경용)
        if not user:
            user = User.objects.create_user(username='practice_user', password='password123')
            print("[DEBUG] Created practice_user as no user found")

        try:
            submission = Submission.objects.create(
                user=user,
                problem=problem,
                code=code,
                status='Pending'
            )

            # 지표 할당 및 동적 피드백 생성
            submission.status = 'Success'
            submission.accuracy = 88.0 # 임시 고정값 (향후 실제 평가 엔진 연동)
            submission.hallucination_rate = 8.0
            submission.latency = 1.1
            submission.token_cost = 240

            if submission.accuracy >= 90:
                feedback = "프롬프트의 지시사항이 매우 명확합니다! 특히 지식 범위를 Context로 한정하고 예제로 가이드한 점이 완벽합니다."
            elif submission.accuracy >= 75:
                feedback = "기본적인 답변 능력은 우수하지만, 복잡한 질문에서 약간의 추론 오류가 보입니다. Few-shot 예제를 추가해 보세요."
            else:
                feedback = "에이전트가 지시사항을 무시하고 지어내는 경우가 많습니다. 'System' 역할을 더 강하게 부여하고 제약 사항을 번호로 나누어 작성해 보세요."
            
            if submission.hallucination_rate > 10:
                feedback += " 또한 현재 환각율이 높습니다. '모르는 내용은 모른다고 말해'라는 명시적 금지어를 추가해 보세요."

            submission.feedback_message = feedback
            submission.save()
            
            print(f"[DEBUG] Submission processed with dynamic feedback: {submission.id}")
            return Response(SubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"[DEBUG] Error creating submission: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
