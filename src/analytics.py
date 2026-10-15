"""
Analytics and Dataset Exploration Module for MedQuAD.
Calculates distribution metrics, frequency charts, and descriptive statistics.
"""

from typing import Dict, Any
import pandas as pd


def compute_comprehensive_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute statistical distributions and KPI metrics for the dataset.
    """
    total_records = len(df)
    unique_diseases = int(df["focus_area"].nunique())
    unique_sources = int(df["source"].nunique())
    unique_qtypes = int(df["question_type"].nunique())

    # Answer length in words
    word_counts = df["answer"].str.split().str.len()
    avg_words = float(word_counts.mean())
    max_words = int(word_counts.max())
    min_words = int(word_counts.min())

    # Top conditions
    top_conditions = (
        df["focus_area"].value_counts().head(15).reset_index()
    )
    top_conditions.columns = ["Condition", "Count"]

    # Question types
    qtype_counts = (
        df["question_type"].value_counts().head(10).reset_index()
    )
    qtype_counts.columns = ["Question Type", "Count"]

    # Sources
    source_counts = (
        df["source"].value_counts().head(10).reset_index()
    )
    source_counts.columns = ["NIH Source", "Count"]

    return {
        "total_records": total_records,
        "unique_diseases": unique_diseases,
        "unique_sources": unique_sources,
        "unique_qtypes": unique_qtypes,
        "avg_words_per_answer": round(avg_words, 1),
        "max_words_per_answer": max_words,
        "min_words_per_answer": min_words,
        "top_conditions_df": top_conditions,
        "qtype_counts_df": qtype_counts,
        "source_counts_df": source_counts,
    }
