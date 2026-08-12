from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from pathlib import Path

import joblib
import pandas as pd
import numpy as np
import shap


BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

MODEL_PATH = MODELS_DIR / "fraud_detection_model.pkl"
FEATURE_NAMES_PATH = MODELS_DIR / "feature_names.pkl"


model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURE_NAMES_PATH)

explainer = shap.TreeExplainer(model)

FRAUD_THRESHOLD = 0.55


app = FastAPI(
    title="Explainable Fraud Detection API",
    description=(
        "Fraud detection using a tuned Random Forest "
        "with SHAP model explainability."
    ),
    version="2.0.0"
)


class Transaction(BaseModel):
    features: Dict[str, float]


@app.get("/")
def root():
    return {
        "message": "Explainable Fraud Detection API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": True,
        "model": "Tuned Random Forest",
        "threshold": FRAUD_THRESHOLD,
        "number_of_features": len(feature_names)
    }


@app.post("/predict")
def predict_fraud(transaction: Transaction):

    try:
        received = set(transaction.features.keys())
        expected = set(feature_names)

        missing = expected - received
        unexpected = received - expected

        if missing:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "Missing required features",
                    "missing_features": sorted(missing)
                }
            )

        if unexpected:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "Unexpected features supplied",
                    "unexpected_features": sorted(unexpected)
                }
            )

        # These are already processed/model-ready features.
        input_df = pd.DataFrame(
            [transaction.features],
            columns=feature_names
        )

        fraud_probability = model.predict_proba(
            input_df
        )[0, 1]

        prediction = int(
            fraud_probability >= FRAUD_THRESHOLD
        )

        shap_values = explainer.shap_values(input_df)

        if (
            isinstance(shap_values, np.ndarray)
            and shap_values.ndim == 3
        ):
            fraud_shap_values = shap_values[0, :, 1]
        else:
            fraud_shap_values = shap_values[1][0]

        explanation_df = pd.DataFrame({
            "feature": feature_names,
            "model_ready_value": input_df.iloc[0].values,
            "shap_value": fraud_shap_values
        })

        explanation_df["absolute_shap"] = (
            explanation_df["shap_value"].abs()
        )

        explanation_df = explanation_df.sort_values(
            "absolute_shap",
            ascending=False
        )

        explanations = []

        for _, row in explanation_df.head(5).iterrows():

            shap_value = float(row["shap_value"])

            explanations.append({
                "feature": row["feature"],
                "shap_value": round(shap_value, 6),
                "direction": (
                    "increases fraud risk"
                    if shap_value > 0
                    else "reduces fraud risk"
                )
            })

        return {
            "prediction": prediction,
            "classification": (
                "Fraudulent"
                if prediction == 1
                else "Legitimate"
            ),
            "fraud_probability": round(
                float(fraud_probability),
                4
            ),
            "decision_threshold": FRAUD_THRESHOLD,
            "top_explanations": explanations
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )