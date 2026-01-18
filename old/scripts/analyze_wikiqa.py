import pandas as pd
import json
import os

def analyze_wikiqa(file_path):
    try:
        df = pd.read_parquet(file_path)
        print("Columns:", df.columns.tolist())
        print("\nHead:\n", df.head(2))
        
        # Save a sample to JSON for inspection
        sample_path = os.path.join(os.path.dirname(file_path), "sample.json")
        df.head(10).to_json(sample_path, orient='records', force_ascii=False, indent=2)
        print(f"\nSaved sample to {sample_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    path = r"c:\final\final_subject\data\ragas-wikiqa\data\train-00000-of-00001-78b16d7ae6b9b0f1.parquet"
    analyze_wikiqa(path)
