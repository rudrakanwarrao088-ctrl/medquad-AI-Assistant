"""
PowerPoint Generator for MedQuAD AI Medical Assistant Presentation.
Generates a widescreen, 10-slide deck with clinical styling.
Author: Rashi Kanwar Rao
"""

import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


def create_deck():
    prs = Presentation()
    # 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clinical Color Palette
    PRIMARY = RGBColor(13, 118, 110)      # Deep Teal
    PRIMARY_DARK = RGBColor(15, 23, 42)   # Navy Dark
    ACCENT_BLUE = RGBColor(2, 132, 199)   # Ocean Cyan
    TEXT_MAIN = RGBColor(30, 41, 59)      # Slate Dark
    TEXT_MUTED = RGBColor(100, 116, 139)  # Slate Muted
    BG_CARD = RGBColor(248, 250, 252)     # Off-white Card
    BORDER_CARD = RGBColor(226, 232, 240) # Slate Border
    WHITE = RGBColor(255, 255, 255)
    TEAL_LIGHT = RGBColor(240, 253, 250)

    def add_header(slide, title_text, category_text="HEALTHCARE AI & NLP CAPSTONE"):
        # Top banner category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE

        # Slide Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.5), Inches(0.8))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = PRIMARY_DARK

    def add_card(slide, left, top, width, height, title, items, badge=""):
        # Shape background
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = BG_CARD
        shape.line.color.rgb = BORDER_CARD
        shape.line.width = Pt(1.2)

        # Text Frame
        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = f"{title}"
        p0.font.size = Pt(17)
        p0.font.bold = True
        p0.font.color.rgb = PRIMARY
        p0.space_after = Pt(10)

        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.size = Pt(13)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)

    # Gradient background simulation
    bg = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = PRIMARY_DARK
    bg.line.fill.background()

    # Title Box
    title_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(2.2))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "EVIDENCE-BASED HEALTHCARE AI SYSTEM"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = RGBColor(45, 212, 191) # Teal Accent
    p_badge.space_after = Pt(12)

    p_main = tf1.add_paragraph()
    p_main.text = "MedQuAD AI Medical Assistant"
    p_main.font.size = Pt(44)
    p_main.font.bold = True
    p_main.font.color.rgb = WHITE
    p_main.space_after = Pt(12)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Clinical Question Answering, Disease Exploration & Diagnostic Knowledge Retrieval"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = RGBColor(226, 232, 240)

    # Author Card
    author_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.7), Inches(6.5), Inches(1.6))
    author_card.fill.solid()
    author_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    author_card.line.color.rgb = RGBColor(51, 65, 85)

    atb = slide1.shapes.add_textbox(Inches(1.4), Inches(4.8), Inches(6.1), Inches(1.4))
    atf = atb.text_frame
    ap1 = atf.paragraphs[0]
    ap1.text = "Presented By:"
    ap1.font.size = Pt(12)
    ap1.font.color.rgb = RGBColor(148, 163, 184)

    ap2 = atf.add_paragraph()
    ap2.text = "Rashi Kanwar Rao"
    ap2.font.size = Pt(22)
    ap2.font.bold = True
    ap2.font.color.rgb = WHITE
    ap2.space_after = Pt(4)

    ap3 = atf.add_paragraph()
    ap3.text = "Lead Project Developer & Healthcare AI Researcher"
    ap3.font.size = Pt(13)
    ap3.font.color.rgb = RGBColor(94, 234, 212)

    # Metadata Card
    meta_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.0), Inches(4.7), Inches(4.2), Inches(1.6))
    meta_card.fill.solid()
    meta_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    meta_card.line.color.rgb = RGBColor(51, 65, 85)

    mtb = slide1.shapes.add_textbox(Inches(8.2), Inches(4.8), Inches(3.8), Inches(1.4))
    mtf = mtb.text_frame
    mp1 = mtf.paragraphs[0]
    mp1.text = "Dataset & Foundation:"
    mp1.font.size = Pt(12)
    mp1.font.color.rgb = RGBColor(148, 163, 184)
    mp2 = mtf.add_paragraph()
    mp2.text = "NIH MedQuAD Benchmark"
    mp2.font.size = Pt(16)
    mp2.font.bold = True
    mp2.font.color.rgb = WHITE
    mp3 = mtf.add_paragraph()
    mp3.text = "16,350+ Clinical Q&A Pairs | 5,120+ Conditions"
    mp3.font.size = Pt(12)
    mp3.font.color.rgb = RGBColor(203, 213, 225)

    # =========================================================================
    # SLIDE 2: Project Motivation & Problem Statement
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Project Motivation & Clinical Need")

    add_card(slide2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "⚠️ The Healthcare Information Challenge", [
        "Unreliable Public Web Queries: Patients seeking medical advice online are frequently misled by unverified or sensationalized medical advice.",
        "Clinical Density & Jargon: Authoritative medical literature uses dense terminology (dyspnea, idiopathic, ischemia) that creates cognitive barriers.",
        "Diagnostic Anxiety: Misinterpreted health information increases patient anxiety and delays timely consultation with licensed professionals.",
        "Lack of Source Attribution: Most online aggregators do not cite official clinical origins or specific institutional research."
    ])

    add_card(slide2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "💡 The MedQuAD AI Solution", [
        "NIH-Verified Ground Truth: Grounded strictly in peer-reviewed clinical knowledge from 12 National Institutes of Health (NIH) entities.",
        "Hybrid Semantic Retrieval: Combines sublinear TF-IDF, n-gram vector matching, and clinical entity boosting for precision answers.",
        "Patient-Centered NLP Layer: Automatically distills answers into actionable bulleted takeaways and plain-English medical glossaries.",
        "Responsible Medical Governance: Transparent similarity confidence scores and prominent clinical safety notices."
    ])

    # =========================================================================
    # SLIDE 3: The MedQuAD Dataset Architecture
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "MedQuAD Dataset & Institutional Provenance")

    # Metrics row
    metric_cols = [
        ("16,359+", "Curated Q&A Pairs", PRIMARY),
        ("5,126", "Documented Diseases", ACCENT_BLUE),
        ("9", "NIH Institutes", PRIMARY_DARK),
        ("132 Words", "Avg Clinical Response", PRIMARY)
    ]
    for i, (num, label, col) in enumerate(metric_cols):
        m_box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 2.95), Inches(1.8), Inches(2.8), Inches(1.4))
        m_box.fill.solid()
        m_box.fill.fore_color.rgb = TEAL_LIGHT
        m_box.line.color.rgb = RGBColor(153, 246, 228)

        tb = slide3.shapes.add_textbox(Inches(0.9 + i * 2.95), Inches(1.9), Inches(2.6), Inches(1.2))
        tf = tb.text_frame
        p_num = tf.paragraphs[0]
        p_num.text = num
        p_num.font.size = Pt(26)
        p_num.font.bold = True
        p_num.font.color.rgb = col
        p_num.alignment = PP_ALIGN.CENTER

        p_lbl = tf.add_paragraph()
        p_lbl.text = label
        p_lbl.font.size = Pt(12)
        p_lbl.font.color.rgb = TEXT_MAIN
        p_lbl.alignment = PP_ALIGN.CENTER

    add_card(slide3, Inches(0.8), Inches(3.4), Inches(5.6), Inches(3.5), "🏛️ Contributing NIH Institutes", [
        "MedlinePlus: Patient education, anatomy, disorders, medications.",
        "National Cancer Institute (Cancer.gov): Oncology diagnostics & therapies.",
        "CDC: Communicable diseases, public health guidelines.",
        "NIDDK: Diabetes, kidney disease, endocrine & metabolic disorders.",
        "NINDS: Neurological disorders, brain pathologies, dementia.",
        "GARD: Genetic and rare diseases repository."
    ])

    add_card(slide3, Inches(6.8), Inches(3.4), Inches(5.7), Inches(3.5), "🏷️ Question Taxonomy Distribution", [
        "Symptoms & Signs: Clinical indicators, early warning signs, pain profiles.",
        "Treatment & Management: Pharmacotherapy, surgical options, care plans.",
        "Causes & Risk Factors: Genetic etiology, epidemiology, lifestyle habits.",
        "Diagnosis & Tests: Biopsies, blood screening, radiological imaging.",
        "Prognosis & Outlook: Life expectancy, recovery timelines, survival rates."
    ])

    # =========================================================================
    # SLIDE 4: System Architecture & Workflow Pipeline
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "End-to-End System Architecture")

    steps = [
        ("1. Data Ingestion & Schema Normalizer", [
            "Auto-discovers dataset path in environment",
            "Multi-encoding fallback (UTF-8, Latin-1, CP1252)",
            "Dynamic column mapping (Question, Answer, Focus, Source)",
            "Deduplication & search corpus concatenation"
        ]),
        ("2. TF-IDF & Clinical Vector Space Index", [
            "Sublinear term frequency TF-IDF vectorizer",
            "N-gram feature extraction (unigrams & bigrams)",
            "50,000 maximum clinical vocabulary features",
            "Precomputed cosine similarity matrix"
        ]),
        ("3. Retrieval & Domain Entity Boosting", [
            "Query vector transformation & cosine distance",
            "Pathological & anatomical entity detection",
            "+8% similarity score boosting on target condition",
            "Dynamic filtering by condition, category, and source"
        ]),
        ("4. Clinical Post-Processing & UI", [
            "Clinical Takeaways Extractor (heuristic scoring)",
            "Plain-English medical glossary matching",
            "Streamlit responsive reactive web application",
            "Standalone HTML5 + Tailwind web dashboard"
        ]),
    ]

    for i, (title, points) in enumerate(steps):
        top_pos = Inches(1.8 + i * 1.3)
        add_card(slide4, Inches(0.8), top_pos, Inches(11.7), Inches(1.2), title, points)

    # =========================================================================
    # SLIDE 5: Mathematical Formulation & Retrieval Algorithms
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Information Retrieval & NLP Formulation")

    add_card(slide5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "📐 Vector Space Modeling & TF-IDF", [
        "Sublinear Term Frequency Formulation:\n  tf_sub(t, d) = 1 + log(tf(t, d))  if tf > 0, else 0\n  Prevents long medical paragraphs from artificially skewing relevance.",
        "Inverse Document Frequency (IDF):\n  idf(t) = log((1 + N) / (1 + df(t))) + 1\n  Penalizes ubiquitous medical stopwords (e.g. 'patient', 'disease').",
        "N-gram Windowing (1, 2):\n  Captures compound clinical phrases such as 'blood pressure', 'heart attack', and 'optic nerve'."
    ])

    add_card(slide5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "🎯 Cosine Similarity & Entity Boosting", [
        "Cosine Projection:\n  CosineSim(Q, D) = (Q · D) / (||Q|| × ||D||)\n  Evaluates normalized directional angle between query and document vectors.",
        "Clinical Entity Boosting:\n  Score(d) = CosineSim(Q, D) + α · EntityMatch(Q, FocusArea_d)\n  Empirical boost factor α = 0.08 elevates exact condition matches to top rank.",
        "Confidence Normalization:\n  ConfidencePct = min(100.0, Score(d) × 100)\n  Provides transparent match percentages to end users."
    ])

    # =========================================================================
    # SLIDE 6: Core Features & Medical Intelligence
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Key Features & Clinical Intelligence Modules")

    features = [
        ("🩺 Intelligent Natural Language Search", [
            "Accepts free-form patient queries & symptoms",
            "Instant sub-second response times across 16,000+ records",
            "Confidence badge ranking & attribution tags"
        ]),
        ("📌 Automated Takeaway Extractor", [
            "Heuristic sentence evaluation based on high-signal clinical verbs",
            "Synthesizes 3-4 actionable key bullet points",
            "Saves time for clinicians and patients during consultation"
        ]),
        ("📖 Clinical Jargon Simplifier", [
            "Built-in verified medical terminology lexicon",
            "Matches and defines terms: Dyspnea, Ischemia, Neuropathy, etc.",
            "Translates medical terminology into plain English"
        ]),
        ("🔍 Disease & Condition Explorer", [
            "Comprehensive catalog across 5,126 conditions",
            "Categorized accordion view by diagnosis, treatment, prognosis",
            "Interactive search and filter capabilities"
        ]),
    ]

    coords = [
        (Inches(0.8), Inches(1.8)),
        (Inches(6.8), Inches(1.8)),
        (Inches(0.8), Inches(4.3)),
        (Inches(6.8), Inches(4.3)),
    ]

    for (title, items), (c_left, c_top) in zip(features, coords):
        add_card(slide6, c_left, c_top, Inches(5.7), Inches(2.3), title, items)

    # =========================================================================
    # SLIDE 7: User Interface & Clinical Dashboard Design
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "User Experience & Clinical UI Dashboard")

    add_card(slide7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "💻 Web Application Capabilities", [
        "Streamlit Reactive Frontend: Real-time query execution with zero page reloads, cached dataset loads, and instant state management.",
        "Prompt Pill Suggestions: One-click inquiry buttons for common clinical scenarios (Asthma, Diabetes, Hypertension, Glaucoma, Heart Attack).",
        "Dynamic Sidebar Controls: Interactive sliders for confidence thresholds and result counts, with dropdowns for question types and NIH sources.",
        "Responsive Standalone Webpage: Clean HTML5 + Tailwind CSS dashboard (`index.html`) executable in any browser."
    ])

    add_card(slide7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "🎨 Clinical Design System", [
        "Healthcare Color Palette: Deep teal (#0d9488), navy dark (#0f172a), and clean white surfaces to instill clinical trust.",
        "Color-Coded Badges: Immediate visual classification for confidence score, medical focus area, question category, and source institute.",
        "Structured Result Cards: Direct authoritative answer, collapsible takeaway list, glossary tooltips, and related questions.",
        "Prominent Clinical Disclaimer: HIPAA and educational notices displayed prominently for safety."
    ])

    # =========================================================================
    # SLIDE 8: Dataset Analytics & Insights (EDA)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Dataset Analytics & Exploratory Data Analysis")

    add_card(slide8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "📊 Key Quantitative Findings", [
        "Extensive Coverage: Over 16,359 distinct Q&A pairs covering 5,126 conditions, making it one of the largest verified NIH benchmarks.",
        "Top Documented Conditions: Breast cancer, Type 2 diabetes, Asthma, Glaucoma, Hypertension, and Parkinson's disease.",
        "Substantial Clinical Depth: Average answer length of 132 words, providing comprehensive guidance rather than superficial snippets.",
        "Institutional Distribution: MedlinePlus and Cancer.gov constitute the primary knowledge contributors, backed by CDC guidelines."
    ])

    add_card(slide8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "📥 Analytical Tools & Export Capabilities", [
        "Live Metric Telemetry: Real-time calculation of dataset distributions, total conditions, and word length variance.",
        "Interactive Charting: Native Altair & Streamlit bar graphs displaying frequency of question types and condition coverage.",
        "Interactive Data Table: In-app search and filtering of raw clinical pairs across all attributes.",
        "One-Click CSV Export: Filtered subsets can be downloaded directly from the dashboard for downstream research."
    ])

    # =========================================================================
    # SLIDE 9: Deployment & Production DevOps
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Deployment, CI/CD & Cloud Infrastructure")

    add_card(slide9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "☁️ Cloud Deployment Strategies", [
        "Streamlit Community Cloud: 1-click cloud deployment directly connected to GitHub repository with SSL & global CDN.",
        "Docker Containerization: Pre-configured Dockerfile (`python:3.11-slim`) with healthcheck probes for scalable Kubernetes/ECS deployment.",
        "Render Blueprint: Ready-to-deploy `render.yaml` specification for zero-configuration web service deployment.",
        "GitHub Pages Hosting: Automated GitHub Actions workflow publishing the standalone client web UI (`index.html`)."
    ])

    add_card(slide9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "🔐 Code Quality & Version Control", [
        "Git Version Control: Configured with automated push scripts, clean branch workflows, and standardized `.gitignore` rules.",
        "Automated Test Suite (`test_pipeline.py`): Validates schema normalization, TF-IDF ranking, takeaway extraction, and analytics.",
        "Portable Tooling: Integrated portable MinGit execution for frictionless deployment on restricted environments.",
        "Comprehensive Documentation: Full `README.md` containing architectural walkthroughs and deployment guides."
    ])

    # =========================================================================
    # SLIDE 10: Conclusion & Future Scope
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)

    # Dark background for conclusion
    cbg = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    cbg.fill.solid()
    cbg.fill.fore_color.rgb = PRIMARY_DARK
    cbg.line.fill.background()

    ctb = slide10.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(1.0))
    ctf = ctb.text_frame
    cp1 = ctf.paragraphs[0]
    cp1.text = "CONCLUSION & FUTURE HORIZONS"
    cp1.font.size = Pt(13)
    cp1.font.bold = True
    cp1.font.color.rgb = RGBColor(45, 212, 191)

    cp2 = ctf.add_paragraph()
    cp2.text = "Summary of Achievements & Next Steps"
    cp2.font.size = Pt(28)
    cp2.font.bold = True
    cp2.font.color.rgb = WHITE

    # Left card (Achievements)
    ach_card = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.2), Inches(5.4), Inches(4.3))
    ach_card.fill.solid()
    ach_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    ach_card.line.color.rgb = RGBColor(51, 65, 85)

    atb = slide10.shapes.add_textbox(Inches(1.2), Inches(2.3), Inches(5.0), Inches(4.0))
    atf = atb.text_frame
    atf.word_wrap = True
    p = atf.paragraphs[0]
    p.text = "🏆 Project Achievements"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(94, 234, 212)
    p.space_after = Pt(10)

    achievements = [
        "Engineered end-to-end Healthcare QA system over 16,000+ NIH records.",
        "Built high-speed TF-IDF retrieval index with clinical entity boosting.",
        "Implemented automated takeaway summarizer and jargon simplifier.",
        "Designed responsive clinical web UI (Streamlit & standalone HTML).",
        "Packaged with Docker, GitHub CI/CD, and test suite."
    ]
    for ach in achievements:
        ap = atf.add_paragraph()
        ap.text = f"✓  {ach}"
        ap.font.size = Pt(13)
        ap.font.color.rgb = WHITE
        ap.space_after = Pt(6)

    # Right card (Future Scope)
    fut_card = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.2), Inches(5.5), Inches(4.3))
    fut_card.fill.solid()
    fut_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    fut_card.line.color.rgb = RGBColor(51, 65, 85)

    ftb = slide10.shapes.add_textbox(Inches(7.0), Inches(2.3), Inches(5.1), Inches(4.0))
    ftf = ftb.text_frame
    ftf.word_wrap = True
    p = ftf.paragraphs[0]
    p.text = "🔮 Future Roadmap"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(125, 211, 252)
    p.space_after = Pt(10)

    futures = [
        "Dense Neural Retrieval: Integrate BioBERT and ClinicalBERT dense vector embeddings for deep semantic matching.",
        "Voice Navigation: Add speech-to-text input and audio answer synthesis for accessibility.",
        "Multilingual Translation: Real-time localization for non-English speaking patient populations.",
        "EHR Integration: Interoperability with Fast Healthcare Interoperability Resources (FHIR) standards."
    ]
    for fut in futures:
        fp = ftf.add_paragraph()
        fp.text = f"→  {fut}"
        fp.font.size = Pt(13)
        fp.font.color.rgb = WHITE
        fp.space_after = Pt(6)

    # Save presentation
    output_path = "MedQuAD_AI_Assistant_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation successfully saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    create_deck()
