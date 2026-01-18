import json
import os
from scripts.evaluator import AgentEvaluator

def test_on_real_data():
    evaluator = AgentEvaluator()
    data_path = r"c:\final\final_subject\data\merged_bfcl_simple.json"
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Take the first entry
    item = data[0]
    print(f"Testing ID: {item['id']}")
    print(f"Question: {item['question'][0][0]['content']}")
    
    # Simulate a correct model response
    # GT: {"calculate_triangle_area": {"base": [10], "height": [5], "unit": ["units", ""]}}
    correct_model_response = {
        "calculate_triangle_area": {
            "base": 10,
            "height": 5,
            "unit": "units"
        }
    }
    
    result = evaluator.evaluate_tool_calling(correct_model_response, item['ground_truth'])
    print("\n[Correct Response Test]")
    print(f"Result: {result['status']}, Score: {result['score']}")

    # Simulate a response with WRONG parameter
    wrong_val_response = {
        "calculate_triangle_area": {
            "base": 10,
            "height": 999, # WRONG
            "unit": "units"
        }
    }
    result_wrong = evaluator.evaluate_tool_calling(wrong_val_response, item['ground_truth'])
    print("\n[Wrong Value Test]")
    print(f"Result: {result_wrong['status']}, Score: {result_wrong['score']}")
    print(f"Errors: {result_wrong['errors']}")

    # Simulate a response with MISSING parameter
    missing_response = {
        "calculate_triangle_area": {
            "base": 10
            # missing height
        }
    }
    result_missing = evaluator.evaluate_tool_calling(missing_response, item['ground_truth'])
    print("\n[Missing Param Test]")
    print(f"Result: {result_missing['status']}, Score: {result_missing['score']}")
    print(f"Errors: {result_missing['errors']}")

if __name__ == "__main__":
    test_on_real_data()
