# Phishing Detection - Experiment Results

## Dataset
- Source: phishing_urls.csv
- Total URLs: 235,795
- Phishing (0): 100,945 (42.8%)
- Legitimate (1): 134,850 (57.2%)
- Duplicates: 0
- Null values: 0

## Feature Engineering Decisions
- Dropped raw text columns: FILENAME, URL, Title, Domain, TLD
- Reason: model cannot process raw text directly
- Started with 50 numeric features
- Reduced to URL-only features (no page visit required)
- Reason: page-based features require visiting potentially 
  dangerous URLs which is impractical in real deployment

## Experiments

### Experiment 1 — All 21 URL Features (with IsHTTPS)
- Accuracy:          99.65%
- Phishing Recall:   99.40%
- Phishing F1:       99.59%
- Issue: IsHTTPS dominated at 37.6% feature importance
- Problem: modern phishing sites increasingly use HTTPS
  making this an unreliable signal

### Experiment 2 — 20 URL Features (without IsHTTPS) - FINAL
- Accuracy:          99.56%
- Phishing Recall:   99.43%
- Phishing F1:       99.48%
- Top features: LetterRatioInURL, SpacialCharRatioInURL,
  URLLength, NoOfOtherSpecialCharsInURL
- Feature importance more balanced (top feature 21% vs 37%)

## Final Model Decision
Experiment 2 chosen because:
1. Removes reliance on IsHTTPS which is unreliable 
   for modern phishing sites
2. Phishing Recall improved slightly (99.40% → 99.43%)
3. Model learns balanced URL pattern combinations
4. More robust for real world deployment

## Key Insight
Missing a phishing site is more dangerous than wrongly 
flagging a legitimate site. Therefore Recall was 
prioritized over Precision in model selection.

## Saved Files
- model/phishing_model.pkl   → trained Random Forest
- model/feature_names.pkl    → list of 20 expected features

## Known Limitations
- API accepts pre-computed features, not raw URLs
- Feature extraction from raw URLs could not perfectly
  recreate the original dataset's computation methods
- IsHTTPS removed because modern phishing sites 
  increasingly use HTTPS — unreliable signal

## Future Improvements
- Build custom dataset from scratch with own feature extractor
- Train and deploy using same feature extraction code
- Add more models for comparison (XGBoost, Logistic Regression)
- Add raw URL input support once feature extractor is built