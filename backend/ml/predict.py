import joblib

# Load the trained model
model = joblib.load("backend/ml/category_model.pkl")

def predict_category(vendor, text):
    """
    Predict category using the trained ML model.
    Returns:
        - predicted category
        - confidence score (0.0 to 1.0)
    """
    try:
        combined = vendor + " " + text
        probabilities = model.predict_proba([combined])[0]
        predicted_class = model.classes_[probabilities.argmax()]
        confidence = probabilities.max()
        return predicted_class, confidence
    except Exception as e:
        print(f"[Predict Error]: {e}")
        return "General", 0.0
