from pydantic import BaseModel

class AthleteInput(BaseModel):
    Gender: str
    Age: int
    Height_cm: float
    Weight_kg: float
    BMI: float
    Warmup_Time: float
    Stress_Level: float
    Injury_History: int

    Training_Frequency: float
    Training_Duration: float
    Training_Intensity: float
    Sleep_Hours: float
    Recovery_Time: float
    Muscle_Asymmetry: float
    Flexibility_Score: float
