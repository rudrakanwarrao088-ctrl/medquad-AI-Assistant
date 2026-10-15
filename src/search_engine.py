"""
MedQuAD Search & Retrieval Engine.
Provides high-performance hybrid semantic and keyword retrieval across medical Q&A pairs
using TF-IDF vectorization, cosine similarity, and clinical entity boosting.
"""

from typing import List, Dict, Optional
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MedicalSearchEngine:
    """
    Search and retrieval index over MedQuAD dataset.
    Combines n-gram TF-IDF, cosine similarity, and keyword/disease boosting.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            max_features=50000,
            sublinear_tf=True,
        )
        # Fit on combined search corpus
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["search_corpus"])
        # Precompute lowercase lookup series for boosting
        self.focus_series = self.df["focus_area"].astype(str).str.lower()

    def search(
        self,
        query: str,
        top_k: int = 5,
        min_threshold: float = 0.05,
        focus_filter: Optional[str] = None,
        qtype_filter: Optional[str] = None,
        source_filter: Optional[str] = None,
    ) -> List[Dict]:
        """
        Execute ranked medical retrieval for a user question.

        Args:
            query: Natural language medical question or symptoms.
            top_k: Maximum number of results to return.
            min_threshold: Minimum similarity score cutoff (0.0 to 1.0).
            focus_filter: Optional disease/condition name filter.
            qtype_filter: Optional question type filter.
            source_filter: Optional NIH source filter.

        Returns:
            List of result dictionaries sorted by relevance score.
        """
        clean_query = query.strip().lower()
        if not clean_query:
            return []

        # Transform query vector
        query_vec = self.vectorizer.transform([clean_query])
        sim_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Disease / Entity boosting: if query mentions the exact disease, boost score
        for word in clean_query.split():
            if len(word) > 3:
                mask = self.focus_series.str.contains(word, regex=False).to_numpy()
                sim_scores[mask] += 0.08

        # Apply user filters
        mask = np.ones(len(self.df), dtype=bool)

        if focus_filter and focus_filter != "All Conditions":
            mask &= (self.df["focus_area"] == focus_filter).values

        if qtype_filter and qtype_filter != "All Question Types":
            mask &= (self.df["question_type"] == qtype_filter).values

        if source_filter and source_filter != "All Sources":
            mask &= (self.df["source"] == source_filter).values

        sim_scores[~mask] = 0.0

        # Filter by threshold
        valid_indices = np.where(sim_scores >= min_threshold)[0]
        if len(valid_indices) == 0:
            return []

        # Sort top-k candidates (sample up to 3x top_k to account for duplicates)
        candidate_count = min(len(valid_indices), top_k * 3)
        sorted_indices = valid_indices[np.argsort(-sim_scores[valid_indices])][:candidate_count]

        results = []
        seen_questions = set()
        query_terms = set(w for w in clean_query.split() if len(w) > 2)

        for idx in sorted_indices:
            row = self.df.iloc[idx]
            q_norm = (row["question"].strip().lower(), row["focus_area"].strip().lower())
            if q_norm in seen_questions:
                continue
            seen_questions.add(q_norm)

            raw_score = float(sim_scores[idx])
            # Normalize confidence score between 0% and 100%
            conf_pct = min(100.0, raw_score * 100)

            # Detect matched query words
            q_words = set(row["search_corpus"].split())
            overlap = query_terms.intersection(q_words)

            results.append(
                {
                    "index": int(idx),
                    "question": row["question"],
                    "answer": row["answer"],
                    "focus_area": row["focus_area"],
                    "source": row["source"],
                    "question_type": row["question_type"],
                    "score": raw_score,
                    "confidence_pct": round(conf_pct, 1),
                    "matched_keywords": list(overlap),
                }
            )
            if len(results) >= top_k:
                break

        return results

    def get_related_questions_by_focus(
        self, focus_area: str, exclude_question: str = "", limit: int = 4
    ) -> List[Dict]:
        """Retrieve related questions for the same medical condition."""
        matches = self.df[
            (self.df["focus_area"].str.lower() == focus_area.lower())
            & (self.df["question"] != exclude_question)
        ].head(limit)

        return matches[["question", "answer", "question_type", "source"]].to_dict(
            orient="records"
        )
