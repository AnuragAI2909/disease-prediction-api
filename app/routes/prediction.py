from fastapi import APIRouter , Depends
from app.schemas import Patient, PredictionResponse
from app.schemas import Patient
from app.dependencies import get_current_user
from app.services.prediction_service import make_prediction


router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
def predict(patient: Patient, user=Depends(get_current_user)):
    return make_prediction(
        patient.age,
        patient.glucose,
        patient.bmi
    )