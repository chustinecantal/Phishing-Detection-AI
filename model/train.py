import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# ================================
# LABEL REFERENCE
# 0 = Phishing
# 1 = Legitimate
# ================================

def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'raw', 'phishing_urls.csv')
    df = pd.read_csv(data_path)
    print(f"Data loaded: {df.shape}")
    return df

def prepare_features(df):
    features = [
        'URLLength', 'DomainLength', 'IsDomainIP',
        'TLDLength', 'NoOfSubDomain',
        'NoOfLettersInURL', 'LetterRatioInURL',
        'NoOfDegitsInURL', 'DegitRatioInURL',
        'NoOfEqualsInURL', 'NoOfQMarkInURL',
        'NoOfAmpersandInURL', 'NoOfOtherSpecialCharsInURL',
        'SpacialCharRatioInURL', 'CharContinuationRate',
        'URLCharProb', 'HasObfuscation', 'NoOfObfuscatedChar',
        'ObfuscationRatio', 'TLDLegitimateProb'
    ]
    X = df[features]
    y = df['label']
    return X, y, features

def train_model(X_train, y_train):
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred,
          target_names=['Phishing', 'Legit'], digits=4))

def save_model(model, features):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'model', 'phishing_model.pkl')
    features_path = os.path.join(base_dir, 'model', 'feature_names.pkl')
    joblib.dump(model, model_path)
    joblib.dump(features, features_path)
    print("Model saved!")
    print("Features saved!")

if __name__ == "__main__":
    # Load
    df = load_data()

    # Prepare
    X, y, features = prepare_features(df)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train: {X_train.shape}, Test: {X_test.shape}")

    # Train
    print("Training model...")
    model = train_model(X_train, y_train)
    print("Done!")

    # Evaluate
    evaluate_model(model, X_test, y_test)

    # Save
    save_model(model, features)