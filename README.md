# 🩺 MedQuAD AI Medical Assistant & QA Web App

An evidence-based clinical question answering, disease explorer, and analytics web application built on the National Institutes of Health (**NIH**) **MedQuAD** (Medical Question Answering Dataset).

---

## 🌟 Key Features

1. **🩺 Intelligent Clinical Question Answering**:
   - Natural language search over 47,000+ verified medical Q&A pairs.
   - Hybrid **TF-IDF + N-gram Cosine Similarity** engine with disease/entity boosting.
   - Confidence scoring and dynamic threshold filtering.
   - Verified NIH source attribution (MedlinePlus, Cancer.gov, CDC, NIDDK, etc.).

2. **📋 Clinical Takeaway Extraction & Jargon Simplifier**:
   - Automatically parses complex medical text into high-priority bullet points for patient reading.
   - Built-in medical terminology glossary translating clinical jargon (e.g. *edema*, *dyspnea*, *arrhythmia*, *prophylaxis*) into plain English.

3. **🔍 Disease & Topic Explorer**:
   - Explore over 1,000+ medical conditions, diseases, and disorders.
   - Categorized by question types: Symptoms & Signs, Diagnosis & Tests, Treatment & Management, Causes & Risk Factors, and Prognosis.

4. **🩹 Symptom & Warning Signs Lookup**:
   - Multi-symptom query interface to identify potential matching conditions and verified medical guidelines.

5. **📊 Dataset Exploratory Data Analysis (EDA)**:
   - Interactive KPI cards (total pairs, unique conditions, sources).
   - Bar charts for the top 15 most documented conditions, question types, and NIH sources.
   - Filterable raw data table with one-click **CSV Export**.

6. **⚠️ Clinical & HIPAA Disclaimer**:
   - Prominently displayed medical safety and educational advice disclaimer.

---

## 📁 Project Structure

```
medquad.csv/
├── app.py                      # Streamlit Medical Assistant web application
├── requirements.txt            # Project dependencies
├── run_app.bat                 # One-click Windows runner script
├── README.md                   # Documentation & guide
├── medical dataset/
│   └── medquad.csv             # The MedQuAD medical Q&A dataset
└── src/
    ├── __init__.py
    ├── data_loader.py          # Robust CSV loader with dynamic column mapping
    ├── search_engine.py        # TF-IDF retrieval engine with clinical boosting
    ├── summarizer.py           # Takeaway extractor & clinical jargon explainer
    └── analytics.py            # Dataset distribution metrics and EDA
```

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Web Application
Double-click `run_app.bat` or run in terminal:
```bash
streamlit run app.py
```
Open your browser at: **`http://localhost:8501`**

---

## 🔬 Dataset & Provenance
- **Dataset:** MedQuAD (Medical Question Answering Dataset)
- **Creators:** Asma Ben Abacha and Dina Demner-Fushman, U.S. National Library of Medicine (NLM / NIH).
- **Sources Included:** MedlinePlus, Cancer.gov (NCI), CDC, GARD, NIDDK, NINDS, NIAMS, NHLBI.
