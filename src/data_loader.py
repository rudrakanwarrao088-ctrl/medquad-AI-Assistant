"""
MedQuAD Dataset Loader & Preprocessing Module.
Handles automatic location detection, robust column mapping, encoding fallbacks,
and data normalization for the MedQuAD medical Q&A dataset.
"""

import os
import glob
from typing import Optional, Tuple, List, Dict
import pandas as pd


def find_dataset_path() -> Optional[str]:
    """
    Search for medquad.csv in common relative locations.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(base_dir, "medical dataset", "medquad.csv"),
        os.path.join(base_dir, "medquad.csv"),
        os.path.join(os.getcwd(), "medical dataset", "medquad.csv"),
        os.path.join(os.getcwd(), "medquad.csv"),
    ]

    for p in candidates:
        if os.path.exists(p) and os.path.isfile(p):
            return p

    # Recursive fallback search
    matches = glob.glob(os.path.join(base_dir, "**", "*medquad*.csv"), recursive=True)
    if matches:
        return matches[0]

    csv_matches = glob.glob(os.path.join(base_dir, "**", "*.csv"), recursive=True)
    if csv_matches:
        return csv_matches[0]

    return None


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Dynamically detect and standardize column names across different MedQuAD variations.
    Guarantees standard schema: 'question', 'answer', 'focus_area', 'source', 'question_type'.
    """
    col_map = {}
    lower_cols = {c.lower().strip(): c for c in df.columns}

    # Detect Question column
    for candidate in ["question", "q_text", "query", "q"]:
        for col_name in lower_cols:
            if candidate in col_name and "type" not in col_name:
                col_map[lower_cols[col_name]] = "question"
                break
        if "question" in col_map.values():
            break

    # Detect Answer column
    for candidate in ["answer", "a_text", "response", "ans", "a"]:
        for col_name in lower_cols:
            if candidate in col_name:
                col_map[lower_cols[col_name]] = "answer"
                break
        if "answer" in col_map.values():
            break

    # Detect Focus Area / Disease column
    for candidate in ["focus_area", "focus", "disease", "condition", "topic"]:
        for col_name in lower_cols:
            if candidate in col_name:
                col_map[lower_cols[col_name]] = "focus_area"
                break
        if "focus_area" in col_map.values():
            break

    # Detect Source column
    for candidate in ["source", "url", "origin", "site", "institute"]:
        for col_name in lower_cols:
            if candidate in col_name:
                col_map[lower_cols[col_name]] = "source"
                break
        if "source" in col_map.values():
            break

    # Detect Question Type column
    for candidate in ["qtype", "question_type", "type", "category"]:
        for col_name in lower_cols:
            if candidate in col_name and lower_cols[col_name] not in col_map:
                col_map[lower_cols[col_name]] = "question_type"
                break
        if "question_type" in col_map.values():
            break

    # Rename matched columns
    df = df.rename(columns=col_map)

    # Supply default columns if missing
    if "question" not in df.columns:
        first_text_col = df.select_dtypes(include=["object"]).columns[0]
        df["question"] = df[first_text_col]

    if "answer" not in df.columns:
        text_cols = [c for c in df.select_dtypes(include=["object"]).columns if c != "question"]
        if text_cols:
            df["answer"] = df[text_cols[0]]
        else:
            df["answer"] = "No answer text provided."

    if "focus_area" not in df.columns:
        # Heuristic fallback: extract medical subject or use general
        df["focus_area"] = "General Health"

    if "source" not in df.columns:
        df["source"] = "NIH / MedlinePlus"

    if "question_type" not in df.columns:
        # Infer question type from question content
        df["question_type"] = df["question"].apply(infer_question_type)

    # Fill NaNs and clean strings
    df["question"] = df["question"].fillna("").astype(str).str.strip()
    df["answer"] = df["answer"].fillna("").astype(str).str.strip()
    df["focus_area"] = df["focus_area"].fillna("General Health").astype(str).str.strip()
    df["source"] = df["source"].fillna("NIH").astype(str).str.strip()
    df["question_type"] = df["question_type"].fillna("General").astype(str).str.strip()

    # Drop empty rows and exact duplicates
    df = df[(df["question"] != "") & (df["answer"] != "")].drop_duplicates(
        subset=["question", "answer"]
    ).reset_index(drop=True)

    # Combined search index text for enhanced semantic matching
    df["search_corpus"] = (
        df["question"] + " " + df["focus_area"] + " " + df["question_type"]
    ).str.lower()

    return df


def infer_question_type(q: str) -> str:
    """Infer the category of a medical question if not explicitly tagged."""
    q_lower = str(q).lower()
    if any(w in q_lower for w in ["symptom", "sign", "feel", "warning sign"]):
        return "Symptoms & Signs"
    if any(w in q_lower for w in ["treat", "cure", "therapy", "surgery", "medication", "drug"]):
        return "Treatment & Management"
    if any(w in q_lower for w in ["cause", "risk", "who is at risk", "genetic", "lifestyle"]):
        return "Causes & Risk Factors"
    if any(w in q_lower for w in ["diagnos", "test", "screen", "exam", "detect"]):
        return "Diagnosis & Tests"
    if any(w in q_lower for w in ["prevent", "avoid", "protect"]):
        return "Prevention"
    if any(w in q_lower for w in ["prognos", "outlook", "life expectancy", "expect"]):
        return "Prognosis & Outlook"
    if any(w in q_lower for w in ["what is", "what are", "overview", "definition"]):
        return "Overview & Information"
    return "General Medical Inquiry"


def load_medquad_data(csv_path: Optional[str] = None) -> Tuple[pd.DataFrame, str]:
    """
    Load and preprocess the MedQuAD dataset with encoding fallbacks.
    Returns: (cleaned_dataframe, resolved_file_path)
    """
    path = csv_path or find_dataset_path()
    if not path or not os.path.exists(path):
        raise FileNotFoundError(
            f"MedQuAD CSV file could not be found. Searched path: {path}"
        )

    encodings = ["utf-8", "latin-1", "cp1252", "utf-8-sig"]
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc, on_bad_lines="skip", low_memory=False)
            break
        except (UnicodeDecodeError, Exception):
            continue

    if df is None:
        raise ValueError(f"Unable to decode CSV file at {path} with supported encodings.")

    df = normalize_columns(df)
    return df, path


def get_dataset_stats(df: pd.DataFrame) -> Dict:
    """Generate high-level metadata statistics for dashboard analytics."""
    return {
        "total_qa_pairs": len(df),
        "unique_diseases": df["focus_area"].nunique(),
        "unique_sources": df["source"].nunique(),
        "unique_question_types": df["question_type"].nunique(),
        "top_diseases": df["focus_area"].value_counts().head(10).to_dict(),
        "top_sources": df["source"].value_counts().head(8).to_dict(),
        "question_type_dist": df["question_type"].value_counts().to_dict(),
    }
