from fastapi import FastAPI
from app.schema import AthleteInput
from app.inference import predict_risk

app = FastAPI(title='Injury Risk Prediction API')

@app.get("/")
def health():
    return {"staus": "API running"}

@app.post("/predict")
def predict(data: AthleteInput):
    return predict_risk(data.dict())