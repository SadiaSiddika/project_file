# train_model.py
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression

# ---------------- LOAD DATA ----------------
DATA_PATH = r"C:\Users\Asus\Downloads\thyroid\Thyroid_Diff.csv"
df = pd.read_csv(DATA_PATH)

# ---------------- STANDARDIZE COLUMN NAMES ----------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# ---------------- FIX COLUMN NAMES / TYPO ----------------
df = df.rename(columns={
    "gender": "sex",
    "hx_radiothreapy": "hx_radiotherapy",
    "physical_examination": "physical_exam"
})

# ---------------- CHECK TARGET ----------------
if "recurrence" not in df.columns:
    raise ValueError("Target column 'recurrence' not found!")

df = df.dropna(subset=["recurrence"])

# ---------------- SPLIT FEATURES & TARGET ----------------
y = df["recurrence"]
X = df.drop(columns=["recurrence"])

# ---------------- ENCODE CATEGORICAL FEATURES ----------------
label_encoders = {}
for col in X.columns:
    if X[col].dtype == "object":
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le

# ---------------- SCALE AGE ----------------
if "age" not in X.columns:
    raise ValueError("Column 'age' not found!")

scaler = StandardScaler()
X["age"] = scaler.fit_transform(X[["age"]])

# ---------------- TRAIN STACKING MODEL ----------------
model = StackingClassifier(
    estimators=[
        ("rf", RandomForestClassifier(n_estimators=200, random_state=42)),
        ("gb", GradientBoostingClassifier(random_state=42))
    ],
    final_estimator=LogisticRegression(max_iter=1000)
)
model.fit(X, y)

# ---------------- SAVE MODEL, PREPROCESSORS & FEATURE ORDER ----------------
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))
pickle.dump(label_encoders, open("encoders.pkl", "wb"))
feature_order = X.columns.tolist()
pickle.dump(feature_order, open("feature_order.pkl", "wb"))

print("✅ TRAINING COMPLETE — model.pkl, scaler.pkl, encoders.pkl, feature_order.pkl SAVED")