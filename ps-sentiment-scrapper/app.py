from fastapi import FastAPI, Request, Body
from transformers import pipeline
import numpy as np
import json
from pydantic import BaseModel
from simager.preprocess import TextPreprocess

class SentimentText(BaseModel):
    text: str

class PredictionModel():

    def __init__(self) -> None:
        self.loaded = False
        self._load_preprocess()

    def _load_preprocess(self):
        # Text preprocessing
        methods = [
            "rm_hastag",
            "rm_mention",
            "rm_nonascii",
            "rm_emoticons",
            "rm_html",
            "rm_url",
            "sparate_str_numb",
            "pad_punct",
            "rm_punct",
            "rm_repeat_char",
            "rm_repeat_word",
            "rm_numb",
            "rm_whitespace",
            "normalize",
        ]
        self.cleaner = TextPreprocess(methods=methods)

    def _load_model(self):
        # sentiment model
        print("-" * 5 * 20)
        pretrained_name = "models"
        self.model = pipeline(
            "sentiment-analysis",
            model=pretrained_name,
            tokenizer=pretrained_name,
            use_auth_token=True,
        )
        print("Load model success!")
        print("-" * 5 * 20)

        self.loaded = True

    def predict(self, text: str):
        if not self.loaded:
            self._load_model()

        if text:
            text = self.cleaner(text)
            result = self.model(text)[0]
            return result["label"], result["score"]
        else:
            return "neutral", 0

app = FastAPI()
model = PredictionModel()

@app.post("/predict")
async def predict(text: SentimentText ):
    label, score =  model.predict(text)
    return {"label": label, "score": score}