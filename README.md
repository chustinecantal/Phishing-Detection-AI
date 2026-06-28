# Intelligent Phishing Detection System

A machine learning system that detects phishing URLs 
using Random Forest classification, deployed as a 
REST API with FastAPI.

---

## Project Structure
\```
phishing-detection-ai/
├── data/
│   ├── raw/          
│   └── processed/   
├── notebooks/
│   └── 01_eda.ipynb  
├── model/
│   ├── train.py      
│   ├── evaluate.py  
│   └── phishing_model.pkl 
├── api/
│   └── main.py       
├── experiments/
│   └── results.md    
└── requirements.txt
\```

## Dataset
- 235,795 URLs (legitimate and phishing)
- 56 features per URL
- Source: phishing_urls.csv

---

## Approach

### EDA Findings
- Dataset: 57.2% legitimate, 42.8% phishing
- No duplicates or null values
- Phishing URLs are longer on average (45.7 vs 26.2 chars)
- Phishing URLs have more special characters and digits

### Feature Engineering
- Removed raw text columns (URL, Domain, Title, FILENAME)
- Selected 20 URL-based features only
- Reason: page-based features require visiting potentially
  dangerous URLs which is impractical in real deployment
- Removed IsHTTPS: modern phishing sites increasingly
  use HTTPS making it an unreliable signal

### Model Training
Two experiments conducted:

| Experiment | Features | Accuracy | Phishing Recall |
|------------|----------|----------|-----------------|
| Exp 1 | 21 (with IsHTTPS) | 99.65% | 99.40% |
| Exp 2 | 20 (without IsHTTPS) | 99.56% | 99.43% |

**Experiment 2 chosen** because:
- Removes reliance on IsHTTPS (unreliable signal)
- Higher Phishing Recall (99.43% vs 99.40%)
- More balanced feature importance

### Model Evaluation
- Algorithm: Random Forest (100 estimators)
- Accuracy: 99.56%
- Phishing Precision: 99.54%
- Phishing Recall: 99.43%
- Phishing F1: 99.48%

Recall prioritized over Precision because missing a 
phishing site is more dangerous than wrongly flagging 
a legitimate site.

---

## API Usage

### Run the API
cd api
uvicorn main:app --reload

### Endpoints
GET  /         → health check
GET  /health   → model status
POST /predict  → classify URL features

### Example Request
POST http://localhost:8000/predict

{
  "URLLength": 25.0,
  "DomainLength": 18.0,
  "IsDomainIP": 0.0,
  "TLDLength": 3.0,
  "NoOfSubDomain": 1.0,
  "NoOfLettersInURL": 12.0,
  "LetterRatioInURL": 0.48,
  "NoOfDegitsInURL": 0.0,
  "DegitRatioInURL": 0.0,
  "NoOfEqualsInURL": 0.0,
  "NoOfQMarkInURL": 0.0,
  "NoOfAmpersandInURL": 0.0,
  "NoOfOtherSpecialCharsInURL": 1.0,
  "SpacialCharRatioInURL": 0.04,
  "CharContinuationRate": 1.0,
  "URLCharProb": 0.063854666,
  "HasObfuscation": 0.0,
  "NoOfObfuscatedChar": 0.0,
  "ObfuscationRatio": 0.0,
  "TLDLegitimateProb": 0.5229071
}

### Example Response
{
  "prediction": "Legitimate",
  "confidence": "100.0%",
  "is_phishing": false
}

---

## Known Limitations
- API accepts pre-computed features, not raw URLs
- Feature extraction from raw URLs requires matching
  the original dataset's computation methods
- Future work: build custom feature extractor from scratch

---

## Resume Bullet
Developed a machine learning phishing detection system 
using Random Forest on 235,795 URLs, achieving 99.56% 
accuracy and 99.43% phishing recall, deployed as a 
REST API with FastAPI.

---

## Tech Stack
- Python
- pandas, scikit-learn, numpy
- matplotlib, seaborn
- FastAPI, uvicorn
- joblib
