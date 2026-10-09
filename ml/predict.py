from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_FILE = BASE_DIR / "ml" / "emergency_model.joblib"


def ensure_model():
    # Re-train automatically if the model is missing or incompatible with
    # the installed scikit-learn/joblib version. This keeps the college demo
    # self-contained after copying the project to another machine.
    if not MODEL_FILE.exists():
        from ml.train_model import train_model
        train_model()

def load_bundle():
    ensure_model()
    try:
        return joblib.load(MODEL_FILE)
    except Exception:
        from ml.train_model import train_model
        train_model()
        return joblib.load(MODEL_FILE)


def predict_priority(data: dict) -> str:
    bundle = load_bundle()
    row = {
        "Type": data["Type"],
        "People": int(data["People"]),
        "Injury": data["Injury"],
        "Fire": data["Fire"],
        "MedicalCondition": data["MedicalCondition"],
        "ResponseTime": int(data.get("ResponseTime", 15)),
    }
    frame = pd.DataFrame([row])
    return str(bundle["pipeline"].predict(frame)[0])


def model_accuracy() -> float:
    return float(load_bundle()["accuracy"])
