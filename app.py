import streamlit as st

st.title("Intelli Credit Demo")

company = st.text_input("Company Name")
sector = st.text_input("Sector")
loan = st.number_input("Loan Amount")

notes = st.text_area("Officer Notes")

if st.button("Analyze"):
    score = 70
    
    if loan > 10000000:
        score -= 20
        
    if "litigation" in notes.lower():
        score -= 15
        
    if score > 60:
        decision = "APPROVE"
    elif score > 40:
        decision = "REVIEW"
    else:
        decision = "REJECT"
        
    st.write("Risk Score:", score)
    st.write("Decision:", decision)
