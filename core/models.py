# 2026-01-16: Architecture Gym의 핵심 데이터 모델(Chapter, Problem, Progress, Submission) 정의
# [Role: 데이터베이스 스키마 정의 및 비즈니스 객체 모델링]
from django.db import models
from django.contrib.auth.models import User

class Chapter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Problem(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='problems', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    initial_code = models.TextField(blank=True, null=True)
    difficulty = models.CharField(max_length=20, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    token_reward = models.IntegerField(default=10)

    def __str__(self):
        return self.title

class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_tokens = models.IntegerField(default=0)
    completed_problems = models.ManyToManyField(Problem, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Progress"

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()  # Agent Practice에서는 수정된 프롬프트나 설정이 담김
    status = models.CharField(max_length=20, default='Pending') # Pending, Success, Failed
    result_detail = models.JSONField(null=True, blank=True)
    
    # 2026-01-16: Agent 성능 측정을 위한 전용 지표 추가
    accuracy = models.FloatField(default=0.0)
    hallucination_rate = models.FloatField(default=0.0)
    token_cost = models.IntegerField(default=0)
    latency = models.FloatField(default=0.0)
    feedback_message = models.TextField(blank=True, null=True) # 2026-01-16: AI 코치의 상세 분석 피드백
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"

# 2026-01-16: Agent Practice 전용 시나리오 정보 모델
class AgentProblem(models.Model):
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE, related_name='agent_info')
    base_system_prompt = models.TextField()
    base_retrieval_config = models.JSONField(default=dict) # 2026-01-16: top_k, chunk_size 등 RAG 설정
    tool_definitions = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"Agent Info for: {self.problem.title}"

# 2026-01-16: Agent 검증을 위한 테스트 케이스 모델
class AgentTestCase(models.Model):
    agent_problem = models.ForeignKey(AgentProblem, related_name='test_cases', on_delete=models.CASCADE)
    input_query = models.TextField()
    expected_response = models.TextField()
    ground_truth_context = models.TextField(blank=True, null=True) # 2026-01-16: RAG 검증용 근거 필드
    
    def __str__(self):
        return f"Test Case for {self.agent_problem.problem.title}"
