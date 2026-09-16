from app.model import pipeline


def make_prediction(
    age,
    glucose,
    bmi
):

    input_data = [[
        age,
        glucose,
        bmi
    ]]

    prediction = pipeline.predict(
        input_data
    )
    probability = pipeline.predict_proba(input_data)

    return {
        "prediction": int(prediction[0]),
        "probability": float(probability[0][1])
    }