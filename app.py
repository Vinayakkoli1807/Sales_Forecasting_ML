import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Forecast Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS — Professional Dark Theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* ---------- Google Font ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ---------- Root Variables ---------- */
    :root {
        --primary: #6C63FF;
        --primary-light: #8B83FF;
        --primary-dark: #4F46E5;
        --accent: #00D4AA;
        --accent-light: #34E0BE;
        --bg-dark: #0E1117;
        --bg-card: #1A1D29;
        --bg-card-hover: #22263A;
        --text-primary: #F0F2F6;
        --text-secondary: #9CA3AF;
        --text-muted: #6B7280;
        --border: #2D3348;
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
        --gradient-1: linear-gradient(135deg, #6C63FF 0%, #00D4AA 100%);
        --gradient-2: linear-gradient(135deg, #1A1D29 0%, #2D3348 100%);
        --shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
        --shadow-glow: 0 0 30px rgba(108, 99, 255, 0.15);
    }

    /* ---------- Global Overrides ---------- */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Hide default Streamlit header & footer */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #13162B 0%, #1A1D29 100%);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }

    /* ---------- Hero Header ---------- */
    .hero-header {
        background: linear-gradient(135deg, #1a1140 0%, #0d1b3e 40%, #0a2639 100%);
        border: 1px solid rgba(108, 99, 255, 0.2);
        border-radius: 16px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-glow);
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(108,99,255,0.12) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-header::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: 10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(0,212,170,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #F0F2F6 0%, #6C63FF 50%, #00D4AA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: var(--text-secondary);
        font-weight: 400;
        position: relative;
        z-index: 1;
        margin-bottom: 0;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(108, 99, 255, 0.15);
        border: 1px solid rgba(108, 99, 255, 0.3);
        color: var(--primary-light);
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        margin-bottom: 0.75rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        position: relative;
        z-index: 1;
    }

    /* ---------- Section Headers ---------- */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 1rem;
        margin-top: 1.5rem;
    }
    .section-header-icon {
        font-size: 1.3rem;
    }
    .section-header-text {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.3px;
    }
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, var(--border) 0%, transparent 100%);
        margin-bottom: 1.2rem;
    }

    /* ---------- Input Cards ---------- */
    .input-group-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .input-group-card:hover {
        border-color: rgba(108, 99, 255, 0.3);
        box-shadow: var(--shadow-glow);
    }
    .input-group-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--primary-light);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ---------- KPI / Result Cards ---------- */
    .kpi-card {
        background: linear-gradient(135deg, #1a1140 0%, #0d1b3e 100%);
        border: 1px solid rgba(108, 99, 255, 0.3);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 40px rgba(108,99,255,0.12);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-1);
    }
    .kpi-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #F0F2F6 0%, #00D4AA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    .kpi-sublabel {
        font-size: 0.8rem;
        color: var(--text-muted);
    }

    /* ---------- Metric Mini Cards ---------- */
    .metric-mini {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1.2rem 1rem;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-mini:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow);
    }
    .metric-mini-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 0.4rem;
    }
    .metric-mini-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
    }

    /* ---------- Insight Cards ---------- */
    .insight-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: flex-start;
        gap: 0.8rem;
    }
    .insight-icon {
        font-size: 1.3rem;
        margin-top: 2px;
    }
    .insight-text {
        font-size: 0.9rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }
    .insight-text strong {
        color: var(--text-primary);
    }

    /* ---------- Predict Button ---------- */
    .stButton > button {
        background: var(--gradient-1) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.75rem 2.5rem !important;
        border-radius: 10px !important;
        border: none !important;
        width: 100% !important;
        letter-spacing: 0.3px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3) !important;
    }
    .stButton > button:hover {
        box-shadow: 0 6px 25px rgba(108, 99, 255, 0.5) !important;
        transform: translateY(-1px);
    }
    .stButton > button:active {
        transform: translateY(0);
    }

    /* ---------- Selectbox / Input Styling ---------- */
    .stSelectbox label, .stNumberInput label, .stTextInput label {
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        font-size: 0.85rem !important;
    }

    /* ---------- Footer ---------- */
    .footer {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-top: 3rem;
        text-align: center;
    }
    .footer-text {
        color: var(--text-muted);
        font-size: 0.8rem;
    }
    .footer-text a {
        color: var(--primary-light);
        text-decoration: none;
    }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* ---------- Scrollbar ---------- */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Load Model & Feature Columns 
# ──────────────────────────────────────────────
@st.cache_resource
def load_model():
    """Load the trained ML model and feature columns."""
    model = joblib.load("sales_forecasting_model.pkl")
    feature_columns = joblib.load("feature_columns.pkl")
    return model, feature_columns

try:
    model, feature_columns = load_model()
    model_loaded = True
except FileNotFoundError as e:
    model_loaded = False
    model_error = str(e)


# ──────────────────────────────────────────────
# Sidebar — Project Info & Instructions
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem 0;">
        <span style="font-size: 2.5rem;">📊</span>
        <h2 style="
            background: linear-gradient(135deg, #6C63FF 0%, #00D4AA 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            margin: 0.5rem 0 0 0;
            font-size: 1.3rem;
        ">Sales Forecaster</h2>
        <p style="color: #6B7280; font-size: 0.8rem; margin-top: 0.2rem;"></p>
    </div>
    <hr style="border-color: #2D3348; margin: 1rem 0;">
    """, unsafe_allow_html=True)

    st.markdown("#### 📖 About")
    st.markdown(
        "This dashboard uses a **trained Machine Learning model** to predict "
        "sales based on order attributes such as shipping mode, customer segment, "
        "product category, and more."
    )

    st.markdown("#### 🛠️ How to Use")
    st.markdown("""
    1. Fill in the **order details** in the main panel.
    2. Click **🚀 Generate Forecast**.
    3. View your predicted sales and insights.
    """)

    st.markdown("#### 🧠 Model Info")
    if model_loaded:
        st.success("Model loaded successfully", icon="✅")
        st.markdown(f"""
        | Property | Value |
        |----------|-------|
        | **Algorithm** | `Regression` |
        | **Features** | `21` |
        """)
    else:
        st.error("Model not loaded", icon="❌")

    st.markdown("#### 🏗️ Tech Stack")
    st.markdown("""
    - **Python** — Core Language
    - **Scikit-learn** — ML Framework
    - **Streamlit** — Web Interface
    - **Plotly** — Interactive Charts
    - **Pandas** — Data Processing
    """)

    st.markdown("""
    <hr style="border-color: #2D3348; margin: 1.5rem 0 1rem 0;">
    <div style="text-align:center; padding: 0.5rem 0;">
        <p style="color: #6B7280; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.4rem;">Developed by</p>
        <p style="
            font-size: 1.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #6C63FF 0%, #00D4AA 50%, #6C63FF 100%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: shimmer 3s linear infinite;
            margin: 0;
            letter-spacing: 0.5px;
        ">⚡ Vinayak Koli  </p>
        <p style="color: #4B5563; font-size: 0.7rem; margin-top: 0.3rem;"></p>
    </div>
    <style>
        @keyframes shimmer {
            0% { background-position: 0% center; }
            100% { background-position: 200% center; }
        }
    </style>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Hero Header
# ──────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-badge">🤖 Machine Learning Powered</div>
    <div class="hero-title">Sales Forecasting System</div>
    <div class="hero-subtitle">
        Predict future sales with precision using advanced ML algorithms.
        Enter your order details below and generate an accurate sales forecast instantly.
    </div>
</div>
""", unsafe_allow_html=True)

# Show error banner if model failed to load
if not model_loaded:
    st.error(
        f"⚠️ **Model files not found.** Please ensure `sales_forecasting_model.pkl` "
        f"and `feature_columns.pkl` are in the application directory.\n\n"
        f"Details: `{model_error}`",
        icon="🚫"
    )
    st.stop()


# ──────────────────────────────────────────────
# Input Section
# ──────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <span class="section-header-icon">📝</span>
    <span class="section-header-text">Order Details</span>
</div>
<div class="section-divider"></div>
""", unsafe_allow_html=True)

# --- Row 1: Shipping & Customer ---
col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown("""
    <div class="input-group-title">
        🚚 Shipping & Customer
    </div>
    """, unsafe_allow_html=True)

    ship_mode = st.selectbox(
        "Ship Mode",
        ["First Class", "Second Class", "Standard Class", "Same Day"],
        help="Select the shipping method for the order."
    )

    segment = st.selectbox(
        "Customer Segment",
        ["Consumer", "Corporate", "Home Office"],
        help="The market segment the customer belongs to."
    )

    region = st.selectbox(
        "Region",
        ["Central", "East", "South", "West"],
        help="Geographic region where the order was placed."
    )

with col_right:
    st.markdown("""
    <div class="input-group-title">
        📦 Product Information
    </div>
    """, unsafe_allow_html=True)

    category = st.selectbox(
        "Product Category",
        ["Furniture", "Office Supplies", "Technology"],
        help="The broad product category."
    )

    sub_category = st.text_input(
        "Sub-Category",
        placeholder="e.g., Chairs, Phones, Binders",
        help="The specific sub-category of the product."
    )

    city = st.text_input(
        "City",
        placeholder="e.g., New York, Los Angeles",
        help="City where the order was shipped."
    )

    state = st.text_input(
        "State",
        placeholder="e.g., California, Texas",
        help="State where the order was shipped."
    )

st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)

# --- Row 2: Financial Details ---
st.markdown("""
<div class="input-group-title" style="margin-top: 0.5rem;">
    💰 Financial Parameters
</div>
""", unsafe_allow_html=True)

fin_col1, fin_col2, fin_col3 = st.columns(3, gap="large")

with fin_col1:
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1,
        step=1,
        help="Number of units ordered."
    )

with fin_col2:
    discount = st.number_input(
        "Discount",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.01,
        format="%.2f",
        help="Discount applied (0.0 = no discount, 1.0 = 100% off)."
    )

with fin_col3:
    profit = st.number_input(
        "Profit",
        value=0.0,
        step=1.0,
        format="%.2f",
        help="Expected or known profit for this order."
    )


# ──────────────────────────────────────────────
# Predict Button
# ──────────────────────────────────────────────
st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)

predict_col1, predict_col2, predict_col3 = st.columns([1, 2, 1])
with predict_col2:
    predict_clicked = st.button("🚀  Generate Forecast", use_container_width=True)

st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Prediction Logic 
# ──────────────────────────────────────────────
if predict_clicked:
    # Validate required text inputs
    missing_fields = []
    if not sub_category.strip():
        missing_fields.append("Sub-Category")
    if not city.strip():
        missing_fields.append("City")
    if not state.strip():
        missing_fields.append("State")

    if missing_fields:
        st.warning(
            f" Please fill in the following fields: **{', '.join(missing_fields)}**",
            icon="⚠️"
        )
    else:
        with st.spinner("Running prediction model..."):
            # ── ML PREDICTION LOGIC — PRESERVED EXACTLY ──
            input_df = pd.DataFrame(
                [[0] * len(feature_columns)],
                columns=feature_columns
            )

            # Numerical values
            if "Quantity" in input_df.columns:
                input_df.loc[0, "Quantity"] = quantity

            if "Discount" in input_df.columns:
                input_df.loc[0, "Discount"] = discount

            if "Profit" in input_df.columns:
                input_df.loc[0, "Profit"] = profit

            # Dummy columns
            dummy_values = [
                f"Ship Mode_{ship_mode}",
                f"Segment_{segment}",
                f"Region_{region}",
                f"Category_{category}",
                f"Sub-Category_{sub_category}",
                f"City_{city}",
                f"State_{state}"
            ]

            for col in dummy_values:
                if col in input_df.columns:
                    input_df.loc[0, col] = 1

            prediction = model.predict(input_df)
            # ── END OF PRESERVED ML LOGIC ──

            predicted_sales = prediction[0]

        # ──────────────────────────────────────────
        # Result Display
        # ──────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <span class="section-header-icon">📈</span>
            <span class="section-header-text">Forecast Result</span>
        </div>
        <div class="section-divider"></div>
        """, unsafe_allow_html=True)

        # KPI Card
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Predicted Sales</div>
            <div class="kpi-value">${predicted_sales:,.2f}</div>
            <div class="kpi-sublabel">
                 Based on Regression model 
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)

        # Mini Metric Cards — Input Summary
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="metric-mini">
                <div class="metric-mini-label">Quantity</div>
                <div class="metric-mini-value">{quantity}</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-mini">
                <div class="metric-mini-label">Discount</div>
                <div class="metric-mini-value">{discount:.0%}</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-mini">
                <div class="metric-mini-label">Profit</div>
                <div class="metric-mini-value">${profit:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            profit_margin = (profit / predicted_sales * 100) if predicted_sales != 0 else 0
            st.markdown(f"""
            <div class="metric-mini">
                <div class="metric-mini-label">Profit Margin</div>
                <div class="metric-mini-value">{profit_margin:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)

        # ──────────────────────────────────────────
        # Visualizations & Insights
        # ──────────────────────────────────────────
        viz_tab, insight_tab, summary_tab = st.tabs([
            "📊 Visualizations",
            "💡 Insights",
            "📋 Input Summary"
        ])

        # ── Visualizations Tab ──
        with viz_tab:
            viz_col1, viz_col2 = st.columns(2, gap="large")

            with viz_col1:
                # Gauge Chart — Predicted Sales
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=predicted_sales,
                    number={"prefix": "$", "font": {"size": 28, "color": "#F0F2F6"}},
                    title={"text": "Predicted Sales", "font": {"size": 14, "color": "#9CA3AF"}},
                    gauge={
                        "axis": {
                            "range": [0, max(predicted_sales * 2, 1000)],
                            "tickfont": {"color": "#6B7280"},
                        },
                        "bar": {"color": "#6C63FF"},
                        "bgcolor": "#1A1D29",
                        "borderwidth": 0,
                        "steps": [
                            {"range": [0, max(predicted_sales * 0.5, 250)], "color": "#1e2235"},
                            {"range": [max(predicted_sales * 0.5, 250), max(predicted_sales * 1.0, 500)], "color": "#232942"},
                            {"range": [max(predicted_sales * 1.0, 500), max(predicted_sales * 2, 1000)], "color": "#28304f"},
                        ],
                        "threshold": {
                            "line": {"color": "#00D4AA", "width": 3},
                            "thickness": 0.8,
                            "value": predicted_sales,
                        },
                    },
                ))
                fig_gauge.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#F0F2F6"},
                    height=300,
                    margin=dict(l=30, r=30, t=60, b=30),
                )
                st.plotly_chart(fig_gauge, use_container_width=True)

            with viz_col2:
                # Revenue Breakdown — Sales vs Profit vs Discount Loss
                discount_loss = predicted_sales * discount
                net_revenue = predicted_sales - discount_loss

                fig_waterfall = go.Figure(go.Waterfall(
                    x=["Gross Sales", "Discount", "Net Revenue", "Profit"],
                    y=[predicted_sales, -discount_loss, 0, profit],
                    measure=["absolute", "relative", "total", "absolute"],
                    text=[
                        f"${predicted_sales:,.0f}",
                        f"-${discount_loss:,.0f}",
                        f"${net_revenue:,.0f}",
                        f"${profit:,.0f}",
                    ],
                    textposition="outside",
                    connector={"line": {"color": "#2D3348", "width": 1}},
                    decreasing={"marker": {"color": "#EF4444"}},
                    increasing={"marker": {"color": "#10B981"}},
                    totals={"marker": {"color": "#6C63FF"}},
                ))
                fig_waterfall.update_layout(
                    title={"text": "Revenue Breakdown", "font": {"size": 14, "color": "#9CA3AF"}},
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#F0F2F6", "size": 11},
                    height=300,
                    margin=dict(l=30, r=30, t=60, b=30),
                    xaxis={"gridcolor": "#2D3348"},
                    yaxis={"gridcolor": "#2D3348"},
                    showlegend=False,
                )
                st.plotly_chart(fig_waterfall, use_container_width=True)

            # Scenario Comparison: What-if discount chart
            st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
            st.markdown(
                "<p style='color: #9CA3AF; font-size: 0.85rem; font-weight: 600; "
                "text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 0.5rem;'>"
                "📉 Discount Impact Simulation</p>",
                unsafe_allow_html=True,
            )

            discount_levels = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
            simulated_sales = []
            for d in discount_levels:
                sim_df = input_df.copy().astype(float)
                if "Discount" in sim_df.columns:
                    sim_df.loc[0, "Discount"] = d
                sim_pred = model.predict(sim_df)[0]
                simulated_sales.append(sim_pred)

            fig_discount = go.Figure()
            fig_discount.add_trace(go.Scatter(
                x=[f"{d:.0%}" for d in discount_levels],
                y=simulated_sales,
                mode="lines+markers",
                line={"color": "#6C63FF", "width": 3},
                marker={"size": 8, "color": "#6C63FF", "line": {"width": 2, "color": "#0E1117"}},
                fill="tozeroy",
                fillcolor="rgba(108, 99, 255, 0.08)",
                name="Predicted Sales",
            ))
            # Highlight current discount
            fig_discount.add_trace(go.Scatter(
                x=[f"{discount:.0%}"],
                y=[predicted_sales],
                mode="markers+text",
                marker={"size": 14, "color": "#00D4AA", "symbol": "diamond",
                         "line": {"width": 2, "color": "#0E1117"}},
                text=[f"Current: ${predicted_sales:,.0f}"],
                textposition="top center",
                textfont={"color": "#00D4AA", "size": 11},
                name="Current Discount",
            ))
            fig_discount.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#F0F2F6", "size": 11},
                height=300,
                margin=dict(l=40, r=30, t=20, b=40),
                xaxis={"title": "Discount Level", "gridcolor": "#2D3348",
                        "title_font": {"color": "#6B7280"}},
                yaxis={"title": "Predicted Sales ($)", "gridcolor": "#2D3348",
                        "title_font": {"color": "#6B7280"}},
                legend={"font": {"size": 10}},
                showlegend=True,
            )
            st.plotly_chart(fig_discount, use_container_width=True)

        # ── Insights Tab ──
        with insight_tab:
            st.markdown("""
            <div class="section-header" style="margin-top: 0.5rem;">
                <span class="section-header-icon">💡</span>
                <span class="section-header-text">Business Insights</span>
            </div>
            """, unsafe_allow_html=True)

            # Sales magnitude insight
            if predicted_sales > 1000:
                sales_level = "High"
                sales_icon = "🟢"
                sales_desc = "This is a <strong>high-value order</strong>. Consider prioritizing fulfillment and ensuring quality delivery."
            elif predicted_sales > 200:
                sales_level = "Medium"
                sales_icon = "🟡"
                sales_desc = "This is a <strong>medium-value order</strong>. Standard processing should be adequate."
            else:
                sales_level = "Low"
                sales_icon = "🔴"
                sales_desc = "This is a <strong>low-value order</strong>. Consider bundling strategies or upselling to increase order value."

            st.markdown(f"""
            <div class="insight-card">
                <span class="insight-icon">{sales_icon}</span>
                <div class="insight-text">
                    <strong>Sales Level: {sales_level}</strong><br>
                    {sales_desc}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Discount insight
            if discount > 0.2:
                disc_icon = "⚠️"
                disc_text = (
                    f"A <strong>{discount:.0%} discount</strong> is relatively high. "
                    "Consider whether this discount level is sustainable for maintaining profitability."
                )
            elif discount > 0:
                disc_icon = "💸"
                disc_text = (
                    f"A <strong>{discount:.0%} discount</strong> is applied. "
                    "This is within a moderate range and can help drive sales volume."
                )
            else:
                disc_icon = "✅"
                disc_text = (
                    "<strong>No discount</strong> is applied. "
                    "Full-price sales contribute maximally to revenue."
                )

            st.markdown(f"""
            <div class="insight-card">
                <span class="insight-icon">{disc_icon}</span>
                <div class="insight-text">{disc_text}</div>
            </div>
            """, unsafe_allow_html=True)

            # Profit margin insight
            if predicted_sales != 0:
                margin = profit / predicted_sales * 100
                if margin > 20:
                    margin_icon = "📈"
                    margin_text = (
                        f"<strong>Profit margin: {margin:.1f}%</strong> — "
                        "Excellent margin. This order configuration is highly profitable."
                    )
                elif margin > 0:
                    margin_icon = "📊"
                    margin_text = (
                        f"<strong>Profit margin: {margin:.1f}%</strong> — "
                        "Positive margin. Acceptable profitability for this order."
                    )
                else:
                    margin_icon = "📉"
                    margin_text = (
                        f"<strong>Profit margin: {margin:.1f}%</strong> — "
                        "Negative or zero margin. Review pricing or discount strategy."
                    )
            else:
                margin_icon = "ℹ️"
                margin_text = "Unable to compute profit margin (predicted sales is zero)."

            st.markdown(f"""
            <div class="insight-card">
                <span class="insight-icon">{margin_icon}</span>
                <div class="insight-text">{margin_text}</div>
            </div>
            """, unsafe_allow_html=True)

            # Shipping insight
            shipping_insights = {
                "Same Day": ("⚡", "Same-day shipping has the highest urgency and cost. Typically used for time-sensitive orders."),
                "First Class": ("✈️", "First Class shipping balances speed and cost. A good option for priority customers."),
                "Second Class": ("📬", "Second Class shipping offers moderate delivery times at lower cost."),
                "Standard Class": ("📦", "Standard shipping is the most economical option, suitable for non-urgent orders."),
            }
            s_icon, s_text = shipping_insights.get(ship_mode, ("📦", ""))
            st.markdown(f"""
            <div class="insight-card">
                <span class="insight-icon">{s_icon}</span>
                <div class="insight-text">
                    <strong>Shipping: {ship_mode}</strong><br>
                    {s_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Segment insight
            segment_insights = {
                "Consumer": ("🛒", "Consumer segment typically has the highest volume but may have lower per-order profitability."),
                "Corporate": ("🏢", "Corporate orders often involve bulk purchases and can have negotiated pricing."),
                "Home Office": ("🏠", "Home Office customers tend to order smaller quantities with varied product preferences."),
            }
            seg_icon, seg_text = segment_insights.get(segment, ("👤", ""))
            st.markdown(f"""
            <div class="insight-card">
                <span class="insight-icon">{seg_icon}</span>
                <div class="insight-text">
                    <strong>Segment: {segment}</strong><br>
                    {seg_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Summary Tab ──
        with summary_tab:
            st.markdown("""
            <div class="section-header" style="margin-top: 0.5rem;">
                <span class="section-header-icon">📋</span>
                <span class="section-header-text">Complete Input Summary</span>
            </div>
            """, unsafe_allow_html=True)

            summary_data = {
                "Parameter": [
                    "Ship Mode", "Customer Segment", "Region",
                    "Product Category", "Sub-Category",
                    "City", "State",
                    "Quantity", "Discount", "Profit",
                ],
                "Value": [
                    ship_mode, segment, region,
                    category, sub_category,
                    city, state,
                    str(quantity), f"{discount:.0%}", f"${profit:,.2f}",
                ],
            }
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(
                summary_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Parameter": st.column_config.TextColumn("Parameter", width="medium"),
                    "Value": st.column_config.TextColumn("Value", width="medium"),
                },
            )

            # Feature match info
            matched = [col for col in dummy_values if col in feature_columns]
            unmatched = [col for col in dummy_values if col not in feature_columns]

            if matched:
                st.markdown(
                    f"<p style='color: #10B981; font-size: 0.8rem; margin-top: 1rem;'>"
                    f"✅ <strong>{len(matched)}</strong> of {len(dummy_values)} "
                    f"categorical features matched the training data.</p>",
                    unsafe_allow_html=True,
                )
            if unmatched:
                st.markdown(
                    f"<p style='color: #F59E0B; font-size: 0.8rem;'>"
                    f"⚠️ <strong>{len(unmatched)}</strong> features were not found in training columns "
                    f"(set to 0): <code>{', '.join(unmatched)}</code></p>",
                    unsafe_allow_html=True,
                )


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <div class="footer-text">
         <strong></strong>⚠️ Model Scope: This model was trained on historical U.S. sales data. Forecast results should be interpreted within the context of the U.S. market and may not generalize to other regions.<br>
        <span style="margin-top: 0.5rem; display: inline-block; color: #6B7280;">
            <span style="
                font-weight: 800;
                background: linear-gradient(135deg, #6C63FF, #00D4AA);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">Vinayak</span>
        </span><br>
        <span style="color: #4B5563; font-size: 0.7rem;">© 2026 | Data Science & ML</span>
    </div>
</div>
""", unsafe_allow_html=True)

