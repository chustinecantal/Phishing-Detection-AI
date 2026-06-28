from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

# ================================
# Load model at startup
# ================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model    = joblib.load(os.path.join(BASE_DIR, 'model', 'phishing_model.pkl'))
features = joblib.load(os.path.join(BASE_DIR, 'model', 'feature_names.pkl'))

# ================================
# App setup
# ================================
app = FastAPI(
    title="Phishing Detection API",
    description="Detects whether a URL is phishing or legitimate based on pre-computed URL features",
    version="1.0.0"
)

# ================================
# Input model — accepts pre-computed features
# ================================
class URLFeatures(BaseModel):
    URLLength                 : float
    DomainLength              : float
    IsDomainIP                : float
    TLDLength                 : float
    NoOfSubDomain             : float
    NoOfLettersInURL          : float
    LetterRatioInURL          : float
    NoOfDegitsInURL           : float
    DegitRatioInURL           : float
    NoOfEqualsInURL           : float
    NoOfQMarkInURL            : float
    NoOfAmpersandInURL        : float
    NoOfOtherSpecialCharsInURL: float
    SpacialCharRatioInURL     : float
    CharContinuationRate      : float
    URLCharProb               : float
    HasObfuscation            : float
    NoOfObfuscatedChar        : float
    ObfuscationRatio          : float
    TLDLegitimateProb         : float

# ================================
# Endpoints
# ================================
@app.get("/")
def root():
    return {"message": "Phishing Detection API is running!"}

@app.get("/health")
def health():
    return {
        "status"  : "healthy",
        "model"   : "Random Forest",
        "features": len(features)
    }

@app.post("/predict")
def predict(input: URLFeatures):
    try:
        feature_dict  = input.dict()
        feature_array = pd.DataFrame([feature_dict])[features]

        prediction     = model.predict(feature_array)[0]
        confidence     = model.predict_proba(feature_array)[0]

        label          = "Legitimate" if prediction == 1 else "Phishing"
        confidence_pct = round(float(max(confidence)) * 100, 2)

        return {
            "prediction" : label,
            "confidence" : f"{confidence_pct}%",
            "is_phishing": bool(prediction == 0)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))