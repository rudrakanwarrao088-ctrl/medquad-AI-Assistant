"""
Unit and integration tests for MedQuAD AI Assistant pipeline.
Validates normalization, search retrieval, summarization, and analytics.
"""

import pandas as pd
from src.data_loader import normalize_columns
from src.search_engine import MedicalSearchEngine
from src.summarizer import extract_key_takeaways, detect_clinical_terms, format_medical_disclaimer
from src.analytics import compute_comprehensive_metrics


def run_tests():
    print("--- 1. Testing Summarizer & Clinical Jargon ---")
    sample_text = (
        "Patients diagnosed with hypertension often experience dyspnea and headache. "
        "Standard treatment includes ACE inhibitors and lifestyle modifications such as reducing sodium intake. "
        "The prognosis is generally favorable when monitored regularly by a cardiologist."
    )
    takeaways = extract_key_takeaways(sample_text)
    assert len(takeaways) > 0, "Takeaways should not be empty"
    print(f"[OK] Extracted {len(takeaways)} key takeaways.")

    terms = detect_clinical_terms(sample_text)
    matched_names = [t[0].lower() for t in terms]
    assert "hypertension" in matched_names, "Hypertension should be detected"
    assert "dyspnea" in matched_names, "Dyspnea should be detected"
    print(f"[OK] Detected clinical terms: {matched_names}")

    disclaimer = format_medical_disclaimer()
    assert "Disclaimer" in disclaimer
    print("[OK] Clinical disclaimer generated successfully.")

    print("\n--- 2. Testing Data Normalization & Search Engine ---")
    mock_raw_data = pd.DataFrame({
        "Question": [
            "What are the symptoms of Asthma?",
            "What treatments exist for Type 2 Diabetes?",
            "How to prevent heart disease?",
            "What causes Glaucoma?",
        ],
        "Answer": [
            "Common symptoms of asthma include wheezing, coughing, chest tightness, and shortness of breath.",
            "Type 2 diabetes treatments include insulin therapy, metformin, diet control, and regular exercise.",
            "Preventing heart disease involves healthy eating, exercising 150 minutes weekly, and avoiding tobacco.",
            "Glaucoma is primarily caused by elevated intraocular pressure damaging the optic nerve.",
        ],
        "Focus": ["Asthma", "Diabetes", "Heart Disease", "Glaucoma"],
        "Source": ["MedlinePlus", "NIDDK", "CDC", "GARD"],
    })

    cleaned = normalize_columns(mock_raw_data)
    assert "question" in cleaned.columns
    assert "answer" in cleaned.columns
    assert "focus_area" in cleaned.columns
    assert "question_type" in cleaned.columns
    assert "search_corpus" in cleaned.columns
    print(f"[OK] Columns normalized successfully: {list(cleaned.columns)}")

    engine = MedicalSearchEngine(cleaned)
    results = engine.search("What are the warning signs of asthma?", top_k=2)
    assert len(results) > 0, "Search should return results"
    top_res = results[0]
    print(f"[OK] Top search hit: {top_res['question']} (Confidence: {top_res['confidence_pct']}%)")
    assert top_res["focus_area"] == "Asthma", "Expected Asthma as top result"

    print("\n--- 3. Testing Analytics Computation ---")
    metrics = compute_comprehensive_metrics(cleaned)
    assert metrics["total_records"] == 4
    assert metrics["unique_diseases"] == 4
    print(f"[OK] Computed metrics: {metrics['total_records']} records, {metrics['unique_diseases']} diseases.")

    print("\n==========================================")
    print(">>> ALL TESTS PASSED SUCCESSFULLY! <<<")
    print("==========================================")


if __name__ == "__main__":
    run_tests()
