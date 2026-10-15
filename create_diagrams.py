"""
Generate high-resolution clinical diagrams for MedQuAD AI presentation using Matplotlib.
Creates:
1. diagram_architecture.png - Multi-tier system pipeline flowchart
2. diagram_retrieval.png - Mathematical vector retrieval & entity boosting
3. diagram_taxonomy.png - Question categories and NIH source distributions
4. diagram_devops.png - Cloud deployment and containerization flow
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Styling configuration
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.family"] = "sans-serif"

TEAL = "#0d9488"
NAVY = "#0f172a"
CYAN = "#0284c7"
SLATE = "#334155"
LIGHT_BG = "#f8fafc"
BORDER_COL = "#cbd5e1"
GREEN = "#059669"
PURPLE = "#7c3aed"
AMBER = "#d97706"


def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_facecolor(LIGHT_BG)
    fig.patch.set_facecolor(LIGHT_BG)

    # Coordinates and box definitions
    boxes = [
        {"x": 0.05, "y": 0.55, "w": 0.22, "h": 0.32, "title": "User Query / Symptom", "desc": "Free-text input\ne.g., 'asthma treatments'", "col": CYAN},
        {"x": 0.38, "y": 0.55, "w": 0.24, "h": 0.32, "title": "TF-IDF Vector Space", "desc": "Sublinear TF + N-grams\n50,000 Vocab Features", "col": TEAL},
        {"x": 0.72, "y": 0.55, "w": 0.24, "h": 0.32, "title": "Hybrid Match Engine", "desc": "Cosine Sim + Entity Boost\n(+8% Condition Match)", "col": PURPLE},
        {"x": 0.20, "y": 0.08, "w": 0.26, "h": 0.32, "title": "NIH MedQuAD DB", "desc": "16,359 Curated Q&As\n5,126 Health Conditions", "col": NAVY},
        {"x": 0.58, "y": 0.08, "w": 0.34, "h": 0.32, "title": "Clinical Output & UI", "desc": "Takeaways + Jargon Glossary\nStreamlit & Web Dashboard", "col": GREEN},
    ]

    for b in boxes:
        rect = patches.FancyBboxPatch(
            (b["x"], b["y"]), b["w"], b["h"],
            boxstyle="round,pad=0.02,rounding_size=0.03",
            facecolor="white", edgecolor=b["col"], linewidth=2.5, zorder=2
        )
        ax.add_patch(rect)
        # Header strip inside box
        header_rect = patches.FancyBboxPatch(
            (b["x"], b["y"] + b["h"] - 0.09), b["w"], 0.09,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            facecolor=b["col"], edgecolor="none", zorder=3
        )
        ax.add_patch(header_rect)
        ax.text(b["x"] + b["w"]/2, b["y"] + b["h"] - 0.045, b["title"],
                ha="center", va="center", color="white", fontsize=10, weight="bold", zorder=4)
        ax.text(b["x"] + b["w"]/2, b["y"] + (b["h"] - 0.09)/2 + 0.01, b["desc"],
                ha="center", va="center", color=SLATE, fontsize=9, zorder=4)

    # Connecting arrows
    arrow_props = dict(facecolor=TEAL, edgecolor=TEAL, width=2, headwidth=8, headlength=8)
    ax.annotate("", xy=(0.38, 0.71), xytext=(0.27, 0.71), arrowprops=arrow_props)
    ax.annotate("", xy=(0.72, 0.71), xytext=(0.62, 0.71), arrowprops=arrow_props)
    ax.annotate("", xy=(0.58, 0.24), xytext=(0.46, 0.24), arrowprops=arrow_props)
    # Downward arrow from Hybrid Match to Output
    ax.annotate("", xy=(0.75, 0.40), xytext=(0.84, 0.55),
                arrowprops=dict(facecolor=GREEN, edgecolor=GREEN, width=2, headwidth=8, headlength=8))
    # Upward arrow from DB to TF-IDF
    ax.annotate("", xy=(0.48, 0.55), xytext=(0.35, 0.40),
                arrowprops=dict(facecolor=NAVY, edgecolor=NAVY, width=2, headwidth=8, headlength=8))

    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 0.95)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("diagram_architecture.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("[OK] Created diagram_architecture.png")


def create_retrieval_diagram():
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)
    ax.set_facecolor(LIGHT_BG)
    fig.patch.set_facecolor(LIGHT_BG)

    # 4 Pipeline Stages
    stages = [
        {"x": 0.04, "w": 0.20, "col": CYAN, "title": "1. Query Tokenization", "bullets": ["Clean & lowercase", "Extract key tokens", "Stopword filtering"]},
        {"x": 0.28, "w": 0.21, "col": TEAL, "title": "2. Vector Projection", "bullets": ["Sublinear TF weight", "N-gram windowing", "Unit length normalization"]},
        {"x": 0.53, "w": 0.21, "col": PURPLE, "title": "3. Cosine Projection", "bullets": ["Sparse dot product", "Directional angle cos(θ)", "Fast candidate ranking"]},
        {"x": 0.78, "w": 0.20, "col": GREEN, "title": "4. Clinical Boosting", "bullets": ["+8% Target disease", "Threshold cutoff", "Confidence scoring"]},
    ]

    for s in stages:
        rect = patches.FancyBboxPatch(
            (s["x"], 0.15), s["w"], 0.72,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            facecolor="white", edgecolor=s["col"], linewidth=2.5, zorder=2
        )
        ax.add_patch(rect)
        hdr = patches.FancyBboxPatch(
            (s["x"], 0.72), s["w"], 0.15,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            facecolor=s["col"], edgecolor="none", zorder=3
        )
        ax.add_patch(hdr)
        ax.text(s["x"] + s["w"]/2, 0.795, s["title"], ha="center", va="center", color="white", fontsize=9.5, weight="bold", zorder=4)
        for idx, bullet in enumerate(s["bullets"]):
            ax.text(s["x"] + 0.02, 0.58 - idx * 0.14, f"• {bullet}", ha="left", va="center", color=SLATE, fontsize=8.5, zorder=4)

    # Connectors
    for x_arr in [0.24, 0.49, 0.74]:
        ax.annotate("", xy=(x_arr + 0.04, 0.51), xytext=(x_arr, 0.51),
                    arrowprops=dict(facecolor=TEAL, edgecolor=TEAL, width=2, headwidth=7, headlength=7))

    ax.set_xlim(0, 1.02)
    ax.set_ylim(0.05, 0.95)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("diagram_retrieval.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("[OK] Created diagram_retrieval.png")


def create_dataset_taxonomy_diagram():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300)
    fig.patch.set_facecolor(LIGHT_BG)

    # 1. Question Type Pie/Donut Chart
    labels = ["Overview & Info", "General Inquiry", "Symptoms & Signs", "Treatment", "Causes & Risks"]
    sizes = [42, 28, 14, 11, 5]
    colors = [TEAL, CYAN, GREEN, AMBER, PURPLE]
    wedges, texts, autotexts = ax1.pie(
        sizes, labels=labels, autopct="%1.0f%%", startangle=140,
        colors=colors, wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
        textprops=dict(color=NAVY, fontsize=8)
    )
    for at in autotexts:
        at.set_color("white")
        at.set_weight("bold")
        at.set_fontsize(8)
    ax1.set_title("Question Categories Breakdown", fontsize=11, weight="bold", color=NAVY, pad=12)

    # 2. Top Conditions Bar Chart
    conditions = ["Breast Cancer", "Glaucoma", "Diabetes", "Asthma", "Hypertension", "Parkinson's"]
    counts = [184, 156, 142, 128, 115, 98]
    y_pos = np.arange(len(conditions))
    ax2.set_facecolor("white")
    bars = ax2.barh(y_pos, counts, color=TEAL, edgecolor="none", height=0.6)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(conditions, fontsize=9, color=NAVY)
    ax2.invert_yaxis()
    ax2.set_xlabel("Verified NIH Q&A Pairs", fontsize=9, color=SLATE)
    ax2.set_title("Top Documented Conditions", fontsize=11, weight="bold", color=NAVY, pad=12)
    for bar in bars:
        ax2.text(bar.get_width() + 4, bar.get_y() + bar.get_height()/2, f"{int(bar.get_width())}",
                 va="center", ha="left", fontsize=8.5, color=SLATE, weight="bold")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color(BORDER_COL)
    ax2.spines["bottom"].set_color(BORDER_COL)

    plt.tight_layout()
    plt.savefig("diagram_taxonomy.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("[OK] Created diagram_taxonomy.png")


def create_devops_diagram():
    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=300)
    ax.set_facecolor(LIGHT_BG)
    fig.patch.set_facecolor(LIGHT_BG)

    # Nodes for DevOps deployment
    nodes = [
        {"x": 0.05, "y": 0.50, "w": 0.22, "h": 0.35, "title": "GitHub Repository", "desc": "Version Control\nCI/CD Actions\n`main` Branch", "col": NAVY},
        {"x": 0.40, "y": 0.55, "w": 0.25, "h": 0.35, "title": "Streamlit Cloud", "desc": "1-Click Public SaaS\nFree Global CDN\nAutomated SSL", "col": TEAL},
        {"x": 0.40, "y": 0.08, "w": 0.25, "h": 0.35, "title": "Docker Container", "desc": "Python 3.11-slim\nHealth Check Probes\nContainer Registry", "col": CYAN},
        {"x": 0.74, "y": 0.32, "w": 0.23, "h": 0.35, "title": "End-User Access", "desc": "Clinicians & Patients\nWeb, Mobile, Desktop\nOffline Fallback", "col": GREEN},
    ]

    for n in nodes:
        rect = patches.FancyBboxPatch(
            (n["x"], n["y"]), n["w"], n["h"],
            boxstyle="round,pad=0.02,rounding_size=0.03",
            facecolor="white", edgecolor=n["col"], linewidth=2.5, zorder=2
        )
        ax.add_patch(rect)
        hdr = patches.FancyBboxPatch(
            (n["x"], n["y"] + n["h"] - 0.09), n["w"], 0.09,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            facecolor=n["col"], edgecolor="none", zorder=3
        )
        ax.add_patch(hdr)
        ax.text(n["x"] + n["w"]/2, n["y"] + n["h"] - 0.045, n["title"], ha="center", va="center", color="white", fontsize=9.5, weight="bold", zorder=4)
        ax.text(n["x"] + n["w"]/2, n["y"] + (n["h"] - 0.09)/2 + 0.01, n["desc"], ha="center", va="center", color=SLATE, fontsize=8.5, zorder=4)

    # Connecting arrows
    arrow_props1 = dict(facecolor=TEAL, edgecolor=TEAL, width=2, headwidth=8, headlength=8)
    arrow_props2 = dict(facecolor=CYAN, edgecolor=CYAN, width=2, headwidth=8, headlength=8)
    arrow_props3 = dict(facecolor=GREEN, edgecolor=GREEN, width=2, headwidth=8, headlength=8)

    ax.annotate("", xy=(0.40, 0.72), xytext=(0.27, 0.72), arrowprops=arrow_props1)
    ax.annotate("", xy=(0.40, 0.25), xytext=(0.27, 0.55), arrowprops=arrow_props2)
    ax.annotate("", xy=(0.74, 0.55), xytext=(0.65, 0.72), arrowprops=arrow_props3)
    ax.annotate("", xy=(0.74, 0.45), xytext=(0.65, 0.25), arrowprops=arrow_props3)

    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 0.95)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("diagram_devops.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("[OK] Created diagram_devops.png")


if __name__ == "__main__":
    create_architecture_diagram()
    create_retrieval_diagram()
    create_dataset_taxonomy_diagram()
    create_devops_diagram()
    print("All 4 diagrams generated successfully!")
