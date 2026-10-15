"""
MedQuAD AI Medical Assistant - Streamlit Web Application.
A full-stack medical question answering, disease explorer, and dataset analytics dashboard
powered by the National Institutes of Health (NIH) MedQuAD dataset.
"""

import sys
import os
import streamlit as st
import pandas as pd

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import load_medquad_data, get_dataset_stats
from src.search_engine import MedicalSearchEngine
from src.summarizer import extract_key_takeaways, detect_clinical_terms, format_medical_disclaimer
from src.analytics import compute_comprehensive_metrics


# ---------------------------------------------------------------------------
# Page Configuration & Modern Clinical Theme
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="MedQuAD AI - Medical Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for Healthcare UI
st.markdown(
    """
    <style>
    /* Main Layout Aesthetics */
    .main {
        background-color: #f8fafc;
    }
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* Header Container */
    .med-header {
        background: linear-gradient(135deg, #0f766e 0%, #0369a1 100%);
        color: white;
        padding: 1.8rem 2.2rem;
        border-radius: 14px;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 14px rgba(15, 118, 110, 0.15);
    }
    .med-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
    }
    .med-header p {
        margin: 0.4rem 0 0 0;
        font-size: 1.05rem;
        color: #e0f2fe;
    }
    
    /* Result Card */
    .qa-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1.4rem;
        margin-bottom: 1.3rem;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #0d9488;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .qa-card:hover {
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.12);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        font-size: 0.78rem;
        font-weight: 600;
        border-radius: 9999px;
        margin-right: 0.45rem;
        margin-bottom: 0.35rem;
    }
    .badge-score {
        background-color: #ecfdf5;
        color: #065f46;
        border: 1px solid #a7f3d0;
    }
    .badge-disease {
        background-color: #eff6ff;
        color: #1e40af;
        border: 1px solid #bfdbfe;
    }
    .badge-qtype {
        background-color: #f5f3ff;
        color: #5b21b6;
        border: 1px solid #ddd6fe;
    }
    .badge-source {
        background-color: #f1f5f9;
        color: #334155;
        border: 1px solid #cbd5e1;
    }
    
    /* Disclaimer Banner */
    .disclaimer-box {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 0.85rem 1.1rem;
        border-radius: 8px;
        margin-top: 1.2rem;
        margin-bottom: 1.5rem;
        font-size: 0.88rem;
        color: #92400e;
    }
    
    /* Takeaways Box */
    .takeaways-box {
        background-color: #f0fdfa;
        border: 1px solid #ccfbf1;
        border-radius: 8px;
        padding: 0.9rem 1.2rem;
        margin-top: 0.8rem;
    }
    .takeaways-box ul {
        margin: 0.3rem 0;
        padding-left: 1.2rem;
    }
    .takeaways-box li {
        color: #134e4a;
        margin-bottom: 0.25rem;
    }

    /* Glossaries */
    .glossary-chip {
        display: inline-block;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        margin: 0.2rem;
        font-size: 0.82rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Data & Search Engine Caching
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading MedQuAD medical knowledge base...")
def get_data():
    """Load and normalize MedQuAD dataset with caching."""
    df, path = load_medquad_data()
    return df, path


@st.cache_resource(show_spinner="Indexing medical questions with TF-IDF Vector Space Model...")
def get_engine(_df: pd.DataFrame):
    """Initialize retrieval engine with caching."""
    return MedicalSearchEngine(_df)


try:
    df, dataset_path = get_data()
    engine = get_engine(df)
    stats = get_dataset_stats(df)
    data_loaded = True
except Exception as e:
    st.error(f"Error loading MedQuAD dataset: {str(e)}")
    data_loaded = False
    st.stop()


# ---------------------------------------------------------------------------
# Sidebar Navigation & Filters
# ---------------------------------------------------------------------------
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/US-NIH-Logo.svg/320px-US-NIH-Logo.svg.png",
        width=130,
    )
    st.title("MedQuAD AI")
    st.caption("National Institutes of Health (NIH) Medical QA")

    st.markdown("---")
    navigation = st.radio(
        "Navigation",
        [
            "🩺 AI Medical Assistant",
            "🔍 Disease & Topic Explorer",
            "🩹 Symptom Lookup",
            "📊 Dataset Analytics",
            "ℹ️ About & Provenance",
        ],
        index=0,
    )

    st.markdown("---")
    st.subheader("⚙️ Search Preferences")
    top_k = st.slider("Max Search Results", min_value=1, max_value=15, value=5, step=1)
    min_confidence = (
        st.slider("Min Confidence Cutoff (%)", min_value=0, max_value=80, value=10, step=5)
        / 100.0
    )

    # Condition & Question Type Filters
    all_qtypes = ["All Question Types"] + sorted(list(df["question_type"].unique()))
    selected_qtype = st.selectbox("Filter Question Category", all_qtypes)

    all_sources = ["All Sources"] + sorted(list(df["source"].unique()))
    selected_source = st.selectbox("Filter NIH Source", all_sources)

    st.markdown("---")
    st.markdown(
        f"""
        **Dataset Telemetry**
        - **Total Records:** `{stats['total_qa_pairs']:,}`
        - **Conditions:** `{stats['unique_diseases']:,}`
        - **NIH Sources:** `{stats['unique_sources']}`
        """
    )
    st.caption(f"Loaded from: `{os.path.basename(dataset_path)}`")


# ---------------------------------------------------------------------------
# Header Section
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="med-header">
        <h1>🩺 MedQuAD AI Medical Assistant</h1>
        <p>Evidence-based clinical question answering powered by 47,000+ verified National Institutes of Health (NIH) Q&A pairs</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Mandatory Clinical Disclaimer
st.markdown(
    f"""
    <div class="disclaimer-box">
        ⚠️ {format_medical_disclaimer()}
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# TAB 1: AI MEDICAL ASSISTANT
# ---------------------------------------------------------------------------
if navigation == "🩺 AI Medical Assistant":
    st.markdown("### 🔍 Ask a Medical Question")
    st.markdown(
        "Ask questions about symptoms, treatments, risk factors, or diagnoses. "
        "The retrieval engine locates the closest verified NIH medical guidance."
    )

    # Example Query Pills
    col_e1, col_e2, col_e3, col_e4, col_e5 = st.columns(5)
    selected_prompt = None

    if col_e1.button("🩸 Diabetes Signs", use_container_width=True):
        selected_prompt = "What are the warning signs and symptoms of diabetes?"
    if col_e2.button("🫁 Asthma Treatments", use_container_width=True):
        selected_prompt = "What are the treatments and medications for asthma?"
    if col_e3.button("❤️ Hypertension Causes", use_container_width=True):
        selected_prompt = "What causes high blood pressure and hypertension?"
    if col_e4.button("👁️ Glaucoma Risks", use_container_width=True):
        selected_prompt = "Who is at risk for glaucoma and how is it detected?"
    if col_e5.button("🧠 Parkinson's Prognosis", use_container_width=True):
        selected_prompt = "What is the prognosis and life expectancy for Parkinson's disease?"

    # User Input Field
    default_text = selected_prompt or ""
    query = st.text_input(
        "Enter your medical inquiry or symptoms:",
        value=default_text,
        placeholder="e.g., What are the early signs of breast cancer? How is migraine treated?",
        key="main_query_input",
    )

    if query:
        with st.spinner("Searching verified NIH medical database..."):
            results = engine.search(
                query=query,
                top_k=top_k,
                min_threshold=min_confidence,
                qtype_filter=selected_qtype,
                source_filter=selected_source,
            )

        if not results:
            st.warning(
                "No matching medical answers found above the selected confidence threshold. "
                "Try lowering the confidence cutoff in the sidebar or using broader medical terms."
            )
        else:
            st.success(f"Found **{len(results)}** verified medical answers matching your inquiry.")

            for i, res in enumerate(results, start=1):
                with st.container():
                    # Header badges
                    score_badge = f"<span class='badge badge-score'>🎯 {res['confidence_pct']}% Match</span>"
                    disease_badge = f"<span class='badge badge-disease'>🏥 {res['focus_area']}</span>"
                    qtype_badge = f"<span class='badge badge-qtype'>🏷️ {res['question_type']}</span>"
                    source_badge = f"<span class='badge badge-source'>🏛️ {res['source']}</span>"

                    st.markdown(
                        f"""
                        <div class="qa-card">
                            <div>{score_badge}{disease_badge}{qtype_badge}{source_badge}</div>
                            <h4 style="margin: 0.6rem 0 0.8rem 0; color: #0f172a;">Q{i}: {res['question']}</h4>
                            <p style="color: #334155; line-height: 1.6; white-space: pre-line;">{res['answer']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Dynamic Takeaways & Clinical Terminology Breakdown
                    col_t1, col_t2 = st.columns(2)

                    with col_t1:
                        with st.expander("📌 Key Clinical Takeaways"):
                            takeaways = extract_key_takeaways(res["answer"])
                            if takeaways:
                                for pt in takeaways:
                                    st.markdown(f"- {pt}")
                            else:
                                st.write("Direct guidance provided in answer text above.")

                    with col_t2:
                        with st.expander("📖 Clinical Terms Defined"):
                            matched_terms = detect_clinical_terms(res["answer"] + " " + res["question"])
                            if matched_terms:
                                for term_name, defn in matched_terms:
                                    st.markdown(f"**{term_name}**: *{defn}*")
                            else:
                                st.caption("No specialized clinical jargon detected; plain terminology used.")

                    # Related Questions for this Condition
                    related = engine.get_related_questions_by_focus(
                        focus_area=res["focus_area"], exclude_question=res["question"], limit=3
                    )
                    if related:
                        with st.expander(f"🔗 Related questions on {res['focus_area']}"):
                            for rq in related:
                                st.markdown(f"- **{rq['question']}** *({rq['question_type']})*")

                    st.markdown("---")


# ---------------------------------------------------------------------------
# TAB 2: DISEASE & TOPIC EXPLORER
# ---------------------------------------------------------------------------
elif navigation == "🔍 Disease & Topic Explorer":
    st.markdown("### 🔍 Disease & Health Condition Explorer")
    st.markdown("Browse all medical conditions covered across NIH institutes in MedQuAD.")

    # Unique conditions
    all_diseases = sorted(df["focus_area"].dropna().unique())
    selected_disease = st.selectbox(
        "Select a Medical Condition to Explore:",
        options=all_diseases,
        index=0 if all_diseases else 0,
    )

    if selected_disease:
        disease_df = df[df["focus_area"] == selected_disease]
        st.markdown(
            f"#### Medical Guidance for **{selected_disease}** ({len(disease_df)} Q&A pairs available)"
        )

        # Overview Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Available Questions", len(disease_df))
        m2.metric("Covered Topics", disease_df["question_type"].nunique())
        m3.metric("Primary NIH Source", disease_df["source"].mode()[0] if not disease_df.empty else "NIH")

        # Questions categorized by question type
        for qtype, group in disease_df.groupby("question_type"):
            st.markdown(f"##### 🏷️ {qtype}")
            for idx, row in group.iterrows():
                with st.expander(f"❓ {row['question']}"):
                    st.markdown(f"**Answer:**\n\n{row['answer']}")
                    st.caption(f"Source: {row['source']}")


# ---------------------------------------------------------------------------
# TAB 3: SYMPTOM LOOKUP
# ---------------------------------------------------------------------------
elif navigation == "🩹 Symptom Lookup":
    st.markdown("### 🩹 Symptom & Warning Signs Lookup")
    st.markdown("Search for specific symptoms to find associated conditions and diagnostic advice.")

    symptom_query = st.text_input(
        "Enter observed symptoms (comma-separated):",
        placeholder="e.g. chest pain, shortness of breath, dizziness",
    )

    if symptom_query:
        with st.spinner("Analyzing symptoms across clinical database..."):
            symptom_results = engine.search(
                query=f"symptoms of {symptom_query}",
                top_k=8,
                min_threshold=0.08,
                qtype_filter="Symptoms & Signs"
                if "Symptoms & Signs" in df["question_type"].values
                else None,
            )

        if not symptom_results:
            st.info("No direct symptom matches. Showing general health matches:")
            symptom_results = engine.search(query=symptom_query, top_k=5, min_threshold=0.05)

        for res in symptom_results:
            with st.expander(f"🩺 {res['focus_area']} - {res['question']}"):
                st.markdown(res["answer"])
                st.caption(f"Source: {res['source']} | Confidence: {res['confidence_pct']}%")


# ---------------------------------------------------------------------------
# TAB 4: DATASET ANALYTICS & INSIGHTS
# ---------------------------------------------------------------------------
elif navigation == "📊 Dataset Analytics":
    st.markdown("### 📊 MedQuAD Dataset Exploratory Data Analysis (EDA)")
    st.markdown("Statistical distribution and metrics of the National Institutes of Health benchmark.")

    metrics = compute_comprehensive_metrics(df)

    # KPI Metrics
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Q&A Pairs", f"{metrics['total_records']:,}")
    kpi2.metric("Unique Conditions", f"{metrics['unique_diseases']:,}")
    kpi3.metric("NIH Sources", f"{metrics['unique_sources']}")
    kpi4.metric("Avg Words / Answer", f"{metrics['avg_words_per_answer']}")

    st.markdown("---")

    # Visualizations
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("#### 🏆 Top 15 Most Documented Medical Conditions")
        st.bar_chart(
            metrics["top_conditions_df"].set_index("Condition")["Count"],
            color="#0d9488",
        )

    with col_chart2:
        st.markdown("#### 📋 Question Categories Distribution")
        st.bar_chart(
            metrics["qtype_counts_df"].set_index("Question Type")["Count"],
            color="#0284c7",
        )

    st.markdown("#### 🏛️ Top NIH Contributing Institutes")
    st.bar_chart(
        metrics["source_counts_df"].set_index("NIH Source")["Count"],
        color="#6366f1",
    )

    st.markdown("---")
    st.markdown("#### 📋 Interactive Data Table & Export")
    search_filter = st.text_input("Filter raw data by keyword:", placeholder="Type any word...")
    filtered_df = df
    if search_filter:
        filtered_df = df[
            df["question"].str.contains(search_filter, case=False, na=False)
            | df["focus_area"].str.contains(search_filter, case=False, na=False)
        ]

    st.dataframe(
        filtered_df[["question", "focus_area", "question_type", "source", "answer"]].head(100),
        use_container_width=True,
    )

    csv_data = filtered_df.head(500).to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Dataset (CSV)",
        data=csv_data,
        file_name="medquad_filtered_export.csv",
        mime="text/csv",
    )


# ---------------------------------------------------------------------------
# TAB 5: ABOUT & PROVENANCE
# ---------------------------------------------------------------------------
elif navigation == "ℹ️ About & Provenance":
    st.markdown("### ℹ️ About MedQuAD AI Assistant")
    st.markdown(
        """
        **MedQuAD** (Medical Question Answering Dataset) is a standardized benchmark created by 
        Asma Ben Abacha and Dina Demner-Fushman at the National Library of Medicine (NLM), 
        part of the U.S. National Institutes of Health (NIH).
        
        #### 🏛️ Contributing NIH Institutes & Websites
        The dataset synthesizes verified medical information from 12 official NIH health resources:
        - **Cancer.gov** (National Cancer Institute)
        - **CDC** (Centers for Disease Control and Prevention)
        - **GARD** (Genetic and Rare Diseases Information Center)
        - **MedlinePlus Health Topics** (National Library of Medicine)
        - **NIDDK** (National Institute of Diabetes and Digestive and Kidney Diseases)
        - **NINDS** (National Institute of Neurological Disorders and Stroke)
        - **NIAMS** (National Institute of Arthritis and Musculoskeletal and Skin Diseases)
        - **NHLBI** (National Heart, Lung, and Blood Institute)
        
        #### 🔬 Technical Architecture
        - **Hybrid Retrieval System:** Combines sublinear Term Frequency-Inverse Document Frequency (TF-IDF) 
          n-gram representations with cosine similarity vector projections and domain-specific clinical entity boosting.
        - **Clinical Entity & Jargon Simplifier:** Matches medical concepts against a verified clinical lexicon 
          to provide plain-English definitions alongside authoritative answers.
        - **Response Synthesis:** Extracts high-relevance clinical takeaways and organizes answers by topic category.
        
        #### 📜 Citation
        If using this dataset or application for research, please cite:
        ```bibtex
        @article{BenAbacha-DemnerFushman-2019,
          author    = {Asma Ben Abacha and Dina Demner-Fushman},
          title     = {A Question-Entailment Approach to Question Answering in the Medical Domain},
          journal   = {BMC Bioinformatics},
          volume    = {20},
          number    = {1},
          pages     = {511:1--511:23},
          year      = {2019}
        }
        ```
        """
    )
