import json
import pandas as pd
from datasets import load_dataset
from deep_translator import GoogleTranslator
from tqdm import tqdm
import time

def create_korean_gorilla_dataset(num_samples=10):
    print("🚀 Gorilla 데이터셋 다운로드 중...")
    # Gorilla 리더보드 데이터 로드
    ds = load_dataset("gorilla-llm/Berkeley-Function-Calling-Leaderboard", split="train")
    
    # 'simple' 카테고리만 필터링 (초보자 훈련용으로 가장 적합)
    # 데이터셋 구조상 ast_eval 등으로 필터링하거나, 그냥 앞부분 데이터가 보통 simple입니다.
    # 여기서는 범용성을 위해 무작위로 섞어서 뽑지 않고 앞에서부터 가져옵니다.
    
    # 번역기 초기화
    translator = GoogleTranslator(source='auto', target='ko')
    
    new_dataset = []
    
    print(f"🔄 {num_samples}개의 데이터를 한국어로 변환합니다...")
    
    # 데이터 변환 루프
    for i in tqdm(range(num_samples)):
        item = ds[i]
        
        original_question = item['question']
        
        # 1. 질문 번역 (영어 -> 한국어)
        try:
            # 번역 API 과부하 방지를 위해 0.5초 대기
            time.sleep(0.5) 
            korean_question = translator.translate(original_question)
            
            # 번역 품질이 딱딱할 수 있으니 나중에 사람이 검수하면 더 좋습니다.
            # 예: "Get weather" -> "날씨를 얻다" (X) -> "날씨 알려줘" (O)
            
        except Exception as e:
            print(f"⚠️ 번역 실패 (Index {i}): {e}")
            korean_question = original_question # 실패하면 그냥 영어로 둠
            
        # 2. 새로운 데이터 구조 생성
        new_entry = {
            "id": i,
            "category": "simple",
            "question_en": original_question, # 원본 영어 질문 (참고용)
            "question_ko": korean_question,   # 번역된 한국어 질문 (이걸로 테스트!)
            "function": item['function'],     # 툴 스펙 (그대로 둠)
            "ground_truth": item['ground_truth'] # 정답 (그대로 둠)
        }
        
        new_dataset.append(new_entry)

    # 3. 파일로 저장
    output_filename = "korean_gorilla_sample.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(new_dataset, f, ensure_ascii=False, indent=4)
        
    print(f"\n✅ 변환 완료! '{output_filename}' 파일이 생성되었습니다.")
    print("📂 내용을 확인해보세요. 이제 이걸로 RAG/Agent를 테스트하면 됩니다.")

if __name__ == "__main__":
    create_korean_gorilla_dataset(num_samples=10) # 원하는 만큼 숫자를 늘리세요