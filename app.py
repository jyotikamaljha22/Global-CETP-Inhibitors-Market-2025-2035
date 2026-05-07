import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# =============================================================================
# 1. PAGE CONFIGURATION & THEME
# =============================================================================
st.set_page_config(
    page_title="Global CETP Inhibitors Market Dashboard | Menarini",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS to inject the Burgundy & Gold theme from the HTML sample
st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp { background-color: #F3F4F6; }
    h1, h2, h3 { color: #800020 !important; font-family: 'Inter', sans-serif; }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #800020;
        color: white;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* Navigation Link active state simulation */
    .nav-label {
        font-weight: bold;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        margin-top: 1rem;
        color: #D4AF37 !important;
    }

    /* KPI Cards */
    .kpi-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-top: 4px solid #800020;
        text-align: center;
    }
    .kpi-card-gold { border-top: 4px solid #D4AF37; }
    .kpi-title { font-size: 0.75rem; font-weight: bold; color: #6B7280; text-transform: uppercase; margin-bottom: 5px; }
    .kpi-value { font-size: 1.5rem; font-weight: bold; color: #1F2937; }

    /* Tables */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        border-radius: 8px 8px 0 0;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    }
    .styled-table thead tr {
        background-color: #800020;
        color: #ffffff;
        text-align: left;
    }
    .styled-table th, .styled-table td { padding: 12px 15px; }
    .styled-table tbody tr { border-bottom: 1px solid #dddddd; background-color: white; }
    .styled-table tbody tr:nth-of-type(even) { background-color: #f3f3f3; }

    /* Redacted Tag */
    .redacted {
        color: #9CA3AF;
        font-size: 0.85em;
        font-family: monospace;
        font-weight: bold;
        background: #e5e7eb;
        padding: 2px 4px;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. SECURITY / LOGIN METHOD
# =============================================================================
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] == "SMR" and st.session_state["password"] == "SMR@2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.markdown("<div style='text-align: center; padding: 50px;'>", unsafe_allow_html=True)
        st.image("https://img.icons8.com/ios-filled/100/800020/security-configuration.png")
        st.markdown("<h2 style='color: #800020;'>Strategic Market Research Portal</h2>", unsafe_allow_html=True)
        st.text_input("Username", on_change=None, key="username")
        st.text_input("Password", type="password", on_change=None, key="password")
        if st.button("Log In"):
            password_entered()
            if not st.session_state.get("password_correct", False):
                 st.error("😕 User not known or password incorrect")
        st.markdown("</div>", unsafe_allow_html=True)
        return False
    else:
        return st.session_state["password_correct"]

if not check_password():
    st.stop()

# =============================================================================
# 3. DATA & CALCULATIONS (Parsed from Report.txt)
# =============================================================================
# Global TAM Data
df_tam = pd.DataFrame({
    "Market Layer": ["Global Practical TAM", "Menarini Territory TAM", "CETP SAM Potential", "Menarini SOM Revenue"],
    "2025": [31800.0, 9015.0, 0.0, 0.0],
    "2030": [38319.0, 10643.6, 6688.9, 181.7],
    "2035": [46174.3, 12568.4, 6709.2, 468.1],
    "CAGR": ["3.8%", "3.4%", "Activated 2027", "Launch-driven"]
})

# Patient Funnel Data
funnel_data = pd.DataFrame({
    "Stage": ["Adult Pop", "Diagnosed", "Treated", "Uncontrolled", "Relevant", "Reachable"],
    "Value": [507.4, 161.1, 102.3, 42.1, 17.5, 4.4]
})

# Geographic Splits 2035
geo_data = pd.DataFrame({
    "Country": ["Germany", "UK", "France", "Italy", "Spain", "Switzerland", "Rest of Europe"],
    "Revenue": [142.2, 72.2, 76.4, 52.5, 32.6, 17.4, 74.8]
})

# =============================================================================
# 4. SIDEBAR NAVIGATION
# =============================================================================
with st.sidebar:
    st.markdown("<div style='padding: 20px 0;'><h2 style='color: white; border:none;'>SMR</h2><p style='color: #D4AF37; font-size: 0.8rem; font-weight:bold;'>STRATEGIC MARKET RESEARCH</p></div>", unsafe_allow_html=True)
    st.markdown('<p class="nav-label">Report Navigation</p>', unsafe_allow_html=True)
    
    page = st.radio("Go to", [
        "1. Executive Overview",
        "2. Market Architecture",
        "3. Disease Burden & Funnel",
        "4. Forecast & SOM Trajectory",
        "5. Country Analysis",
        "6. Competitive Landscape",
        "7. Scenario & Risk Analysis"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("""
        <div style='font-size: 0.7rem; opacity: 0.8;'>
            <b>Prepared for:</b><br>Menarini Group<br><br>
            <b style='color: #D4AF37;'>CONFIDENTIAL DATA</b><br>
            © 2026 SMR Global
        </div>
    """, unsafe_allow_html=True)

# =============================================================================
# 5. PAGE CONTENT
# =============================================================================

# Header
st.markdown('<p style="color: #D4AF37; font-weight: bold; letter-spacing: 0.2em; font-size: 0.8rem; margin-bottom:0;">INTERACTIVE STRATEGY DOCUMENT</p>', unsafe_allow_html=True)
st.title("Global CETP Inhibitors Market, 2025–2035")
st.markdown('<h3 style="margin-top: -20px; color: #4B5563 !important;">Obicetrapib-Led Lipid-Lowering Opportunity</h3>', unsafe_allow_html=True)
st.markdown("---")

if page == "1. Executive Overview":
    st.header("1. Executive Overview & Strategic Snapshot")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("1.1. Strategic Market Thesis")
        st.write("""
        The global landscape for lipid-lowering therapies (LLT) is currently undergoing a structural transformation, 
        characterized by the emergence of high-efficacy oral alternatives to established injectable biologics. 
        The CETP inhibitor class, once sidelined, is being revived through **obicetrapib**. [cite: 2, 3]
        """)
        st.write("""
        As of 2025, the strict CETP inhibitor market generates zero commercial revenue. [cite: 4] 
        However, the potential is anchored in a massive landscape where patients fail to achieve LDL-C goals. 
        Menarini’s role is focused on the successful navigation of European HTA and payer landscapes for obicetrapib monotherapy and its FDC with ezetimibe. [cite: 5, 12]
        """)
    
    with col2:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #D4AF37;">
            <p style="color: #800020; font-weight: bold; margin-bottom: 5px;">STRATEGIC IMPERATIVE</p>
            <p style="font-size: 0.9rem; color: #1F2937;">Position obicetrapib as a "biologic-like" oral alternative to win in the uncontrolled high-risk pool. [cite: 13, 14]</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI Grid
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown('<div class="kpi-card"><p class="kpi-title">Global Practical TAM</p><p class="kpi-value">$31.8B</p></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown('<div class="kpi-card kpi-card-gold"><p class="kpi-title">Addressable SAM</p><p class="kpi-value">$6.7B</p></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown('<div class="kpi-card"><p class="kpi-title">2035 SOM (Base)</p><p class="kpi-value">$468.1M</p></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown('<div class="kpi-card kpi-card-gold"><p class="kpi-title">FDC Revenue Share</p><p class="kpi-value">61.9%</p></div>', unsafe_allow_html=True)

elif page == "2. Market Architecture":
    st.header("2. Market Definition & Architecture")
    st.write("The report employs a strict revenue recognition logic where the category size is $0 until regulatory approval. [cite: 19]")
    
    st.markdown("""
    <table class="styled-table">
        <thead>
            <tr>
                <th>Market Layer</th>
                <th>Definition</th>
                <th>Starts From</th>
                <th>Relevance to Menarini</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>Strict CETP Market</b></td>
                <td>Revenue from approved CETP inhibitors only.</td>
                <td>2027 (Launch)</td>
                <td>Represents client product sales. [cite: 21]</td>
            </tr>
            <tr>
                <td><b>Practical TAM</b></td>
                <td>Current revenue of all relevant lipid-lowering therapies.</td>
                <td>2025</td>
                <td>Competitive revenue pool. [cite: 21]</td>
            </tr>
            <tr>
                <td><b>SAM</b></td>
                <td>CETP-addressable subset post-label and access filters.</td>
                <td>2027</td>
                <td>Territory volume potential. [cite: 21]</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

elif page == "3. Disease Burden & Funnel":
    st.header("3. Disease Burden & Addressable Patient Pool")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Patient Conversion Logic")
        st.write("""
        Cardiovascular disease remains the leading cause of death in Europe. [cite: 30] 
        Adult populations exhibit hypercholesterolemia prevalence between 40-49%. 
        The primary challenge is "funneling" this population into a reachable, high-risk base. [cite: 30, 31]
        """)
        st.markdown('<p class="redacted">41% OF TREATED PATIENTS REMAIN UNCONTROLLED</p>', unsafe_allow_html=True)
    
    with col2:
        fig = go.Figure(go.Funnel(
            y = funnel_data["Stage"],
            x = funnel_data["Value"],
            marker = {"color": ["#E5E7EB", "#9CA3AF", "#e6c86a", "#D4AF37", "#800020", "#4b0012"]},
            textinfo = "value+percent initial"
        ))
        fig.update_layout(title="Menarini Territory Patient Funnel (Mn Patients)", height=400, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

elif page == "4. Forecast & SOM Trajectory":
    st.header("4. Market Size & Forecast, 2025–2035")
    
    # Forecast Data for Plotting
    years = [2025, 2027, 2030, 2035]
    som_vals = [0, 10.8, 181.7, 468.1]
    
    fig = px.line(x=years, y=som_vals, labels={'x': 'Year', 'y': 'Revenue ($Mn)'}, title="Menarini SOM Revenue Trajectory")
    fig.update_traces(line_color='#800020', line_width=4, mode='lines+markers')
    fig.update_layout(plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Executive Market Sizing Summary ($Mn)")
    st.table(df_tam.set_index("Market Layer"))
    st.write("Insight: Menarini SOM experiences a rapid ramp-up following 2027 reimbursement. [cite: 7]")

elif page == "5. Country Analysis":
    st.header("5. Europe, UK & Switzerland Opportunity Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(geo_data, values='Revenue', names='Country', 
                     title='2035 SOM Revenue Distribution',
                     color_discrete_sequence=['#800020', '#99334d', '#B91C1C', '#DC2626', '#D4AF37', '#e6c86a', '#F3F4F6'])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Launch Sequencing & Access")
        st.write("""
        **Germany and the UK** drive early value due to their 2027 reimbursement activation. [cite: 78] 
        Wave 2 markets (France, Italy, Spain) follow in 2028. [cite: 59, 80]
        """)
        st.info("Switzerland offers the highest net price potential ($1,200/yr). [cite: 79]")

elif page == "6. Competitive Landscape":
    st.header("6. Competitive Landscape & Substitute Pressure")
    st.write("Direct competition is non-existent; however, indirect competition determines adoption ceilings. [cite: 81]")
    
    st.markdown("""
    <table class="styled-table">
        <thead>
            <tr>
                <th>Therapy Class</th>
                <th>Route</th>
                <th>Efficacy (LDL-C)</th>
                <th>Threat Profile</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>Obicetrapib FDC</b></td>
                <td>Oral</td>
                <td>~49% Reduction</td>
                <td><b style="color: green;">Target Asset</b></td>
            </tr>
            <tr>
                <td>Bempedoic Acid</td>
                <td>Oral</td>
                <td>~18% Reduction</td>
                <td><b style="color: red;">High (Direct Oral)</b></td>
            </tr>
            <tr>
                <td>PCSK9 mAbs</td>
                <td>Injectable</td>
                <td>~60% Reduction</td>
                <td><b style="color: red;">High (Efficacy Ceiling)</b></td>
            </tr>
            <tr>
                <td>Inclisiran</td>
                <td>Injectable</td>
                <td>~50% Reduction</td>
                <td><b>Moderate (Long-acting)</b></td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

elif page == "7. Scenario & Risk Analysis":
    st.header("7. Scenario Analysis & Forecast Sensitivities")
    
    # Scenario Chart
    sc_years = [2025, 2030, 2035]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sc_years, y=[0, 417.5, 1075.3], name='Upside Case', line=dict(color='green', dash='dash')))
    fig.add_trace(go.Scatter(x=sc_years, y=[0, 181.7, 468.1], name='Base Case', line=dict(color='#800020', width=4)))
    fig.add_trace(go.Scatter(x=sc_years, y=[0, 90, 250], name='Downside Case', line=dict(color='red', dash='dot')))
    
    fig.update_layout(title="Revenue Scenario Outcomes ($Mn)", plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Key Market Risks")
    risk_col1, risk_col2 = st.columns(2)
    with risk_col1:
        st.error("**Narrow Label (High Severity)**: Reduces SAM by 40%. [cite: 102]")
        st.warning("**Class Skepticism**: Slows adoption ramp for cardiologists. [cite: 89, 102]")
    with risk_col2:
        st.warning("**Price Pressure**: HAS/CEPS and regional variations in Italy/Spain. [cite: 59, 102]")
        st.info("**Injectable Substitution**: PCSK9 efficacy remains a ceiling. [cite: 40, 102]")

# =============================================================================
# 6. FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6B7280; font-size: 0.75rem; padding-bottom: 20px;">
        CONFIDENTIAL DASHBOARD PREPARED FOR MENARINI GROUP | DATA VALID AS OF 2026<br>
        Source Registry: 1: Model patient funnel; 2: Pricing engine; 3: Workbook extractions.
    </div>
""", unsafe_allow_html=True)
