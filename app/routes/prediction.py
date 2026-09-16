from fastapi import APIRouter 
from app.schemas import Patient, PredictionResponse
from app.schemas import Patient

from fastapi import APIRouter, Depends
from app.dependencies import verify_api_key
from app.dependencies import verify_api_key, get_app_name , get_current_user
from app.services.prediction_service import (
    make_prediction
)


router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
def predict(patient: Patient, user=Depends(get_current_user)):

    prediction_data = make_prediction(
        patient.age,
        patient.glucose,
        patient.bmi
        
    )

    if prediction_data["prediction"] == 1:
        message = "High Risk"

    else:
        message = "Low Risk"

    return {
        "prediction": prediction_data["prediction"],
        "probability": prediction_data["probability"],
        "result": message
    }