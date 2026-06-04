import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
import requests
import time
from streamlit_lottie import st_lottie

# ==========================================
# 1. PAGE CONFIGURATION & GOD-TIER CSS
# ==========================================
st.set_page_config(page_title="NEXUS AI | Core", page_icon="🌌", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Deep Space Background */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #111118 0%, #050505 100%);
        color: #E0E0E0;
    }
    
    /* MASSIVE Glowing Title */
    .glowing-text {
        font-size: 75px;
        font-weight: 900;
        background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 50%, #00F2FE 100%);
        background-size: 200% auto;
        color: #000;
        background-clip: text;
        text-fill-color: transparent;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        text-align: left;
        margin-bottom: 0px;
        padding-bottom: 0px;
        line-height: 1.1;
    }
    
    @keyframes shine { to { background-position: 200% center; } }
    
    /* Cyberpunk Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, rgba(20,20,30,0.6) 0%, rgba(10,10,15,0.8) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 242, 254, 0.2);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.05);
        border-top: 3px solid #00F2FE;
        transition: all 0.4s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-10px) scale(1.02);
        border-top: 3px solid #FF007A;
        box-shadow: 0 15px 30px rgba(255, 0, 122, 0.2);
    }
    
    /* THE NEW "GOLD" INTELLIGENCE CARD */
    .insight-card {
        background: linear-gradient(145deg, rgba(255, 215, 0, 0.05) 0%, rgba(20, 20, 20, 0.8) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-left: 5px solid #FFD700; /* Neon Gold */
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        transition: transform 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.1);
    }
    
    .insight-title {
        color: #FFD700;
        font-family: 'Courier New', Courier, monospace;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .insight-body {
        color: #E0E0E0;
        font-size: 15px;
        line-height: 1.6;
    }
    
    .sub-tech {
        font-family: 'Courier New', Courier, monospace;
        color: #00F2FE;
        letter-spacing: 2px;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOAD RESOURCES 
# ==========================================
@st.cache_resource
def load_data():
    model = joblib.load('churn_model.pkl')
    model_columns = joblib.load('model_columns.pkl')
    return model, model_columns

@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

model, model_columns = load_data()

# Animations
lottie_brain = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_qp1q7mct.json")
lottie_success = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_jbrw3hcz.json")

# ==========================================
# 3. MASSIVE HERO HEADER
# ==========================================
c_anim, c_text = st.columns([1, 3])
with c_anim:
    st_lottie(lottie_brain, height=250, key="main_brain")
with c_text:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="glowing-text">NEXUS ENTERPRISE<br>AI DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-tech">>> V.5.0 NEURAL PREDICTION ENGINE ONLINE</div>', unsafe_allow_html=True)

st.divider()

# ==========================================
# 4. MAIN INTERFACE
# ==========================================
tab1, tab2 = st.tabs(["🌌 BATCH PROCESSING MATRIX", "🎯 SINGLE TARGET ISOLATION"])

with tab1:
    st.markdown("### 📡 UPLINK ENTERPRISE DATA")
    uploaded_file = st.file_uploader("", type=["csv"])
    
    if uploaded_file is not None:
        # --- THE CYBER PROCESSING SEQUENCE ---
        with st.status("🔗 Establishing connection to dataset...", expanded=True) as status:
            st.write("📥 Downloading packets...")
            time.sleep(0.5)
            raw_df = pd.read_csv(uploaded_file)
            work_df = raw_df.copy()
            st.write("🧹 Scrubbing corrupted sectors (Data Cleaning)...")
            time.sleep(0.5)
            
            if 'TotalCharges' in work_df.columns:
                work_df['TotalCharges'] = pd.to_numeric(work_df['TotalCharges'], errors='coerce').fillna(0)
            if 'customerID' in work_df.columns:
                work_df = work_df.drop('customerID', axis=1)
                
            st.write("🧠 Pushing through Neural Network...")
            time.sleep(1)
            encoded_df = pd.get_dummies(work_df).reindex(columns=model_columns, fill_value=0)
            predictions = model.predict(encoded_df)
            probabilities = model.predict_proba(encoded_df)[:, 1]
            status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
        
        # --- ULTRA LEVEL ANIMATION TRIGGER ---
        success_placeholder = st.empty()
        with success_placeholder.container():
            st_lottie(lottie_success, height=300, key="success_blast")
            time.sleep(2.5) 
        success_placeholder.empty() 
        
        result_df = raw_df.copy()
        result_df['Risk_Probability'] = probabilities
        result_df['AI_Decision'] = ['High Risk' if p >= 0.5 else 'Safe' for p in probabilities]
        high_risk_df = result_df[result_df['AI_Decision'] == 'High Risk']
        
        # --- MASSIVE METRICS ---
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Profiles", f"{len(result_df):,}")
        m2.metric("Critical Risk", f"{len(high_risk_df):,}", delta="Requires Action", delta_color="inverse")
        m3.metric("Retention Rate", f"{((len(result_df)-len(high_risk_df))/len(result_df))*100:.1f}%", delta="Stable")
        m4.metric("Capital at Risk", f"${high_risk_df['MonthlyCharges'].sum():,.2f}", delta="Urgent", delta_color="inverse")
        
        st.divider()

        # --- AUTOMATED INSIGHTS ENGINE (GOLD CARDS) ---
        st.markdown("<h3 style='color:#FFD700;'>⚠️ STRATEGIC INTELLIGENCE REPORT</h3>", unsafe_allow_html=True)
        
        if len(high_risk_df) > 0:
            insight_col1, insight_col2 = st.columns(2)
            
            with insight_col1:
                if 'Contract' in high_risk_df.columns:
                    top_contract = high_risk_df['Contract'].mode()[0]
                    contract_pct = (len(high_risk_df[high_risk_df['Contract'] == top_contract]) / len(high_risk_df)) * 100
                    st.markdown(f"""
                    <div class="insight-card">
                        <div class="insight-title">⚡ CONTRACT VULNERABILITY DETECTED</div>
                        <div class="insight-body">
                            <strong>Observation:</strong> {contract_pct:.0f}% of churners are on <b>{top_contract}</b> plans.<br>
                            <strong>Root Cause:</strong> Lack of commitment barrier allows instant exit.<br>
                            <strong>Action:</strong> Auto-generate 15% discount offers for 1-Year upgrades.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with insight_col2:
                if 'PaymentMethod' in high_risk_df.columns:
                    top_payment = high_risk_df['PaymentMethod'].mode()[0]
                    st.markdown(f"""
                    <div class="insight-card">
                        <div class="insight-title">💳 PAYMENT GATEWAY FRICTION</div>
                        <div class="insight-body">
                            <strong>Observation:</strong> High churn correlation with <b>{top_payment}</b>.<br>
                            <strong>Root Cause:</strong> Manual processing fatigue increases cancellation risk.<br>
                            <strong>Action:</strong> Incentivize "Auto-Pay" setup with immediate $5 account credit.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # --- ADVANCED DATA VISUALIZATION MATRIX ---
        st.markdown("<br><h3 style='color:#00F2FE;'>🛰️ FULL SPECTRUM TELEMETRY MATRIX</h3>", unsafe_allow_html=True)
        
        # Row 1 of Charts
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            fig_scatter = px.scatter(result_df, x="tenure", y="MonthlyCharges", color="AI_Decision",
                                     color_discrete_map={'Safe':'#00F2FE', 'High Risk':'#FF007A'},
                                     title="Fleet Map: Tenure vs. Spend", template="plotly_dark")
            fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with chart_col2:
            if 'Contract' in result_df.columns and 'PaymentMethod' in result_df.columns:
                fig_sun = px.sunburst(high_risk_df, path=['Contract', 'PaymentMethod'], 
                                      title="Risk Origin Matrix (Contract -> Payment)",
                                      color_discrete_sequence=['#FF007A', '#FF4B2B'], template="plotly_dark")
                fig_sun.update_layout(paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_sun, use_container_width=True)

        # Row 2 of Charts
        chart_col3, chart_col4, chart_col5 = st.columns(3)
        with chart_col3:
            fig_donut = px.pie(result_df, names='AI_Decision', hole=0.7, 
                               color='AI_Decision', color_discrete_map={'Safe':'#00F2FE', 'High Risk':'#FF007A'},
                               title="System Status", template="plotly_dark")
            fig_donut.update_layout(paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
            st.plotly_chart(fig_donut, use_container_width=True)
            
        with chart_col4:
            if 'InternetService' in high_risk_df.columns:
                risk_by_net = high_risk_df['InternetService'].value_counts().reset_index()
                fig_bar = px.bar(risk_by_net, x='InternetService', y='count', title="Vulnerability by Network",
                                 color='count', color_continuous_scale='sunset', template="plotly_dark")
                fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False)
                st.plotly_chart(fig_bar, use_container_width=True)

        with chart_col5:
            fig_hist = px.histogram(high_risk_df, x="tenure", nbins=20, title="Churn Lifetime Distribution",
                                    color_discrete_sequence=['#FF007A'], template="plotly_dark")
            fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_hist, use_container_width=True)
                
        # --- DATA GRID ---
        st.markdown("<h3 style='color:#00F2FE;'>📋 ACTION PROTOCOL QUEUE</h3>", unsafe_allow_html=True)
        st.dataframe(result_df.sort_values(by='Risk_Probability', ascending=False).head(100), use_container_width=True)

with tab2:
    st.markdown("### 🎯 MANUAL OVERRIDE (SINGLE TARGET)")
    st.info("System optimized for bulk data. Single target uplink standing by.")