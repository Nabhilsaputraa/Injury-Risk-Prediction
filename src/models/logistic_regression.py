import logging
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

logger = logging.getLogger(__name__)

def train_logistic_regression(X_train, X_test, y_train, y_test, threshold=0.3):
    logger.info("Training Logistic Regression model")

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    logger.info("Model training completed")
    proba = model.predict_proba(X_test)
    y_pred = np.where(proba[:,1] >= threshold, 1, 0)

    acc = accuracy_score(y_test, y_pred)
    logger.info(f"Test Accuracy: {acc:.4f}")
    logger.info("Confusion Matrix:\n%s", confusion_matrix(y_test, y_pred))
    logger.info("Classification Report:\n%s", classification_report(y_test, y_pred))

    print("\n=== LOGISTIC REGRESSION (CUSTOM THRESHOLD) ===")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return model
