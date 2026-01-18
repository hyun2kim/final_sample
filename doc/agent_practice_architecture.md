# 🏗️ Agent Practice 시스템 아키텍처 가이드

본 문서는 **Engineer RPG: AI 에이전트 마스터 클래스**의 전체 시스템 구조와 각 레이어의 상세 구현 명세를 다룹니다.

## 📊 시스템 아키텍처 다이어그램 (Mermaid)

```mermaid
graph TB
    subgraph "Client Layer"
        UI[Streamlit Web UI]
        InputArea[Interactive Input]
        Monitor[Real-time Feedback]
    end

    subgraph "API Gateway & Auth"
        Gateway[API Router]
        Auth[Key Management]
        RateLimit[Simulation Policy]
    end

    subgraph "Practice Router"
        TrackerRouter[Mission Router]
        DataRouter[Dynamic Mapping]
        EvalHook[Eval Hooking]
    end

    subgraph "Agent Services Pipeline"
        Submission[Agent Submission]
        PromptEval[Prompt Evaluator]
        RAGCheck[RAG Quality Checker]
        HalluDetect[Hallucination Detector]
    end

    subgraph "Evaluation Engine"
        QuestMgr[Test Case Manager]
        MetricsAgg[Metrics Aggregator]
        FeedbackGen[Objective Feedback]
        Checklist[Checklist Engine]
    end

    subgraph "AI/LLM Layer"
        LLMOrch[LLM Orchestrator]
        QGen[Question Generator]
        Coach[Coach Feedback]
        AltSol[Alternative Solutions]
    end

    subgraph "Content Management"
        ScenarioDB[(Scenario DB)]
        Constraints[(Constraints DB)]
        Templates[(Solution Templates)]
    end

    subgraph "Infrastructure"
        SystemMon[System Monitoring]
        Storage[Storage/S3 Mock]
        Queue[Kafka Queue Mock]
    end

    subgraph "User Progress"
        Progress[Progress Tracker]
        History[(User History)]
        Recommender[Challenge Recommender]
    end

    UI --> Gateway
    Gateway --> Auth
    Auth --> TrackerRouter
    
    TrackerRouter --> ScenarioDB
    TrackerRouter --> Submission
    
    Submission --> PromptEval
    PromptEval --> RAGCheck
    RAGCheck --> HalluDetect
    
    HalluDetect --> MetricsAgg
    MetricsAgg --> QuestMgr
    QuestMgr --> Checklist
    Checklist --> FeedbackGen
    
    FeedbackGen --> Coach
    Coach --> Progress
    Progress --> History
    History --> Recommender
    
    LLMOrch <--> Gateway
    LLMOrch --> QGen
    LLMOrch --> AltSol
    
    Infrastructure -.-> Client Layer
    Infrastructure -.-> Service Layer
```

---

# 🏗️ Agent Practice Architecture: Client Layer (사용자 인터페이스 레이어)

Client Layer는 사용자가 시스템과 직접 상호작용하며 실습을 수행하는 접점입니다. 본 프로젝트에서는 Streamlit 프레임워크를 통해 반응형 웹 환경으로 구현되었습니다.

## 1. Web Dashboard (웹 대시보드)
모든 실습 도구와 모니터링 지표가 통합된 중앙 관리 화면입니다.
*   **코드 구현**: `app.py` 전반 (Sidebar, Tabs, Layout 설정)
*   **역할**: 도구 호출, RAG, 가드레일 등 각 실습 퀘스트와 인프라 상태를 한눈에 파악할 수 있는 대시보드 역할을 합니다.

## 2. Interactive Input Area (대화형 입력 및 에디터)
사용자가 직접 에이전트의 답변이나 도구 호출 JSON을 입력하고 제출하는 영역입니다.
*   **코드 구현**: `st.text_area`, `st.button`
*   **역할**: 사용자의 입력물(Artifacts)을 수집하여 백엔드 평가 엔진으로 전달하며, AI 버튼을 통한 자동 생성(Auto-Submission) 작업의 흐름을 제어합니다.

## 3. Real-time Monitoring & Feedback (실시간 모니터링 및 시각화)
시스템의 자원 상태와 평가 결과를 시각적으로 즉시 반영하여 보여줍니다.
*   **코드 구현**: `st.metric`, `st.progress`, `st.json`, `st.success/error`
*   **역할**: 에이전트 성능 점수, 시스템 리소스(CPU/MEM) 상태, 도구 명세(JSON Schema) 등을 직관적인 UI 요소로 변환하여 사용자에게 전달합니다.

---

# 🏗️ API Gateway & Auth (인터페이스 관문 및 보안)

시스템의 보안과 외부 서비스와의 통신 경로를 제어하는 '검문소' 역할을 수행합니다.

## 1. API Gateway (연동 관문)
에이전트가 외부 LLM(OpenAI, Google)과 통신하기 위한 단일 진입로를 제공합니다.
*   **코드 구현**: `app.py` 사이드바 내 **LLM 제공자** 선택 박스 및 `call_llm` 함수 인터페이스.
*   **역할**: 시뮬레이션 모드와 실제 API 호출 모드를 스위칭하여, 요청을 각 서비스 엔드포인트로 라우팅합니다.

## 2. Auth Service (인증 및 보안 관리)
사용자의 API 키를 안전하게 수집하고 세션 내에서 관리합니다.
*   **코드 구현**: `st.sidebar.text_input(type="password")`
*   **역할**: 민감한 정보인 API Key를 화면에 노출하지 않고 암호화된 입력창으로 처리하며, 유효한 키가 없는 경우 외부 API 호출을 차단하는 보호 로직을 수행합니다.

## 3. Rate Limiting (사용량 및 속도 제한)
시스템 부하 방지 및 API 비용 관리를 위한 제어 계층입니다.
*   **코드 구현**: "시뮬레이션 모드"를 통한 로컬 처리 유도.
*   **역할**: 실제 API 호출 전 단계에서 '시뮬레이션 모드'를 우선 제안함으로써 무분별한 토큰 소모와 비용 발생을 방지하는 정책적 가이드 역할을 수행합니다.

---

# 🏗️ Agent Practice Architecture: Content Management 레이어

Content Management 레이어는 본 프로젝트에서 에이전트 훈련에 필요한 모든 '연습 문제'와 '정답 기준'을 관리하는 핵심 데이터 저장소입니다.

## 1. Scenario DB (실습 시나리오)
사용자가 해결해야 할 구체적인 상황과 질문 데이터를 보관합니다.
*   **관련 파일**: `merged_bfcl_simple_ko.json`, `merged_bfcl_multi_ko.json`, `sample_ko.json`
*   **데이터 내용**: 에이전트가 처리해야 할 사용자들의 현실적인 한국어 요청 사항(Question)들입니다.

## 2. Constraints DB (제약 조건 및 도구 명세)
에이전트가 지켜야 할 엄격한 규칙과 도구 사용법이 담겨 있습니다.
*   **관련 속성**: JSON 내의 `"function"` 객체 (JSON Schema)
*   **데이터 내용**: 도구의 명칭, 파라미터 타입, 필수 입력 항목 등 에이전트가 출력 시 반드시 준수해야 하는 규격입니다.

## 3. Test Cases (검증용 테스트 세트)
에이전트의 약점을 파악하기 위한 특수한 시나리오들입니다.
*   **가드레일 데이터**: 도구와 무관한 질문을 통해 에이전트의 보안/거절 능력을 테스트합니다. (`merged_bfcl_irrelevance_ko.json`)
*   **멀티턴 데이터**: 이전 대화 맥락 유지 능력을 테스트하는 연속 질문 세트입니다.

## 4. Solution Templates (모범 답안 및 채점 기준)
평가 엔진(`evaluator.py`)이 성능을 측정할 때 사용하는 '그라운드 트루스(Ground Truth)'입니다.
*   **관련 속성**: `"ground_truth"`, `"correct_answer"`
*   **데이터 내용**: 도구 호출 시 필요한 정확한 인자값들과 RAG 시스템의 환각 없는 표준 답변 템플릿입니다.

---
💡 **현지화 전략**: 모든 콘텐츠는 한국어권 사용자를 위해 번역 스크립트(`translate_to_ko.py`)를 통해 최적화된 형태로 관리됩니다.

# 🏗️ Agent Practice Architecture: Infrastructure 레이어

Infrastructure 레이어는 현재 소스 코드(`app.py`)에서 시스템 자원을 실시간으로 감시하고 관리하는 하부 지지대 역할을 수행합니다.

## 1. System Monitoring (`psutil` 연동)
서버의 물리적인 자원 상태를 실시간으로 모니터링하여 가시화합니다.
*   **코드 구현**: `app.py` 사이드바 섹션 내 `psutil` 호출
*   **핵심 로직**:
    ```python
    cpu_usage = psutil.cpu_percent() # CPU 실시간 추출
    mem_usage = psutil.virtual_memory().percent # 메모리 점유율 추출
    st.sidebar.progress(cpu_usage / 100) # 시각적 게이지 표시
    ```
*   **목적**: AI 추론 시 발생하는 하드웨어 부하를 실시간으로 추적합니다.

## 2. Storage / S3 Mock (데이터 저장소 관리)
로컬 환경에서 클라우드 스토리지(S3) 환경을 재현하여 문제 파일들의 현황을 관리합니다.
*   **코드 구현**: `app.py` 상단 데이터 경로 설정 및 모니터링 로직
*   **핵심 로직**:
    ```python
    BASE_DATA_DIR = r"c:\final\final_subject\data" # 데이터 입구 정의
    # 파일 탐색 및 용량 합계 계산
    files = [f for f in os.listdir(BASE_DATA_DIR) if f.endswith('.json')]
    total_size = sum(os.path.getsize(os.path.join(BASE_DATA_DIR, f)) for f in files)
    ```
*   **목적**: 수천 개의 훈련 시나리오 데이터의 무결성과 용량을 감시합니다.

## 3. Task Queue / Kafka Mock (비동기 처리 시뮬레이션)
대규모 요청을 처리하는 비동기 대기열의 작동 상태를 사용자에게 투명하게 공개합니다.
*   **코드 구현**: `app.py` 사이드바 내 Status Indicator
*   **핵심 로직**:
    ```python
    st.sidebar.success("● Queue Status: Healthy") # 서비스 건전성 표시
    st.sidebar.caption("Active Workers: 4") # 비동기 워커 상태 시뮬레이션
    ```

## 4. Execution Stack & Optimization
시스템이 안정적으로 돌아가도록 보장하는 기술 스택의 실제 소스 구현 정보입니다.

### 1. Data Access Optimization (`st.cache_data`)
대규모 데이터셋을 매번 디스크에서 읽지 않도록 메모리 캐싱을 적용합니다.
*   **핵심 로직**:
    ```python
    @st.cache_data
    def load_json_data(file_path):
        # 중복 로딩 방지 및 반응 속도 극대화
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    ```

### 2. UI State & Workflow Optimization (`st.session_state`)
페이지 새로고침 시에도 AI 답변 데이터를 유지하여 연속적인 실험을 지원합니다.
*   **핵심 로직**:
    ```python
    # AI 응답 결과를 세션에 저장하여 상태 유지
    st.session_state['res_simple'] = ai_res 
    
    # 지연 시간 동안 사용자 이탈 방지를 위한 시각적 피드백
    with st.spinner("AI가 고민 중..."):
        ai_res = call_llm(...)
    ```

### 3. Inference Determinism (`temperature=0`)
에이전트 성능 평가의 재현성과 일관성을 위해 모델 설정을 최적화합니다.
*   **핵심 로직**:
    ```python
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0 # 동일 질문에 항상 동일한(결정론적) 답변 유도
    )
    ```

### 4. Robust Runtime Engineering (`try-except`)
외부 API 장애 시에도 서비스가 중단되지 않도록 안전 장치를 구축했습니다.
*   **핵심 로직**:
    ```python
    try:
        # API 호출 및 결과 파싱
        return response.choices[0].message.content
    except Exception as e:
        # 장애 시 에러 메시지 표시 및 시스템 가용성 유지
        st.error(f"❌ API 호출 오류: {e}")
        return None
    ```

---
💡 **실전 인사이트**: 이 레이어의 구현을 통해 개발자는 코드의 정확도뿐만 아니라, 실제 서비스 운영 시 발생하는 자원 소모와 스토리지 관리라는 '운영적 관점(Ops)'을 가질 수 있게 됩니다.

# 🏗️ Core Practice Services: Practice Router (실습 라우터)

Practice Router는 아키텍처 상의 **Core Practice Services** 레이어 입구에서 사용자의 요청을 각각의 전문 실습 트랙으로 지능적으로 분기해 주는 **'교통 관제'** 역할을 수행합니다.

## 1. UI 및 미션 라우팅 (Tab-based Routing)
사용자가 공부하고자 하는 미션 타입에 따라 시각적 UI와 실습 환경을 즉시 전환합니다.
*   **코드 구현**: `app.py`의 `st.tabs` 시스템
*   **핵심 로직**:
    ```python
    # 사용자의 클릭에 따라 5개 전문 실습 서비스(Tool, RAG, Security, Multi-turn, Stable)로 라우팅
    tabs = st.tabs(["🔧 Tool Calling", "📚 RAG 최적화", "🛡️ 가드레일(보안)", "🔄 멀티턴 대화", "🧪 안정화 실험실"])
    ```
*   **목적**: 단일 진입점에서 여러 전문 분야의 실습을 단절 없이 경험하게 합니다.

## 2. Dynamic Content Routing (동적 데이터 바인딩)
사용자가 선택한 언어 옵션과 실습 항목에 따라 최적의 데이터 소스 경로를 안내합니다.
*   **코드 구현**: `app.py`의 조건부 데이터 로딩 부
*   **핵심 로직**:
    ```python
    # 언어 설정(KO/EN)에 따라 기반 데이터 저장소(Scenario DB)로 경로 라우팅
    simple_data = load_json_data(BFCL_SIMPLE_KO if lang_key == "ko" else BFCL_SIMPLE_EN)
    rag_data = load_json_data(WIKIQA_KO if lang_key == "ko" else WIKIQA_EN)
    ```
*   **목적**: 사용자의 설정 상태(State)에 따라 정확한 실습 자산을 연결합니다.

## 3. Evaluation Hooking (평가 엔진 연결)
라우팅된 답변 제출물(Artifacts)을 미션 성격에 맞는 전문 평가 로직으로 정확하게 전달합니다.
*   **코드 구현**: 미션 탭별 Button Handler 내 호출 로직
*   **동작**:
    *   Tool Calling 요청 → `evaluator.evaluate_tool_calling`으로 라우팅
    *   RAG 요청 → `evaluator.evaluate_rag`으로 라우팅
    *   Guardrail 요청 → `evaluator.evaluate_guardrail`으로 라우팅

---
💡 **아키텍처적 의미**: Practice Router를 통해 시스템은 **높은 응집도**와 **낮은 결합도**를 유지합니다. 새로운 실습 주제가 추가되어도 Router에 경로만 추가하면 기존 시스템의 안정성을 유지하며 무한히 확장할 수 있는 구조를 제공합니다.

# 🏗️ Core Practice Services: Agent Services Pipeline

에이전트 실습의 핵심 로직이 작동하는 파이프라인으로, 모델의 응답을 수집하고 다각도로 품질을 분석합니다.

## 1. Agent Submission (제출 핸들러)
사용자 또는 모델이 생성한 에이전트의 최종 결과물(Artifacts)을 수집하는 인터페이스입니다.
*   **구현 위치**: `app.py`의 각 미션 탭 내부 (`user_res`, `r_ans`, `i_res` 등)
*   **주요 기능**: 데이터 정규화(JSON 파싱), 입력값 유효성 검사, 평가 엔진으로의 브릿지 역할.

## 2. Prompt Evaluator (프롬프트 평가기)
입력된 명령문과 출력된 인자값 사이의 연관성을 분석하여 프롬프트의 지시 이행력을 평가합니다.
*   **구현 위치**: `evaluator.py > evaluate_tool_calling`
*   **핵심 로직**:
    *   **Argument Integrity**: 호출된 함수의 인자가 도구 명세(Constraints DB)에 정의된 허용 범위 내에 있는지 검사.
    *   **Constraint Matching**: 필수 파라미터 누락 여부 확인.

## 3. RAG Quality Checker (RAG 품질 검사기)
에이전트가 외부 지식(Context)을 얼마나 정확하게 참조하여 답변했는지 정량적으로 측정합니다.
*   **구현 위치**: `evaluator.py > evaluate_rag`
*   **핵심 로직**:
    *   **Recall (재현율)**: 모범 답안의 핵심 키워드가 답변에 얼마나 포함되었는가.
    *   **Similarity Match**: 문장 수준의 유사도 분석을 통한 답변 일치도 확인.

## 4. Hallucination Detector (환각 탐지기)
지식 문맥(Context)에 없는 내용을 지어내거나, 무관한 질문에 도구를 호출하는 '환각' 현상을 탐지합니다.
*   **구현 위치**: `evaluator.py > evaluate_guardrail`, `evaluate_staged_rag`
*   **핵심 로직**:
    *   **Faithfulness (충실도)**: 답변의 모든 내용이 제공된 Context 내에 존재하는지 역추적.
    *   **Guardrail Violation**: 부적절한 상황에서의 도구 호출(Calling in irrelevant scenarios) 여부 감시.

---

---

# 🏗️ Evaluation Engine (평가 엔진 레이어)

모든 실습 트랙의 결과물을 수치화하고 정량적/정성적 판단을 내리는 시스템의 '심판' 역할입니다.

## 1. Test Case Manager (테스트 케이스 관리자)
수천 개의 훈련 시나리오 중 현재 사용자가 선택한 특정 '퀘스트'를 활성화하고 관리합니다.
*   **코드 구현**: `app.py`의 `st.select_slider`, `st.selectbox` 컨트롤 
*   **역할**: 훈련 데이터셋(Scenario DB)에서 인덱스 기반으로 질문, 도구 명세, 정답 데이터를 추출하여 평가 파이프라인에 공급합니다.

## 2. Metrics Aggregator (지표 집계기)
개별 검증 로직에서 산출된 파편화된 점수들을 모아 최종 성적표로 가공합니다.
*   **코드 구현**: `evaluator.py`의 리포트 사전(`dict`) 반환 구조
*   **역할**: Tool Calling 점수, RAG 재현율/충실도 지표를 통합하여 `status`(통과/실패)와 최종 `score`를 결정합니다.

## 3. Objective Feedback (객관적 피드백 생성기)
단순 점수 외에 "왜 실패했는지"에 대한 구체적이고 기술적인 근거를 사용자에게 제시합니다.
*   **코드 구현**: `evaluator.py` 내의 `errors` 리스트 및 `reason` 필드
*   **역할**: "파라미터 누락", "허용되지 않은 값 입력" 등 사용자가 즉각적으로 수정 가능한 행동 가이드를 생성합니다.

## 4. Checklist Engine (규칙 검증 엔진)
에이전트가 반드시 통과해야 하는 '합격 기준'을 코드화된 규칙으로 검사합니다.
*   **코드 구현**: `evaluate_tool_calling` 내의 필수 인자 체크 루프 및 `evaluate_guardrail`의 JSON 포함 여부 검사
*   **역할**: 사전에 정의된 도구 명세(Constraint)를 체크리스트 삼아 하나라도 어긋날 경우 '실패' 판정을 내리는 엄격한 규칙 기반 필터입니다.

---

# 🏗️ AI/LLM Layer (LLM Orchestrator)

에이전트의 지능을 담당하는 핵심 레이어로, 외부 LLM API(OpenAI, Google) 및 시뮬레이션 로직을 조율(Orchestration)합니다.

## 1. Question Generator (질문 생성 및 전처리기)
정적인 시나리오 데이터를 LLM이 이해하기 쉬운 형태의 '프롬프트'로 변환하고, 필요한 경우 동적으로 상황을 구성합니다.
*   **코드 구현**: `app.py`의 `call_llm`에 주입되는 `prompt` 및 `system_prompt` 구성 로직.
*   **역할**: 시나리오 DB의 "질문"과 "함수 명세"를 결합하여 에이전트가 즉시 실행 가능한 형태의 'Task'를 생성합니다.

## 2. Coach Feedback (코치 피드백 엔진)
자동화된 점수(Metric)를 넘어, 사용자의 작업물에 대해 언어적으로 설명하고 개선 방향을 제시하는 주관적 피드백 시스템입니다.
*   **코드 구현**: `evaluator.py > evaluate_staged_rag`의 `feedback` 필드
*   **역할**: "환각이 제거되어 안정성이 향상되었습니다"와 같은 자연어 형태의 피드백을 통해 학습자가 수정의 방향성을 이해하도록 돕습니다.

## 3. Alternative Solutions (모범 답안 및 대안 제시)
사용자가 작성한 답안 외에, 에이전트가 선택할 수 있는 최적의 '다른 길'을 보여주는 기능입니다.
*   **코드 구현**: `app.py`의 **Simulation Mode** 및 **Auto-Submission** 결과물
*   **역할**: AI 버튼 클릭 시 생성되는 "SIMULATED_RESPONSE" 또는 실제 GPT-4o의 결과물을 통해, 사용자가 자신의 답과 비교할 수 있는 레퍼런스(Reference)를 실시간으로 공급합니다.

---

# 🏗️ User Progress (사용자 성장 및 이력 관리)

사용자의 실습 진행 상황을 추적하고, 데이터를 기반으로 개인화된 학습 경험을 제공하는 레이어입니다.

## 1. Progress Tracker (진도 추적기)
현재 사용자가 도전 중인 퀘스트의 완료 여부와 달성 점수를 실시간으로 기록합니다.
*   **코드 구현**: `app.py`의 `st.metric` 및 `st.success/error` 알림 시스템.
*   **역할**: "성공/실패" 상태와 "점수(Score)"를 시각적으로 피드백하여 사용자가 자신의 현재 숙련도를 즉각적으로 파악하게 합니다.

## 2. User Data & History (사용자 이력 저장소)
실습 중 발생한 답변 시도 이력과 AI의 피드백 데이터를 세션 단위로 보관합니다.
*   **코드 구현**: `st.session_state` (세션 상태 관리).
*   **역할**: 페이지가 리프레시되어도 이전의 AI 생성 결과(`res_simple`, `res_rag` 등)를 유지하여, 사용자가 과거의 시도를 바탕으로 답변을 점진적으로 수정(Iterative Refinement)할 수 있는 토대를 제공합니다.

## 3. Next Challenge Recommender (다음 도전 추천기)
사용자의 현재 위치와 난이도를 고려하여 다음에 수행해야 할 최적의 미션을 안내합니다.
*   **코드 구현**: `app.py`의 `tabs` 구성 순서 및 `select_slider/selectbox` 시퀀스.
*   **역할**: Tool Calling(기초) → RAG(심화) → Guardrail(보안) → Multi-turn(복합) 순으로 이어지는 커리큘럼 아키텍처를 통해 학습자가 자연스럽게 실력을 쌓도록 유도합니다.

---

# 🏗️ Extended Workflow: Auto-Submission Manager

아키텍처의 확장 영역으로, 사람의 개입 없이 에이전트 성능을 대량으로 테스트할 수 있는 자동화 엔진입니다.

## 1. LLM Orchestration (추론 조율)
*   사용자의 설정에 따라 다양한 모델(OpenAI, Google)에 최적화된 프롬프트를 주입하고 추론 결과를 수신합니다.
*   `call_llm` 함수를 통해 추론 레이어와 통신합니다.

## 2. Simulation & Benchmarking
*   사전에 정의된 정답셋을 활용하여 가상의 에이전트 환경(Mock)을 구축하고 성능 지표를 즉시 산출합니다.
*   실습 과정에서의 병목 현상을 제거하고 개발 반복 주기(Iterative Loop)를 가속화합니다.

---
💡 **추가 아키텍처 포인트**:
*   **Scalability**: 현재의 파이프라인은 Stateless하게 설계되어 있어, 향후 대규모 벤치마킹을 위한 병렬 처리(Parallel Processing) 레이어로 확장이 용이합니다.
*   **Hybrid Evaluation**: 기계적인 AST 매칭과 LLM을 이용한 정성적 평가가 결합될 수 있는 확장 인터페이스를 갖추고 있습니다.

