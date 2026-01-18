import json
import os
from deep_translator import GoogleTranslator
from tqdm import tqdm

def translate_json_data(input_path, output_path, is_jsonl=False, limit=20):
    """
    JSON 또는 JSONL 데이터의 질문 필드를 한국어로 번역하여 저장합니다.
    """
    if not os.path.exists(input_path):
        print(f"파일을 찾을 수 없습니다: {input_path}")
        return

    translator = GoogleTranslator(source='en', target='ko')
    translated_data = []

    # 데이터 로드
    if is_jsonl:
        raw_data = []
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip(): raw_data.append(json.loads(line))
    else:
        with open(input_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

    sample_data = raw_data[:limit]
    print(f"번역 시작: {input_path} (대상: {len(sample_data)}개)")

    for item in tqdm(sample_data):
        try:
            # 1. BFCL 구조 번역 (질문 + 도구 명세)
            if 'question' in item and isinstance(item['question'], list):
               if isinstance(item['question'][0], list) and 'content' in item['question'][0][0]:
                   item['question'][0][0]['content'] = translator.translate(item['question'][0][0]['content'])
               elif isinstance(item['question'][0], list) and len(item['question']) > 1:
                   for turn in range(len(item['question'])):
                       item['question'][turn][0]['content'] = translator.translate(item['question'][turn][0]['content'])

            # 도구 명세(function) 내부의 description 번역 추가
            if 'function' in item and isinstance(item['function'], list):
                for func in item['function']:
                    if 'description' in func:
                        func['description'] = translator.translate(func['description'])
                    
                    # 파라미터 설명 번역
                    if 'parameters' in func and 'properties' in func['parameters']:
                        props = func['parameters']['properties']
                        for p_name in props:
                            if 'description' in props[p_name]:
                                props[p_name]['description'] = translator.translate(props[p_name]['description'])

            # 2. RAG WikiQA 구조 대응
            for field in ['question', 'context', 'correct_answer']:
                if field in item and isinstance(item[field], str):
                    item[field] = translator.translate(item[field])
            
            translated_data.append(item)
        except Exception as e:
            print(f"오류 발생: {e}")
            translated_data.append(item)

    # 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, indent=2, ensure_ascii=False)
    print(f"번역 완료: {output_path}")

if __name__ == "__main__":
    # 1. Tool Calling (Simple)
    translate_json_data(
        r"c:\final\final_subject\data\merged_bfcl_simple.json",
        r"c:\final\final_subject\data\merged_bfcl_simple_ko.json",
        limit=50
    )
    # 2. Guardrail (Irrelevance)
    translate_json_data(
        r"c:\final\final_subject\data\BFCL_v3_irrelevance.json",
        r"c:\final\final_subject\data\merged_bfcl_irrelevance_ko.json",
        is_jsonl=True,
        limit=30
    )
    # 3. Multi-turn
    translate_json_data(
        r"c:\final\final_subject\data\merged_bfcl_multi.json",
        r"c:\final\final_subject\data\merged_bfcl_multi_ko.json",
        limit=10
    )
    # 4. RAG
    translate_json_data(
        r"c:\final\final_subject\data\ragas-wikiqa\data\sample.json",
        r"c:\final\final_subject\data\ragas-wikiqa\data\sample_ko.json",
        limit=10
    )
