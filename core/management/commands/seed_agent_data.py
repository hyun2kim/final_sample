# 2026-01-16: Architecture Gym의 모든 5개 챕터 초기 데이터 생성을 위한 시드 커맨드
# [Role: 초기 서비스 운영에 필요한 모든 챕터(Unit 1~5) 및 문제 데이터를 DB에 자동 삽입]
from django.core.management.base import BaseCommand
from core.models import Chapter, Problem, AgentProblem, AgentTestCase

class Command(BaseCommand):
    help = 'Seeds all initial chapters and problems for Architecture Gym'

    def handle(self, *args, **kwargs):
        chapters_data = [
            {
                'name': 'Code Practice',
                'description': '엔지니어링 실무 코딩 테스트 및 알고리즘 훈련',
                'order': 1,
                'problem': {
                    'title': 'API 응답 캐싱 로직 구현',
                    'content': 'Redis를 활용하여 중복 요청에 대한 응답 속도를 개선하세요.',
                    'difficulty': 'Easy',
                    'token_reward': 50
                }
            },
            {
                'name': 'Debug Practice',
                'description': '복잡한 시스템의 숨겨진 버그를 찾아내고 수정하기',
                'order': 2,
                'problem': {
                    'title': '분산 트랜잭션 데이터 유실 찾기',
                    'content': '결제 시스템에서 발생하는 간헐적인 데이터 불일치 버그를 해결하세요.',
                    'difficulty': 'Medium',
                    'token_reward': 120
                }
            },
            {
                'name': 'System Practice',
                'description': '대규모 시스템 아키텍처 설계 및 드로잉 입문',
                'order': 3,
                'problem': {
                    'title': '글로벌 초저지연 채팅 시스템 설계',
                    'content': '웹소켓과 메시지 브로커를 활용한 확장 가능한 채팅 구조를 설계하세요.',
                    'difficulty': 'Hard',
                    'token_reward': 200
                }
            },
            {
                'name': 'Ops Practice',
                'description': '인프라 장애 대응 및 실시간 모니터링 실습',
                'order': 4,
                'problem': {
                    'title': '쿠버네티스 파드 재시작 루프 해결',
                    'content': '잦은 OOM 발생으로 인한 서비스 중단을 방지하기 위한 설정을 최적화하세요.',
                    'difficulty': 'Medium',
                    'token_reward': 150
                }
            },
            {
                'name': 'Agent Practice',
                'description': 'AI 에이전트 최적화 및 환각 제거 훈련',
                'order': 5,
                'problems': [
                    {
                        'title': '사내 보안 문서 RAG 시스템 최적화',
                        'content': '에이전트가 사내 문서에 없는 내용을 지어내고 있습니다. 시스템 프롬프트를 수정하여 환각을 방지하세요.',
                        'difficulty': 'Medium',
                        'token_reward': 100,
                        'agent_info': {
                            'base_system_prompt': '너는 사내 문서 전문가야. 사용자의 질문에 친절하게 답해줘.',
                            'test_cases': [
                                {'input': '복지 포인트는 1년에 얼마야?', 'expected': '200만원입니다.', 'ground': '복지 규전 제 4조: 연간 200만원 지급.'},
                                {'input': '재택근무 규정은?', 'expected': '주 2회 가능합니다.', 'ground': '재택 운영 지침: 주 최대 2회.'},
                            ]
                        }
                    },
                    {
                        'title': '에이전트 도구(Tool) 호출 정밀도 향상',
                        'content': '사용자의 요청에 따라 적절한 API 도구를 호출해야 합니다. 불필요한 도구 호출을 줄이고 정확한 인자를 전달하세요.',
                        'difficulty': 'Hard',
                        'token_reward': 150,
                        'agent_info': {
                            'base_system_prompt': '사용자의 요청에 따라 검색 또는 예약 도구를 사용해.',
                            'test_cases': [
                                {'input': '회의실 예약해줘', 'expected': '예약 도구를 호출합니다.', 'ground': '도구 정의: reserve_room'},
                            ]
                        }
                    }
                ]
            },
            {
                'name': 'Pseudo Practice',
                'description': '유사 코드(Pseudo-Code) 작성 및 알고리즘 사고력 훈련',
                'order': 6,
                'problem': {
                    'title': 'Hello World 반복문 작성하기',
                    'content': 'FOR 반복문을 사용하여 "Hello World"를 정확히 5번 출력하는 의사코드를 작성하세요.',
                    'difficulty': 'Easy',
                    'token_reward': 30
                }
            }
        ]

        for c_data in chapters_data:
            chapter, created = Chapter.objects.get_or_create(
                name=c_data['name'],
                defaults={
                    'description': c_data['description'],
                    'order': c_data['order']
                }
            )
            
            # 기존에는 단일 problem이었으나 리스트로 처리하도록 대응
            problems_to_create = c_data.get('problems') or [c_data.get('problem')]
            
            for p_idx, p_data in enumerate(problems_to_create):
                if not p_data: continue
                problem, p_created = Problem.objects.get_or_create(
                    chapter=chapter,
                    title=p_data['title'],
                    defaults={
                        'content': p_data['content'],
                        'difficulty': p_data['difficulty'],
                        'token_reward': p_data['token_reward']
                    }
                )
                
                # Agent Info (if exists)
                if 'agent_info' in p_data:
                    a_data = p_data['agent_info']
                    agent_info, _ = AgentProblem.objects.get_or_create(
                        problem=problem,
                        defaults={
                            'base_system_prompt': a_data['base_system_prompt'],
                            'base_retrieval_config': {'top_k': 3},
                            'tool_definitions': []
                        }
                    )
                    
                    for tc in a_data.get('test_cases', []):
                        AgentTestCase.objects.get_or_create(
                            agent_problem=agent_info,
                            input_query=tc['input'],
                            defaults={
                                'expected_response': tc['expected'],
                                'ground_truth_context': tc.get('ground')
                            }
                        )

        self.stdout.write(self.style.SUCCESS('Successfully updated units with multiple problems!'))

        self.stdout.write(self.style.SUCCESS('Successfully restored all 6 chapters and initial problems!'))
