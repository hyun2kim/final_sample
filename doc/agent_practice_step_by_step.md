# 2026-01-16: Agent Practice 초기 데이터 및 API 구현 계획

## 1. 초기 데이터 생성 (Initialization)
- **Chapter**: Unit 5 - Agent Practice
- **Problem**: "사내 보안 문서 RAG 시스템 최적화"
- **AgentProblem**: 환각이 발생하는 기본 시스템 프롬프트 및 RAG 설정
- **AgentTestCase**: 3개 이상의 테스트 케이스 (정답 유무 및 근거 확인)

## 2. API 개발 (REST Framework)
- `GET /api/chapters/`: 챕터 및 문제 목록 조회 (이미 기초는 있으나 확장 필요)
- `GET /api/problems/<id>/agent/`: 특정 문제의 에이전트 설정(프롬프트 등) 조회
- `POST /api/submissions/agent/`: 사용자가 수정한 설정 제출 및 채점 수락

## 3. UI 연동 (Vue.js)
- 수직 경로에서 "Agent Practice" 클릭 시 워크스페이스 모달 또는 페이지 열기
- 프롬프트 편집기 및 테스트 결과 대시보드 연동
