import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("./notebooks/adr_risk_model.pkl")

st.set_page_config(page_title="ADR Risk Predictor", layout="centered")

st.title("💊 ADR Risk Prediction System")
st.markdown("### Predict Adverse Drug Reaction Risk (DOXORUBICIN)")

# Sidebar
st.sidebar.header("Patient Input")

age = st.sidebar.slider("Age", 1, 100, 50)
sex = st.sidebar.selectbox("Sex", ["Male", "Female"])
year = st.sidebar.selectbox("Report Year", [2013, 2014, 2015])

# Convert sex
sex_val = 1 if sex == "Male" else 2

# Input DataFrame
input_data = pd.DataFrame({
    "Age": [age],
    "Sex": [sex_val],
    "Year": [year]
})

st.subheader("📋 Input Data")
st.write(input_data)

if st.button("Predict ADR Risk"):
    
    prob = model.predict_proba(input_data)[0][1]
    
    threshold = 0.2
    prediction = 1 if prob > threshold else 0

    st.subheader("📊 Prediction Result")

    if prediction == 1:
        st.error(f"⚠️ High Risk of ADR\n\nProbability: {prob:.2f}")
    else:
        st.success(f"✅ Low Risk of ADR\n\nProbability: {prob:.2f}")

    # Simple interpretation
    st.subheader("🧠 Model Insight")

    if age > 60:
        st.write("🔴 Higher age increases ADR risk")
    if sex == "Female":
        st.write("🟡 Gender may influence ADR risk")
    if year < 2014:
        st.write("🔵 Earlier reports show slight variation")

# Footer
st.markdown("---")
st.markdown("Developed for Pharmacovigilance Analysis Project 🚀")