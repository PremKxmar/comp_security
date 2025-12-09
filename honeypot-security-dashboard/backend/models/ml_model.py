import pickle
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

class AttackClassifier:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), 'classifier.pkl')
        self.vectorizer_path = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')
        self.model = None
        self.vectorizer = None
        self.load_model()

    def load_model(self):
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(self.vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                print("ML Model loaded successfully.")
            else:
                print("ML Model not found. Please train the model.")
        except Exception as e:
            print(f"Error loading ML model: {e}")

    def predict(self, payload):
        if not self.model or not self.vectorizer:
            return "Unknown (Model Not Loaded)"
        
        if not payload:
            return "Normal"

        try:
            # Vectorize the payload
            features = self.vectorizer.transform([payload])
            # Predict
            prediction = self.model.predict(features)[0]
            return prediction
        except Exception as e:
            print(f"Prediction Error: {e}")
            return "Error"
