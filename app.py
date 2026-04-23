import streamlit as st
import pickle
import pandas as pd
import requests
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Thyroid Prediction System", layout="wide")

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))

# ---------------- INPUT ----------------
st.sidebar.header("Patient Input")

patient_name = st.sidebar.text_input("Patient Name")

age = st.sidebar.number_input("Age", 0, 120, 45)
gender = st.sidebar.selectbox("Gender", ["F", "M"])
smoking = st.sidebar.selectbox("Smoking", ["No", "Yes"])
hx_smoking = st.sidebar.selectbox("Hx Smoking", ["No", "Yes"])
hx_radiotherapy = st.sidebar.selectbox("Hx Radiothreapy", ["No", "Yes"])

thyroid_function = st.sidebar.selectbox(
    "Thyroid Function",
    ["Euthyroid", "Hypothyroid", "Clinical Hyperthyroidism",
     "Subclinical Hypothyroidism", "Hyperthyroid"]
)

physical_exam = st.sidebar.selectbox(
    "Physical Examination",
    ["Diffuse goiter", "Single nodular goiter-left",
     "Single nodular goiter-right", "Normal",
     "Multinodular goiter"]
)

adenopathy = st.sidebar.selectbox(
    "Adenopathy",
    ["No","Right","Posterior","Bilateral","Left","Extensive"]
)

pathology = st.sidebar.selectbox(
    "Pathology",
    ["Papillary", "Follicular", "Micropapillary", "Hurthel cell"]
)

focality = st.sidebar.selectbox("Focality", ["Unifocal", "Multi-Focal"])
risk = st.sidebar.selectbox("Risk", ["Low", "Intermediate", "High"])

t = st.sidebar.selectbox("T", ["T1a", "T1b", "T2", "T3a", "T3b", "T4a", "T4b"])
n = st.sidebar.selectbox("N", ["N0", "N1a", "N1b"])
m = st.sidebar.selectbox("M", ["M0", "M1"])
stage = st.sidebar.selectbox("Stage", ["I", "II", "III", "IV", "IVA", "IVB"])
response = st.sidebar.selectbox(
    "Response",
    ["Excellent", "Biochemical Incomplete",
     "Structural Incomplete", "Indeterminate"]
)

# ---------------- PREDICT ----------------
if st.sidebar.button("Predict"):

    if patient_name == "":
        st.warning("⚠ Please enter patient name")
    else:

        input_data = pd.DataFrame([{
            "Age": age,
            "Gender": gender,
            "Smoking": smoking,
            "Hx Smoking": hx_smoking,
            "Hx Radiothreapy": hx_radiotherapy,
            "Thyroid Function": thyroid_function,
            "Physical Examination": physical_exam,
            "Adenopathy": adenopathy,
            "Pathology": pathology,
            "Focality": focality,
            "Risk": risk,
            "T": t,
            "N": n,
            "M": m,
            "Stage": stage,
            "Response": response
        }])

        prediction = model.predict(input_data)[0]

        try:
            probability = model.predict_proba(input_data)[0][1] * 100
        except:
            probability = 0

        st.title("🦋 Thyroid Cancer Prediction Result")

        st.success(f"Prediction: {prediction}")
        st.info(f"Probability of Recurred: {probability:.2f}%")

        # ---------------- SAVE TO BACKEND ----------------
        payload = {
            "patient_name": patient_name,
            "timestamp": str(datetime.now()),
            "prediction": str(prediction),
            "probability": float(probability)
        }

        try:
            res = requests.post(
                "http://127.0.0.1:5000/save_history",
                json=payload
            )

            if res.status_code == 200:
                st.success("✅ Data saved to backend successfully!")
            else:
                st.error(f"❌ Backend error: {res.text}")

        except Exception as e:
            st.error(f"❌ Connection error: {e}")