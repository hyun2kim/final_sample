# 에이전트 답변 정합성 판단 기준 (Evaluation Criteria)

BFCL(Berkeley Function Calling Leaderboard) 데이터셋을 활용하여 에이전트의 답변이 정답인지 오답인지 판단하는 핵심 기술적 기준을 설명합니다.

---

## 1. 함수 이름 매칭 (Function Name Match)
모델이 선택한 함수(API)의 이름이 정답(`ground_truth`)에 명시된 이름과 한 글자도 틀림없이 일치해야 합니다.
*   **판단 로직**: `model_output["name"] == ground_truth["function_name"]`
*   **설명**: 여러 개의 도구 중 문제 해결에 적합한 도구를 정확히 '선택'했는지를 평가합니다.

## 2. 파라미터 및 인자 일치 (Argument Match)
추출된 인자(Arguments)의 키(Key)와 값(Value)이 정답과 일치해야 합니다.

### (1) 필수 인자 포함 여부
*   함수 명세에서 정의한 `required` 파라미터가 모델 출력에 모두 포함되어야 합니다.

### (2) 값의 유효성 (Fuzzy/List Match)
*   정답 데이터의 Value가 리스트 형태(예: `["units", ""]`)인 경우, 모델의 답변이 그 리스트 안에 포함된 값 중 하나라면 정답으로 인정합니다.
*   이는 모델이 특정 단위를 명시하거나 생략하는 두 가지 케이스를 모두 허용하기 위함입니다.
*   **판단 로직**: `model_output["arguments"]["unit"] in ground_truth["arguments"]["unit"]`

### (3) 데이터 타입 검증
*   숫자(`10`)를 문자열(`"10"`)로 추출하는 등 타입이 명세와 다르면 오답으로 처리될 수 있습니다. (정적 타입 체크가 중요한 에이전트 실습에서는 엄격하게 적용 권장)

## 3. 구조적 정합성 (Structural/AST Match)
단순한 텍스트 비교가 아닌, JSON 객체의 구조를 기반으로 비교합니다.
*   **순서 무관**: JSON 객체 내에서 인자의 선언 순서가 달라도 값만 정확하면 정답입니다.
*   **할루시네이션(Hallucination) 체크**: 정답 리스트에 없는 불필요한 파라미터를 임의로 생성하여 추가했다면 감점 또는 오답 대상입니다.

---

## 4. 정답 데이터 해석 예시

**대상 데이터 (`BFCL_v3_simple.json` - ID: `simple_0`)**:
```json
{
  "id": "simple_0", 
  "ground_truth": [
    {
      "calculate_triangle_area": {
        "base": [10], 
        "height": [5], 
        "unit": ["units", ""]
      }
    }
  ]
}
```

*   **함수명 필터**: 반드시 `calculate_triangle_area`여야 합니다.
*   **값 필터**:
    - `base`는 무조건 `10`
    - `height`는 무조건 `5`
    - `unit`은 `"units"`로 입력하거나, 혹은 키 자체를 입력하지 않아도(Default 취급) 정답입니다.

---

## 5. 대시보드 구현 시 권장 로직
정답 유무를 판단하는 '검사기(Evaluator)' 모듈을 만들 때 다음 단계를 거칩니다.
1.  **Parse**: LLM의 텍스트 응답에서 JSON 코드 블록만 추출합니다.
2.  **Compare**: 위에서 설명한 `ground_truth` 리스트의 각 항목과 비교합니다.
3.  **Feedback**: 불일치 발생 시, "함수명은 맞았으나 `base` 인자값이 틀림"과 같이 구체적인 에러 메시지를 대시보드에 표시하여 프롬프트 수정을 돕습니다.
