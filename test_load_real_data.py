"""
Test loading the actual MedQuAD dataset file and building the TF-IDF search index.
"""
import time
from src.data_loader import load_medquad_data, get_dataset_stats
from src.search_engine import MedicalSearchEngine

def main():
    print("Loading MedQuAD dataset...")
    t0 = time.time()
    df, path = load_medquad_data()
    t1 = time.time()
    print(f"[OK] Loaded {len(df):,} Q&A pairs from '{path}' in {t1 - t0:.2f}s")
    
    stats = get_dataset_stats(df)
    print(f"[OK] Unique Conditions: {stats['unique_diseases']:,}")
    print(f"[OK] Unique Sources: {stats['unique_sources']}")
    print(f"[OK] Question Types: {list(stats['question_type_dist'].keys())[:5]}")

    print("Building TF-IDF Index...")
    t2 = time.time()
    engine = MedicalSearchEngine(df)
    t3 = time.time()
    print(f"[OK] Indexed in {t3 - t2:.2f}s")

    test_query = "What are the warning signs of breast cancer?"
    print(f"\nTesting Query: '{test_query}'")
    results = engine.search(test_query, top_k=2)
    for r in results:
        print(f"-> [{r['confidence_pct']}%] {r['question']} ({r['focus_area']} / {r['source']})")

if __name__ == "__main__":
    main()
