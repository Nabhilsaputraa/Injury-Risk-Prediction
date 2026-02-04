import joblib
import pandas as pd

proprocessor = joblib.load("artifacts/proprocessor.joblib")
model = joblib.load("artifacts/random_forest.joblib")

def risk_category(prob):
    if prob < 0.4:
        return "Low"
    elif prob < 0.65:
        return "Medium"
    else:
        return "High"

def predict_risk(data: dict):
    df = pd.DataFrame([data])

    df["Training_Load"] = (
        df["Training_Frequency"]
        * df["Training_Duration"]
        * df["Training_Intensity"]
    )

    df["Recovery_Quality"] = df["Sleep_Hours"] * df["Recovery_Time"]
    df["Physical_Imbalance"] = (
        df["Muscle_Asymmetry"] / (df["Flexibility_Score"] + 1)
    )

    X = proprocessor.transform(df)
    prediction = model.predict(X)[0]
    proba = model.predict_proba(X)[0][1]

    return {
        "injury_risk": int(prediction),
        "risk_level": risk_category(proba),
        "confidence": round(float(proba), 3)
    }
