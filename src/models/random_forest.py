import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

logger = logging.getLogger(__name__)

def train_random_forest(X_train, X_test, y_train, y_test):
    logger.info("Training Random Forest model")

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    logger.info(
        "RandomForest params: n_estimators=300, max_depth=10, "
        "min_samples_split=5, min_samples_leaf=3"
    )

    model.fit(X_train, y_train)
    logger.info("Model training completed")

    #TODO EVALUATION
    y_pred = model.predict(X_test)

    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)

    logger.info(f"Train Accuracy: {train_acc:.4f}")
    logger.info(f"Test Accuracy : {test_acc:.4f}")

    if train_acc - test_acc > 0.05:
        logger.warning("Potential overfitting detected")

    logger.info("Confusion Matrix:\n%s", confusion_matrix(y_test, y_pred))
    logger.info("Classification Report:\n%s",
                classification_report(y_test, y_pred))

    print("\n=== RANDOM FOREST RESULTS ===")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))
    print("Train accuracy:", train_acc)
    print("Test accuracy :", test_acc)

    return model
