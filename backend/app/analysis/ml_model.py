from collections import Counter
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


def train_exercise_classifier(X, y, test_size=10, random_state=42):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size,
        random_state=random_state, stratify=y)

    model = RandomForestClassifier(n_estimators=200,random_state=random_state,class_weight="balanced")
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return {
        "model": model,
        "accuracy": accuracy,
        "y_test": y_test,
        "predictions": predictions,
        "report": classification_report(y_test, predictions, zero_division=0),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "class_distribution": Counter(y)
    }

def predict_exercise(model, features):
    features = np.asarray(features, dtype=float).reshape(1, -1)
    return model.predict(features)[0]