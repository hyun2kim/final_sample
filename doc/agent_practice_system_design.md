# Agent Practice System Design (Based on BFCL Dataset)

본 문서는 `Berkeley Function Calling Leaderboard (BFCL)` 데이터셋을 활용하여 구축할 수 있는 **에이전트 실습 시스템(Agent Practice System)**의 설계 방안을 담고 있습니다. 이 데이터셋은 에이전트의 핵심 역량인 프롬프트 엔지니어링, RAG, 툴 사용, 가드레일 설계를 연습하기에 최적화되어 있습니다.

---

## 1. 툴 선택 및 파라미터 추출 디버거 (Tool Calling Debugger)
에이전트가 사용자 질문에 적합한 함수를 선택하고, 필요한 인자(Arguments)를 정확히 추출하는 능력을 테스트합니다.

*   **활용 데이터**: `BFCL_v3_simple.json`, `BFCL_v3_multiple.json`
*   **시스템 기능**: 
    - 사용자의 질문에 대해 LLM이 생성한 함수 호출(JSON) 결과와 `possible_answer`의 정답 시나리오를 실시간 비교.
    - 모델이 잘못된 파라미터를 추출하거나 엉뚱한 함수를 선택했을 때, 프롬프트를 즉석에서 수정하며 실험할 수 있는 Playground 제공.

## 2. 멀티턴 및 부족 정보 보충 연습 (Multi-turn & Slot Filling)
사용자가 모든 정보를 한 번에 주지 않았을 때, 에이전트가 "부족한 정보를 되묻는지" 혹은 "추측해서 실행하는지"를 관리합니다.

*   **활용 데이터**: `BFCL_v3_multi_turn_miss_param.json`, `BFCL_v3_multi_turn_base.json`
*   **시스템 기능**: 
    - 필수 파라미터가 누락된 대화 기록을 모델에게 입력으로 제공.
    - 모델이 함수를 바로 실행하지 않고, 사용자에게 "어떤 추가 정보가 필요한지" 질문하도록 유도하는 프롬프트 최적화 실습.

## 3. RAG 기반 함수 문서 검색 시스템 (Tool RAG Integration)
에이전트가 사용할 수 있는 도구가 수천 개에 달할 때, 필요한 도구의 명세만 동적으로 가져오는 기술을 구현합니다.

*   **활용 데이터**: `multi_turn_func_doc` 폴더 내 API 명세 데이터.
*   **시스템 기능**: 
    - 수많은 함수 문서를 벡터 DB에 적재하고, 질문에 적합한 도구만 검색(Retrieval)하여 프롬프트에 동적 삽입.
    - 검색된 정보가 불충분할 때 에이전트가 어떻게 반응하는지, 검색 정확도가 에이전트 성능에 미치는 영향 분석.

## 4. 가드레일 및 할루시네이션 방어 (Guardrail & Hallucination Prevention)
보유한 도구로 해결할 수 없는 요청에 대해 에이전트가 억지로 답변하지 않도록 방어 체계를 구축합니다.

*   **활용 데이터**: `BFCL_v3_irrelevance.json`, `BFCL_v3_live_irrelevance.json`
*   **시스템 기능**: 
    - 툴과 무관한 질문 유입 시, 모델이 "가능한 도구가 없습니다"라고 정중히 거절하도록 가드레일 설정.
    - 존재하지 않는 도구를 만들어내는 'Tool Hallucination' 현상을 방지하기 위한 시스템 프롬프트 및 검증 로직 개발.

## 5. 복합/병렬 도구 실행기 (Parallel & Multiple Tool Execution)
하나의 질문에 여러 개의 도구를 동시에 혹은 순차적으로 실행해야 하는 복합 요청 처리 능력을 연습합니다.

*   **활용 데이터**: `BFCL_v3_exec_parallel.json`, `BFCL_v3_exec_multiple.json`
*   **시스템 기능**: 
    - 병렬 호출(Parallel Calling)이 필요한 상황을 인지하고 정확한 JSON 리스트를 생성하는지 확인.
    - 첫 번째 도구의 결과값이 두 번째 도구의 입력 파라미터로 들어가는 '도구 간 연쇄(Tool Chaining)' 로직 테스트.

---

## 추천 학습 로드맵
1.  **Level 1**: `Simple` 데이터를 활용하여 단일 함수 호출 성공률 100% 도전.
2.  **Level 2**: `Irrelevance` 질문을 섞어 가드레일 응답(거절) 처리 로직 추가.
3.  **Level 3**: `Multi-turn` 데이터를 통해 부족한 정보를 채워나가는 대화형 에이전트 구현.
4.  **Level 4**: `Tool RAG`를 도입하여 대규모 도구 환경에서 최적의 도구 검색 및 실행 엔진 고도화.
