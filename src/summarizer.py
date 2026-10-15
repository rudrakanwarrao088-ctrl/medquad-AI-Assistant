"""
Medical Text Summarizer & Clinical Jargon Explainer.
Generates key takeaway bullet points, highlights clinical terminology,
and provides patient-friendly definitions for complex medical concepts.
"""

import re
from typing import List, Dict, Tuple


# Clinical Terminology Glossary with Plain-English explanations
MEDICAL_GLOSSARY = {
    "hypertension": "High blood pressure inside arteries, which can strain the heart.",
    "hypotension": "Abnormally low blood pressure.",
    "myocardial infarction": "Heart attack, occurring when blood flow to part of the heart is blocked.",
    "edema": "Swelling caused by excess fluid trapped in bodily tissues.",
    "dyspnea": "Shortness of breath or difficulty breathing comfortably.",
    "arrhythmia": "An irregular or abnormal heartbeat rhythm.",
    "neuropathy": "Nerve damage causing numbness, tingling, or weakness, often in hands and feet.",
    "etiology": "The underlying cause or origin of a disease or medical condition.",
    "prognosis": "The predicted or expected course and outcome of a disease.",
    "asymptomatic": "Showing no symptoms of disease even when infected or affected.",
    "benign": "Not cancerous and not spreading to nearby tissue or other parts of the body.",
    "malignant": "Cancerous cells that can invade nearby tissues and spread.",
    "idiopathic": "A condition or disease that arises spontaneously or from an unknown cause.",
    "prophylaxis": "Preventive treatment or action taken to stave off a disease.",
    "palliative": "Care focused on relieving pain and symptoms rather than curing the underlying condition.",
    "contraindication": "A specific situation or condition where a drug or procedure should not be used.",
    "acute": "Sudden onset of severe symptoms that usually lasts a short time.",
    "chronic": "A long-lasting condition that persists over months or years.",
    "systemic": "Affecting the entire body rather than a single organ or part.",
    "bilateral": "Affecting both the right and left sides of the body.",
    "congenital": "A medical condition present from birth.",
    "metastasis": "The spread of cancer cells from primary site to other body parts.",
    "remission": "A temporary or permanent period where symptoms of disease disappear or decrease.",
    "biopsy": "Removal of a small tissue sample for laboratory examination.",
    "tachycardia": "Abnormally fast resting heart rate (over 100 beats/min).",
    "bradycardia": "Abnormally slow resting heart rate (under 60 beats/min).",
    "erythema": "Redness of the skin caused by increased blood flow in superficial capillaries.",
    "pruritus": "Severe medical term for itching sensation.",
    "syncope": "Temporary loss of consciousness or fainting.",
    "ischemia": "Inadequate blood supply to an organ or part of the body.",
}


def extract_key_takeaways(text: str, max_points: int = 4) -> List[str]:
    """
    Extract the most informative sentences/clauses as bullet points.
    """
    if not text:
        return []

    # Clean text
    clean = re.sub(r"\s+", " ", text).strip()

    # Split into candidate sentences
    sentences = re.split(r"(?<=[.!?])\s+", clean)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    if not sentences:
        return [clean[:160] + "..."] if len(clean) > 160 else [clean]

    # Prioritize sentences with high-value clinical indicators
    scored_sentences = []
    keywords = [
        "symptom", "treatment", "cause", "prevent", "diagnos", "doctor",
        "therapy", "medication", "risk", "test", "common", "important",
        "recommend", "avoid", "help", "patient", "guideline"
    ]

    for sent in sentences:
        score = sum(1 for kw in keywords if kw in sent.lower())
        # Penalize overly long or short sentences
        if 40 <= len(sent) <= 220:
            score += 2
        scored_sentences.append((score, sent))

    scored_sentences.sort(key=lambda x: x[0], reverse=True)
    takeaways = [s for _, s in scored_sentences[:max_points]]

    # If takeaways order is scrambled, preserve chronological order of original text
    takeaways = sorted(takeaways, key=lambda s: clean.find(s))
    return takeaways


def detect_clinical_terms(text: str) -> List[Tuple[str, str]]:
    """
    Scan text for clinical jargon and return matched terms with plain-English definitions.
    """
    text_lower = text.lower()
    matched = []

    for term, definition in MEDICAL_GLOSSARY.items():
        # Match whole word
        pattern = r"\b" + re.escape(term) + r"\b"
        if re.search(pattern, text_lower):
            matched.append((term.title(), definition))

    return matched


def format_medical_disclaimer() -> str:
    """Return standard clinical disclaimer for medical AI systems."""
    return (
        "**Clinical & Educational Disclaimer:** MedQuAD AI is an educational search assistant powered by "
        "verified National Institutes of Health (NIH) data. It is intended for informational reference only "
        "and does not constitute formal medical diagnosis, prognosis, or personalized treatment advice. "
        "Always consult a qualified healthcare professional for urgent medical conditions."
    )
