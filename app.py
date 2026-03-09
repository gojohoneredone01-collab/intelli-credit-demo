import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="CredIntel AI",
    page_icon="🏦",
    layout="wide"
)

# -----------------------
# HEADER
# -----------------------

st.markdown("""
<style>
.big-title {
    font-size:42px !important;
    font-weight:700;
}
.subtitle {
    font-size:18px;
    color:gray;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🏦 CredIntel AI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Corporate Credit Decisioning Platform</p>', unsafe_allow_html=True)

st.write("Smarter, faster, and explainable credit appraisal for modern lending teams.")

st.markdown("---")

# -----------------------
# DATA INGESTOR
# -----------------------

st.header("📂 Data Ingestor")

col1, col2 = st.columns(2)

with col1:
    company = st.text_input("Company Name")
    sector = st.text_input("Sector")

with col2:
    requested_loan = st.text_input("Requested Loan Amount")

st.subheader("Upload Business Documents")

gst_file = st.file_uploader("Upload GST Filing", type=["pdf","csv"])
bank_file = st.file_uploader("Upload Bank Statement", type=["pdf","csv"])
annual_file = st.file_uploader("Upload Annual Report", type=["pdf"])
financial_file = st.file_uploader("Upload Financial Statement", type=["pdf","csv"])

# -----------------------
# RESEARCH AGENT
# -----------------------

st.markdown("---")
st.header("🔎 Research Agent")

news_input = st.text_area("Company News / Research Notes")

legal_input = st.text_area("Legal Disputes / Litigation Notes")

sector_input = st.text_area("Sector Trends")

officer_notes = st.text_area("Credit Officer Notes")

# -----------------------
# RUN ANALYSIS BUTTON
# -----------------------

st.markdown("---")
st.header("⚙ Recommendation Engine")

run_analysis = st.button("Generate Credit Decision")

# -----------------------
# ANALYSIS LOGIC
# -----------------------

if run_analysis:

    score = 80
    warnings = []
    reasons = []

    legal = legal_input.lower()
    sector_t = sector_input.lower()
    notes = officer_notes.lower()
    news = news_input.lower()

    # Legal risk
    if "litigation" in legal or "case" in legal or "dispute" in legal:
        score -= 20
        warnings.append("Legal dispute detected")

    # Sector risk
    if "slowdown" in sector_t or "decline" in sector_t:
        score -= 15
        warnings.append("Sector slowdown detected")

    # Operational risk
    if "40% capacity" in notes:
        score -= 15
        warnings.append("Factory operating below normal capacity")

    # Financial risk
    if "debt increasing" in notes:
        score -= 15
        warnings.append("Debt increasing rapidly")

    # News risk
    if "fraud" in news or "default" in news:
        score -= 20
        warnings.append("Negative company news detected")

    # Document count
    uploaded_docs = [gst_file, bank_file, annual_file, financial_file]
    uploaded_count = sum(x is not None for x in uploaded_docs)

    if uploaded_count < 2:
        score -= 10
        warnings.append("Limited supporting documents")

    # Clamp score
    if score < 0:
        score = 0

    # Decision
    if score >= 75:
        decision = "APPROVE"
        interest = "Base + 1%"
        loan_amount = "80% of requested limit"
    elif score >= 55:
        decision = "REVIEW"
        interest = "Base + 3%"
        loan_amount = "60% of requested limit"
    else:
        decision = "REJECT"
        interest = "Base + 5%"
        loan_amount = "High risk"

    # Positive reasons
    if uploaded_count >= 3:
        reasons.append("Sufficient supporting documents uploaded")

    if "litigation" not in legal:
        reasons.append("No major litigation found")

    if "slowdown" not in sector_t:
        reasons.append("Sector demand stable")

    if "fraud" not in news:
        reasons.append("No severe adverse news detected")

    # -----------------------
    # RESULTS DASHBOARD
    # -----------------------

    st.markdown("---")
    st.header("📊 Credit Decision Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Credit Score", score)
    c2.metric("Recommended Loan", loan_amount)
    c3.metric("Interest Rate", interest)
    c4.metric("Documents Reviewed", uploaded_count)

    st.subheader("Final Decision")

    if decision == "APPROVE":
        st.success(decision)
    elif decision == "REVIEW":
        st.warning(decision)
    else:
        st.error(decision)

    # -----------------------
    # EXPLAINABLE AI
    # -----------------------

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Explainable AI")

        if reasons:
            for r in reasons:
                st.write("✔", r)

    with col2:
        st.subheader("Early Warning Signals")

        if warnings:
            for w in warnings:
                st.warning(w)
        else:
            st.success("No major risk signals")

    st.subheader("Key Risk Summary")

    if warnings:
        st.info(" | ".join(warnings))
    else:
        st.info("No significant risk signals detected")

    # -----------------------
    # RISK RADAR
    # -----------------------

    st.subheader("Risk Radar Visualization")

    financial_risk = 100 - score
    legal_risk = 70 if "litigation" in legal else 20
    sector_risk = 60 if "slowdown" in sector_t else 25
    operational_risk = 65 if "40% capacity" in notes else 30

    labels = ["Financial", "Legal", "Sector", "Operational"]
    values = [financial_risk, legal_risk, sector_risk, operational_risk]

    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, polar=True)

    angles = [0,1.57,3.14,4.71]
    values_cycle = values + [values[0]]
    angles_cycle = angles + [angles[0]]

    ax.plot(angles_cycle, values_cycle)
    ax.fill(angles_cycle, values_cycle, alpha=0.2)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels)

    st.pyplot(fig)

    # -----------------------
    # CAM GENERATOR
    # -----------------------

    st.subheader("Smart Credit Appraisal Memo")

    cam = f"""
Company Overview
{company} operates in the {sector} sector.

Financial Analysis
Credit score generated: {score}.
Documents reviewed: {uploaded_count}.

Risk Factors
{', '.join(warnings) if warnings else 'No major risk factors detected'}

Sector Analysis
{sector_input}

Final Recommendation
Decision: {decision}
Suggested Loan: {loan_amount}
Interest Rate: {interest}
"""

    st.text_area("Generated CAM", cam, height=250)

st.markdown("---")
st.caption("CredIntel AI • Explainable Credit Decisioning Platform")
