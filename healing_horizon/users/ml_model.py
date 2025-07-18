import joblib
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

MODEL_PATH = Path(__file__).parent / "assessment_model.joblib"

def train_model():
    # Update the number of features to match your actual assessment
    NUM_FEATURES = 22  # Change this to match your actual number of questions

    # Simulate more data and balance classes
    X = np.random.rand(1000, NUM_FEATURES) * 4  # More samples
    y = np.tile(np.arange(5), 200)  # 5 classes, balanced

    # Shuffle data
    idx = np.random.permutation(len(y))
    X, y = X[idx], y[idx]

    # Split for quick accuracy check (not used in production)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    # Optional: print accuracy for debugging
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Training accuracy (simulated): {acc:.2f}")

    joblib.dump(model, MODEL_PATH)
    return model

def predict_stress_level(answers):
    if not MODEL_PATH.exists():
        model = train_model()
    else:
        model = joblib.load(MODEL_PATH)

    answers_array = np.array(answers).reshape(1, -1)

    if answers_array.shape[1] != model.n_features_in_:
        raise ValueError(
            f"Model expects {model.n_features_in_} features, "
            f"but got {answers_array.shape[1]} features. "
            "Please ensure the number of assessment questions matches the trained model."
        )

    prediction = model.predict(answers_array)
    proba = model.predict_proba(answers_array)[0]
    pred_class = prediction[0]
    pred_prob = proba[pred_class] if pred_class < len(proba) else max(proba)
    return pred_class, pred_prob