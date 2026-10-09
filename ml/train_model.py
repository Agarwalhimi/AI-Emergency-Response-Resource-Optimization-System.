from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "emergencies.csv"
MODEL_FILE = BASE_DIR / "ml" / "emergency_model.joblib"

FEATURES = ["Type", "People", "Injury", "Fire", "MedicalCondition", "ResponseTime"]
TARGET = "Priority"


def build_pipeline() -> Pipeline:
    categorical = ["Type", "Injury", "Fire", "MedicalCondition"]
    numeric = ["People", "ResponseTime"]
    preprocess = ColumnTransformer([
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("numeric", "passthrough", numeric),
    ])
    model = RandomForestClassifier(n_estimators=120, random_state=42, max_depth=6)
    return Pipeline([("preprocess", preprocess), ("model", model)])


def train_model() -> float:
    df = pd.read_csv(DATA_FILE)
    X = df[FEATURES].copy()
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, pipeline.predict(X_test))
    joblib.dump({"pipeline": pipeline, "features": FEATURES, "accuracy": accuracy}, MODEL_FILE)
    return float(accuracy)


if __name__ == "__main__":
    acc = train_model()
    print(f"Model trained. Test accuracy: {acc:.2%}")
