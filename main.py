import pandas as pd
from src.data.preprocessing import preprocessing 
from src.models.logistic_regression import train_logistic_regression 
from src.models.random_forest import train_random_forest
import joblib

df = pd.read_csv(f"G:\Projek\Prediksi-Cidera\data\High_Accuracy_Sport_Injury_Dataset.csv")

#! PREPROCESSING
X_train, X_test, y_train, y_test, preprocessor = preprocessing(df)
print(X_train.shape, X_test.shape)
#! MODEL
# print("============= Logistic Regression =============")
# model = train_logistic_regression(X_train, X_test, y_train, y_test)
print("============= random_forest =============")
rf_model = train_random_forest(X_train, X_test, y_train, y_test)

#! Save model
joblib.dump(preprocessor, "artifacts/proprocessor.joblib")
joblib.dump(rf_model, "artifacts/random_forest.joblib")
