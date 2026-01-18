# 2026-01-16: Agent Practice API를 위한 Serializer 정의
# [Role: DB 모델 객체와 JSON 데이터 간의 직렬화/역직렬화 로직 관리]
from rest_framework import serializers
from .models import Chapter, Problem, AgentProblem, AgentTestCase, Submission

class AgentTestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentTestCase
        fields = ['id', 'input_query', 'expected_response']

class AgentProblemSerializer(serializers.ModelSerializer):
    test_cases = AgentTestCaseSerializer(many=True, read_only=True)
    
    class Meta:
        model = AgentProblem
        fields = ['base_system_prompt', 'base_retrieval_config', 'tool_definitions', 'test_cases']

class ProblemSerializer(serializers.ModelSerializer):
    agent_info = AgentProblemSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = ['id', 'title', 'content', 'difficulty', 'token_reward', 'agent_info']

class ChapterSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description', 'order', 'problems']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['user', 'accuracy', 'hallucination_rate', 'token_cost', 'latency', 'status', 'result_detail', 'feedback_message']
