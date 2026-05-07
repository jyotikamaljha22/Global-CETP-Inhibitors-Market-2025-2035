import re
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="SMR | CETP Inhibitors Market Preview",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# ACCESS CREDENTIALS
# =========================================================
USERNAME = "SMR"
PASSWORD = "SMR@2026"


# =========================================================
# THEME CONSTANTS
# =========================================================
DEEP_BURGUNDY = "#5B0E2D"
DARK_WINE = "#3A071C"
MID_BURGUNDY = "#8D1645"
SOFT_ROSE = "#D8A7B1"
GOLD = "#C9A227"
LIGHT_GREY = "#F4F5F7"
WHITE = "#FFFFFF"
DARK_TEXT = "#2B2B2B"
MUTED_TEXT = "#666666"
BORDER_GREY = "#E1E4E8"


# =========================================================
# MASKING FUNCTION
# =========================================================
def mask_sensitive_numbers(text: str) -> str:
    """
    Masks market-sensitive numeric values while preserving important year references
    such as 2025, 2030, 2035, Phase 2, Phase 3, and 10mg.
    """

    if not text:
        return text

    protected_tokens = {
        "2025": "__YEAR_2025__",
        "2026": "__YEAR_2026__",
        "2027": "__YEAR_2027__",
        "2028": "__YEAR_2028__",
        "2029": "__YEAR_2029__",
        "2030": "__YEAR_2030__",
        "2031": "__YEAR_2031__",
        "2032": "__YEAR_2032__",
        "2033": "__YEAR_2033__",
        "2034": "__YEAR_2034__",
        "2035": "__YEAR_2035__",
        "Phase 2": "__PHASE_2__",
        "Phase 3": "__PHASE_3__",
        "10mg": "__TEN_MG__",
        "10 mg": "__TEN_MG_SPACE__",
    }

    for original, token in protected_tokens.items():
        text = text.replace(original, token)

    # Currency / revenue / market values
    text = re.sub(r"(US\$|USD|\$)\s?\d[\d,]*(?:\.\d+)?\s?(billion|million|Mn|M|B|bn|m)?", "US$ [Proprietary]", text, flags=re.I)
    text = re.sub(r"\d[\d,]*(?:\.\d+)?\s?(billion|million|Mn|M|B|bn)\b", "[Proprietary]", text, flags=re.I)

    # Percentages and CAGRs
    text = re.sub(r"\d+(?:\.\d+)?\s?%", "[Proprietary]%", text)
    text = re.sub(r"\bCAGR\s+of\s+\[Proprietary\]%", "CAGR of [Proprietary]%", text, flags=re.I)

    # Patient counts / pools
    text = re.sub(r"\d+(?:\.\d+)?\s?(patients|patient pool|pts|individuals)", "[Proprietary] patients", text, flags=re.I)

    # Ratios / prevalence formats
    text = re.sub(r"\b1\s+in\s+\d+\b", "[Proprietary] prevalence", text, flags=re.I)

    # Broad standalone decimals likely to be market data
    text = re.sub(r"\b\d{1,3},\d{3}(?:\.\d+)?\b", "[Proprietary]", text)
    text = re.sub(r"\b\d+\.\d+\b", "[Proprietary]", text)

    for original, token in protected_tokens.items():
        text = text.replace(token, original)

    return text


# =========================================================
# EMBEDDED REPORT CONTENT — SECTION 1 ONLY FOR THIS BUILD
# All sensitive values are already masked for GitHub safety.
# =========================================================
REPORT_SECTIONS = {
    "Cover & Executive Snapshot": """
## 1. Executive Overview & Strategic Snapshot ($Mn, %, 2025–2035)

### 1.1. Strategic Market Thesis

The global landscape for lipid-lowering therapies (LLT) is currently undergoing a structural transformation, characterized by the emergence of high-efficacy oral alternatives to established injectable biologics. The cholesteryl ester transfer protein (CETP) inhibitor class, once sidelined due to the historical clinical failures of earlier-generation assets, is being revived through the development of obicetrapib. Analysis indicates that the current market represents a unique category-creation opportunity rather than a mature, multi-product space.

As of 2025, the strict CETP inhibitor market generates zero commercial revenue, reflecting its pre-approval status. However, the commercial potential is anchored in a massive, established lipid-lowering treatment landscape where a significant proportion of high-risk patients fail to achieve low-density lipoprotein cholesterol (LDL-C) goals.

Obicetrapib is positioned as the first next-generation CETP inhibitor to successfully decouple potent LDL-C lowering from the off-target safety issues and efficacy neutralities that plagued predecessors such as torcetrapib and evacetrapib. This asset serves as the primary vehicle for class revival, targeting the LDL-C gap in patients who remain uncontrolled despite maximally tolerated statin therapy.

The strategic thesis for Menarini focuses on the commercialization of obicetrapib monotherapy and its fixed-dose combination (FDC) with ezetimibe across Europe, the UK, and Switzerland. Success is predicated on overcoming historical class skepticism through a robust evidence base, including the pivotal Phase 3 BROADWAY, BROOKLYN, and TANDEM trials, alongside the ongoing PREVAIL cardiovascular outcomes trial.

### 1.2. Market Size Snapshot

The market sizing architecture differentiates between the currently monetized lipid-lowering landscape, defined as the Practical Total Addressable Market (TAM), and the specific opportunity for CETP inhibitors post-approval, defined as the Serviceable Addressable Market (SAM) and Menarini’s Serviceable Obtainable Market (SOM).

The global practical TAM is reset to US$ [Proprietary] in 2025, reflecting the total revenue generated by existing therapies including statins, ezetimibe, bempedoic acid, PCSK9 monoclonal antibodies, and inclisiran.

Analysis indicates that while the global TAM grows at a steady [Proprietary]% CAGR, the Menarini-specific opportunity experiences a rapid ramp-up following expected reimbursement activation, reaching US$ [Proprietary] by 2035. The practical TAM reflects the existing budget pool for lipid management, while the SAM narrows this to the specific uncontrolled and high-risk patients that obicetrapib will target.

### 1.3. Executive Growth Indicators

The trajectory of the CETP inhibitor market is defined by a strategic shift from monotherapy volume to high-value combination treatment. The forecast indicates that while obicetrapib monotherapy will drive early volume in the initial launch period, the obicetrapib / ezetimibe FDC will become the primary revenue driver by the mid-2030s.

Product Split Evolution: By 2035, the FDC is expected to account for [Proprietary]% of total Menarini SOM revenue, reflecting the clinical trend toward earlier intensification and the convenience of single-pill combinations.

Geographic Concentration: Menarini’s opportunity is concentrated in Germany and the United Kingdom, which represent two of the highest-priority commercial markets in the launch territory.

Launch Velocity and Ramp: Revenue generation is strictly launch-flagged, with no commercial revenue projected before 2027. The first full five years of launch are critical for establishing specialist trust and securing inclusion in clinical guidelines.

Sensitivity to Outcomes Data: Analysis indicates that positive results from the PREVAIL cardiovascular outcomes trial serve as a major upside lever, potentially increasing adoption multipliers above base-case projections in the post-2030 window.

### 1.4. Strategic Implications for Menarini

Menarini’s role in this category-creation effort is focused on the successful navigation of European Health Technology Assessment and payer landscapes. The opportunity is concentrated in high-risk patient groups, specifically those with Heterozygous Familial Hypercholesterolemia and established Atherosclerotic Cardiovascular Disease who fail to reach LDL-C targets on standard oral therapies.

Commercial adoption is expected to depend on the ability to position obicetrapib as a biologic-like oral alternative. Menarini must win in the uncontrolled high-risk pool, which represents the primary demand engine for early adoption. Priority markets include Germany, the UK, and France, where infrastructure for lipid management is most advanced and the addressable patient pool is largest.

Strategic efforts must be directed toward medical education that addresses the historical CETP failures by emphasizing obicetrapib’s high selectivity and lack of blood pressure side effects. Furthermore, positioning the FDC as a superior oral alternative to bempedoic acid / ezetimibe combinations will be essential for maximizing blended net price per patient.
"""
}


EXECUTIVE_MARKET_TABLE = [
    {
        "Market Layer": "Global Practical TAM",
        "2025 Value": "US$ [Proprietary]",
        "2030 Value": "US$ [Proprietary]",
        "2035 Value": "US$ [Proprietary]",
        "2025–35 CAGR": "[Proprietary]%",
    },
    {
        "Market Layer": "Menarini Territory TAM",
        "2025 Value": "US$ [Proprietary]",
        "2030 Value": "US$ [Proprietary]",
        "2035 Value": "US$ [Proprietary]",
        "2025–35 CAGR": "[Proprietary]%",
    },
    {
        "Market Layer": "CETP-Addressable SAM",
        "2025 Value": "US$ [Proprietary]",
        "2030 Value": "US$ [Proprietary]",
        "2035 Value": "US$ [Proprietary]",
        "2025–35 CAGR": "Activated from launch",
    },
    {
        "Market Layer": "Menarini-Capturable SOM",
        "2025 Value": "US$ [Proprietary]",
        "2030 Value": "US$ [Proprietary]",
        "2035 Value": "US$ [Proprietary]",
        "2025–35 CAGR": "Launch-driven",
    },
    {
        "Market Layer": "Strict CETP Inhibitor Revenue",
        "2025 Value": "US$ [Proprietary]",
        "2030 Value": "US$ [Proprietary]",
        "2035 Value": "US$ [Proprietary]",
        "2025–35 CAGR": "Launch-driven",
    },
]


# =========================================================
# CSS
# =========================================================
def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif !important;
            background: {LIGHT_GREY};
            color: {DARK_TEXT};
        }}

        /* Hide Streamlit clutter */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        [data-testid="stToolbar"] {{display: none !important;}}
        [data-testid="stDecoration"] {{display: none !important;}}
        [data-testid="stStatusWidget"] {{display: none !important;}}

        .block-container {{
            padding-top: 1.5rem !important;
            padding-bottom: 3rem !important;
            max-width: 1420px !important;
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {DARK_WINE} 0%, {DEEP_BURGUNDY} 55%, #230312 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }}

        section[data-testid="stSidebar"] * {{
            color: #ffffff;
        }}

        .sidebar-title {{
            font-size: 1.1rem;
            font-weight: 800;
            color: white;
            margin-bottom: 0.2rem;
            letter-spacing: -0.02em;
        }}

        .sidebar-subtitle {{
            font-size: 0.72rem;
            color: {GOLD};
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 800;
            margin-bottom: 1rem;
        }}

        .hero {{
            background: linear-gradient(135deg, {DARK_WINE} 0%, {DEEP_BURGUNDY} 48%, {MID_BURGUNDY} 100%);
            border-radius: 28px;
            padding: 3.2rem 3.4rem;
            color: white;
            box-shadow: 0 22px 60px rgba(58,7,28,0.28);
            position: relative;
            overflow: hidden;
            margin-bottom: 1.5rem;
        }}

        .hero:before {{
            content: "";
            position: absolute;
            width: 420px;
            height: 420px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(201,162,39,0.30), rgba(201,162,39,0));
            right: -110px;
            top: -140px;
        }}

        .hero:after {{
            content: "";
            position: absolute;
            width: 340px;
            height: 340px;
            border-radius: 50%;
            border: 1px solid rgba(255,255,255,0.10);
            right: 80px;
            bottom: -180px;
        }}

        .hero-content {{
            position: relative;
            z-index: 2;
        }}

        .eyebrow {{
            display: inline-block;
            background: rgba(201,162,39,0.16);
            color: #FFE7A3;
            border: 1px solid rgba(201,162,39,0.42);
            padding: 0.42rem 0.72rem;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 1.2rem;
        }}

        .hero h1 {{
            color: white;
            font-size: 2.75rem;
            line-height: 1.05;
            letter-spacing: -0.045em;
            margin: 0 0 1rem 0;
            max-width: 980px;
            font-weight: 850;
        }}

        .hero p {{
            color: rgba(255,255,255,0.84);
            font-size: 1.05rem;
            line-height: 1.65;
            max-width: 960px;
            margin: 0;
        }}

        .meta-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.8rem;
            margin-top: 1.4rem;
        }}

        .meta-pill {{
            background: rgba(255,255,255,0.10);
            border: 1px solid rgba(255,255,255,0.16);
            color: white;
            padding: 0.5rem 0.75rem;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 700;
        }}

        .kpi-card {{
            background: white;
            border: 1px solid {BORDER_GREY};
            border-radius: 20px;
            padding: 1.25rem 1.2rem;
            box-shadow: 0 12px 36px rgba(20,20,20,0.05);
            height: 100%;
        }}

        .kpi-label {{
            color: {MUTED_TEXT};
            font-size: 0.76rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.55rem;
        }}

        .kpi-value {{
            color: {DEEP_BURGUNDY};
            font-size: 1.35rem;
            font-weight: 850;
            letter-spacing: -0.025em;
            line-height: 1.2;
        }}

        .kpi-note {{
            color: {MUTED_TEXT};
            font-size: 0.78rem;
            margin-top: 0.6rem;
            line-height: 1.45;
        }}

        .section-card {{
            background: white;
            border: 1px solid {BORDER_GREY};
            border-radius: 24px;
            padding: 1.8rem 2rem;
            box-shadow: 0 12px 40px rgba(20,20,20,0.045);
            margin-bottom: 1.2rem;
        }}

        .section-card h2, .section-card h3 {{
            color: {DEEP_BURGUNDY};
            letter-spacing: -0.02em;
        }}

        .section-card p {{
            color: {DARK_TEXT};
            line-height: 1.72;
            font-size: 0.98rem;
        }}

        .insight-box {{
            background: linear-gradient(135deg, #FFF9EA 0%, #FFFFFF 100%);
            border-left: 5px solid {GOLD};
            border-radius: 16px;
            padding: 1.15rem 1.25rem;
            color: {DARK_TEXT};
            box-shadow: 0 8px 24px rgba(201,162,39,0.12);
            margin: 1rem 0;
            line-height: 1.65;
        }}

        .burgundy-callout {{
            background: linear-gradient(135deg, {DEEP_BURGUNDY} 0%, {DARK_WINE} 100%);
            color: white;
            border-radius: 22px;
            padding: 1.5rem 1.6rem;
            margin: 1.2rem 0;
            box-shadow: 0 16px 42px rgba(91,14,45,0.22);
        }}

        .burgundy-callout h3 {{
            color: white;
            margin-top: 0;
        }}

        .burgundy-callout p {{
            color: rgba(255,255,255,0.86);
            line-height: 1.65;
        }}

        .report-table-wrap {{
            border: 1px solid {BORDER_GREY};
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 10px 28px rgba(20,20,20,0.045);
            margin: 1rem 0 1.4rem 0;
        }}

        .report-table-title {{
            background: {DEEP_BURGUNDY};
            color: white;
            padding: 0.9rem 1rem;
            font-weight: 800;
            font-size: 0.86rem;
            letter-spacing: 0.02em;
        }}

        table.report-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}

        table.report-table th {{
            background: #F5EEF2;
            color: {DEEP_BURGUNDY};
            padding: 0.85rem;
            text-align: left;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            border-bottom: 1px solid {BORDER_GREY};
        }}

        table.report-table td {{
            padding: 0.85rem;
            border-bottom: 1px solid #EEF0F2;
            color: {DARK_TEXT};
            font-size: 0.88rem;
            vertical-align: top;
        }}

        table.report-table tr:nth-child(even) td {{
            background: #FAFAFB;
        }}

        .footer {{
            text-align: center;
            color: {MUTED_TEXT};
            font-size: 0.78rem;
            padding: 1.4rem 0 0.5rem 0;
            border-top: 1px solid {BORDER_GREY};
            margin-top: 2rem;
        }}

        /* Compact login */
        .login-shell {{
            max-width: 430px;
            margin: 8vh auto 0 auto;
            background: white;
            border-radius: 24px;
            padding: 2rem;
            border: 1px solid {BORDER_GREY};
            box-shadow: 0 22px 70px rgba(58,7,28,0.14);
        }}

        .login-brand {{
            text-align: center;
            color: {DEEP_BURGUNDY};
            font-size: 1.45rem;
            font-weight: 850;
            margin-bottom: 0.2rem;
            letter-spacing: -0.02em;
        }}

        .login-sub {{
            text-align: center;
            color: {GOLD};
            font-size: 0.74rem;
            text-transform: uppercase;
            font-weight: 850;
            letter-spacing: 0.08em;
            margin-bottom: 1.1rem;
        }}

        div[data-testid="stTextInput"] input {{
            border-radius: 10px !important;
            border: 1px solid {BORDER_GREY} !important;
            padding: 0.55rem 0.75rem !important;
            min-height: 38px !important;
            font-size: 0.9rem !important;
        }}

        .stButton > button {{
            background: linear-gradient(135deg, {DEEP_BURGUNDY}, {DARK_WINE}) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 800 !important;
            min-height: 40px !important;
            box-shadow: 0 10px 24px rgba(91,14,45,0.22);
        }}

        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 14px 30px rgba(91,14,45,0.32);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# AUTHENTICATION
# =========================================================
def render_login():
    st.markdown(
        """
        <div class="login-shell">
            <div class="login-brand">Strategic Market Research</div>
            <div class="login-sub">Secure Client Preview</div>
            <p style="text-align:center; color:#666666; font-size:0.9rem; line-height:1.55; margin-bottom:1.2rem;">
                Confidential sample dashboard prepared for Menarini.
                Please enter authorized access credentials.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1.1, 0.85, 1.1])
    with col2:
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        login = st.button("Enter Dashboard", use_container_width=True)

    if login:
        if username == USERNAME and password == PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid credentials. Please check username and password.")

    st.stop()


def check_authentication():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        render_login()


# =========================================================
# REUSABLE RENDER HELPERS
# =========================================================
def render_footer():
    st.markdown(
        """
        <div class="footer">
            © 2026 Strategic Market Research. Confidential sample report preview prepared for Menarini.
            Full quantitative outputs available in the complete report.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_card(title, body):
    masked_body = mask_sensitive_numbers(body)
    st.markdown(
        f"""
        <div class="section-card">
            <h2>{title}</h2>
            <div>{masked_body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_html_table(title, rows):
    if not rows:
        return

    columns = list(rows[0].keys())

    header_html = "".join([f"<th>{col}</th>" for col in columns])
    body_html = ""

    for row in rows:
        body_html += "<tr>"
        for col in columns:
            body_html += f"<td>{row.get(col, '')}</td>"
        body_html += "</tr>"

    st.markdown(
        f"""
        <div class="report-table-wrap">
            <div class="report-table-title">{title}</div>
            <table class="report-table">
                <thead><tr>{header_html}</tr></thead>
                <tbody>{body_html}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# CHART 1 — TAM / SAM / SOM FUNNEL
# =========================================================
def create_tam_sam_som_funnel():
    labels = [
        "Lipid-Lowering Therapy Revenue Pool",
        "CETP-Relevant Opportunity",
        "Obicetrapib-Addressable Pool",
        "Menarini Commercial Opportunity",
    ]

    # Symbolic values only for rendering shape; not displayed to users.
    values = [100, 72, 46, 24]

    fig = go.Figure(
        go.Funnel(
            y=labels,
            x=values,
            text=[
                "US$ [Proprietary]",
                "US$ [Proprietary]",
                "US$ [Proprietary]",
                "US$ [Proprietary]",
            ],
            textinfo="text",
            marker=dict(
                color=[DEEP_BURGUNDY, MID_BURGUNDY, SOFT_ROSE, GOLD],
                line=dict(color="white", width=2),
            ),
            hovertemplate="<b>%{y}</b><br>Value: US$ [Proprietary]<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(
            text="TAM / SAM / SOM Preview — Masked Market Architecture",
            x=0.02,
            y=0.95,
            font=dict(size=18, color=DEEP_BURGUNDY),
        ),
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        margin=dict(l=20, r=20, t=70, b=30),
        height=420,
        font=dict(color=DARK_TEXT, size=12),
    )

    fig.update_xaxes(visible=False)
    return fig


# =========================================================
# COVER PAGE
# =========================================================
def render_cover_page():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-content">
                <div class="eyebrow">Confidential Sample Report Preview</div>
                <h1>Global CETP Inhibitors Market, 2025–2035</h1>
                <p>
                    Obicetrapib, next-generation lipid-lowering therapy and strategic positioning for Menarini.
                    This digital preview demonstrates the analytical structure, commercial logic and strategic depth
                    of the full report while intentionally masking proprietary market values.
                </p>
                <div class="meta-row">
                    <div class="meta-pill">Prepared by Strategic Market Research</div>
                    <div class="meta-pill">Prepared for Menarini</div>
                    <div class="meta-pill">Forecast Horizon: 2025–2035</div>
                    <div class="meta-pill">Full quantitative model available in complete report</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    kpi_cols = st.columns(6)
    with kpi_cols[0]:
        render_kpi_card("Global Market Opportunity", "US$ [Proprietary]", "Full TAM disclosed in report")
    with kpi_cols[1]:
        render_kpi_card("Europe / UK / Switzerland SAM", "US$ [Proprietary]", "Filtered access pool")
    with kpi_cols[2]:
        render_kpi_card("Menarini SOM Potential", "US$ [Proprietary]", "Launch-driven revenue view")
    with kpi_cols[3]:
        render_kpi_card("Launch Window", "Available in Full Report", "Regulatory and reimbursement logic")
    with kpi_cols[4]:
        render_kpi_card("Eligible Patient Pool", "[Proprietary] patients", "High-risk LDL-C gap")
    with kpi_cols[5]:
        render_kpi_card("Forecast Horizon", "2025–2035", "Market creation window")


# =========================================================
# SECTION 1 — EXECUTIVE SNAPSHOT
# =========================================================
def render_executive_snapshot():
    st.markdown(
        """
        <div class="section-card">
            <h2>Executive Overview & Strategic Snapshot</h2>
            <p>
                The CETP inhibitor category represents a near-launch market creation opportunity rather than a mature
                therapy class. Obicetrapib is positioned as the key revival asset, with Menarini’s commercial opportunity
                concentrated in high-risk, uncontrolled LDL-C patients across Europe, the UK and Switzerland.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_html_table(
        "TABLE 1: Executive Market Sizing Summary — Masked Preview ($Mn, 2025–2035)",
        EXECUTIVE_MARKET_TABLE,
    )

    st.markdown(
        """
        <div class="insight-box">
            <strong>Strategic interpretation:</strong>
            The practical TAM represents the existing lipid-lowering budget pool, while SAM and SOM narrow the opportunity
            to post-label, reimbursable and Menarini-capturable demand. The sample dashboard masks values; the full report
            unlocks market sizing tables, country-level revenue forecasts and patient funnel assumptions.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.plotly_chart(create_tam_sam_som_funnel(), use_container_width=True)

    with st.expander("Read full executive summary text — masked", expanded=True):
        st.markdown(mask_sensitive_numbers(REPORT_SECTIONS["Cover & Executive Snapshot"]))

    st.markdown(
        """
        <div class="burgundy-callout">
            <h3>Menarini-facing implication</h3>
            <p>
                Commercial success depends on positioning obicetrapib as a high-efficacy oral intensification option
                that can sit between generic oral therapies and injectable biologics. The full report details launch
                sequencing, payer evidence requirements, FDC positioning and country-level prioritization.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
def render_sidebar():
    st.sidebar.markdown('<div class="sidebar-title">Strategic Market Research</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-subtitle">Menarini CETP Preview</div>', unsafe_allow_html=True)

    pages = [
        "Cover & Executive Snapshot",
        "Market Architecture",
        "CETP Inhibitor Opportunity Logic",
        "Menarini / Obicetrapib Strategic Fit",
        "TAM / SAM / SOM Preview",
        "Competitive Landscape",
        "Clinical & Regulatory Readiness",
        "Pricing, Access & Adoption",
        "Regional Launch Prioritization",
        "Risk, Barriers & Watchpoints",
        "Strategic Recommendations",
        "Why Menarini Should Access the Full Report",
        "Full Report Summary Explorer",
    ]

    selected = st.sidebar.radio("Dashboard Navigation", pages, label_visibility="collapsed")

    st.sidebar.markdown("---")
    st.sidebar.caption("Confidential preview. Proprietary values masked.")
    if st.sidebar.button("End Secure Session", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

    return selected


# =========================================================
# PLACEHOLDER FOR NEXT SECTIONS
# =========================================================
def render_placeholder(page_name):
    st.markdown(
        f"""
        <div class="section-card">
            <h2>{page_name}</h2>
            <p>
                This section will be added in the next build step. The final dashboard will include full-length masked
                report content, structured tables, strategic callouts and advanced Plotly visuals for each section.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# MAIN APP
# =========================================================
def main():
    inject_css()
    check_authentication()

    selected_page = render_sidebar()

    if selected_page == "Cover & Executive Snapshot":
        render_cover_page()
        render_executive_snapshot()
    else:
        render_placeholder(selected_page)

    render_footer()


if __name__ == "__main__":
    main()
