import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# ---------------- LOAD DATA ----------------
DATA_PATH = r"C:\Users\Asus\Downloads\thyroid\Thyroid_Diff.csv"
df = pd.read_csv(DATA_PATH)

# ---------------- CLEAN ----------------
df.columns = df.columns.str.strip()

# ---------------- TARGET ----------------
df = df.rename(columns={"Recurred": "target"})

X = df.drop("target", axis=1)
y = df["target"]

# ---------------- COLUMNS ----------------
cat_cols = X.select_dtypes(include="object").columns.tolist()
num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

# ---------------- PREPROCESS ----------------
preprocess = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ("num", StandardScaler(), num_cols)
])

# ---------------- MODEL ----------------
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

# ---------------- PIPELINE ----------------
clf = Pipeline([
    ("preprocess", preprocess),
    ("model", model)
])

# ---------------- TRAIN ----------------
clf.fit(X, y)

# ---------------- SAVE ----------------
pickle.dump(clf, open("model.pkl", "wb"))

print("✅ Model trained and saved successfully!")