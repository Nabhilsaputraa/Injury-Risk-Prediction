import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


#! LOGGING CONFIG
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

def preprocessing(df, target="Injury_Risk", test_size=0.2, random_state=42):
    logger.info("Starting preprocessing pipeline")

    df = df.copy()
    logger.info(f"Initial dataset shape: {df.shape}")

    #TODO FEATURE ENGINEERING

    logger.info("Performing feature engineering")

    df["Training_Load"] = (
        df["Training_Frequency"]
        * df["Training_Duration"]
        * df["Training_Intensity"]
    )

    df["Recovery_Quality"] = df["Sleep_Hours"] * df["Recovery_Time"]

    df["Physical_Imbalance"] = (
        df["Muscle_Asymmetry"] / (df["Flexibility_Score"] + 1)
    )

    logger.info("Feature engineering completed")


    #TODO SPLIT FEATURE & TARGET
    X = df.drop(columns=[target])
    y = df[target]

    logger.info(f"Target distribution:\n{y.value_counts(normalize=True)}")

    categorical_cols = ["Gender"]
    numeric_cols = X.columns.difference(categorical_cols)

    logger.info(f"Numerical features: {len(numeric_cols)}")
    logger.info(f"Categorical features: {categorical_cols}")

    #TODO PREPROCESSING PIPELINE
    numeric_transformer = Pipeline([
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline([
        ("encoder", OneHotEncoder(drop="first", handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols)
        ]
    )

    logger.info("Preprocessing pipeline created")


    #TODO TRAIN TEST SPLIT
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    logger.info(
        f"Train size: {X_train.shape[0]} | Test size: {X_test.shape[0]}"
    )


    #TODO FIT & TRANSFORM
    logger.info("Fitting preprocessor on training data")

    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    logger.info(f"Processed train shape: {X_train.shape}")
    logger.info(f"Processed test shape : {X_test.shape}")

    logger.info("Preprocessing pipeline finished successfully")

    return X_train, X_test, y_train, y_test, preprocessor
