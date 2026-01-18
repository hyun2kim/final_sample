# 🛡️ Engineer RPG: AI 에이전트 마스터 클래스 시스템 가이드

본 문서는 BFCL 및 Ragas-WikiQA 데이터셋을 활용하여 구축된 **AI 에이전트 모의 면접 및 성능 최적화 실습 플랫폼**인 'Engineer RPG'의 시스템 명세서입니다.

---

## 1. 프로젝트 개요
**Engineer RPG**는 AI 엔지니어가 실무에서 마주하는 다양한 에이전트 실패 시나리오를 시뮬레이션하고, 이를 시스템 프롬프트 수정 및 로직 개선을 통해 해결하는 과정을 학습하는 플랫폼입니다.

- **목적**: 툴 호출 정확도 향상, RAG 환각 방지, 보안 가드레일 설계, 대화 맥락 관리 능력 배양.
- **핵심 기술**: Python, Streamlit, AST 기반 평가 로직, Ragas 지표.

---

## 2. 시스템 아키텍처

### 데이터 레이어 (Data Layer)
- **BFCL (Berkeley Function Calling Leaderboard)**: 
    - `simple`: 기본적인 함수 호출 인자 추출 테스트.
    - `multi_turn`: 여러 단계의 대화 Context 유지 테스트.
    - `irrelevance`: 도구와 무관한 질문에 대한 방어력(Guardrail) 테스트.
- **Ragas-WikiQA**: 
    - 위키피디아 기반 검색 문맥과 정답 데이터셋을 활용한 RAG 성능 평가.

### 평가 엔진 (Evaluation Engine - `evaluator.py`)
- **Tool Evaluator**: JSON 구조 분석(AST Matcher)을 통해 함수명, 파라미터 유무, 값의 정확도를 검증합니다.
- **RAG Evaluator**: 답변의 **충실도(Faithfulness)**와 **재현율(Recall)**을 측정하여 할루시네이션 여부를 판별합니다.
- **Guardrail Evaluator**: 부적절한 요청에 대해 도구 실행을 차단했는지 물리적으로 검증합니다.

---

## 3. 주요 기능 (4대 핵심 코스)

### 🔧 탭 1: Tool Calling (도구 호출)
- **미션**: 복잡한 사용자 질문에서 필요한 함수를 식별하고 인자값을 정확히 추출하기.
- **평가**: 정답 데이터와 1:1 매칭하여 성공 여부 판단.

### 📚 탭 2: RAG 최적화 (지식 기반 답변)
- **미션**: 검색된 외부 문맥(Context)만을 사용하여 근거 있는 답변 생성하기.
- **평가**: Ragas 지표를 활용한 신뢰도 점수 산출 및 시각화.

### 🛡️ 탭 3: 가드레일 (보안)
- **미션**: 에이전트가 처리할 수 없는 영역의 질문을 걸러내고 도구 오남용 방지하기.
- **평가**: 무관한 질문 시 툴 호출 시도 여부를 감지하여 차단 성공률 측정.

### 🔄 탭 4: 멀티턴 대화 (상태 관리)
- **미션**: 이전 대화의 흐름을 기억하고 목표 도달을 위해 연속적인 액션 수행하기.
- **평가**: 대화 타임라인 분석 및 각 턴별 예상 동작 검토.

---

## 4. 파일 구조
```text
c:\final\final_subject\
├── app.py                     # 메인 Streamlit 대시보드
├── requirements.txt            # 라이브러리 종속성
├── engineer_rpg_manual.md      # 본 메뉴얼 파일
├── scripts/
│   ├── evaluator.py           # 핵심 평가 로직 엔진
│   ├── preprocess_bfcl.py      # BFCL 데이터 병합 및 전처리 스크립트
│   └── test_evaluator.py       # 평가 엔진 유닛 테스트
└── data/
    ├── merged_bfcl_simple.json # 전처리된 툴 호출 데이터
    ├── merged_bfcl_multi.json  # 멀티턴 대화 데이터
    └── ragas-wikiqa/           # RAG 실습용 데이터셋
```

---

## 5. 실행 및 사용 방법
1. **서버 실행**:
   ```powershell
   streamlit run app.py
   ```
2. **실습 프로세스**:
   - 상단 탭에서 실습하고 싶은 **코스를 선택**합니다.
   - 좌측 영역의 **사용자 질문**과 **도구 명세**를 분석합니다.
   - **시스템 프롬프트**를 수정하여 에이전트의 전략을 변경합니다.
   - **실행 및 평가** 버튼을 눌러 점수와 에러 메시지를 확인하고 개선을 반복합니다.

---
**Advanced Agentic Coding Framework - 2026**
