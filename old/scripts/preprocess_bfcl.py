import json
import os

def merge_bfcl_data(input_file, answer_file, output_file):
    # Load input data (Questions & Functions)
    input_data = {}
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            input_data[item['id']] = item

    # Load answer data (Ground Truth)
    merged_data = []
    with open(answer_file, 'r', encoding='utf-8') as f:
        for line in f:
            answer = json.loads(line)
            item_id = answer['id']
            
            if item_id in input_data:
                # Merge input and answer
                combined = input_data[item_id]
                combined['ground_truth'] = answer['ground_truth']
                merged_data.append(combined)

    # Save merged data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully merged {len(merged_data)} items into {output_file}")

if __name__ == "__main__":
    base_path = r"c:\final\final_subject\data"
    # Merge Multi-turn data
    multi_input = os.path.join(base_path, "BFCL_v3_multi_turn_base.json")
    multi_answer = os.path.join(base_path, "possible_answer", "BFCL_v3_multi_turn_base.json")
    if os.path.exists(multi_input):
        merge_bfcl_data(multi_input, multi_answer, os.path.join(base_path, "merged_bfcl_multi.json"))

    # Merge Irrelevance (Guardrail) data
    # Note: Irrelevance often has "simple_answer" as ground truth
    irr_input = os.path.join(base_path, "BFCL_v3_irrelevance.json")
    irr_answer = os.path.join(base_path, "possible_answer", "BFCL_v3_irrelevance.json")
    if os.path.exists(irr_input):
        merge_bfcl_data(irr_input, irr_answer, os.path.join(base_path, "merged_bfcl_irrelevance.json"))
