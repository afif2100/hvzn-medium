import logging
import os
import warnings
import torch
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from transformers import pipeline
from simager.preprocess import TextPreprocess
from helper.helper import insert_reviews_to_database

logging.getLogger().addHandler(logging.StreamHandler())
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


class SentimentPredictor:
    def __init__(self):
        self._load_preprocess()
        self._postgres_conn()
        self._load_model()
        self.loaded = True

    def _postgres_conn(self):
        connection_info = {
            "host": os.environ.get("PG_HOST", "localhost"),
            "port": os.environ.get("PG_PORT", 5432),
            "db": os.environ.get("PG_DATABASE", "playstore"),
            "user": os.environ.get("PG_USER", "postgres"),
            "password": os.environ.get("PG_PASS", "postgres"),
        }
        self.db_engine = create_engine(
            "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
                **connection_info
            )
        )

        self.db_conn = psycopg2.connect(
            host=connection_info["host"],
            port=connection_info["port"],
            database=connection_info["db"],
            user=connection_info["user"],
            password=connection_info["password"],
        )
        print("-" * 5 * 20)
        self.db_conn.cursor()
        print("PostgreSQL connection successful!")
        print("-" * 5 * 20)

    def _gpu(self):
        return 0 if torch.cuda.is_available() else -1

    def _load_model(self):
        pretrained_name = "models"
        _device = self._gpu()
        self.model = pipeline(
            "sentiment-analysis",
            model=pretrained_name,
            tokenizer=pretrained_name,
            use_auth_token=True,
            device=_device,
        )
        print("-" * 5 * 20)
        print("Model loaded successfully!")
        print("-" * 5 * 20)

    def _load_preprocess(self):
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

    def _text_filler(self, text: str):
        if not text:
            return " "
        else:
            return text

    def _predict_text(self, text: str):
        if text:
            r_ = self.model(text)[0]
            return r_["label"], r_["score"]
        else:
            print("No text found")
            return "neutral", 0

    # create _preedict_text_v2 return list of dict
    def _predict_text_v2(self, text: list) -> list[dict]:
        try:
            return self.model(text)
        except Exception as e:
            logger.error(e)

    def _get_data_from_postgres(self, n=1000):
        query = f"""
        SELECT "review"."reviewId"
        , "review"."content"
        FROM review
        LEFT JOIN sentiment
        ON ("review"."reviewId"="sentiment"."reviewId")
        WHERE "sentiment"."sentiment" IS NULL
        LIMIT {n};
        """
        return pd.read_sql(query, self.db_engine)

    def _check_prediction_status(self):
        curr = self.db_conn.cursor()
        curr.execute("SELECT Count('reviewId') as review_count from sentiment")
        db_length = curr.fetchall()[0][0]
        curr.execute("SELECT Count('reviewId') as review_count from review")
        db_target = curr.fetchall()[0][0]

        # Print prediction status logger
        _pred_status_info = f"Prediction Status: {db_length}/{db_target} | {round(db_length / db_target * 100, 3)}%"
        logger.info(_pred_status_info)

    def batch_prediction(self, batch_size=1000):
        self._check_prediction_status()
        df = self._get_data_from_postgres(batch_size)
        while not df.empty:
            try:
                df["clean_text"] = df["content"].apply(self.cleaner)
                df["clean_text"] = df["clean_text"].apply(self._text_filler)

                # do prediction return tuple
                try:
                    predictions = self._predict_text_v2(df["clean_text"].tolist())
                except Exception as e:
                    print("predict_text_v2 error")
                    predictions = df["clean_text"].apply(self._predict_text)

                df[["sentiment", "pscore"]] = pd.DataFrame(predictions, index=df.index)
                insert_reviews_to_database(
                    df, db_table="sentiment", engine=self.db_engine
                )
                df = self._get_data_from_postgres(batch_size)
            except Exception as e:
                print(e)
                print(df)
            self._check_prediction_status()


if __name__ == "__main__":
    preds = SentimentPredictor()
    preds.batch_prediction(batch_size=10)
