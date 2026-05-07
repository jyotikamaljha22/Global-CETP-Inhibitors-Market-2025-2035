import re
import html
import streamlit as st


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Global CETP Inhibitors Market Preview | Menarini",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# THEME COLORS
# =============================================================================
BURGUNDY = "#5B0E2D"
BURGUNDY_DARK = "#3A071C"
MID_BURGUNDY = "#8D1645"
SOFT_ROSE = "#D8A7B1"
GOLD = "#C9A227"
LIGHT_GREY = "#F4F5F7"
WHITE = "#FFFFFF"
DARK_TEXT = "#2B2B2B"
MUTED_TEXT = "#666666"
BORDER_GREY = "#E1E4E8"


# =============================================================================
# LOGIN CREDENTIALS
# =============================================================================
USERNAME = "SMR"
PASSWORD = "SMR@2026"


# =============================================================================
# REPORT TEXT
# =============================================================================
# IMPORTANT:
# Paste your complete existing REPORT_TEXT here exactly as it is now.
# Do not shorten it. Keep all chapters 1–18.
REPORT_TEXT = r"""
PASTE YOUR COMPLETE REPORT_TEXT HERE
"""


# =============================================================================
# TABLE COLUMN COUNTS
# =============================================================================
TABLE_COLUMN_COUNTS = {
    1: 5,
    2: 5,
    3: 5,
    4: 5,
    5: 6,
    6: 5,
    7: 5,
    8: 5,
    9: 5,
    10: 5,
    11: 5,
    12: 5,
    13: 6,
    14: 5,
    15: 5,
    16: 6,
    17: 5,
    18: 4,
    19: 4,
    20: 4,
    21: 5,
}


# =============================================================================
# TEXT CLEANING / MASKING
# =============================================================================
def parse_report_sections(text: str) -> dict:
    sections = {}
    current_header = "Cover / Report Title"
    current_lines = []

    for line in text.strip().splitlines():
        if line.startswith("## "):
            sections[current_header] = "\n".join(current_lines).strip()
            current_header = line.replace("## ", "").strip()
            current_lines = []
        else:
            current_lines.append(line)

    sections[current_header] = "\n".join(current_lines).strip()
    return sections


def remove_source_markers(text: str) -> str:
    cleaned_lines = []

    for line in text.splitlines():
        raw = line.rstrip()

        # Remove source registry lines such as "1: Model patient funnel..."
        if re.match(r"^\s*\d{1,2}:\s+", raw):
            continue

        # Remove sentence citations such as word.1 / therapy.18
        raw = re.sub(r"(?<=[A-Za-z\)\]])\.(\d{1,2})(?=\s|$)", ".", raw)

        # Remove trailing table-cell source numbers such as "High 1", "Client Asset 18"
        # Keep table / section / wave / phase labels safe.
        protected_line = (
            re.match(r"^\s*TABLE\s+\d+", raw, flags=re.I)
            or re.match(r"^\s*\d{1,2}\.\d{1,2}", raw)
            or re.match(r"^\s*Phase\s+\d", raw, flags=re.I)
            or re.match(r"^\s*Wave\s+\d", raw, flags=re.I)
            or re.match(r"^\s*Year\s+\d", raw, flags=re.I)
        )

        if not protected_line:
            raw = re.sub(r"(?<=[A-Za-z\)\]])\s+\d{1,2}$", "", raw)
            raw = re.sub(r"(?<=%)\s+\d{1,2}$", "", raw)

        cleaned_lines.append(raw)

    return "\n".join(cleaned_lines)


def mask_sensitive_numbers(text: str) -> str:
    protected = {}

    def protect(pattern: str):
        nonlocal text

        def repl(match):
            token = f"__SAFE_{len(protected)}__"
            protected[token] = match.group(0)
            return token

        text = re.sub(pattern, repl, text, flags=re.I | re.M)

    # Protect headings, years and clinical labels
    protect(r"\b20\d{2}\s*[–-]\s*20\d{2}\b")
    protect(r"\b20\d{2}\s*[–-]\s*\d{2}\b")
    protect(r"(?m)^\s*\d{1,2}\.\d{1,2}\.?\s+")
    protect(r"\bTABLE\s+\d{1,2}\b")
    protect(r"\b20\d{2}\b")
    protect(r"\bPhase\s+\d[a-zA-Z]?\b")
    protect(r"\bWave\s+\d\b")
    protect(r"\bYear\s+\d\b")
    protect(r"\b\d+\s?mg\b")
    protect(r"\b\d+(st|nd|rd|th)-line\b")
    protect(r"\bNICE\b|\bEMA\b|\bMHRA\b|\bAMNOG\b|\bHAS\b|\bCEPS\b|\bESC\b|\bEAS\b")

    # Currency and revenue
    text = re.sub(r"\bUS\s?\d[\d,\.]*\s?(Mn|million|billion|B|M)?", "US$ [Proprietary]", text, flags=re.I)
    text = re.sub(r"US\$?\s?\d[\d,\.]*\s?(Mn|million|billion|B|M)?", "US$ [Proprietary]", text, flags=re.I)
    text = re.sub(r"\$\s?\d[\d,\.]*\s?(Mn|million|billion|B|M|yr|year)?", "$ [Proprietary]", text, flags=re.I)

    # Percentages
    text = re.sub(r"\b\d[\d,\.]*\s?%", "[Proprietary]%", text)

    # Patient / market units
    text = re.sub(
        r"\b\d[\d,\.]*\s?(million|billion|Mn|patients|patient|pts|CAGR)\b",
        r"[Proprietary] \1",
        text,
        flags=re.I,
    )

    # Large values
    text = re.sub(r"\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b", "[Proprietary]", text)

    # Decimals
    text = re.sub(r"\b\d+\.\d+\b", "[Proprietary]", text)

    # Large standalone integers except years
    text = re.sub(r"\b(?!(?:19|20)\d{2}\b)\d{4,}\b", "[Proprietary]", text)

    for token, value in protected.items():
        text = text.replace(token, value)

    return text


def clean_and_mask(text: str) -> str:
    return mask_sensitive_numbers(remove_source_markers(text))


REPORT_SECTIONS = parse_report_sections(REPORT_TEXT)


# =============================================================================
# CSS
# =============================================================================
def inject_css():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {LIGHT_GREY};
            color: {DARK_TEXT};
        }}

        [data-testid="stHeader"] {{
            background: rgba(244,245,247,0.72);
        }}

        footer {{
            visibility: hidden;
        }}

        .block-container {{
            max-width: 1380px;
            padding-top: 1.2rem;
            padding-bottom: 1rem;
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {BURGUNDY_DARK} 0%, {BURGUNDY} 100%);
        }}

        section[data-testid="stSidebar"] * {{
            color: white;
        }}

        .hero {{
            background: linear-gradient(135deg, {BURGUNDY_DARK} 0%, {BURGUNDY} 45%, {MID_BURGUNDY} 100%);
            color: white;
            padding: 48px;
            border-radius: 28px;
            box-shadow: 0 20px 55px rgba(58,7,28,0.22);
            margin-bottom: 24px;
        }}

        .hero-kicker {{
            display: inline-block;
            background: rgba(201,162,39,0.18);
            color: {GOLD};
            border: 1px solid rgba(201,162,39,0.45);
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 18px;
        }}

        .hero h1 {{
            font-size: 42px;
            line-height: 1.08;
            font-weight: 850;
            margin: 0 0 14px 0;
            letter-spacing: -0.03em;
        }}

        .hero h2 {{
            color: {SOFT_ROSE};
            font-size: 19px;
            font-weight: 500;
            margin: 0 0 22px 0;
            max-width: 980px;
        }}

        .hero p {{
            max-width: 930px;
            font-size: 15px;
            line-height: 1.7;
            color: rgba(255,255,255,0.88);
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 16px;
            margin: 18px 0 28px 0;
        }}

        .kpi-card {{
            background: {WHITE};
            border: 1px solid {BORDER_GREY};
            border-radius: 18px;
            padding: 20px;
            min-height: 132px;
            box-shadow: 0 10px 30px rgba(43,43,43,0.045);
        }}

        .kpi-label {{
            color: {MUTED_TEXT};
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}

        .kpi-value {{
            color: {BURGUNDY};
            font-size: 25px;
            line-height: 1.15;
            font-weight: 850;
            margin-bottom: 10px;
        }}

        .kpi-note {{
            color: {MUTED_TEXT};
            font-size: 13px;
            line-height: 1.45;
        }}

        .section-card {{
            background: {WHITE};
            border: 1px solid {BORDER_GREY};
            border-radius: 22px;
            padding: 26px 28px;
            box-shadow: 0 10px 34px rgba(43,43,43,0.045);
            margin-bottom: 22px;
        }}

        .section-title {{
            color: {BURGUNDY_DARK};
            font-size: 25px;
            font-weight: 850;
            letter-spacing: -0.02em;
            margin: 0 0 12px 0;
        }}

        .section-subtitle {{
            color: {MUTED_TEXT};
            font-size: 14px;
            line-height: 1.65;
            margin-bottom: 16px;
        }}

        .report-wrapper {{
            background: #FBFBFC;
            border: 1px solid {BORDER_GREY};
            border-left: 5px solid {BURGUNDY};
            border-radius: 16px;
            padding: 18px 20px;
            margin: 14px 0 22px 0;
        }}

        .report-subheading {{
            color: {BURGUNDY};
            font-size: 17px;
            font-weight: 850;
            margin: 20px 0 10px 0;
        }}

        .report-paragraph {{
            color: {DARK_TEXT};
            font-size: 14.5px;
            line-height: 1.72;
            margin: 0 0 12px 0;
        }}

        .report-table-wrap {{
            background: {WHITE};
            border: 1px solid {BORDER_GREY};
            border-radius: 16px;
            margin: 18px 0 24px 0;
            overflow-x: auto;
            box-shadow: 0 8px 24px rgba(43,43,43,0.045);
        }}

        .report-table-title {{
            background: linear-gradient(135deg, {BURGUNDY} 0%, {MID_BURGUNDY} 100%);
            color: {WHITE};
            font-size: 14px;
            font-weight: 850;
            padding: 13px 16px;
        }}

        .report-table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 760px;
            font-size: 13px;
        }}

        .report-table th {{
            background: {BURGUNDY_DARK};
            color: {WHITE};
            text-align: left;
            padding: 12px 14px;
            font-weight: 800;
            border-right: 1px solid rgba(255,255,255,0.12);
            vertical-align: top;
        }}

        .report-table td {{
            padding: 12px 14px;
            border-bottom: 1px solid {BORDER_GREY};
            color: {DARK_TEXT};
            vertical-align: top;
            line-height: 1.45;
        }}

        .report-table tbody tr:nth-child(even) td {{
            background: #F8F8FA;
        }}

        .chart-card {{
            background: {WHITE};
            border: 1px solid {BORDER_GREY};
            border-radius: 22px;
            padding: 22px;
            margin: 18px 0 24px 0;
            box-shadow: 0 10px 34px rgba(43,43,43,0.045);
        }}

        .chart-title {{
            font-size: 18px;
            font-weight: 850;
            color: {BURGUNDY};
            margin-bottom: 6px;
        }}

        .chart-caption {{
            font-size: 13px;
            color: {MUTED_TEXT};
            line-height: 1.55;
            margin-bottom: 18px;
        }}

        .funnel-row {{
            min-height: 46px;
            border-radius: 12px;
            margin: 10px auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 18px;
            color: white;
            font-weight: 750;
            box-shadow: 0 8px 20px rgba(58,7,28,0.10);
            gap: 16px;
        }}

        .matrix {{
            position: relative;
            height: 470px;
            background:
                linear-gradient(to right, transparent 49.8%, rgba(91,14,45,0.14) 50%, transparent 50.2%),
                linear-gradient(to bottom, transparent 49.8%, rgba(91,14,45,0.14) 50%, transparent 50.2%),
                #FFFFFF;
            border: 1px solid {BORDER_GREY};
            border-radius: 18px;
            overflow: hidden;
        }}

        .bubble {{
            position: absolute;
            width: 112px;
            min-height: 38px;
            padding: 7px 10px;
            border-radius: 999px;
            text-align: center;
            font-size: 11px;
            line-height: 1.25;
            font-weight: 800;
            box-shadow: 0 10px 24px rgba(91,14,45,0.16);
        }}

        .axis-label-x {{
            position: absolute;
            bottom: 12px;
            left: 50%;
            transform: translateX(-50%);
            color: {MUTED_TEXT};
            font-size: 12px;
            font-weight: 700;
        }}

        .axis-label-y {{
            position: absolute;
            top: 50%;
            left: -24px;
            transform: rotate(-90deg) translateY(-50%);
            transform-origin: left top;
            color: {MUTED_TEXT};
            font-size: 12px;
            font-weight: 700;
        }}

        .flow-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            align-items: stretch;
        }}

        .flow-card {{
            background: #FAFAFB;
            border: 1px solid {BORDER_GREY};
            border-radius: 18px;
            padding: 18px;
            min-height: 110px;
            position: relative;
        }}

        .flow-card-dark {{
            background: linear-gradient(135deg, {BURGUNDY} 0%, {MID_BURGUNDY} 100%);
            color: white;
        }}

        .flow-label {{
            font-size: 13px;
            font-weight: 850;
            margin-bottom: 8px;
        }}

        .flow-note {{
            font-size: 12px;
            color: {MUTED_TEXT};
            line-height: 1.45;
        }}

        .flow-card-dark .flow-note {{
            color: rgba(255,255,255,0.82);
        }}

        .arrow {{
            text-align: center;
            color: {BURGUNDY};
            font-size: 28px;
            font-weight: 900;
            padding-top: 36px;
        }}

        .architecture-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
        }}

        .architecture-card {{
            background: #FAFAFB;
            border: 1px solid {BORDER_GREY};
            border-radius: 18px;
            padding: 18px;
            min-height: 120px;
        }}

        .architecture-card.highlight {{
            background: linear-gradient(135deg, #FFF9EA 0%, #FFFFFF 100%);
            border: 1px solid rgba(201,162,39,0.45);
        }}

        .heatmap {{
            display: grid;
            grid-template-columns: 155px repeat(6, 1fr);
            border: 1px solid {BORDER_GREY};
            border-radius: 18px;
            overflow: hidden;
            background: white;
        }}

        .heat-cell {{
            padding: 12px 10px;
            border-right: 1px solid {BORDER_GREY};
            border-bottom: 1px solid {BORDER_GREY};
            font-size: 12px;
            font-weight: 750;
            text-align: center;
        }}

        .heat-head {{
            background: {BURGUNDY};
            color: white;
        }}

        .heat-row {{
            background: #FAFAFB;
            color: {BURGUNDY};
            text-align: left;
        }}

        .high {{
            background: {BURGUNDY};
            color: white;
        }}

        .medium {{
            background: {SOFT_ROSE};
            color: {DARK_TEXT};
        }}

        .low {{
            background: #F1E5E9;
            color: {MUTED_TEXT};
        }}

        .risk-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
        }}

        .risk-card {{
            border: 1px solid {BORDER_GREY};
            border-radius: 18px;
            padding: 16px;
            background: #FAFAFB;
        }}

        .risk-band {{
            height: 9px;
            border-radius: 999px;
            margin-top: 12px;
            background: linear-gradient(90deg, {SOFT_ROSE}, {GOLD}, {BURGUNDY});
        }}

        .closing-panel {{
            background: linear-gradient(135deg, {BURGUNDY_DARK} 0%, {BURGUNDY} 100%);
            color: white;
            border-radius: 24px;
            padding: 34px 36px;
            box-shadow: 0 20px 55px rgba(58,7,28,0.24);
            margin-top: 18px;
        }}

        .closing-panel h2 {{
            color: white;
            margin-top: 0;
            font-size: 30px;
            line-height: 1.2;
        }}

        .closing-panel p, .closing-panel li {{
            color: rgba(255,255,255,0.88);
            line-height: 1.7;
            font-size: 15px;
        }}

        .footer-smr {{
            text-align: center;
            color: {MUTED_TEXT};
            font-size: 12px;
            padding: 20px 0 6px 0;
            border-top: 1px solid {BORDER_GREY};
            margin-top: 28px;
        }}

        .stTextInput input {{
            border-radius: 10px !important;
            border: 1px solid {BORDER_GREY} !important;
            height: 42px !important;
            font-size: 14px !important;
        }}

        .stButton > button {{
            background: linear-gradient(135deg, {BURGUNDY} 0%, {BURGUNDY_DARK} 100%) !important;
            color: white !important;
            border-radius: 10px !important;
            border: 0 !important;
            font-weight: 800 !important;
            min-height: 42px !important;
        }}

        @media (max-width: 900px) {{
            .kpi-grid,
            .flow-grid,
            .architecture-grid,
            .risk-grid {{
                grid-template-columns: repeat(1, minmax(0, 1fr));
            }}

            .hero {{
                padding: 30px;
            }}

            .hero h1 {{
                font-size: 30px;
            }}

            .heatmap {{
                grid-template-columns: 130px repeat(6, 145px);
                overflow-x: auto;
            }}

            .funnel-row {{
                width: 100% !important;
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# REPORT RENDERING
# =============================================================================
def render_paragraph_line(line: str):
    cleaned = clean_and_mask(line.strip())

    if not cleaned:
        return

    if re.match(r"^\d{1,2}\.\d{1,2}\.?\s+", cleaned):
        st.markdown(
            f"<div class='report-subheading'>{html.escape(cleaned)}</div>",
            unsafe_allow_html=True,
        )
        return

    if ":" in cleaned and len(cleaned.split(":")[0]) <= 55:
        left, right = cleaned.split(":", 1)
        st.markdown(
            f"<p class='report-paragraph'><strong>{html.escape(left)}:</strong>{html.escape(right)}</p>",
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f"<p class='report-paragraph'>{html.escape(cleaned)}</p>",
        unsafe_allow_html=True,
    )


def render_table(table_title: str, table_lines: list[str]):
    table_match = re.search(r"TABLE\s+(\d+)", table_title, flags=re.I)
    if not table_match:
        return

    table_num = int(table_match.group(1))
    col_count = TABLE_COLUMN_COUNTS.get(table_num, 5)

    rows_source = [x.strip() for x in table_lines if x.strip()]

    if len(rows_source) < col_count:
        return

    headers = rows_source[:col_count]
    body = rows_source[col_count:]

    if len(body) % col_count != 0:
        body = body + [""] * (col_count - (len(body) % col_count))

    header_html = "".join(
        f"<th>{html.escape(clean_and_mask(h))}</th>" for h in headers
    )

    rows_html = ""
    for i in range(0, len(body), col_count):
        row = body[i : i + col_count]
        if not any(cell.strip() for cell in row):
            continue

        rows_html += "<tr>"
        for cell in row:
            rows_html += f"<td>{html.escape(clean_and_mask(cell))}</td>"
        rows_html += "</tr>"

    st.markdown(
        f"""
        <div class="report-table-wrap">
            <div class="report-table-title">{html.escape(clean_and_mask(table_title))}</div>
            <table class="report-table">
                <thead><tr>{header_html}</tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_report_block(raw_text: str, stop_before_table=False):
    lines = raw_text.strip().splitlines()

    st.markdown("<div class='report-wrapper'>", unsafe_allow_html=True)

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        if re.match(r"^18\.2\.\s+Source Registry", line, flags=re.I):
            i += 1
            while i < len(lines) and not re.match(r"^18\.3\.", lines[i].strip()):
                i += 1
            continue

        if re.match(r"^TABLE\s+\d+:", line, flags=re.I):
            if stop_before_table:
                break

            table_title = line
            i += 1

            while i < len(lines) and not lines[i].strip():
                i += 1

            table_lines = []

            while i < len(lines):
                candidate = lines[i].strip()

                if not candidate:
                    break

                if candidate.startswith("## "):
                    break

                if re.match(r"^\d{1,2}\.\d{1,2}\.?\s+", candidate):
                    break

                if re.match(r"^TABLE\s+\d+:", candidate, flags=re.I):
                    break

                table_lines.append(candidate)
                i += 1

            render_table(table_title, table_lines)
            continue

        render_paragraph_line(line)
        i += 1

    st.markdown("</div>", unsafe_allow_html=True)


def section_intro(title, subtitle=""):
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title">{html.escape(title)}</div>
            {f'<div class="section-subtitle">{html.escape(subtitle)}</div>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer():
    st.markdown(
        """
        <div class="footer-smr">
            © 2026 Strategic Market Research. Confidential sample report preview prepared for Menarini.
            Full quantitative outputs available in the complete report.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# LOGIN
# =============================================================================
def login_screen():
    st.markdown("<div style='height:10vh;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1.2, 1.0, 1.2])

    with c2:
        st.markdown(
            f"""
            <div style="background:{WHITE};border:1px solid {BORDER_GREY};border-radius:22px;padding:26px 28px;box-shadow:0 18px 48px rgba(58,7,28,0.10);">
                <div style="text-align:center;font-size:24px;font-weight:900;color:{BURGUNDY};letter-spacing:-0.02em;">Strategic Market Research</div>
                <div style="text-align:center;font-size:12px;font-weight:800;color:{GOLD};letter-spacing:0.08em;text-transform:uppercase;margin-top:6px;margin-bottom:18px;">Secure Client Preview</div>
                <div style="text-align:center;font-size:13px;color:{MUTED_TEXT};line-height:1.5;margin-bottom:18px;">
                    Confidential sample report dashboard prepared for Menarini.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="SMR")
            password = st.text_input("Password", type="password", placeholder="SMR@2026")
            login_btn = st.form_submit_button("Enter Dashboard", use_container_width=True)

        if login_btn:
            if username == USERNAME and password == PASSWORD:
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Invalid username or password.")


# =============================================================================
# PURE HTML / CSS VISUALS — NO SVG
# =============================================================================
def chart_tam_sam_som_funnel():
    st.markdown(
        f"""
        <div class="chart-card">
            <div class="chart-title">TAM / SAM / SOM Funnel</div>
            <div class="chart-caption">
                The full report quantifies each market layer. This preview masks proprietary values while preserving the narrowing logic.
            </div>
            <div class="funnel-row" style="width:100%;background:{BURGUNDY};">
                <span>Lipid-Lowering Therapy Revenue Pool</span><span>US$ [Proprietary]</span>
            </div>
            <div class="funnel-row" style="width:84%;background:{MID_BURGUNDY};">
                <span>CETP-Relevant Opportunity</span><span>US$ [Proprietary]</span>
            </div>
            <div class="funnel-row" style="width:66%;background:{SOFT_ROSE};color:{DARK_TEXT};">
                <span>Obicetrapib-Addressable Pool</span><span>US$ [Proprietary]</span>
            </div>
            <div class="funnel-row" style="width:48%;background:{GOLD};color:{DARK_TEXT};">
                <span>Menarini Commercial Opportunity</span><span>US$ [Proprietary]</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_competitive_matrix():
    bubbles = [
        ("Statins", 72, 68, BURGUNDY_DARK),
        ("Ezetimibe", 61, 62, MID_BURGUNDY),
        ("PCSK9 mAbs", 54, 24, GOLD),
        ("Inclisiran", 44, 30, SOFT_ROSE),
        ("Bempedoic Acid", 48, 56, MID_BURGUNDY),
        ("Obicetrapib", 64, 19, BURGUNDY),
        ("Obicetrapib + Ezetimibe FDC", 50, 16, BURGUNDY),
        ("Other CETP", 25, 34, SOFT_ROSE),
    ]

    bubble_html = ""
    for label, left, top, color in bubbles:
        text_color = DARK_TEXT if color in [GOLD, SOFT_ROSE] else WHITE
        bubble_html += (
            f"<div class='bubble' style='left:{left}%;top:{top}%;"
            f"background:{color};color:{text_color};'>{html.escape(label)}</div>"
        )

    st.markdown(
        f"""
        <div class="chart-card">
            <div class="chart-title">Competitive Intensity vs Differentiation Matrix</div>
            <div class="chart-caption">
                Therapy classes are positioned qualitatively. No numeric scores are disclosed in this sample preview.
            </div>
            <div class="matrix">
                {bubble_html}
                <div class="axis-label-x">Commercial maturity →</div>
                <div class="axis-label-y">LDL-C differentiation / residual-risk relevance →</div>
                <div style="position:absolute;left:12px;top:10px;color:{MUTED_TEXT};font-size:12px;font-weight:700;">High differentiation / lower maturity</div>
                <div style="position:absolute;right:12px;bottom:34px;color:{MUTED_TEXT};font-size:12px;font-weight:700;">High maturity / lower differentiation</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_commercial_pathway():
    st.markdown(
        f"""
        <div class="chart-card">
            <div class="chart-title">Commercialization Pathway Map</div>
            <div class="chart-caption">
                Directional patient-to-revenue conversion logic. No proprietary patient counts or revenue values are disclosed.
            </div>
            <div class="flow-grid">
                <div class="flow-card flow-card-dark">
                    <div class="flow-label">High-risk dyslipidemia patients</div>
                    <div class="flow-note">Broad clinical need pool</div>
                </div>
                <div class="flow-card">
                    <div class="flow-label">Uncontrolled LDL-C despite standard therapy</div>
                    <div class="flow-note">Narrowed by goal non-attainment and treatment intensification gap</div>
                </div>
                <div class="flow-card">
                    <div class="flow-label">CETP-eligible opportunity</div>
                    <div class="flow-note">Filtered by label, HTA access and specialist reach</div>
                </div>
                <div class="flow-card flow-card-dark">
                    <div class="flow-label">Menarini commercial opportunity</div>
                    <div class="flow-note">Obicetrapib mono + obicetrapib / ezetimibe FDC</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_transition_map():
    st.markdown(
        f"""
        <div class="chart-card">
            <div class="chart-title">Therapy Class Transition Map</div>
            <div class="chart-caption">
                The lipid-lowering landscape is moving from generic volume therapy toward high-efficacy, specialist-led and next-generation oral intensification options.
            </div>
            <div class="flow-grid">
                <div class="flow-card flow-card-dark">
                    <div class="flow-label">Generic baseline therapy</div>
                    <div class="flow-note">Statins and low-cost established backbone</div>
                </div>
                <div class="flow-card">
                    <div class="flow-label">Add-on oral therapy</div>
                    <div class="flow-note">Ezetimibe and branded oral non-statin options</div>
                </div>
                <div class="flow-card">
                    <div class="flow-label">Injectable / long-acting escalation</div>
                    <div class="flow-note">PCSK9 mAbs and inclisiran set the high-efficacy benchmark</div>
                </div>
                <div class="flow-card flow-card-dark">
                    <div class="flow-label">Next-generation oral CETP / FDC</div>
                    <div class="flow-note">Potential oral biologic-like intensification step</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_value_architecture():
    items = [
        ("Epidemiology", "Defines high-risk and uncontrolled LDL-C pools"),
        ("Treatment Revenue Pools", "Frames practical TAM and budget substitution logic"),
        ("LDL-C Gap", "Identifies the goal non-attainment demand engine"),
        ("CETP Clinical Evidence", "Supports class revival and obicetrapib differentiation"),
        ("Pricing Benchmarks", "Positions oral branded therapy against injectables and add-ons"),
        ("Regulatory Timing", "Links approval, reimbursement and launch activation"),
        ("Competitive Landscape", "Maps substitution pressure and therapy-class threats"),
        ("Adoption Readiness", "Assesses physician, payer and specialist pathway friction"),
        ("Menarini Strategy", "Converts market evidence into launch and value-capture decisions"),
    ]

    cards = ""
    for idx, (title, note) in enumerate(items):
        cls = "architecture-card highlight" if idx in [3, 8] else "architecture-card"
        cards += f"""
        <div class="{cls}">
            <div class="flow-label">{html.escape(title)}</div>
            <div class="flow-note">{html.escape(note)}</div>
        </div>
        """

    st.markdown(
        f"""
        <div class="chart-card">
            <div class="chart-title">Report Value Architecture</div>
            <div class="chart-caption">
                The full report converts research inputs into Menarini-specific strategic decisions.
            </div>
            <div class="architecture-grid">
                {cards}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_heatmap():
    rows = {
        "Europe": ["High", "High", "Medium", "High", "High", "Medium"],
        "United Kingdom": ["High", "High", "Medium", "High", "Medium", "High"],
        "Switzerland": ["High", "Medium", "Medium", "High", "High", "Medium"],
        "United States": ["Medium", "High", "High", "High", "Low", "High"],
        "Japan": ["Medium", "Medium", "Medium", "Medium", "Low", "Medium"],
        "China": ["Medium", "High", "Medium", "Medium", "Medium", "Medium"],
        "Rest of World": ["Low", "Low", "Low", "Low", "Low", "Low"],
    }

    cols = [
        "Reimbursement",
        "LDL-C Gap",
        "Specialist Adoption",
        "Pricing Potential",
        "Menarini Fit",
        "Competitive Pressure",
    ]

    grid = "<div class='heatmap'><div class='heat-cell heat-head'>Region</div>"
    for c in cols:
        grid += f"<div class='heat-cell heat-head'>{html.escape(c)}</div>"

    for region, vals in rows.items():
        grid += f"<div class='heat-cell heat-row'>{html.escape(region)}</div>"
        for v in vals:
            grid += f"<div class='heat-cell {v.lower()}'>{v}</div>"

    grid += "</div>"

    st.markdown(
        f"""
        <div class="chart-card">
            <div class="chart-title">Regional Launch Readiness Heatmap</div>
            <div class="chart-caption">
                Qualitative readiness view across launch-relevant markets.
            </div>
            {grid}
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_risk():
    items = [
        ("Regulatory timing", "High control requirement"),
        ("Payer acceptance", "HTA-sensitive"),
        ("Competitive displacement", "Substitution pressure"),
        ("Physician adoption", "Education-dependent"),
        ("FDC differentiation", "Value-capture lever"),
        ("Pricing discipline", "Net-price sensitivity"),
        ("Evidence durability", "CVOT-linked upside"),
        ("Class skepticism", "Legacy CETP barrier"),
    ]

    cards = ""
    for title, note in items:
        cards += f"""
        <div class="risk-card">
            <div class="flow-label">{html.escape(title)}</div>
            <div class="flow-note">{html.escape(note)}</div>
            <div class="risk-band"></div>
        </div>
        """

    st.markdown(
        f"""
        <div class="chart-card">
            <div class="chart-title">Risk vs Control Dashboard</div>
            <div class="chart-caption">
                Directional risk map. Exact risk scores and sensitivity outputs are available in the full report.
            </div>
            <div class="risk-grid">
                {cards}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# PAGES
# =============================================================================
def render_cover():
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">Confidential Sample Report Preview</div>
            <h1>Global CETP Inhibitors Market Preview</h1>
            <h2>2025–2035: Obicetrapib, Next-Generation Lipid-Lowering Therapy & Strategic Positioning for Menarini</h2>
            <p>
                Prepared by <b>Strategic Market Research</b> for <b>Menarini</b>.
                This dashboard previews the report architecture, strategic logic, competitive framing and commercialization implications.
                All proprietary market values, patient counts, percentages and forecast outputs are intentionally masked.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="kpi-grid">
            <div class="kpi-card"><div class="kpi-label">Global Market Opportunity</div><div class="kpi-value">US$ [Proprietary]</div><div class="kpi-note">Full value available in complete report</div></div>
            <div class="kpi-card"><div class="kpi-label">Europe / UK / Switzerland SAM</div><div class="kpi-value">US$ [Proprietary]</div><div class="kpi-note">CETP-addressable opportunity</div></div>
            <div class="kpi-card"><div class="kpi-label">Menarini SOM Potential</div><div class="kpi-value">US$ [Proprietary]</div><div class="kpi-note">Launch-driven territory capture</div></div>
            <div class="kpi-card"><div class="kpi-label">Launch Window</div><div class="kpi-value">[Available in Full Report]</div><div class="kpi-note">Regulatory and reimbursement timing</div></div>
            <div class="kpi-card"><div class="kpi-label">Eligible Patient Pool</div><div class="kpi-value">[Proprietary] patients</div><div class="kpi-note">High-risk uncontrolled LDL-C pool</div></div>
            <div class="kpi-card"><div class="kpi-label">Forecast Horizon</div><div class="kpi-value">2025–2035</div><div class="kpi-note">Commercial forecast period</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_intro(
        "Executive Thesis",
        "CETP inhibitors are being repositioned from a historically challenged mechanism into a potential next-generation oral lipid-lowering category.",
    )
    render_report_block(
        REPORT_SECTIONS["1. Executive Overview & Strategic Snapshot ($Mn, %, 2025–2035)"],
        stop_before_table=True,
    )
    chart_tam_sam_som_funnel()
    chart_competitive_matrix()


def render_market_architecture():
    section_intro(
        "Market Architecture",
        "The report separates the practical lipid-lowering therapy budget pool from the SAM and SOM available to CETP inhibitors after regulatory approval and payer access.",
    )
    render_report_block(REPORT_SECTIONS["2. Market Definition, Scope & TAM/SAM/SOM Architecture"])
    chart_tam_sam_som_funnel()


def render_opportunity_logic():
    section_intro(
        "CETP Inhibitor Opportunity Logic",
        "Obicetrapib reframes the CETP class by addressing historical potency and safety concerns while targeting the uncontrolled LDL-C gap.",
    )
    render_report_block(REPORT_SECTIONS["3. CETP Mechanism, Class History & Repositioning Logic"])
    chart_commercial_pathway()
    chart_transition_map()


def render_menarini_fit():
    section_intro(
        "Menarini / Obicetrapib Strategic Fit",
        "Menarini’s commercial opportunity is tied to successful HTA navigation, evidence-led physician education and territory-specific launch sequencing.",
    )
    render_report_block(REPORT_SECTIONS["14. Menarini Opportunity, Value Capture & Strategic Positioning"])
    chart_value_architecture()


def render_tam_preview():
    section_intro(
        "TAM / SAM / SOM Preview",
        "The full report provides year-by-year quantitative tables, but this sample preview masks all values to preserve proprietary model outputs.",
    )
    render_report_block(REPORT_SECTIONS["10. Market Size & Forecast, 2025–2035 ($Mn, Patients, %)"])
    chart_tam_sam_som_funnel()
    chart_commercial_pathway()


def render_competitive():
    section_intro(
        "Competitive Landscape",
        "Direct CETP competition is limited, but substitute pressure from statins, ezetimibe, bempedoic acid, PCSK9 mAbs and inclisiran shapes adoption ceilings.",
    )
    render_report_block(REPORT_SECTIONS["12. Competitive Landscape & Substitute Therapy Pressure"])
    chart_competitive_matrix()
    chart_transition_map()


def render_regulatory():
    section_intro(
        "Clinical & Regulatory Readiness",
        "Approval timing, label breadth and outcomes evidence are critical variables in the forecast.",
    )
    render_report_block(REPORT_SECTIONS["7. Obicetrapib Clinical Evidence & Pipeline Positioning"])
    render_report_block(REPORT_SECTIONS["8. Regulatory Pathway, Label Scenarios & Launch Timing"])


def render_pricing_access():
    section_intro(
        "Pricing, Access & Adoption",
        "Pricing strategy must navigate between low-cost generic add-ons and high-cost injectables while building a payer case for an oral biologic-like step.",
    )
    render_report_block(REPORT_SECTIONS["9. Pricing, Reimbursement & Monetization Architecture ($/Patient/Year)"])
    render_report_block(REPORT_SECTIONS["13. Adoption Dynamics, Access Readiness & Market Conversion"])


def render_region():
    section_intro(
        "Regional Launch Prioritization",
        "Germany and the UK anchor Wave 1 commercialization, while France, Switzerland, Italy and Spain shape mid-term expansion.",
    )
    render_report_block(REPORT_SECTIONS["11. Europe, UK & Switzerland Opportunity Analysis"])
    chart_heatmap()


def render_risk():
    section_intro(
        "Risk, Barriers & Watchpoints",
        "The most important downside risks relate to restrictive labeling, payer filters, CETP class skepticism and FDC timing.",
    )
    render_report_block(REPORT_SECTIONS["15. Scenario Analysis & Forecast Sensitivities"])
    render_report_block(REPORT_SECTIONS["16. Risk Assessment & Mitigation Framework"])
    chart_risk()


def render_strategy():
    section_intro(
        "Strategic Roadmap & Recommendations",
        "The commercial roadmap moves from approval preparation and Wave 1 launch to Wave 2 scaling and outcomes-supported broader adoption.",
    )
    render_report_block(REPORT_SECTIONS["17. Strategic Roadmap & Future Outlook, 2025–2035"])
    chart_value_architecture()


def render_closing():
    st.markdown(
        f"""
        <div class="closing-panel">
            <h2>Why Menarini Should Access the Full Report</h2>
            <p>
                The CETP inhibitors market is not a conventional lipid-lowering category. It is a revived mechanism entering a crowded, payer-disciplined market where success depends on proving that obicetrapib can create biologic-like efficacy through an oral, commercially scalable model.
            </p>
            <p>
                Obicetrapib’s opportunity depends on identifying the right uncontrolled LDL-C patient segments, the right launch sequence, the right reimbursement argument and the right differentiation against statins, ezetimibe, bempedoic acid, PCSK9 mAbs and inclisiran.
            </p>
            <ul>
                <li>The full report unlocks complete market size, SAM and SOM values by year and geography.</li>
                <li>It provides country-level access logic for Europe, the UK and Switzerland.</li>
                <li>It benchmarks obicetrapib and the FDC against current and emerging lipid-lowering therapies.</li>
                <li>It converts clinical, regulatory, payer and competitive complexity into actionable launch decisions.</li>
                <li>The sample dashboard intentionally masks proprietary values; the full report provides the complete quantitative model.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_full_report():
    section_intro(
        "Full Report Summary Explorer",
        "Every section from the embedded report summary is shown below with market-sensitive values masked and tables rendered as structured exhibits.",
    )

    query = st.text_input(
        "Search report summary",
        placeholder="Example: obicetrapib, HTA, Germany, SAM, FDC, PCSK9",
    )

    show_all = st.toggle("Show complete summary in one continuous view", value=False)

    if show_all:
        for title, content in REPORT_SECTIONS.items():
            if title == "Cover / Report Title":
                continue

            st.markdown(
                f"<div class='section-title' style='margin-top:28px;'>{html.escape(title)}</div>",
                unsafe_allow_html=True,
            )
            render_report_block(content)
    else:
        for title, content in REPORT_SECTIONS.items():
            if title == "Cover / Report Title":
                continue

            combined = f"{title}\n{content}"
            if query.strip() and query.lower() not in combined.lower():
                continue

            with st.expander(title, expanded=False):
                render_report_block(content)


# =============================================================================
# MAIN
# =============================================================================
def main():
    inject_css()

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_screen()
        footer()
        return

    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding:10px 0 18px 0;">
                <div style="font-size:20px;font-weight:900;color:white;">Strategic Market Research</div>
                <div style="font-size:11px;font-weight:800;color:{GOLD};letter-spacing:0.08em;text-transform:uppercase;margin-top:5px;">Menarini CETP Preview</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        page = st.radio(
            "Dashboard sections",
            [
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
            ],
            label_visibility="collapsed",
        )

        st.markdown("<hr style='border-color:rgba(255,255,255,0.18);'>", unsafe_allow_html=True)

        if st.button("End Secure Session", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()

    if page == "Cover & Executive Snapshot":
        render_cover()
    elif page == "Market Architecture":
        render_market_architecture()
    elif page == "CETP Inhibitor Opportunity Logic":
        render_opportunity_logic()
    elif page == "Menarini / Obicetrapib Strategic Fit":
        render_menarini_fit()
    elif page == "TAM / SAM / SOM Preview":
        render_tam_preview()
    elif page == "Competitive Landscape":
        render_competitive()
    elif page == "Clinical & Regulatory Readiness":
        render_regulatory()
    elif page == "Pricing, Access & Adoption":
        render_pricing_access()
    elif page == "Regional Launch Prioritization":
        render_region()
    elif page == "Risk, Barriers & Watchpoints":
        render_risk()
    elif page == "Strategic Recommendations":
        render_strategy()
    elif page == "Why Menarini Should Access the Full Report":
        render_closing()
    elif page == "Full Report Summary Explorer":
        render_full_report()

    footer()


if __name__ == "__main__":
    main()
