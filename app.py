import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="CredIntel AI", layout="wide")

st.title("CredIntel AI - Corporate Credit Intelligence")

st.markdown("AI assisted credit appraisal prototype")

# -------------------------------
# COMPANY INFORMATION
# -------------------------------

st.header("Company Information")

company = st.text_input("Company Name")
sector = st.text_input("Sector")
loan_amount = st.number_input("Requested Loan Amount", value=1000000)

# -------------------------------
# STRUCTURED FINANCIAL DATA
# -------------------------------

st.header("Structured Financial Data")

revenue = st.number_input("Annual Revenue", value=0)
profit = st.number_input("Net Profit / Loss", value=0)
debt = st.number_input("Total Debt Outstanding", value=0)
gst_turnover = st.number_input("GST Turnover", value=0)

# -------------------------------
# DOCUMENT UPLOADS
# -------------------------------

st.header("Unstructured Documents")

annual_report = st.file_uploader("Upload Annual Report", type=["txt","pdf"])
financial_statement = st.file_uploader("Upload Financial Statement", type=["txt","pdf"])

# -------------------------------
# EXTERNAL INTELLIGENCE
# -------------------------------

st.header("External Intelligence")

news_reports = st.text_area("Sector News / Company News")
mca_filings = st.text_area("MCA Filing Observations")
legal_disputes = st.text_area("Legal Disputes (e-Courts)")

# -------------------------------
# PRIMARY INSIGHTS
# -------------------------------

st.header("Primary Insights")

factory_visit = st.text_area("Factory Visit Observations")
management_notes = st.text_area("Management Interview Notes")

# -------------------------------
# TEXT EXTRACTION FUNCTION
# -------------------------------

def extract_text(uploaded_file):

    if uploaded_file is None:
        return ""

    try:
        text = uploaded_file.read().decode("utf-8")
    except:
        text = ""

    return text.lower()

# -------------------------------
# CREDIT SCORING ENGINE
# -------------------------------

def calculate_score():

    score = 80
    reasons = []

    # financial checks

    if profit < 0:
        score -= 20
        reasons.append("Company reporting losses")

    if debt > revenue and revenue != 0:
        score -= 15
        reasons.append("Debt higher than revenue")

    if gst_turnover == 0:
        score -= 10
        reasons.append("GST turnover unavailable")

    # extract uploaded file text

    report_text = extract_text(annual_report)
    financial_text = extract_text(financial_statement)

    combined_text = (
        report_text +
        financial_text +
        news_reports +
        mca_filings +
        legal_disputes +
        factory_visit +
        management_notes
    ).lower()

    risk_keywords = {
        "litigation":20,
        "fraud":25,
        "loss":15,
        "default":25,
        "slowdown":10,
        "debt":10,
        "shutdown":20,
        "bankruptcy":30
    }

    for word, penalty in risk_keywords.items():

        if word in combined_text:
            score -= penalty
            reasons.append(f"Risk detected: {word}")

    return score, reasons

# -------------------------------
# DECISION ENGINE
# -------------------------------

if st.button("Generate Credit Decision"):

    score, reasons = calculate_score()

    if score >= 75:
        decision = "APPROVE"
        interest = "Base + 1%"
    elif score >= 55:
        decision = "REVIEW"
        interest = "Base + 3%"
    else:
        decision = "REJECT"
        interest = "High Risk Premium"

    st.subheader("Credit Analysis Result")

    col1, col2, col3 = st.columns(3)

    col1.metric("Credit Score", score)
    col2.metric("Decision", decision)
    col3.metric("Interest Rate", interest)

    st.subheader("Reasoning")

    for r in reasons:
        st.write("-", r)

    # -------------------------------
    # RISK RADAR
    # -------------------------------

    financial_risk = min(100, debt/(revenue+1)*50)
    legal_risk = 80 if "litigation" in legal_disputes.lower() else 20
    sector_risk = 60 if "slowdown" in news_reports.lower() else 30
    operational_risk = 60 if "capacity" in factory_visit.lower() else 30

    labels = ["Financial","Legal","Sector","Operational"]
    values = [financial_risk,legal_risk,sector_risk,operational_risk]

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
