import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="CredIntel AI", layout="wide")

st.title("CredIntel AI – Credit Intelligence Prototype")

st.markdown("Paste all available company information below for credit analysis.")

# -----------------------------------
# BASIC COMPANY DETAILS
# -----------------------------------

company = st.text_input("Company Name")
sector = st.text_input("Sector")
loan_amount = st.number_input("Requested Loan Amount", value=1000000)

# -----------------------------------
# SINGLE DATA INPUT SOURCE
# -----------------------------------

st.header("Company Data Extraction")

company_data = st.text_area(
"Paste all extracted company data here (financial statements, annual report insights, legal notices, sector news, etc.)",
height=300
)

# -----------------------------------
# CREDIT SCORING ALGORITHM
# -----------------------------------

def calculate_credit_score(data):

    score = 80
    reasons = []

    text = data.lower()

    # keyword penalties
    risk_keywords = {
        "loss":15,
        "debt":10,
        "litigation":20,
        "fraud":25,
        "default":25,
        "slowdown":10,
        "shutdown":20,
        "bankruptcy":30,
        "legal notice":20
    }

    for word, penalty in risk_keywords.items():

        if word in text:
            score -= penalty
            reasons.append(f"Risk signal detected: {word}")

    return score, reasons


# -----------------------------------
# DECISION ENGINE
# -----------------------------------

if st.button("Generate Credit Decision"):

    score, reasons = calculate_credit_score(company_data)

    if score >= 75:
        decision = "APPROVE"
        interest = "Base + 1%"
    elif score >= 55:
        decision = "REVIEW"
        interest = "Base + 3%"
    else:
        decision = "REJECT"
        interest = "High Risk Premium"

    st.subheader("Credit Decision Result")

    col1, col2, col3 = st.columns(3)

    col1.metric("Credit Score", score)
    col2.metric("Decision", decision)
    col3.metric("Interest Rate", interest)

    st.subheader("Risk Explanation")

    if reasons:
        for r in reasons:
            st.write("-", r)
    else:
        st.write("No significant risk signals detected.")

    # -----------------------------------
    # RISK RADAR VISUALIZATION
    # -----------------------------------

    financial_risk = 70 if "debt" in company_data.lower() else 30
    legal_risk = 80 if "litigation" in company_data.lower() else 20
    sector_risk = 60 if "slowdown" in company_data.lower() else 30
    operational_risk = 60 if "capacity" in company_data.lower() else 30

    labels = ["Financial", "Legal", "Sector", "Operational"]
    values = [financial_risk, legal_risk, sector_risk, operational_risk]

    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111, polar=True)

    angles = [0,1.57,3.14,4.71]
    values_cycle = values + [values[0]]
    angles_cycle = angles + [angles[0]]

    ax.plot(angles_cycle, values_cycle)
    ax.fill(angles_cycle, values_cycle, alpha=0.2)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels)

    st.pyplot(fig)
