"""
PowerPoint Generator for MedQuAD AI Medical Assistant Presentation.
Generates a widescreen, 10-slide deck with embedded diagrams and clinical styling.
Author: Rashi Kanwar Rao
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clinical Color Palette
    PRIMARY = RGBColor(13, 118, 110)      # Deep Teal
    PRIMARY_DARK = RGBColor(15, 23, 42)   # Navy Dark
    ACCENT_BLUE = RGBColor(2, 132, 199)   # Ocean Cyan
    TEXT_MAIN = RGBColor(30, 41, 59)      # Slate Dark
    BG_CARD = RGBColor(248, 250, 252)     # Off-white Card
    BORDER_CARD = RGBColor(226, 232, 240) # Slate Border
    WHITE = RGBColor(255, 255, 255)
    TEAL_LIGHT = RGBColor(240, 253, 250)

    def add_header(slide, title_text, category_text="HEALTHCARE AI & NLP CAPSTONE"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE

        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.5), Inches(0.7))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = PRIMARY_DARK

    def add_card(slide, left, top, width, height, title, items):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = BG_CARD
        shape.line.color.rgb = BORDER_CARD
        shape.line.width = Pt(1.2)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = f"{title}"
        p0.font.size = Pt(15)
        p0.font.bold = True
        p0.font.color.rgb = PRIMARY
        p0.space_after = Pt(8)

        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.size = Pt(11.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = PRIMARY_DARK
    bg.line.fill.background()

    title_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(2.2))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "EVIDENCE-BASED HEALTHCARE AI SYSTEM"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = RGBColor(45, 212, 191)
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
    mp3.text = "16,359+ Clinical Q&A Pairs | 5,126 Conditions"
    mp3.font.size = Pt(12)
    mp3.font.color.rgb = RGBColor(203, 213, 225)

    # =========================================================================
    # SLIDE 2: Problem Statement
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Project Motivation & Clinical Need")

    add_card(slide2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "⚠️ The Healthcare Information Challenge", [
        "Unreliable Public Web Queries: Patients seeking medical advice online are frequently misled by unverified or sensationalized medical advice.",
        "Clinical Density & Jargon: Authoritative medical literature uses dense terminology (dyspnea, idiopathic, ischemia) that creates cognitive barriers.",
        "Diagnostic Anxiety: Misinterpreted health information increases patient anxiety and delays timely consultation with licensed professionals.",
        "Lack of Source Attribution: Most online aggregators do not cite official clinical origins or specific institutional research."
    ])

    add_card(slide2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "💡 The MedQuAD AI Solution", [
        "NIH-Verified Ground Truth: Grounded strictly in peer-reviewed clinical knowledge from 12 National Institutes of Health (NIH) entities.",
        "Hybrid Semantic Retrieval: Combines sublinear TF-IDF, n-gram vector matching, and clinical entity boosting for precision answers.",
        "Patient-Centered NLP Layer: Automatically distills answers into actionable bulleted takeaways and plain-English medical glossaries.",
        "Responsible Medical Governance: Transparent similarity confidence scores and prominent clinical safety notices."
    ])

    # =========================================================================
    # SLIDE 3: MedQuAD Dataset & Diagram
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "MedQuAD Dataset & Institutional Taxonomy")

    add_card(slide3, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.2), "🏛️ Clinical Benchmark Overview", [
        "Scale: 16,359+ curated Q&A pairs covering 5,126 unique diseases.",
        "Provenance: MedlinePlus, Cancer.gov, CDC, NIDDK, NINDS, GARD, NHLBI.",
        "Comprehensive Depth: 132 words average clinical response length.",
        "Standardized Typology: Symptoms, Treatments, Causes, Diagnosis, Prognosis."
    ])

    # Insert Taxonomy Diagram
    if os.path.exists("diagram_taxonomy.png"):
        slide3.shapes.add_picture("diagram_taxonomy.png", Inches(5.8), Inches(1.6), width=Inches(6.8), height=Inches(5.2))

    # =========================================================================
    # SLIDE 4: End-to-End System Architecture Pipeline Diagram
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "End-to-End System Architecture Flowchart")

    add_card(slide4, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.2), "⚙️ Multi-Tier Architecture", [
        "1. Ingestion: Auto-path detection, UTF-8/Latin-1 fallbacks, deduplication.",
        "2. TF-IDF Index: Sublinear term weighting with 50,000 medical features.",
        "3. Hybrid Match: Cosine angle projection with +8% pathology boosting.",
        "4. Output Synthesis: Takeaways extractor, glossary, Streamlit reactive UI."
    ])

    # Insert Architecture Diagram
    if os.path.exists("diagram_architecture.png"):
        slide4.shapes.add_picture("diagram_architecture.png", Inches(5.8), Inches(1.6), width=Inches(6.8), height=Inches(5.2))

    # =========================================================================
    # SLIDE 5: Mathematical Retrieval & Boosting Flowchart
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Information Retrieval & Mathematical Flowchart")

    add_card(slide5, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.2), "📐 Algorithmic Formulation", [
        "Sublinear TF: tf_sub = 1 + log(tf). Prevents paragraph length distortion.",
        "IDF Scoring: Penalizes frequent non-specific stopwords.",
        "N-grams (1, 2): Captures clinical bigrams like 'heart attack', 'blood pressure'.",
        "Clinical Boost: Exact matches on focus conditions gain +8% priority boost."
    ])

    # Insert Retrieval Diagram
    if os.path.exists("diagram_retrieval.png"):
        slide5.shapes.add_picture("diagram_retrieval.png", Inches(5.8), Inches(1.6), width=Inches(6.8), height=Inches(5.2))

    # =========================================================================
    # SLIDE 6: Core Features
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Key Features & Medical Intelligence Modules")

    features = [
        ("🩺 Intelligent Natural Language Search", [
            "Accepts free-form patient queries & symptoms",
            "Sub-second response times across 16,000+ records",
            "Color-coded confidence percentages and badges"
        ]),
        ("📌 Automated Takeaway Extractor", [
            "Heuristic sentence evaluation based on clinical verbs",
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
        (Inches(0.8), Inches(1.6)),
        (Inches(6.8), Inches(1.6)),
        (Inches(0.8), Inches(4.3)),
        (Inches(6.8), Inches(4.3)),
    ]
    for (title, items), (c_left, c_top) in zip(features, coords):
        add_card(slide6, c_left, c_top, Inches(5.7), Inches(2.5), title, items)

    # =========================================================================
    # SLIDE 7: UI & Dashboard Design
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "User Experience & Clinical UI Dashboard")

    add_card(slide7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "💻 Web Application Capabilities", [
        "Streamlit Reactive Frontend: Real-time query execution with zero page reloads, cached dataset loads, and instant state management.",
        "Prompt Pill Suggestions: One-click inquiry buttons for common clinical scenarios (Asthma, Diabetes, Hypertension, Glaucoma, Heart Attack).",
        "Dynamic Sidebar Controls: Interactive sliders for confidence thresholds and result counts, with dropdowns for question types and NIH sources.",
        "Responsive Standalone Webpage: Clean HTML5 + Tailwind CSS dashboard (`index.html`) executable in any browser."
    ])

    add_card(slide7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "🎨 Clinical Design System", [
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

    add_card(slide8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "📊 Quantitative Findings", [
        "Extensive Coverage: Over 16,359 distinct Q&A pairs covering 5,126 conditions, making it one of the largest verified NIH benchmarks.",
        "Top Documented Conditions: Breast cancer, Type 2 diabetes, Asthma, Glaucoma, Hypertension, and Parkinson's disease.",
        "Substantial Clinical Depth: Average answer length of 132 words, providing comprehensive guidance rather than superficial snippets.",
        "Institutional Distribution: MedlinePlus and Cancer.gov constitute the primary knowledge contributors, backed by CDC guidelines."
    ])

    add_card(slide8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "📥 Analytical Tools & Export", [
        "Live Metric Telemetry: Real-time calculation of dataset distributions, total conditions, and word length variance.",
        "Interactive Charting: Native Altair & Streamlit bar graphs displaying frequency of question types and condition coverage.",
        "Interactive Data Table: In-app search and filtering of raw clinical pairs across all attributes.",
        "One-Click CSV Export: Filtered subsets can be downloaded directly from the dashboard for downstream research."
    ])

    # =========================================================================
    # SLIDE 9: DevOps & Cloud Infrastructure Diagram
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Cloud Infrastructure & DevOps Flowchart")

    add_card(slide9, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.2), "☁️ Production Strategies", [
        "GitHub CI/CD: Automated version control with branch protections and testing.",
        "Streamlit Community Cloud: 1-Click continuous deployment connected to GitHub.",
        "Docker Containerization: Python 3.11-slim container with health check probes.",
        "Test Suite: 100% passing integration tests (`test_pipeline.py`)."
    ])

    # Insert DevOps Diagram
    if os.path.exists("diagram_devops.png"):
        slide9.shapes.add_picture("diagram_devops.png", Inches(5.8), Inches(1.6), width=Inches(6.8), height=Inches(5.2))

    # =========================================================================
    # SLIDE 10: Conclusion & Roadmap
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
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

    output_path = "MedQuAD_AI_Assistant_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation successfully saved with diagrams to: {output_path}")
    return output_path


if __name__ == "__main__":
    create_deck()
