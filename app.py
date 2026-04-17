import streamlit as st
import pickle
import pandas as pd
import requests
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Thyroid Cancer Recurrence Risk Prediction System",
    page_icon="🦋",
    layout="wide"
)

# ---------------- GET PATIENT NAME ----------------
try:
    query_params = st.query_params
    patient_name = query_params.get("patient", "Unknown")
except:
    patient_name = "Unknown"

# ✅ SHOW NAME CLEARLY
st.sidebar.success(f"👤 Patient: {patient_name}")

# ---------------- LOAD MODEL ----------------
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

with open("feature_order.pkl", "rb") as f:
    feature_order = pickle.load(f)

# ---------------- SIDEBAR ----------------
st.sidebar.header("📋 Input Patient Clinical Feature")

age = st.sidebar.number_input("Age", 0, 120, 45)
sex = st.sidebar.selectbox("Gender", ["F", "M"])
smoking = st.sidebar.selectbox("Smoking", ["No", "Yes"])
hx_smoking = st.sidebar.selectbox("Hx Smoking", ["No", "Yes"])
hx_radiotherapy = st.sidebar.selectbox("Hx Radiotherapy", ["No", "Yes"])
thyroid_function = st.sidebar.selectbox("Thyroid Function", ["Euthyroid", "Hypothyroid", "Hyperthyroid"])
physical_exam = st.sidebar.selectbox("Physical Examination", ["Diffuse goiter", "Nodular goiter", "Normal"])
adenopathy = st.sidebar.selectbox("Adenopathy", ["No","Right","Posterior","Bilateral","Left","Extensive"])
pathology = st.sidebar.selectbox("Pathology", ["Papillary", "Follicular", "Medullary", "Anaplastic"])
focality = st.sidebar.selectbox("Focality", ["Unifocal", "Multi-Focal"])
risk = st.sidebar.selectbox("Risk", ["Low", "Intermediate", "High"])
t = st.sidebar.selectbox("T", ["T1a", "T1b", "T2", "T3", "T4"])
n = st.sidebar.selectbox("N", ["N0", "N1a", "N1b"])
m = st.sidebar.selectbox("M", ["M0", "M1"])
stage = st.sidebar.selectbox("Stage", ["I", "II", "III", "IV"])
response = st.sidebar.selectbox("Response", ["Excellent", "Biochemical Incomplete", "Structural Incomplete", "Indeterminate"])

predict_btn = st.sidebar.button("🔍 Predict")

# ---------------- MAIN ----------------
st.title("🦋 Thyroid Cancer Recurrence Risk Prediction System")

if predict_btn:

    st.subheader(f"📌 Patient Name: {patient_name}")

    input_data = pd.DataFrame([[age, sex, smoking, hx_smoking, hx_radiotherapy,
                                thyroid_function, physical_exam, adenopathy,
                                pathology, focality, risk, t, n, m, stage, response]],
                              columns=["age","sex","smoking","hx_smoking","hx_radiotherapy",
                                       "thyroid_function","physical_exam","adenopathy",
                                       "pathology","focality","risk","t","n","m","stage","response"])

    # Encoding
    for col in input_data.columns:
        if col in label_encoders:
            le = label_encoders[col]
            val = input_data.at[0, col]
            input_data.at[0, col] = le.transform([val])[0] if val in le.classes_ else -1

    input_data["age"] = scaler.transform(input_data[["age"]])
    input_data = input_data[feature_order]

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1] * 100

    st.success(f"Prediction: {'Yes' if prediction == 1 else 'No'}")
    st.info(f"Probability: {probability:.2f}%")

    # SAVE HISTORY
    try:
        payload = {
            "patient_name": patient_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prediction": "Yes" if prediction == 1 else "No",
            "probability": round(probability, 2)
        }

        requests.post("http://127.0.0.1:5000/save_history", json=payload)

        st.success("✅ Saved to database")

    except Exception as e:
        st.error(f"Error: {e}")
