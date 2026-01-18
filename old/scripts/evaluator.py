import json
from typing import Any, Dict, List, Optional, Tuple

class AgentEvaluator:
    """
    에이전트의 성능을 다양한 지표로 측정하는 평가 엔진 클래스입니다.
    Tool Calling, RAG, 가드레일 성능 등을 평가합니다.
    """
    def __init__(self):
        pass

    def evaluate_tool_calling(self, model_output: Any, ground_truth: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        [Tool Calling 평가]
        모델이 생성한 JSON 출력을 정답 데이터(ground_truth)와 비교하여 정확도를 측정합니다.
        
        - model_output: 모델이 생성한 툴 호출 결과 (JSON 리스트 또는 딕셔너리)
        - ground_truth: BFCL 데이터셋에 정의된 정답 리스트
        """
        # 1. 모델 출력 정규화 (문자열인 경우 JSON 파싱, 단일 객체인 경우 리스트로 변환)
        if isinstance(model_output, str):
            try:
                model_output = json.loads(model_output)
            except json.JSONDecodeError:
                return {"status": "실패", "reason": "유효하지 않은 JSON 형식입니다.", "score": 0, "errors": ["유효하지 않은 JSON 형식입니다."]}
        
        if isinstance(model_output, dict):
            # OpenAI/Anthropic 포맷 대응: {"name": "...", "arguments": {...}} -> [{"함수명": {인자}}]
            if "name" in model_output and "arguments" in model_output:
                model_output = [{model_output["name"]: model_output["arguments"]}]
            else:
                model_output = [model_output]
        
        if not isinstance(model_output, list):
             return {"status": "실패", "reason": "모델 출력은 함수 호출 리스트 형태여야 합니다.", "score": 0, "errors": ["모델 출력은 함수 호출 리스트 형태여야 합니다."]}

        # 2. 평가 로직 진행
        errors = []
        total_possible = len(ground_truth)
        matches = 0

        # 정답셋의 각 함수 호출과 모델의 출력을 하나씩 대조
        for gt_call_dict in ground_truth:
            gt_func_name = list(gt_call_dict.keys())[0]
            gt_params = gt_call_dict[gt_func_name]
            
            found_match = False
            for model_call in model_output:
                m_func_name = ""
                m_args = {}
                
                # 모델 답변 포맷 확인 및 추출
                if isinstance(model_call, dict):
                    if "name" in model_call and "arguments" in model_call:
                        m_func_name = model_call["name"]
                        m_args = model_call["arguments"]
                    else:
                        m_func_name = list(model_call.keys())[0]
                        m_args = model_call[m_func_name]
                
                # 함수 이름이 일치하는 경우 인자(Arguments) 검증 시작
                if m_func_name == gt_func_name:
                    arg_errors = []
                    
                    # 1) 필수 파라미터 유무 및 값의 정확도 체크
                    for p_name, p_allowed_values in gt_params.items():
                        if p_name not in m_args:
                            # BFCL 특성상 빈 문자열([""])이 허용값에 있으면 선택적 인자로 간주
                            if "" in p_allowed_values:
                                continue
                            else:
                                arg_errors.append(f"필수 파라미터 누락: {p_name}")
                                continue
                        
                        m_val = m_args[p_name]
                        # 허용된 값 리스트 중 하나와 일치하는지 확인 (Fuzzy Match)
                        if m_val not in p_allowed_values:
                            if m_val == "" and "" in p_allowed_values:
                                continue
                            arg_errors.append(f"'{p_name}' 값이 잘못되었습니다. 예상값 중 하나: {p_allowed_values}, 입력값: {m_val}")
                    
                    # 2) 정의되지 않은 파라미터 추출 여부 체크 (할루시네이션 방지)
                    for m_p_name in m_args.keys():
                        if m_p_name not in gt_params:
                            arg_errors.append(f"정의되지 않은 파라미터 추출 (할루시네이션): {m_p_name}")

                    # 에러가 없으면 해당 함수 호출은 성공으로 간주
                    if not arg_errors:
                        found_match = True
                        matches += 1
                        break
                    else:
                        errors.extend(arg_errors)
            
            if not found_match:
                errors.append(f"모델이 '{gt_func_name}' 함수를 올바르게 호출하지 못했습니다.")

        # 최종 점수 계산 (모든 필수 호출을 성공했는지 확인)
        score = matches / total_possible if total_possible > 0 else 0
        status = "통과" if score == 1.0 else "실패"
        
        return {
            "status": status,
            "score": score * 100,
            "errors": errors if status == "실패" else []
        }

    def evaluate_rag(self, model_answer: str, correct_answer: str, context: str) -> Dict[str, Any]:
        """
        [RAG 성능 지표 측정]
        답변의 충실도(Faithfulness)와 재현율(Recall)을 계산합니다.
        
        - model_answer: 에이전트가 생성한 답변
        - correct_answer: 데이터셋의 모범 답안
        - context: 검색을 통해 제공된 배경 지식
        """
        m_ans = model_answer.lower().strip()
        c_ans = correct_answer.lower().strip()
        
        # 1. 완전 일치 여부 (Strict Match)
        exact_match = (m_ans == c_ans)
        
        # 2. 충실도 (Faithfulness): 답변의 내용이 제공된 컨텍스트 내에 존재하는지 체크
        # (간단한 포함 여부로 구현, 실제 고도화 시 LLM 판단 권장)
        is_faithful = m_ans in context.lower() or len(set(m_ans.split()) & set(context.lower().split())) / len(set(m_ans.split())) > 0.5
        
        # 3. 재현율 (Recall): 정답에 있는 핵심 단어가 답변에 얼마나 포함되었는지
        m_words = set(m_ans.split())
        c_words = set(c_ans.split())
        overlap = len(m_words.intersection(c_words))
        recall = overlap / len(c_words) if len(c_words) > 0 else 0
        
        # 종합 점수 가중치 적용
        score = (recall * 0.7 + (1.0 if is_faithful else 0.0) * 0.3) * 100
        
        return {
            "status": "통과" if score > 60 else "실패",
            "score": round(score, 2),
            "metrics": {
                "exact_match": exact_match,
                "faithfulness": is_faithful,
                "recall": round(recall, 2)
            }
        }

    def evaluate_guardrail(self, model_response: str, is_irrelevance: bool) -> Dict[str, Any]:
        """
        [가드레일 성능 평가]
        무관한 질문에 대해 모델이 도구를 호출하지 않고 적절히 거절했는지 판별합니다.
        
        - model_response: 모델의 원문 답변
        - is_irrelevance: 해당 질문이 툴과 무관한 질문인지 여부
        """
        # 결과에 JSON(툴 호출)이 포함되어 있는지 확인
        has_json = "{" in model_response and "}" in model_response
        
        if is_irrelevance:
            # 툴과 무관한 질문인데 툴을 호출하려고 했다면 실패
            if has_json:
                return {"status": "실패", "score": 0, "reason": "무관한 질문임에도 도구를 호출하려고 시도했습니다. (Hallucination)"}
            else:
                return {"status": "통과", "score": 100, "reason": "부적절한 요청을 적절히 거부했습니다."}
        else:
            # 툴을 써야 하는 질문인데 일반 답변만 했다면 실패
            if not has_json:
                return {"status": "실패", "score": 0, "reason": "도구를 사용해야 하는 질문임에도 일반 답변만 수행했습니다."}
            else:
                return {"status": "통과", "score": 100, "reason": "올바르게 도구 사용을 시도했습니다."}

    def evaluate_staged_rag(self, draft_answer: str, final_answer: str, context: str) -> Dict[str, Any]:
        """
        [상태별 RAG 안정화 평가]
        초안(Draft)과 최종본(Final)의 환각 여부를 비교하여 안정화 효율을 측정합니다.
        """
        # 초안 평가 (정답은 모르므로 빈 문자열 전달)
        draft_report = self.evaluate_rag(draft_answer, "", context)
        # 최종본 평가
        final_report = self.evaluate_rag(final_answer, "", context)
        
        improvement = final_report['score'] - draft_report['score']
        
        return {
            "draft_score": draft_report['score'],
            "final_score": final_report['score'],
            "improvement": round(improvement, 2),
            "status": "성공" if final_report['score'] > 80 else "보완 필요",
            "feedback": "최종 답변에서 환각이 제거되어 안정성이 향상되었습니다." if improvement > 0 else "안정화 과정에서 개선이 필요합니다."
        }
