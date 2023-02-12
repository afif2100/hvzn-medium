from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel
from simager.preprocess import TextPreprocess


class SentimentText(BaseModel):
    text: str


class PredictionModel:
    def __init__(self) -> None:
        self.loaded = False
        self.model = None
        self.text_cleaner = TextPreprocess(
            methods=[
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
        )

    def load_model(self):
        self.model = pipeline(
            task="sentiment-analysis",
            model="models",
            tokenizer="models",
            use_auth_token=True,
        )
        self.loaded = True

    def predict(self, text: str):
        if not self.loaded:
            self.load_model()

        if text:
            cleaned_text = self.text_cleaner(text)
            prediction = self.model(cleaned_text)[0]
            return prediction["label"], prediction["score"]
        else:
            return "neutral", 0


app = FastAPI()
model = PredictionModel()


@app.post("/predict")
async def predict(text: SentimentText):
    label, score = model.predict(text)
    return {"label": label, "score": score}
