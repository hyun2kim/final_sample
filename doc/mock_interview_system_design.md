ㅋ# Engineer RPG: AI Agent 모의 면접 시스템 설계서

본 문서는 `Berkeley Function Calling Leaderboard (BFCL)`와 `Ragas-WikiQA` 데이터셋을 활용하여 구축하는 **"AI 엔지니어 실전 모의 면접 플랫폼"**의 아키텍처 및 상세 구축 계획을 담고 있습니다.

---

## 1. 시스템 컨셉: "Engineer RPG"
단순한 질의응답 면접을 넘어, 실제 망가진 에이전트 시스템을 엔지니어링 관점에서 복구하고 최적화하는 과정을 평가합니다.

- **주요 미션**: 프롬프트 수정, RAG 파이프라인 최적화, 툴 스키마 교정, 가드레일 설정.
- **게임화 요소**: 미션 완료 시 정확도(Accuracy), 신뢰도(Faithfulness), 비용 최적화 점수를 합산하여 레벨업.

---

## 2. 시스템 아키텍처 (Architecture)

### (1) 전체 구조
- **Frontend**: Dashboard 및 Code Editor (사용자가 프롬프트/설정 수정)
- **Backend (Interview Engine)**:
    - **Quest Controller**: 미션 시나리오 및 망가진 에이전트 상태 주입.
    - **Agent Runner**: 사용자가 수정한 프롬프트로 에이전트 실행.
    - **Evaluator**: 정답 데이터와 비교하여 수치적 지표 생성.
- **Storage**:
    - **Vector DB**: WikiQA 데이터를 임베딩하여 저장.
    - **Metadata Store**: BFCL 기반 툴 명세 및 정답 매핑 데이터.

### (2) 평가 지표 (Core Metrics)
- **Tool Selection Accuracy**: 정답 함수 호출 여부 (AST 기반 비교).
- **RAG Faithfulness**: 답변이 주어진 문서 근거 내에서 작성되었는지 (Ragas 활용).
- **Hallucination Rate**: 가드레일 질문에 대해 적절히 거절했는지 여부.
- **Efficiency**: 답변 생성까지의 토큰 비용 및 지연 시간.

---

## 3. 상세 컴포넌트 설명

### ① Quest Controller
- `etc.md`의 시나리오를 바탕으로 의도적으로 결함이 있는 프롬프트나 잘못된 툴 명세를 주입합니다.
- 예: "필수 인자를 누락하도록 유도된 프롬프트 제공".

### ② Agent Runner & Evaluator
- 사용자가 수정한 코드를 바탕으로 에이전트를 가동합니다.
- 추출된 JSON을 `possible_answer`와 비교하여 상세 피드백("base 인자 타입 오류")을 제공합니다.

### ③ Data & Knowledge Layer
- **BFCL**: 툴 호출의 골든 데이터셋으로 활용.
- **WikiQA**: RAG 성능 평가를 위한 지식 소스로 활용.

---

## 4. 단계별 구축 계획 (Roadmap)

### Step 1: 데이터 전처리 및 인프라 구축 (현재 진행 단계)
- BFCL 데이터(질문+툴 명세)와 정답 데이터를 ID 기반으로 매핑하여 `database.json` 생성.
- WikiQA 데이터를 읽어 Vector DB 초기화 환경 구축.

### Step 2: 실시간 평가 엔진 (Evaluator) 개발
- 정답 JSON과 모델 출력을 비교하는 로직(순서 무관, 타입 체크) 구현.
- Ragas 라이브러리 연동을 통한 RAG 지표 측정 모듈 개발.

### Step 3: 대시보드 및 Playground UI 개발
- Streamlit 기반의 인터랙티브 대시보드 구현.
- 사용자가 프롬프트를 수정하고 결과를 즉시 확인하는 '반복 훈련' 환경 구축.

### Step 4: 시나리오(Quest) 확장 및 게임화
- `etc.md` 기반의 5가지 핵심 퀘스트 시나리오 코드화.
- 총점 및 랭킹 시스템 연동.

---

## 5. 기대 효과
- **실무 역량 증명**: 프롬프트 하나로 해결되지 않는 시스템적 문제 해결 능력 배양.
- **정량적 평가**: 면접자에게 주관적인 평가가 아닌 데이터 기반의 피드백 제공.
