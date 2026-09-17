from app.model import pipeline
from app.logging_config import logger

def make_prediction(age, glucose, bmi):

    logger.info("Prediction requested")

    input_data = [[
        age,
        glucose,
        bmi]]

    prediction = pipeline.predict(input_data)

    probability = pipeline.predict_proba(input_data)[0][1]

    if prediction[0] == 1:
        result = "High Risk"
    else:
        result = "Low Risk"

    return {
        "prediction": int(prediction[0]),
        "probability": float(probability),
        "result": result
    }