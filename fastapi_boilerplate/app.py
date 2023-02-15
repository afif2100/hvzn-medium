from fastapi import FastAPI, Request, Body
import joblib
import numpy as np
from pydantic import BaseModel


class User(BaseModel):
    age: int
    bmi: float


class PredictionModel:
    def __init__(self) -> None:
        self.model = joblib.load("model.pkl")

    def predict(self, age, bmi):
        result = self.model.predict([[age, bmi]])

        if result[0] == 1:
            result = "Diabetes"
        else:
            result = "Not Diabetes"

        return result


app = FastAPI()
predict_function = PredictionModel()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/predict")
async def predict(user: User):
    return predict_function.predict(user.age, user.bmi)
