import streamlit as st
import json
import os
import requests
import psutil
from datetime import datetime
from scripts.evaluator import AgentEvaluator

# --------------------------------------------------------------------------------
# Constants & File Paths (데이터 경로 설정)
# --------------------------------------------------------------------------------
BASE_DATA_DIR = r"c:\final\final_subject\data"

# 원본(English) 경로
BFCL_SIMPLE_EN = os.path.join(BASE_DATA_DIR, "merged_bfcl_simple.json")
WIKIQA_EN = os.path.join(BASE_DATA_DIR, "ragas-wikiqa", "data", "sample.json")
BFCL_MULTI_EN = os.path.join(BASE_DATA_DIR, "merged_bfcl_multi.json")
BFCL_IRRELEVANCE_EN = os.path.join(BASE_DATA_DIR, "BFCL_v3_irrelevance.json")

# 한국어(Korean) 경로
BFCL_SIMPLE_KO = os.path.join(BASE_DATA_DIR, "merged_bfcl_simple_ko.json")
WIKIQA_KO = os.path.join(BASE_DATA_DIR, "ragas-wikiqa", "data", "sample_ko.json")
BFCL_MULTI_KO = os.path.join(BASE_DATA_DIR, "merged_bfcl_multi_ko.json")
BFCL_IRRELEVANCE_KO = os.path.join(BASE_DATA_DIR, "merged_bfcl_irrelevance_ko.json")

# --------------------------------------------------------------------------------
# Streamlit Page Configuration (페이지 설정)
# --------------------------------------------------------------------------------
st.set_page_config(
    page_title="Engineer RPG: AI 에이전트 마스터 클래스",
    page_icon="🛡️",
    layout="wide"
)

# --------------------------------------------------------------------------------
# Sidebar - Infrastructure Monitor (인프라 모니터링 레이어)
# --------------------------------------------------------------------------------
st.sidebar.title("🏗️ Infrastructure Layer")
st.sidebar.markdown("---")

# 1. 시스템 리소스 (Monitoring 레이어 재현)
st.sidebar.subheader("📊 System Monitoring")
cpu_usage = psutil.cpu_percent()
mem_usage = psutil.virtual_memory().percent
st.sidebar.text(f"CPU Usage: {cpu_usage}%")
st.sidebar.progress(cpu_usage / 100)
st.sidebar.text(f"Memory Usage: {mem_usage}%")
st.sidebar.progress(mem_usage / 100)

# 2. 스토리지 현황 (S3/Disk 레이어 재현)
st.sidebar.subheader("💾 Storage (S3 Mock)")
files = [f for f in os.listdir(BASE_DATA_DIR) if f.endswith('.json')]
total_size = sum(os.path.getsize(os.path.join(BASE_DATA_DIR, f)) for f in files)
st.sidebar.caption(f"총 {len(files)}개의 데이터셋 로드됨")
st.sidebar.caption(f"전체 크기: {total_size / 1024:.1f} KB")

# 3. 비동기 큐 (Kafka Mock)
st.sidebar.subheader("📨 Task Queue (Kafka)")
st.sidebar.success("● Queue Status: Healthy")
st.sidebar.caption("Active Workers: 4")

st.sidebar.markdown("---")
# --------------------------------------------------------------------------------
# Sidebar - Global Settings (전역 설정 창)
# --------------------------------------------------------------------------------
st.sidebar.title("⚙️ 시스템 설정")
language = st.sidebar.radio("🌐 언어 선택 (Language)", ["한국어 (KO)", "English (EN)"])
lang_key = "ko" if language == "한국어 (KO)" else "en"

st.sidebar.markdown("---")
st.sidebar.subheader("🔌 API 연동 (Beta)")
api_type = st.sidebar.selectbox("LLM 제공자", ["시뮬레이션 모드", "OpenAI (GPT-4o)", "Google (Gemini 1.5 Pro)"])
api_key = st.sidebar.text_input("API Key 입력", type="password")

# --------------------------------------------------------------------------------
# Data Loading Functions (데이터 로딩 및 캐싱)
# --------------------------------------------------------------------------------
@st.cache_data
def load_json_data(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def load_irrelevance_data(file_path):
    if not os.path.exists(file_path): return []
    # Ko 버전은 이미 JSON Array로 저장됨 (scripts/translate_to_ko.py 결과)
    if "_ko.json" in file_path:
        return load_json_data(file_path)
    
    # 원본 En 버전은 JSONL 형식임
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try: data.append(json.loads(line))
                except: pass
    return data

# 현재 선택된 언어에 맞춰 데이터 로드
# --------------------------------------------------------------------------------
# LLM API Interaction (Auto-Submission 레이어)
# --------------------------------------------------------------------------------
def call_llm(prompt, system_prompt="당신은 유능한 AI 에이전트입니다."):
    """실제 LLM API를 호출하여 답변을 생성합니다 (Auto-Submission)."""
    if api_type == "시뮬레이션 모드":
        st.info("💡 시뮬레이션 모드: 정답 데이터를 기반으로 가상의 응답을 생성합니다.")
        return "SIMULATED_RESPONSE"
    
    if not api_key:
        st.warning("⚠️ 사이드바에서 API Key를 입력해야 자동 제출이 가능합니다.")
        return None
        
    try:
        if "OpenAI" in api_type:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            return response.choices[0].message.content
        elif "Google" in api_type:
            return "Gemini API 연동 준비 중..."
    except Exception as e:
        st.error(f"❌ API 호출 오류: {e}")
        return None

# 현재 선택된 언어에 맞춰 데이터 로드
simple_data = load_json_data(BFCL_SIMPLE_KO if lang_key == "ko" else BFCL_SIMPLE_EN)
rag_data = load_json_data(WIKIQA_KO if lang_key == "ko" else WIKIQA_EN)
multi_data = load_json_data(BFCL_MULTI_KO if lang_key == "ko" else BFCL_MULTI_EN)
irr_data = load_irrelevance_data(BFCL_IRRELEVANCE_KO if lang_key == "ko" else BFCL_IRRELEVANCE_EN)

evaluator = AgentEvaluator()

# --------------------------------------------------------------------------------
# Main UI - Header
# --------------------------------------------------------------------------------
st.title("🛡️ Engineer RPG: AI 에이전트 마스터 클래스")
st.markdown("""
최고의 AI 엔지니어가 되기 위한 실전 코스에 오신 것을 환영합니다. 
각 단계의 퀘스트를 해결하며 에이전트의 **정확도, 신뢰성, 안전성**을 완성해 보세요.
""")
# 메인 기능 탭 구성
tabs = st.tabs(["🔧 Tool Calling", "📚 RAG 최적화", "🛡️ 가드레일(보안)", "🔄 멀티턴 대화", "🧪 안정화 실험실"])

# --------------------------------------------------------------------------------
# Tab 1: Tool Calling
# --------------------------------------------------------------------------------
with tabs[0]:
    st.subheader("미션: 함수 호출 인자값 최적화")
    if not simple_data:
        st.warning("Tool Calling 데이터를 로드할 수 없습니다.")
    else:
        q_idx = st.select_slider("퀘스트 번호", options=range(len(simple_data)), key="simple_slider")
        quest = simple_data[q_idx]
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"**사용자 요청:** {quest['question'][0][0]['content']}")
            with st.expander("🛠️ 도구 명세(JSON Schema)"):
                st.json(quest['function'])
        with c2:
            st.write("**모델 출력 및 평가**")
            
            # Auto-Submission 기능
            if st.button("🤖 AI에게 대신 물어보기 (Auto-Submission)", key="ai_btn_simple"):
                with st.spinner("AI가 고민 중..."):
                    sys_p = f"당신은 주어진 도구 명세 {quest['function']}를 바탕으로 사용자의 요청에 알맞은 JSON 함수 호출문을 생성하는 에이전트입니다. 반드시 JSON 형식으로만 답하세요."
                    ai_res = call_llm(quest['question'][0][0]['content'], sys_p)
                    if ai_res:
                        # 시뮬레이션 모드면 정답을 살짝 보여줌
                        if ai_res == "SIMULATED_RESPONSE":
                            ai_res = json.dumps(quest['ground_truth'][0])
                        st.session_state['res_simple'] = ai_res

            user_res = st.text_area("결과 JSON", value=st.session_state.get('res_simple', ""), height=150, key="res_simple_input")
            
            if st.button("🚀 성능 평가 실행", key="btn_simple"):
                report = evaluator.evaluate_tool_calling(user_res, quest['ground_truth'])
                if report['status'] == "통과": 
                    st.success(f"성공! 점수: {report['score']}%")
                else: 
                    err_msg = ", ".join(report.get('errors', [report.get('reason', '알 수 없는 오류')]))
                    st.error(f"실패 (점수: {report['score']}%): {err_msg}")

# --------------------------------------------------------------------------------
# Tab 2: RAG 최적화
# --------------------------------------------------------------------------------
with tabs[1]:
    st.subheader("미션: RAG 시스템의 환각(Hallucination) 방제")
    if not rag_data:
        st.warning("RAG 데이터를 로드할 수 없습니다.")
    else:
        r_idx = st.selectbox("실습 케이스 선택", options=range(len(rag_data)), format_func=lambda x: f"Case {x}: {rag_data[x]['question'][:40]}")
        r_quest = rag_data[r_idx]
        c1, c2 = st.columns(2)
        with c1:
            st.warning(f"**검색된 지식(Context):**\n\n{r_quest['context']}")
            st.info(f"**질문:** {r_quest['question']}")
        with c2:
            st.write("**에이전트 답변 및 평가**")
            
            # Auto-Submission 기능
            if st.button("🤖 AI에게 대신 물어보기 (Auto-Submission)", key="ai_btn_rag"):
                with st.spinner("AI가 문맥을 읽는 중..."):
                    sys_p = f"당신은 주어진 지식(Context)을 바탕으로 사용자의 질문에 답하는 RAG 에이전트입니다. 문맥에 없는 내용은 절대 지어내지 마세요."
                    prompt = f"Context: {r_quest['context']}\n\nQuestion: {r_quest['question']}"
                    ai_res = call_llm(prompt, sys_p)
                    if ai_res:
                        if ai_res == "SIMULATED_RESPONSE":
                            ai_res = r_quest['correct_answer']
                        st.session_state['res_rag'] = ai_res

            r_ans = st.text_area("에이전트 답변", value=st.session_state.get('res_rag', ""), height=150, key="res_rag_input")
            
            if st.button("⚖️ RAG 평가 지표 측정", key="btn_rag"):
                report = evaluator.evaluate_rag(r_ans, r_quest['correct_answer'], r_quest['context'])
                st.metric("종합 신뢰도 점수", f"{report['score']}%")

# --------------------------------------------------------------------------------
# Tab 3: 가드레일 (무관 질문 탐지)
# --------------------------------------------------------------------------------
with tabs[2]:
    st.subheader("미션: 에이전트 가드레일 구축")
    if not irr_data:
        st.warning("가드레일 데이터를 로드할 수 없습니다.")
    else:
        i_idx = st.select_slider("가드레일 시나리오", options=range(len(irr_data)), key="irr_slider")
        i_quest = irr_data[i_idx]
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"**무관한 사용자 질문:** {i_quest['question'][0][0]['content']}")
            st.warning(f"**제공된 도구 (이 질문과 무관함):** {i_quest['function'][0]['name']}")
        with c2:
            st.write("**모델 응답 및 검증**")

            # Auto-Submission 기능
            if st.button("🤖 AI에게 대신 물어보기 (Auto-Submission)", key="ai_btn_irr"):
                with st.spinner("AI가 보안 검사 중..."):
                    sys_p = f"당신은 보안 에이전트입니다. 주어진 도구 {i_quest['function']}로 해결할 수 없는 요청은 거절해야 합니다. 절대 도구를 호출하지 마세요."
                    ai_res = call_llm(i_quest['question'][0][0]['content'], sys_p)
                    if ai_res:
                        if ai_res == "SIMULATED_RESPONSE":
                            ai_res = "죄송합니다. 요청하신 기능은 제공되지 않습니다."
                        st.session_state['res_irr'] = ai_res

            i_res = st.text_area("모델 응답 (도구를 호출하면 실패)", value=st.session_state.get('res_irr', ""), height=150, key="res_irr_input")
            
            if st.button("🚔 가드레일 검증", key="btn_irr"):
                report = evaluator.evaluate_guardrail(i_res, is_irrelevance=True)
                if report['status'] == "통과": st.success(report['reason'])
                else: st.error(report['reason'])

# --------------------------------------------------------------------------------
# Tab 4: 멀티턴 (대화 문맥 유지)
# --------------------------------------------------------------------------------
with tabs[3]:
    st.subheader("미션: 멀티턴 대화 시나리오 해결")
    if not multi_data:
        st.warning("멀티턴 실전 데이터를 로드할 수 없습니다.")
    else:
        m_idx = st.selectbox("멀티턴 프로젝트 선택", options=range(len(multi_data)))
        m_quest = multi_data[m_idx]
        turn_num = st.radio("현재 대화 턴(Turn) 선택", options=range(len(m_quest['question'])), horizontal=True)
        st.info(f"**현재 턴 질문:** {m_quest['question'][turn_num][0]['content']}")
        st.write(f"**이 턴의 정답 가이드:** {m_quest['ground_truth'][turn_num]}")

# --------------------------------------------------------------------------------
# Tab 5: 안정화 실험실 (Self-Correction)
# --------------------------------------------------------------------------------
with tabs[4]:
    st.subheader("🕵️ 에이전트 안정화 실험실 (Hallucination Stabilization)")
    st.write("초안의 환각을 잡고 최종 답변을 안정화하는 '자기 수정' 루프를 실습합니다.")
    
    # RAG 데이터 공유 사용
    if not rag_data:
        st.warning("비교 대상 데이터가 없습니다.")
    else:
        s_idx = st.selectbox("안정화 테스트 케이스", options=range(len(rag_data)), key="s_idx")
        s_quest = rag_data[s_idx]
        
        st.warning(f"**제공된 근거(Context):**\n\n{s_quest['context']}")
        
        sc1, sc2 = st.columns(2)
        with sc1:
            st.info("1단계: 초안 작성 (환각 포함 가능성)")
            draft_ans = st.text_area("초안 답변 (Draft Answer)", 
                                     value="이것은 초안입니다. 문맥에 없는 내용이 포함될 수 있습니다.", 
                                     height=150, key="draft_ans")
        
        with sc2:
            st.success("2단계: 최종본 작성 (안정화 완료)")
            final_ans = st.text_area("최종 답변 (Stabilized Answer)", 
                                     value=s_quest['correct_answer'], 
                                     height=150, key="final_ans")
            
        if st.button("⚖️ 안정화 성능 비교", key="btn_stable"):
            report = evaluator.evaluate_staged_rag(draft_ans, final_ans, s_quest['context'])
            
            c_m1, c_m2, c_m3 = st.columns(3)
            c_m1.metric("초안 점수", f"{report['draft_score']}%")
            c_m2.metric("최종 점수", f"{report['final_score']}%")
            c_m3.metric("향상도", f"+{report['improvement']}%")
            
            if report['improvement'] > 0:
                st.success(f"🎉 {report['feedback']}")
            else:
                st.warning(f"⚠️ {report['feedback']}")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Engineer RPG Framework.")
