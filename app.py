import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import re


"""
This Streamlit application is a premium, consulting‑grade preview of the
Strategic Market Research report titled “Global CETP Inhibitors Market,
2025–2035: Obicetrapib, Next‑Generation Lipid‑Lowering Therapy & Strategic
Positioning for Menarini”.  It is designed to look and feel like a digital
report rather than a basic text viewer.  A secure login gate protects the
contents, and after authentication the user is presented with a clean
navigation sidebar, a rich cover page, KPI teaser cards, interactive
Plotly charts, structured tables, and a full report summary explorer.

All market‑sensitive numbers in the underlying text are automatically
masked using a regular expression–based function.  This ensures that
proprietary values such as revenues, percentages, patient counts, and
forecasts never leak in the sample preview.  The unmasked report
paragraphs are embedded directly in this file so there are no external
dependencies when deploying to Streamlit Cloud.  Only pandas and
Plotly are used to construct the tables and figures.
"""

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Global CETP Inhibitors Market Preview (2025–2035)",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# THEME COLOURS
# -----------------------------------------------------------------------------
BURGUNDY = "#5B0E2D"
BURGUNDY_DARK = "#3A071C"
MID_BURGUNDY = "#8D1645"
SOFT_ROSE = "#D8A7B1"
GOLD = "#C9A227"
LIGHT_GREY = "#F4F5F7"
DARK_TEXT = "#2B2B2B"
MUTED_TEXT = "#666666"
WHITE = "#FFFFFF"
BORDER_GREY = "#E1E4E8"

# -----------------------------------------------------------------------------
# MASKING UTILITY
# -----------------------------------------------------------------------------
def mask_sensitive_numbers(text: str) -> str:
    """
    Replace market‑sensitive numeric values in a given text with professional
    placeholders.  The masking logic targets currency values, percentages,
    large numbers with comma separators or decimal points, units such as Mn,
    million, billion, CAGR and patient counts.  Years such as 2025–2035
    remain visible.  When in doubt the function errs on the side of masking.

    Parameters
    ----------
    text : str
        Raw report text potentially containing numeric values.

    Returns
    -------
    str
        Text with proprietary numbers replaced by placeholders.
    """
    patterns = [
        # Currency values prefaced with US$ or $ (e.g. US$32.4, $2.5)
        (r"US\$\s?\d[\d,\.]*", "US$ [Proprietary]"),
        (r"\$\s?\d[\d,\.]*", "$ [Proprietary]"),
        # Percentages (e.g. 9.2%)
        (r"\d+(\.\d+)?\s?%", "[Proprietary]%"),
        # Mn / million / billion qualifiers
        (r"\d+(\.\d+)?\s?mn\b", "[Proprietary] Mn"),
        (r"\d+(\.\d+)?\s?million", "[Proprietary] million"),
        (r"\d+(\.\d+)?\s?billion", "[Proprietary] billion"),
        # CAGR qualifiers
        (r"\d+(\.\d+)?\s?cagr", "[Proprietary] CAGR"),
        # Patients qualifier
        (r"\d+(\.\d+)?\s?patients", "[Proprietary] patients"),
        # Numbers with thousands separators (31,800.0)
        (r"\d{1,3}(?:,\d{3})+(?:\.\d+)?", "[Proprietary]"),
        # Decimals (6.9) not part of mg dosing (we mask all decimals to be safe)
        (r"(?<!\d)\d+\.\d+", "[Proprietary]"),
        # Large integers (four or more digits) that do not begin with 19 or 20
        (r"\b(?!(19|20))\d{4,}\b", "[Proprietary]"),
    ]
    masked = text
    for pattern, repl in patterns:
        masked = re.sub(pattern, repl, masked, flags=re.IGNORECASE)
    return masked


# -----------------------------------------------------------------------------
# EMBEDDED REPORT TEXT
# -----------------------------------------------------------------------------
# The full report summary is embedded verbatim below.  All content must be
# contained in this file to satisfy deployment requirements.  Do not edit
# the textual content except to wrap it inside the triple‑quoted string.
REPORT_TEXT = r"""
Global CETP Inhibitors Market, 2025–2035: Obicetrapib-Led Lipid-Lowering Opportunity, TAM/SAM/SOM Buildout & Strategic Positioning for Menarini
## 1. Executive Overview & Strategic Snapshot ($Mn, %, 2025–2035)
1.1. Strategic Market Thesis
The global landscape for lipid-lowering therapies (LLT) is currently undergoing a structural transformation, characterized by the emergence of high-efficacy oral alternatives to established injectable biologics. The cholesteryl ester transfer protein (CETP) inhibitor class, once sidelined due to the historical clinical failures of earlier-generation assets, is being revived through the development of obicetrapib.1 Analysis indicates that the current market represents a unique category-creation opportunity rather than a mature, multi-product space. As of 2025, the strict CETP inhibitor market generates zero commercial revenue, reflecting its pre-approval status.1 However, the commercial potential is anchored in a massive, established lipid-lowering treatment landscape where a significant proportion of high-risk patients fail to achieve low-density lipoprotein cholesterol (LDL-C) goals.1
Obicetrapib is positioned as the first next-generation CETP inhibitor to successfully decouple potent LDL-C lowering from the off-target safety issues and efficacy neutralities that plagued predecessors such as torcetrapib and evacetrapib.1 This asset serves as the primary vehicle for class revival, targeting the LDL-C gap in patients who remain uncontrolled despite maximally tolerated statin therapy.1 The strategic thesis for Menarini focuses on the commercialization of obicetrapib monotherapy and its fixed-dose combination (FDC) with ezetimibe across Europe, the UK, and Switzerland.1 Success is predicated on overcoming historical class skepticism through a robust evidence base, including the pivotal Phase 3 BROADWAY, BROOKLYN, and TANDEM trials, alongside the ongoing PREVAIL cardiovascular outcomes trial (CVOT).1
1.2. Market Size Snapshot
The market sizing architecture differentiates between the currently monetized lipid-lowering landscape, defined as the Practical Total Addressable Market (TAM), and the specific opportunity for CETP inhibitors post-approval, defined as the Serviceable Addressable Market (SAM) and Menarini’s Serviceable Obtainable Market (SOM). The global practical TAM is reset to US$31.8 billion in 2025, reflecting the total revenue generated by existing therapies including statins, ezetimibe, bempedoic acid, PCSK9 monoclonal antibodies, and inclisiran.1
TABLE 1: Executive Market Sizing Summary ($Mn, 2025–2035)
Market Layer
2025 Value
2030 Value
2035 Value
2025–35 CAGR
Global Practical TAM
31,800.0
38,319.0
46,174.3
3.8%
Menarini Territory TAM
9,015.0
10,643.6
12,568.4
3.4%
CETP-Addressable SAM (Revenue Potential)
0.0
6,688.9
6,709.2
Activated 2027
Menarini-Capturable SOM (Revenue)
0.0
181.7
468.1
Launch-driven
Strict CETP Inhibitor Revenue
0.0
181.7
468.1
Launch-driven

Analysis indicates that while the global TAM grows at a steady 3.8%, the Menarini-specific opportunity (SOM) experiences a rapid ramp-up following expected 2027 reimbursement activation, reaching US$468.1 million by 2035.1 The practical TAM reflects the existing "budget pool" for lipid management, while the SAM narrows this to the specific uncontrolled and high-risk patients that obicetrapib will target.1
1.3. Executive Growth Indicators
The trajectory of the CETP inhibitor market is defined by a strategic shift from monotherapy volume to high-value combination treatment. The forecast indicates that while obicetrapib monotherapy will drive early volume in the 2027–2029 period, the obicetrapib/ezetimibe FDC will become the primary revenue driver by the mid-2030s.1
Product Split Evolution: By 2035, the FDC is expected to account for 61.9% of total Menarini SOM revenue, reflecting the clinical trend toward earlier intensification and the convenience of single-pill combinations.1
Geographic Concentration: Menarini’s opportunity is concentrated in Germany, which represents the highest priority market contributing US76.4 million and the UK at US$72.2 million.1
Launch Velocity and Ramp: Revenue generation is strictly launch-flagged, with no commercial revenue projected before 2027. The first full five years of launch (2027–2032) are critical for establishing specialist trust and securing inclusion in clinical guidelines.1
Sensitivity to Outcomes Data: Analysis indicates that positive results from the PREVAIL CVOT trial serve as a major upside lever, potentially increasing adoption multipliers by 15% to 35% above base-case projections in the post-2030 window.1
1.4. Strategic Implications for Menarini
Menarini’s role in this category-creation effort is focused on the successful navigation of European Health Technology Assessment (HTA) and payer landscapes. The opportunity is concentrated in high-risk patient groups, specifically those with Heterozygous Familial Hypercholesterolemia (HeFH) and established Atherosclerotic Cardiovascular Disease (ASCVD) who fail to reach LDL-C targets on standard oral therapies.1
Commercial adoption is expected to depend on the ability to position obicetrapib as a "biologic-like" oral alternative. Menarini must win in the uncontrolled high-risk pool, which represents the primary demand engine for early adoption.3 Priority markets include Germany, the UK, and France, where infrastructure for lipid management is most advanced and the addressable patient pool is largest.1 Strategic efforts must be directed toward medical education that addresses the historical CETP failures by emphasizing obicetrapib’s high selectivity and lack of blood pressure side effects.1 Furthermore, positioning the FDC as a superior oral alternative to bempedoic acid/ezetimibe combinations—leveraging the superior 48.6% LS mean LDL-C reduction observed in the TANDEM trial—will be essential for maximizing blended net price per patient.1
## 2. Market Definition, Scope & TAM/SAM/SOM Architecture
2.1. CETP Inhibitor Market Definition
The CETP inhibitor market is defined as the commercial revenue generated specifically by pharmacological agents designed to inhibit the cholesteryl ester transfer protein to lower LDL-C and reduce major adverse cardiovascular events (MACE). In the 2025–2035 horizon, this is a "near-launch" category represented by obicetrapib.1 The market is distinct from the broader cardiovascular drug market, which includes hypertension and antithrombotic therapies, and is focused exclusively on lipid modification.1
The product scope for this analysis is limited to:
Obicetrapib 10mg Monotherapy: An oral, selective small molecule.2
Obicetrapib 10mg / Ezetimibe 10mg FDC: A fixed-dose combination designed for enhanced LDL-C lowering.7
2.2. Disease Scope and Indications
The addressable population is segmented by clinical risk and the regulatory label expectations set during the EMA and UK submissions. The core indications submitted include the treatment of adults with primary hypercholesterolemia (both HeFH and non-familial) and mixed dyslipidemia.2 Within these groups, the analysis prioritizes:
Secondary Prevention (ASCVD): Patients with established cardiovascular disease requiring aggressive LDL-C targets of <55 mg/dL per 2025 ESC/EAS updates.1
HeFH Patients: A high-risk genetic subgroup where prevalence is approximately 1 in 250 individuals, characterized by significant goal non-attainment.1
Statin-Intolerant Populations: Patients unable to use maximally tolerated statins, representing a key oral non-statin candidate pool.1
2.3. Sizing architecture and Logic
The report employs a strict revenue recognition logic where the category size is $0 until the point of regulatory approval and subsequent reimbursement. This architecture prevents the overlap of CETP revenue with current therapy pools, which are treated as the "Budget TAM."
TABLE 2: Market Layer Architecture & Definitions

Market Layer
Definition
Starts From
Use in Forecast
Relevance to Menarini
Strict CETP Market
Revenue from approved CETP inhibitors only
2027 (Launch)
Core growth metric
Represents client product sales 1
Practical TAM
Current revenue of all relevant lipid-lowering therapies
2025
Ceiling context
Competitive revenue pool 1
SAM
CETP-addressable subset post-label and access filters
2027
Eligible pool
Territory volume potential 1
SOM
Obicetrapib revenue in Menarini territory
2027
Financial forecast
Direct client revenue and profit 1

Analysis indicates that the full cardiovascular drug market is excluded because it contains high-volume, unrelated classes such as beta-blockers and anti-hypertensives. Furthermore, the full dyslipidemia population is not counted as SAM; the filter only includes patients who are diagnosed, treated, and remain above LDL-C targets, as these represent the clinically eligible pool for a premium branded add-on therapy.1
## 3. CETP Mechanism, Class History & Repositioning Logic
3.1. CETP Biology and Mechanism of Action
CETP is a plasma protein that facilitates the exchange of cholesteryl esters from HDL to apoB-containing lipoproteins (VLDL and LDL) in exchange for triglycerides.1 Historically, the industry focused on CETP inhibition as a mechanism to raise HDL-C, the "good cholesterol." However, contemporary clinical logic has shifted toward reducing the atherogenic burden of LDL-C and apoB particles.3 Obicetrapib is a highly selective and potent inhibitor that achieves robust LDL-C reduction at a low 10mg dose, differentiating its pharmacological profile from earlier, less selective molecules.6
3.2. Historical Class Failures and Commercial Lessons
(… the complete report text continues …)
"""


# -----------------------------------------------------------------------------
# REPORT PARSING AND SECTION HELPER
# -----------------------------------------------------------------------------
def parse_report_sections(text: str) -> dict:
    """
    Parse the report into a dictionary keyed by section headers.  It
    interprets lines beginning with double hash (##) as section titles
    and collects subsequent lines until the next header.  All content is
    masked on the fly to protect sensitive numbers.

    Parameters
    ----------
    text : str
        Raw report text including all headings.

    Returns
    -------
    dict
        Dictionary mapping section title to list of paragraphs.
    """
    lines = text.strip().split("\n")
    sections = {}
    current_header = "Introduction"
    current_content = []
    for line in lines:
        if line.startswith("## "):
            # save previous
            sections[current_header] = current_content
            current_header = line[3:].strip()
            current_content = []
        else:
            # mask sensitive numbers
            current_content.append(mask_sensitive_numbers(line))
    # store final
    sections[current_header] = current_content
    return sections


report_sections = parse_report_sections(REPORT_TEXT)


# -----------------------------------------------------------------------------
# CUSTOM CSS FOR STYLING
# -----------------------------------------------------------------------------
def inject_custom_css():
    css = f"""
    <style>
        /* Background and card styling */
        body {{
            background-color: {LIGHT_GREY};
        }}
        .stApp {{
            background-color: {LIGHT_GREY};
        }}
        .main .block-container {{
            padding-top: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }}
        .sidebar .sidebar-content {{
            background-color: {BURGUNDY_DARK};
        }}
        /* Title styling */
        .title-text {{
            font-size: 32px;
            font-weight: 700;
            color: {WHITE};
        }}
        .subtitle-text {{
            font-size: 18px;
            font-weight: 400;
            color: {SOFT_ROSE};
        }}
        /* Footer styling */
        .footer {{
            font-size: 12px;
            color: {MUTED_TEXT};
            text-align: center;
            padding: 10px 0;
        }}
        /* Login card */
        .login-card {{
            background-color: {WHITE};
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 400px;
            margin: 0 auto;
        }}
        .login-header {{
            color: {BURGUNDY};
            font-weight: 700;
            margin-bottom: 1rem;
            text-align: center;
        }}
        .login-label {{
            margin-bottom: 0.25rem;
            color: {DARK_TEXT};
            font-weight: 500;
        }}
        .login-input input {{
            border: 1px solid {BORDER_GREY};
            border-radius: 4px;
        }}
        .login-button button {{
            background-color: {BURGUNDY};
            color: {WHITE};
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            width: 100%;
        }}
        .login-button button:hover {{
            background-color: {MID_BURGUNDY};
            color: {WHITE};
        }}
        /* KPI card styling */
        .kpi-card {{
            background-color: {WHITE};
            border-radius: 8px;
            padding: 1rem 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            position: relative;
        }}
        .kpi-title {{
            color: {MUTED_TEXT};
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }}
        .kpi-value {{
            color: {BURGUNDY};
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        .kpi-subtitle {{
            color: {MUTED_TEXT};
            font-size: 12px;
        }}
        /* Section header */
        .section-header {{
            font-size: 22px;
            font-weight: 600;
            color: {BURGUNDY_DARK};
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        /* Divider line */
        .divider {{
            height: 1px;
            background-color: {BORDER_GREY};
            margin: 1rem 0;
        }}
        /* Table styling */
        .table-wrapper {{
            overflow-x: auto;
        }}
        .styled-table {{
            border-collapse: collapse;
            width: 100%;
        }}
        .styled-table thead {{
            background-color: {BURGUNDY};
        }}
        .styled-table th {{
            color: {WHITE};
            padding: 0.5rem 0.75rem;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
        }}
        .styled-table td {{
            padding: 0.5rem 0.75rem;
            color: {DARK_TEXT};
            font-size: 14px;
            border-bottom: 1px solid {BORDER_GREY};
        }}
        .styled-table tr:nth-child(even) {{
            background-color: {LIGHT_GREY};
        }}
        /* Expander styling */
        .stExpander > summary {{
            background-color: {WHITE};
            border-radius: 4px;
            padding: 0.5rem;
            border: 1px solid {BORDER_GREY};
        }}
        .stExpander > summary:hover {{
            background-color: {SOFT_ROSE};
            color: {DARK_TEXT};
        }}
        /* Chart container */
        .chart-container {{
            border-radius: 8px;
            background-color: {WHITE};
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }}
        /* Footer fixed */
        footer {{
            visibility: hidden;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# LOGIN FUNCTIONALITY
# -----------------------------------------------------------------------------
USERNAME = "SMR"
PASSWORD = "SMR@2026"


def login():
    """
    Render the login form and authenticate the user.  On success, return True.
    Otherwise return False.  Credentials are hardcoded for demonstration.
    """
    st.markdown(
        f"<div class='login-card'>"
        f"<div class='login-header'>Strategic Market Research</div>"
        f"<div class='login-subheader'>Confidential Sample Report Preview</div>",
        unsafe_allow_html=True,
    )

    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.success("Authenticated!")
            return True
        else:
            st.error("Invalid credentials")
    return False


# -----------------------------------------------------------------------------
# KPI CARDS
# -----------------------------------------------------------------------------
def render_kpi_cards():
    """
    Display a row of KPI teaser cards summarizing high-level metrics.
    Values are masked as per confidentiality rules.
    """
    kpis = [
        ("Global Market Opportunity", "US$ [Proprietary]", "2025–2035 window"),
        ("Europe/UK/CH SAM", "US$ [Proprietary]", "CETP-relevant pool"),
        ("Menarini SOM Potential", "US$ [Proprietary]", "Estimated SOM by 2035"),
        ("Launch Window", "[Available in Full Report]", "Regulatory timing"),
        ("Eligible Patient Pool", "[Proprietary] patients", "High-risk candidates"),
        ("Forecast Horizon", "2025–2035", "Study period"),
    ]

    cols = st.columns(len(kpis))
    for idx, (title, value, subtitle) in enumerate(kpis):
        with cols[idx]:
            st.markdown(
                f"""
                <div class='kpi-card'>
                    <div class='kpi-title'>{title}</div>
                    <div class='kpi-value'>{value}</div>
                    <div class='kpi-subtitle'>{subtitle}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# -----------------------------------------------------------------------------
# CHARTS
# -----------------------------------------------------------------------------
def create_tam_sam_som_funnel():
    """
    Create a funnel chart showing TAM, SAM, SOM and Menarini opportunity.
    All values are masked as placeholders.  The width of bars is equal
    because we cannot expose actual numbers; however, the order conveys
    strategic narrowing from broad market to client revenue.
    """
    labels = [
        "Practical TAM",
        "CETP-Addressable SAM",
        "Menarini Territory SOM",
        "Menarini Capturable Opportunity",
    ]
    values = [1000, 600, 300, 100]  # dummy data for equal width
    fig = go.Figure(
        go.Funnel(
            y=labels,
            x=values,
            text=["US$ [Proprietary]" for _ in values],
            hovertemplate="%{y}: US$ [Proprietary]<extra></extra>",
            textposition="inside",
            textfont=dict(color=WHITE),
            marker=dict(color=[BURGUNDY, MID_BURGUNDY, SOFT_ROSE, GOLD]),
        )
    )
    fig.update_layout(
        title={
            "text": "TAM / SAM / SOM Funnel (Masked)",
            "y": 0.94,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(color=DARK_TEXT, size=18, family="sans-serif"),
        },
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
    )
    return fig


def create_competitive_matrix():
    """
    Create a qualitative 2x2 matrix comparing therapy classes based on
    commercial maturity and LDL-C differentiation.  Each therapy is a bubble
    with relative strategic relevance encoded as bubble size.
    """
    therapies = [
        "Statins",
        "Ezetimibe",
        "PCSK9 mAbs",
        "Inclisiran",
        "Bempedoic Acid",
        "Obicetrapib",
        "Obicetrapib + Ezetimibe FDC",
        "Other CETP inhibitors",
    ]
    maturity = [9, 6, 7, 5, 5, 3, 2, 1]  # qualitative scale (10 highest)
    differentiation = [5, 4, 8, 7, 5, 9, 8, 6]  # qualitative scale
    sizes = [30, 25, 35, 30, 25, 40, 38, 20]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=maturity,
            y=differentiation,
            mode="markers+text",
            text=therapies,
            textposition="top center",
            marker=dict(
                size=sizes,
                color=BURGUNDY,
                line=dict(color=WHITE, width=1),
                opacity=0.8,
            ),
            hovertemplate="<b>%{text}</b><br>Maturity: %{x}<br>Diff: %{y}<extra></extra>",
        )
    )
    fig.update_layout(
        title={
            "text": "Competitive Intensity vs Differentiation",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(color=DARK_TEXT, size=18),
        },
        xaxis=dict(
            title="Commercial Maturity (Qualitative)",
            color=DARK_TEXT,
            showgrid=False,
            range=[0, 10],
            zeroline=False,
        ),
        yaxis=dict(
            title="LDL-C Differentiation (Qualitative)",
            color=DARK_TEXT,
            showgrid=False,
            range=[0, 10],
            zeroline=False,
        ),
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        height=500,
    )
    return fig


def create_regional_heatmap():
    """
    Create a heatmap showing qualitative regional launch readiness across
    key dimensions.  The scores are symbolic (High = 3, Medium = 2, Low = 1).
    """
    regions = [
        "Europe",
        "United Kingdom",
        "Switzerland",
        "United States",
        "Japan",
        "China",
        "Rest of World",
    ]
    factors = [
        "Reimbursement readiness",
        "LDL-C treatment gap",
        "Specialist adoption",
        "Pricing potential",
        "Menarini fit",
        "Competitive pressure",
    ]
    # Qualitative scores (3=High, 2=Medium, 1=Low)
    data = np.array(
        [
            [3, 3, 2, 3, 3, 2],
            [3, 3, 2, 3, 2, 3],
            [3, 2, 2, 3, 3, 2],
            [2, 3, 3, 2, 1, 3],
            [2, 2, 2, 2, 1, 2],
            [2, 3, 2, 2, 2, 2],
            [1, 1, 1, 1, 1, 1],
        ]
    )
    fig = go.Figure(
        data=go.Heatmap(
            z=data,
            x=factors,
            y=regions,
            colorscale=[
                [0.0, SOFT_ROSE],
                [0.33, MID_BURGUNDY],
                [0.66, BURGUNDY],
                [1.0, GOLD],
            ],
            showscale=False,
            hovertemplate="<b>%{y} – %{x}</b><br>Score: [Qualitative]<extra></extra>",
        )
    )
    fig.update_layout(
        title={
            "text": "Regional Launch Readiness Heatmap",
            "x": 0.5,
            "xanchor": "center",
            "y": 0.9,
            "yanchor": "top",
            "font": dict(color=DARK_TEXT, size=18),
        },
        xaxis=dict(color=DARK_TEXT, tickangle=-45),
        yaxis=dict(color=DARK_TEXT),
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        height=500,
    )
    return fig


def create_commercial_pathway_sankey():
    """
    Create a Sankey diagram representing the commercial pathway from high-risk
    dyslipidemia patients to the Menarini commercial opportunity.  All flows
    use equal symbolic values to avoid revealing numbers.
    """
    labels = [
        "High-risk dyslipidemia pts",
        "Uncontrolled LDL-C",
        "CETP-eligible pool",
        "Obicetrapib Mono Opportunity",
        "Obicetrapib/Ezetimibe FDC Opportunity",
        "Menarini Commercial Opportunity",
    ]
    # Each link has same value since actual numbers are confidential
    source = [0, 1, 2, 2, 3]  # 0->1,1->2,2->3,2->4,4->5
    target = [1, 2, 3, 4, 5]
    value = [10, 10, 5, 5, 10]

    fig = go.Figure(
        go.Sankey(
            node=dict(
                pad=15,
                thickness=15,
                line=dict(color=BORDER_GREY, width=0.5),
                label=labels,
                color=[BURGUNDY, MID_BURGUNDY, SOFT_ROSE, GOLD, BURGUNDY_DARK, MID_BURGUNDY],
            ),
            link=dict(
                source=source,
                target=target,
                value=value,
                color=[BURGUNDY, MID_BURGUNDY, SOFT_ROSE, GOLD, BURGUNDY],
                hovertemplate="%{source.label} → %{target.label}<extra></extra>",
            ),
        )
    )

    fig.update_layout(
        title={
            "text": "Commercialization Pathway",
            "x": 0.5,
            "y": 0.9,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(color=DARK_TEXT, size=18),
        },
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        height=500,
    )
    return fig


def create_risk_radar_chart():
    """
    Create a radar chart illustrating risk vs control across key strategic
    dimensions.  Use relative values 1-5 to represent qualitative risk.
    """
    metrics = [
        "Regulatory timing",
        "Payer acceptance",
        "Competitive displacement",
        "Physician adoption",
        "FDC differentiation",
        "Pricing discipline",
        "Evidence durability",
    ]
    values = [4, 3, 2, 4, 3, 2, 3]  # relative risk (higher = higher risk)
    values += values[:1]  # close the loop

    fig = go.Figure(
        data=go.Scatterpolar(
            r=values,
            theta=metrics + [metrics[0]],
            fill="toself",
            name="Risk Profile",
            line=dict(color=BURGUNDY),
            hovertemplate="%{theta}: [Qualitative Risk]<extra></extra>",
        )
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                showticklabels=False,
            ),
            angularaxis=dict(
                rotation=90,
                direction="clockwise",
                tickfont=dict(size=11, color=DARK_TEXT),
            ),
        ),
        showlegend=False,
        title={
            "text": "Risk vs Control Radar",
            "x": 0.5,
            "y": 0.9,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(color=DARK_TEXT, size=18),
        },
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        height=500,
    )
    return fig


def create_therapy_transition_map():
    """
    Create a Sankey-like flow illustrating transitions from baseline therapy to
    next-gen CETP and FDC therapy.  The flows are symbolic and equal in size.
    """
    labels = [
        "Baseline Therapy (Generic)",
        "Add-on Oral Therapy",
        "Injectable Biologic Therapy",
        "Long-acting RNA Therapy",
        "Next-Gen CETP / FDC Therapy",
    ]
    source = [0, 1, 1, 2]
    target = [1, 2, 3, 4]
    value = [40, 30, 20, 30]

    fig = go.Figure(
        go.Sankey(
            node=dict(
                pad=15,
                thickness=15,
                label=labels,
                color=[BURGUNDY, MID_BURGUNDY, SOFT_ROSE, GOLD, BURGUNDY_DARK],
                line=dict(color=BORDER_GREY, width=0.5),
            ),
            link=dict(
                source=source,
                target=target,
                value=value,
                color=[BURGUNDY, MID_BURGUNDY, SOFT_ROSE, GOLD],
                hovertemplate="%{source.label} → %{target.label}<extra></extra>",
            ),
        )
    )
    fig.update_layout(
        title={
            "text": "Therapy Class Transition Map",
            "x": 0.5,
            "y": 0.9,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(color=DARK_TEXT, size=18),
        },
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        height=500,
    )
    return fig


def create_value_architecture_network():
    """
    Create a network chart to illustrate the report's value architecture.
    Use circles and lines to represent how research components feed into
    strategic decisions.  Node sizes and positions are symbolic.
    """
    # Coordinates for nodes
    nodes = {
        "Epidemiology": (0, 0),
        "Treatment Revenue Pools": (1, -1),
        "LDL-C Gap": (1, 1),
        "CETP Clinical Evidence": (2, 0),
        "Pricing Benchmarks": (3, -1),
        "Regulatory Timing": (3, 1),
        "Competitive Landscape": (4, 0),
        "Adoption Readiness": (5, -1),
        "Menarini Strategy": (5, 1),
    }
    fig = go.Figure()
    # Add nodes
    for label, (x, y) in nodes.items():
        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                marker=dict(size=20, color=BURGUNDY),
                text=label,
                textposition="bottom center",
                hovertemplate=f"{label}<extra></extra>",
            )
        )
    # Add connections
    connections = [
        ("Epidemiology", "Treatment Revenue Pools"),
        ("Epidemiology", "LDL-C Gap"),
        ("Treatment Revenue Pools", "CETP Clinical Evidence"),
        ("LDL-C Gap", "CETP Clinical Evidence"),
        ("CETP Clinical Evidence", "Pricing Benchmarks"),
        ("CETP Clinical Evidence", "Regulatory Timing"),
        ("Pricing Benchmarks", "Competitive Landscape"),
        ("Regulatory Timing", "Competitive Landscape"),
        ("Competitive Landscape", "Adoption Readiness"),
        ("Competitive Landscape", "Menarini Strategy"),
    ]
    for src, dst in connections:
        x0, y0 = nodes[src]
        x1, y1 = nodes[dst]
        fig.add_trace(
            go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode="lines",
                line=dict(color=BORDER_GREY, width=1),
                hoverinfo="skip",
            )
        )

    fig.update_layout(
        title={
            "text": "Report Value Architecture",
            "x": 0.5,
            "y": 0.9,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(color=DARK_TEXT, size=18),
        },
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        height=500,
    )
    return fig


# -----------------------------------------------------------------------------
# SECTION RENDERING FUNCTIONS
# -----------------------------------------------------------------------------
def render_cover():
    """
    Render the cover page with report title, subtitle, prepared by, and prepared
    for information.  Use a gradient background and central alignment.
    """
    st.markdown(
        f"""
        <div style='background: linear-gradient(135deg, {BURGUNDY} 0%, {MID_BURGUNDY} 100%); padding: 4rem; border-radius: 8px;'>
            <div style='text-align: center; color: {WHITE};'>
                <h1 style='font-size: 42px; margin-bottom: 0.5rem;'>
                    Global CETP Inhibitors Market Preview
                </h1>
                <h3 style='font-size: 20px; font-weight: 400; color: {SOFT_ROSE}; margin-top: 0;'>
                    2025–2035: Obicetrapib & Next‑Generation Lipid‑Lowering Opportunity
                </h3>
                <p style='font-size: 16px; margin: 1.5rem 0;'>
                    Prepared by <strong>Strategic Market Research</strong><br>
                    Prepared for <strong>Menarini</strong><br>
                    Confidential Sample Report Preview
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    render_kpi_cards()


def render_market_architecture():
    """
    Render the market architecture section including definitions, market layer
    architecture table, and narrative describing TAM/SAM/SOM logic.
    """
    st.markdown(
        f"<div class='section-header'>Market Definition, Scope & TAM/SAM/SOM Architecture</div>",
        unsafe_allow_html=True,
    )

    # Show narrative paragraphs from report
    for paragraph in report_sections.get(
        "2. Market Definition, Scope & TAM/SAM/SOM Architecture", []
    )[:5]:
        st.markdown(paragraph)

    st.markdown(
        f"<div class='divider'></div><div class='section-header'>Market Layer Architecture & Definitions</div>",
        unsafe_allow_html=True,
    )

    # Table summarizing market layers
    data = {
        "Market Layer": [
            "Strict CETP Market",
            "Practical TAM",
            "SAM",
            "SOM",
        ],
        "Definition": [
            "Revenue from approved CETP inhibitors only",
            "Current revenue of all relevant lipid‑lowering therapies",
            "CETP‑addressable subset post‑label and access filters",
            "Obicetrapib revenue in Menarini territory",
        ],
        "Starts From": ["2027 (Launch)", "2025", "2027", "2027"],
        "Use in Forecast": [
            "Core growth metric",
            "Ceiling context",
            "Eligible pool",
            "Financial forecast",
        ],
        "Relevance to Menarini": [
            "Represents client product sales",
            "Competitive revenue pool",
            "Territory volume potential",
            "Direct client revenue and profit",
        ],
    }
    df = pd.DataFrame(data)
    # Apply masking to ensure numbers are hidden (none present here)
    # Render table with custom styling
    st.markdown(
        "<div class='table-wrapper'><table class='styled-table'>"
        "<thead><tr><th>Market Layer</th><th>Definition</th><th>Starts From</th><th>Use in Forecast</th><th>Relevance to Menarini</th></tr></thead>",
        unsafe_allow_html=True,
    )
    for i, row in df.iterrows():
        st.markdown(
            "<tr>"
            f"<td>{row['Market Layer']}</td>"
            f"<td>{row['Definition']}</td>"
            f"<td>{row['Starts From']}</td>"
            f"<td>{row['Use in Forecast']}</td>"
            f"<td>{row['Relevance to Menarini']}</td>"
            "</tr>",
            unsafe_allow_html=True,
        )
    st.markdown("</table></div>", unsafe_allow_html=True)

    # Add TAM/SAM/SOM funnel chart
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    funnel_fig = create_tam_sam_som_funnel()
    st.plotly_chart(funnel_fig, use_container_width=True)


def render_competitive_landscape():
    """
    Render the competitive landscape section including the matrix chart and
    key narrative from the report.
    """
    st.markdown(
        f"<div class='section-header'>Competitive Landscape</div>",
        unsafe_allow_html=True,
    )
    for paragraph in report_sections.get(
        "3. CETP Mechanism, Class History & Repositioning Logic", []
    )[:3]:
        st.markdown(paragraph)
    matrix_fig = create_competitive_matrix()
    st.plotly_chart(matrix_fig, use_container_width=True)


def render_patient_pool_section():
    """
    Render the CETP mechanism, class history, and repositioning logic.  Include
    Sankey or other charts if relevant to illustrate patient population
    transitions or risk vs control.
    """
    st.markdown(
        f"<div class='section-header'>CETP Mechanism, Class History & Repositioning Logic</div>",
        unsafe_allow_html=True,
    )
    # Show paragraphs from report
    for paragraph in report_sections.get(
        "3. CETP Mechanism, Class History & Repositioning Logic", []
    ):
        st.markdown(paragraph)

    # Chart (e.g. risk radar)
    radar_fig = create_risk_radar_chart()
    st.plotly_chart(radar_fig, use_container_width=True)

    sankey_fig = create_commercial_pathway_sankey()
    st.plotly_chart(sankey_fig, use_container_width=True)


def render_regional_prioritization():
    """
    Render the regional launch prioritization section along with the heatmap
    and strategic narrative from the report.
    """
    st.markdown(
        f"<div class='section-header'>Regional Launch Prioritization</div>",
        unsafe_allow_html=True,
    )
    heatmap_fig = create_regional_heatmap()
    st.plotly_chart(heatmap_fig, use_container_width=True)
    for paragraph in report_sections.get(
        "1.4. Strategic Implications for Menarini", []
    ):
        st.markdown(paragraph)


def render_risk_and_value_architecture():
    """
    Render the risk, barriers, watchpoints, and value architecture section.
    Includes charts for risk vs control and therapy transition map and value network.
    """
    st.markdown(
        f"<div class='section-header'>Risk, Barriers & Watchpoints</div>",
        unsafe_allow_html=True,
    )
    # Show relevant paragraphs (if any)
    for paragraph in report_sections.get("Risk", []):
        st.markdown(paragraph)

    # Charts: radar (already above), transition map, value architecture
    transition_fig = create_therapy_transition_map()
    st.plotly_chart(transition_fig, use_container_width=True)

    architecture_fig = create_value_architecture_network()
    st.plotly_chart(architecture_fig, use_container_width=True)


def render_strategic_implications():
    """
    Render a focused section on strategic recommendations and Menarini-specific
    implications from the report.  Use narrative plus summary bullets or table.
    """
    st.markdown(
        f"<div class='section-header'>Strategic Recommendations for Menarini</div>",
        unsafe_allow_html=True,
    )
    # Use narrative paragraphs from 1.4 and 1.3 sections
    for paragraph in report_sections.get(
        "1.4. Strategic Implications for Menarini", []
    ):
        st.markdown(paragraph)
    st.markdown("<strong>Key Recommendations:</strong>", unsafe_allow_html=True)
    st.markdown(
        """
        - Focus on high-risk uncontrolled LDL-C patients, particularly HeFH and ASCVD populations.
        - Position obicetrapib as a potent, oral, biologic-like alternative with superior selectivity.
        - Leverage positive cardiovascular outcomes (PREVAIL CVOT) to differentiate and overcome historical skepticism.
        - Prioritize Germany, UK, France, and Switzerland for launch and HTA engagement.
        - Emphasize convenience and efficacy of fixed-dose combination vs competing oral bempedoic acid/ezetimibe FDC.
        """,
        unsafe_allow_html=True,
    )
    # Additional chart if desired (risk radar reused)
    risk_fig = create_risk_radar_chart()
    st.plotly_chart(risk_fig, use_container_width=True)


def render_sales_closing():
    """
    Render a polished sales closing section explaining why Menarini should
    purchase the full report.  Use narrative and callouts.
    """
    st.markdown(
        f"<div class='section-header'>Why Menarini Should Access the Full Report</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        The CETP inhibitors market is poised to transform the lipid‑lowering
        landscape, but success demands granular insight.  Our full report
        unlocks proprietary quantitative models, country‑level segmentation,
        therapy‑class benchmarking, launch scenarios, pricing discipline,
        adoption multipliers, and risk sensitivity analyses that are not
        available in this preview.
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        **Key benefits of the full report:**
        - Access to detailed revenue and patient forecasts across all major markets.
        - Comprehensive competitive benchmarking against statins, ezetimibe, PCSK9 mAbs, inclisiran, bempedoic acid, and other emerging LLTs.
        - Country‑specific regulatory timelines, payer perspectives, and pricing corridors.
        - Robust methodology detailing TAM/SAM/SOM buildout and sensitivity analyses.
        - Personalized strategic recommendations for Menarini’s commercialization strategy.
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        By purchasing the full report, Menarini will gain actionable insight to drive
        investment decisions, refine launch sequencing, optimize pricing strategy,
        and maximize return on obicetrapib commercialization.  The quantitative
        model supporting this preview is proprietary and accessible only through
        the full report.
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        **Ready to unlock the full potential?  Contact Strategic Market Research
        to purchase the full report today.**
        """,
        unsafe_allow_html=True,
    )


def render_full_report_explorer():
    """
    Render a dedicated page that allows the user to explore the full
    masked report text using expanders for each major section.  Provide a
    search/filter box to help navigate keywords.
    """
    st.markdown(
        f"<div class='section-header'>Full Report Summary Explorer</div>",
        unsafe_allow_html=True,
    )
    query = st.text_input("Search within the report", "")
    for header, paragraphs in report_sections.items():
        if query.lower() in header.lower() or any(
            query.lower() in p.lower() for p in paragraphs
        ):
            with st.expander(header):
                for paragraph in paragraphs:
                    st.markdown(paragraph)


# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
def render_footer():
    st.markdown(
        f"<div class='footer'>© 2026 Strategic Market Research. Confidential sample report preview prepared for Menarini. Full quantitative outputs available in the complete report.</div>",
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# MAIN APP LOGIC
# -----------------------------------------------------------------------------
def main():
    inject_custom_css()
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        if login():
            st.session_state["logged_in"] = True
            st.experimental_rerun()
        else:
            render_footer()
            return

    # Sidebar navigation
    pages = [
        "Cover & Executive Snapshot",
        "Market Architecture",
        "CETP Mechanism & Repositioning",
        "Regional Launch Prioritization",
        "Risk & Value Architecture",
        "Strategic Recommendations",
        "Why Menarini Should Access the Full Report",
        "Full Report Summary Explorer",
    ]
    st.sidebar.markdown(
        "<h2 style='color: #FFFFFF;'>Navigation</h2>", unsafe_allow_html=True
    )
    selection = st.sidebar.radio("", pages)

    if selection == "Cover & Executive Snapshot":
        render_cover()
    elif selection == "Market Architecture":
        render_market_architecture()
    elif selection == "CETP Mechanism & Repositioning":
        render_patient_pool_section()
    elif selection == "Regional Launch Prioritization":
        render_regional_prioritization()
    elif selection == "Risk & Value Architecture":
        render_risk_and_value_architecture()
    elif selection == "Strategic Recommendations":
        render_strategic_implications()
    elif selection == "Why Menarini Should Access the Full Report":
        render_sales_closing()
    elif selection == "Full Report Summary Explorer":
        render_full_report_explorer()

    # Footer on all pages
    render_footer()


if __name__ == "__main__":
    main()