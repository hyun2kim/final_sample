# 에이전트 실습: Simple 데이터-정답 매핑 대시보드 구축 가이드

이 가이드는 `Berkeley Function Calling Leaderboard (BFCL)` 데이터셋을 활용하여 에이전트의 성능을 시각적으로 확인하고 디버깅할 수 있는 마스터 대시보드 구축 방법을 설명합니다.

## 1. 개요 및 목적
에이전트 개발에서 가장 빈번하게 발생하는 문제는 모델이 도구(Function)를 잘못 선택하거나, 인자(Arguments)를 엉뚱한 타입으로 추출하는 것입니다. 이 대시보드는 질문과 정답을 나란히 배치하여 프롬프트 엔지니어링의 효과를 즉각적으로 체감할 수 있도록 돕습니다.

---

## 2. 데이터 매핑 전략

대시보드 구축의 핵심은 서로 다른 위치에 있는 두 데이터를 `id` 필드를 기반으로 병합하는 것입니다.

| 데이터 유형 | 파일 경로 (예시) | 주요 정보 |
| :--- | :--- | :--- |
| **입력 데이터** | `data/BFCL_v3_simple.json` | `id`, `question`, `function` (명세) |
| **정답 데이터** | `data/possible_answer/BFCL_v3_simple.json` | `id`, 예상되는 함수 호출 결과 (JSON) |

### 매핑 예시 (ID: simple_0)
- **질문**: "밑변 10, 높이 5인 삼각형의 넓이를 구해줘."
- **제공된 도구**: `calculate_triangle_area(base, height)`
- **정답 매핑**: `{"name": "calculate_triangle_area", "arguments": {"base": 10, "height": 5}}`

---

## 3. 대시보드 UI 설계 (UI/UX Design)

### (1) 데이터 탐색 영역
- **Dataset Selector**: `Simple`, `Multiple`, `Parallel` 등 파일 종류 선택.
- **Index Navigator**: 특정 케이스 번호(0~400)를 선택할 수 있는 슬라이더 또는 입력창.

### (2) 지식 창고 (Knowledge Base)
- **Function/Tool View**: 모델이 참조할 수 있도록 전송되는 실제 JSON Schema 형태의 도구 설명.
- **User Prompt View**: 모델에게 전달된 순수 질문 메시지.

### (3) 비교 및 검증 (Evaluation Panel)
- **Golden Answer (정답)**: 데이터셋에 정의된 정답 호출 방식.
- **Model Output (추출값)**: 사용자가 설정한 프롬프트를 통해 LLM이 실제 생성한 값.
- **Status Indicator**: 정답과 모델 출력의 키/값이 일치하는지 자동 검사 (Match/Mismatch 표시).

### (4) 프롬프트 튜닝 영역
- **System Message Editor**: "너는 도구 사용 전문가야..."와 같은 페르소나 설정을 실시간 수정하고 즉시 테스트 버튼을 눌러볼 수 있는 창.

---

## 4. 기술 스택 추천
- **Backend API**: Python (데이터 로딩 및 정합성 체크)
- **Frontend Dashboard**: 
    - **Streamlit**: 파이썬만으로 빠르게 인터랙티브 대시보드 제작 가능 (강력 추천).
    - **Gradio**: 머신러닝 모델 테스트에 특화된 인터페이스.
- **LLM SDK**: OpenAI, Anthropic 또는 LangChain을 연결하여 실제 추론 연동.

---

## 5. 단계별 구현 절차
1. **JSON 전처리**: `data/`와 `possible_answer/` 경로의 파일들을 읽어 ID별로 병합된 `database.json` 파일 생성.
2. **UI 레이아웃 구성**: Streamlit을 사용하여 2단 칼럼 레이아웃 제작.
3. **LLM 연동**: 프롬프트 수정 후 'Run' 버튼 클릭 시 선택된 도구 명세와 질문을 모델에게 전송.
4. **결과 시각화**: 모델의 JSON 결과를 정답과 비교하여 Diff 형식으로 표시.

이 대시보드가 완성되면, 특정 문제가 왜 실패하는지(예: 단위 변환 오류, 필수 인자 누락 등)를 명확히 파악하고 프롬프트를 정교하게 다듬을 수 있습니다.
