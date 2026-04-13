import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Customer Churn Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# LOAD MODEL
# -------------------------------
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# -------------------------------
# CUSTOM CSS
# -------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
    color: #0f172a;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Hero */
.hero-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #312e81 100%);
    padding: 2rem 2.2rem;
    border-radius: 24px;
    color: white;
    box-shadow: 0 20px 50px rgba(15, 23, 42, 0.25);
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: 2.15rem;
    font-weight: 800;
    margin-bottom: 0.45rem;
}
.hero-subtitle {
    font-size: 1rem;
    color: #cbd5e1;
    line-height: 1.7;
}

/* Cards */
.glass-card {
    background: rgba(255,255,255,0.86);
    border: 1px solid rgba(255,255,255,0.6);
    backdrop-filter: blur(12px);
    padding: 1.4rem;
    border-radius: 22px;
    box-shadow: 0 10px 30px rgba(2, 6, 23, 0.08);
    margin-bottom: 1rem;
}

.section-title {
    font-size: 1.12rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 1rem;
}

/* Labels visible */
.stSelectbox label,
.stNumberInput label,
.stSlider label {
    color: #0f172a !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

/* Selectbox / input box container */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="base-input"] > div {
    border-radius: 12px !important;
    border: 1px solid #cbd5e1 !important;
    background-color: #ffffff !important;
    min-height: 46px !important;
    color: #0f172a !important;
}

/* Selected text visible */
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #0f172a !important;
}

/* Dropdown options */
ul[role="listbox"] li,
ul[role="listbox"] li span {
    color: #0f172a !important;
    background-color: #ffffff !important;
}

/* Hover on dropdown */
ul[role="listbox"] li:hover {
    background-color: #eef2ff !important;
    color: #0f172a !important;
}

/* Inputs visible */
input, textarea {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
}

/* Placeholder */
input::placeholder,
textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

/* Select dropdown icon */
div[data-baseweb="select"] svg {
    fill: #334155 !important;
}

/* Buttons */
.stFormSubmitButton > button,
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: white !important;
    border: none;
    padding: 0.9rem 1rem;
    font-size: 1rem;
    font-weight: 700;
    border-radius: 14px;
    box-shadow: 0 10px 20px rgba(79, 70, 229, 0.28);
    transition: all 0.2s ease-in-out;
}

.stFormSubmitButton > button:hover,
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 28px rgba(79, 70, 229, 0.35);
}

/* KPI cards */
.kpi-card {
    background: white;
    border-radius: 20px;
    padding: 1.15rem;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
    border: 1px solid #e2e8f0;
    text-align: center;
}
.kpi-label {
    font-size: 0.9rem;
    color: #64748b;
    margin-bottom: 0.35rem;
}
.kpi-value {
    font-size: 1.65rem;
    font-weight: 800;
    color: #0f172a;
}

/* Insight boxes */
.info-box {
    background: #eff6ff;
    border-left: 5px solid #2563eb;
    padding: 1rem 1.1rem;
    border-radius: 16px;
    margin-top: 0.7rem;
    color: #1e3a8a;
    font-weight: 500;
    line-height: 1.6;
}

.success-box {
    background: #ecfdf5;
    border-left: 5px solid #10b981;
    padding: 1rem 1.1rem;
    border-radius: 16px;
    margin-top: 0.7rem;
    color: #065f46;
    font-weight: 500;
    line-height: 1.6;
}

.warn-box {
    background: #fff7ed;
    border-left: 5px solid #ea580c;
    padding: 1rem 1.1rem;
    border-radius: 16px;
    margin-top: 0.7rem;
    color: #9a3412;
    font-weight: 500;
    line-height: 1.6;
}

/* Prediction result cards */
.result-success {
    background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
    border-left: 6px solid #16a34a;
    color: #166534;
    padding: 1rem 1.2rem;
    border-radius: 18px;
    font-weight: 700;
    margin-top: 1rem;
}

.result-danger {
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
    border-left: 6px solid #dc2626;
    color: #991b1b;
    padding: 1rem 1.2rem;
    border-radius: 18px;
    font-weight: 700;
    margin-top: 1rem;
}

.custom-divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #cbd5e1, transparent);
    margin: 1.2rem 0 1.2rem 0;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HERO SECTION
# -------------------------------
st.markdown("""
<div class="hero-card">
    <div class="hero-title">Customer Churn Intelligence Dashboard</div>
    <div class="hero-subtitle">
        Analyze customer information, predict churn risk, and generate retention-focused insights.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# MAIN LAYOUT
# -------------------------------
left_col, right_col = st.columns([1.2, 0.8], gap="large")

with left_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Customer Input Details</div>', unsafe_allow_html=True)

    with st.form("churn_form"):
        c1, c2 = st.columns(2)

        with c1:
            gender = st.selectbox("Gender", ["Male", "Female"], help="Select the customer's gender.")
            SeniorCitizen = st.selectbox("Senior Citizen", [0, 1], help="0 = No, 1 = Yes")
            Partner = st.selectbox("Partner", ["Yes", "No"])
            Dependents = st.selectbox("Dependents", ["Yes", "No"])
            tenure = st.slider("Tenure (Months)", 0, 72, 12)
            PhoneService = st.selectbox("Phone Service", ["Yes", "No"])

        with c2:
            MultipleLines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
            InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
            Contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
            PaymentMethod = st.selectbox(
                "Payment Method",
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)"
                ]
            )
            MonthlyCharges = st.slider("Monthly Charges", 0, 150, 65)
            TotalCharges = st.number_input("Total Charges", min_value=0.0, value=1000.0, step=10.0)

        submitted = st.form_submit_button("Predict Customer Churn")

    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Decision Support Overview</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        This application helps evaluate whether a customer is at risk of leaving based on
        service usage, contract pattern, and billing behavior.
    </div>
    """, unsafe_allow_html=True)

    k1, k2 = st.columns(2)
    with k1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Primary Goal</div>
            <div class="kpi-value" style="font-size:1.1rem;">Churn Detection</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Business Focus</div>
            <div class="kpi-value" style="font-size:1.1rem;">Customer Retention</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="success-box">
        Use the prediction output to identify risky customers early and plan targeted retention actions.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warn-box">
        High churn probability may indicate dissatisfaction, weak engagement, or unsuitable contract conditions.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# PREDICTION OUTPUT
# -------------------------------
if submitted:
    input_dict = {
        "gender": gender,
        "SeniorCitizen": SeniorCitizen,
        "Partner": Partner,
        "Dependents": Dependents,
        "tenure": tenure,
        "PhoneService": PhoneService,
        "MultipleLines": MultipleLines,
        "InternetService": InternetService,
        "Contract": Contract,
        "PaymentMethod": PaymentMethod,
        "MonthlyCharges": MonthlyCharges,
        "TotalCharges": TotalCharges
    }

    input_df = pd.DataFrame([input_dict])
    input_df = pd.get_dummies(input_df)
    input_df = input_df.reindex(columns=columns, fill_value=0)

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    st.markdown("## Prediction Results")

    a, b, c = st.columns(3)

    with a:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Churn Probability</div>
            <div class="kpi-value">{probability * 100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with b:
        risk_level = "High" if probability > 0.7 else "Medium" if probability > 0.4 else "Low"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Risk Level</div>
            <div class="kpi-value">{risk_level}</div>
        </div>
        """, unsafe_allow_html=True)

    with c:
        decision = "Likely to Churn" if prediction == 1 else "Likely to Stay"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Prediction</div>
            <div class="kpi-value" style="font-size:1.2rem;">{decision}</div>
        </div>
        """, unsafe_allow_html=True)

    st.progress(float(probability))

    if prediction == 1:
        st.markdown("""
        <div class="result-danger">
            ⚠️ This customer is likely to churn. A proactive retention response is recommended.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-success">
            ✅ This customer is likely to stay. Current behavior appears comparatively stable.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Recommendation")

    if probability > 0.7:
        st.markdown("""
        <div class="warn-box">
            🔴 High Risk: Consider immediate intervention through personalized discounts,
            contract revision, priority support, or loyalty benefits.
        </div>
        """, unsafe_allow_html=True)
    elif probability > 0.4:
        st.markdown("""
        <div class="info-box">
            🟠 Medium Risk: Improve engagement with customized offers, service communication,
            and usage-based follow-up strategies.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
            🟢 Low Risk: Maintain customer satisfaction with consistent service quality
            and periodic value-based engagement.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Model Insight")

    if probability > 0.6:
        st.write("The customer profile shows stronger similarity to previously churned customers.")
    else:
        st.write("The customer profile is more aligned with retained customers in the historical data.")

    st.markdown("### Key Factors Influencing Prediction")

    try:
        importance = model.feature_importances_
        feat_imp = pd.Series(importance, index=columns).sort_values(ascending=False)
        top_features = feat_imp.head(10)

        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#4f46e5' if i < 3 else '#94a3b8' for i in range(len(top_features))]
        top_features.sort_values().plot(kind='barh', ax=ax, color=colors)

        ax.set_title("Top 10 Important Features", fontsize=14, fontweight='bold')
        ax.set_xlabel("Importance Score")
        ax.set_ylabel("")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.3)

        st.pyplot(fig, use_container_width=True)

    except Exception:
        st.info("Feature importance is not available for this model.")
