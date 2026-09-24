from fastapi import FastAPI, Depends
from app.dependencies import get_app_name
from app.dependencies import verify_api_key, get_app_name , get_current_user
from fastapi import Request

from app.exceptions import general_exception_handler

from app.routes.auth import router as auth_router

from fastapi import FastAPI

from app.database import engine, Base
from app import models

from app.routes.users import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Disease Prediction API",
    description="""
    Machine Learning API for disease-risk prediction.

    The API accepts patient features and returns
    a model prediction and estimated class probability.
    """,
    version="1.0.0")

from app.routes.prediction import (
    router as prediction_router
)


# app = FastAPI(
#     title="ML Prediction API",
#     version="1.0.0"
# )
app.add_exception_handler(
    Exception,
    general_exception_handler
)


@app.get("/")
def home(api_key=Depends(verify_api_key), user=Depends(get_current_user)):

    return {
        "message": "ML API is running"
    }

#using dependency injection to get the app name 
# @app.")
# def predict(patient: Patient, api_key=Depends(verify_api_key)):

@app.get("/app-info")
def app_info(app_name=Depends(get_app_name), user=Depends(get_current_user)):      #def app_info(app_name=Depends(get_app_name), api_key=Depends(verify_api_key)): if i want to protect it by api key
 
    return {
        "name": app_name,
        "user": user
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

app.include_router(auth_router)
app.include_router(prediction_router)
app.include_router(users_router)