import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Intelli Credit Engine", layout="wide")

st.title("Intelli Credit Engine")
st.write("AI-powered credit decisioning demo")

# ----------------------------
# INPUT SECTION
# ----------------------------
st.header("1. Data Ingestor")

company = st.text_input("Company Name")
sector = st.text_input("Sector")

gst_file = st.file_uploader("Upload GST Filing", type=["pdf", "csv"])
bank_file = st.file_uploader("Upload Bank Statement", type=["pdf", "csv"])
annual_file = st.file_uploader("Upload Annual Report", type=["pdf"])
financial_file = st.file_uploader("Upload Financial Statement", type=["pdf", "csv"])

st.header("2. Research Agent")

news_input = st.text_area("Company News / Research Notes", placeholder="Paste any news or research here")
legal_input = st.text_area("Legal Disputes / Litigation Notes", placeholder="Paste legal findings here")
sector_input = st.text_area("Sector Trends", placeholder="Write or paste sector trends")

officer_notes = st.text_area("Credit Officer Notes", placeholder="Example: Factory operating at 40% capacity")

# ----------------------------
# ANALYSIS
# ----------------------------
if st.button("Run Credit Analysis"):
    score = 80
    warnings = []

    # Legal risk
    if "litigation" in legal_input.lower() or "case" in legal_input.lower() or "dispute" in legal_input.lower():
        score -= 20
        warnings.append("Legal dispute detected")

    # Sector risk
    if "slowdown" in sector_input.lower() or "decline" in sector_input.lower() or "weak demand" in sector_input.lower():
        score -= 15
        warnings.append("Sector weakness detected")

    # Operational risk
    if "40% capacity" in officer_notes.lower() or "low capacity" in officer_notes.lower():
        score -= 15
        warnings.append("Factory operating below normal capacity")

    # Financial risk
    if "debt increasing" in officer_notes.lower() or "loss" in officer_notes.lower():
        score -= 15
        warnings.append("Financial stress warning detected")

    # Missing docs check
    uploaded_docs = [gst_file, bank_file, annual_file, financial_file]
    uploaded_count = sum(x is not None for x in uploaded_docs)

    if uploaded_count < 2:
        score -= 10
        warnings.append("Very limited document support uploaded")

    # Decision logic
    if score >= 75:
        decision = "APPROVE"
        interest = "Base + 1%"
        loan_amount = "80% of requested eligible limit"
    elif score >= 55:
        decision = "REVIEW"
        interest = "Base + 3%"
        loan_amount = "60% of requested eligible limit"
    else:
        decision = "REJECT"
        interest = "Base + 5%"
        loan_amount = "High risk - do not sanction full limit"

    # Explainable AI reasons
    reasons = []
    if score >= 75:
        reasons.append("Overall risk appears manageable")
    if uploaded_count >= 3:
        reasons.append("Sufficient supporting documents uploaded")
    if "litigation" not in legal_input.lower():
        reasons.append("No major litigation explicitly reported in input")
    if "slowdown" not in sector_input.lower():
        reasons.append("No severe sector slowdown explicitly reported")

    # ----------------------------
    # OUTPUT SECTION
    # ----------------------------
    st.header("3. Recommendation Engine")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Decision")
        st.write(decision)

        st.subheader("Credit Score")
        st.write(score)

        st.subheader("Recommended Loan Amount")
        st.write(loan_amount)

        st.subheader("Interest Rate")
        st.write(interest)

    with col2:
        st.subheader("Explainable AI")
        if reasons:
            for r in reasons:
                st.write("✔", r)
        else:
            st.write("No strong positive reasons found.")

    st.header("4. Early Warning Signals")
    if warnings:
        for w in warnings:
            st.write("⚠", w)
    else:
        st.write("No major early warning signals detected.")

    # ----------------------------
    # RISK RADAR
    # ----------------------------
    st.header("5. Risk Radar Visualization")

    financial_risk = max(0, 100 - score)
    legal_risk = 70 if "litigation" in legal_input.lower() else 20
    sector_risk = 60 if "slowdown" in sector_input.lower() else 25
    operational_risk = 65 if "40% capacity" in officer_notes.lower() else 30

    labels = ["Financial", "Legal", "Sector", "Operational"]
    values = [financial_risk, legal_risk, sector_risk, operational_risk]

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, polar=True)

    angles = [0, 1.57, 3.14, 4.71]
    values_cycle = values + [values[0]]
    angles_cycle = angles + [angles[0]]

    ax.plot(angles_cycle, values_cycle, linewidth=2)
    ax.fill(angles_cycle, values_cycle, alpha=0.25)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels)
    ax.set_title("Risk Radar")
    st.pyplot(fig)

    # ----------------------------
    # SMART CAM GENERATOR
    # ----------------------------
    st.header("6. Smart CAM Generator")

    cam = f"""
1. Company Overview
Company Name: {company}
Sector: {sector}

2. Financial Analysis
The system generated a credit score of {score}. Uploaded document count: {uploaded_count}.

3. Risk Factors
Key warnings: {', '.join(warnings) if warnings else 'No major warnings detected'}.

4. Sector Analysis
Sector notes considered: {sector_input if sector_input else 'No sector notes provided'}.

5. Final Recommendation
Decision: {decision}
Suggested Loan Amount: {loan_amount}
Interest Rate: {interest}
"""

    st.text_area("Generated CAM", cam, height=300)
