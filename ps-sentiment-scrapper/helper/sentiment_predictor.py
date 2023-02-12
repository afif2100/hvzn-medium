from simager.preprocess import TextPreprocess
from transformers import pipeline
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import logging
from helper.helper import insert_df_to_database
import os
import warnings

logging.getLogger().addHandler(logging.StreamHandler())
warnings.filterwarnings("ignore")


class SentimentPredictor:
    def __init__(self):
        self._load_preprocess()
        self._postgress_conn()
        self.loaded = False

    def _postgress_conn(self):
        connection_info = {
            "host": os.environ.get("PG_HOST", "localhost"),
            "port": os.environ.get("PG_PORT", 5432),
            "db": os.environ.get("PG_DATABASE", "playstore"),
            "user": os.environ.get("PG_USER", "postgres"),
            "password": os.environ.get("PG_PASS", "postgres"),
        }
        # Sql engine
        self.db_engine = create_engine(
            "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
                connection_info["user"],
                connection_info["password"],
                connection_info["host"],
                connection_info["port"],
                connection_info["db"],
            )
        )
        # psql engine
        self.db_conn = psycopg2.connect(
            host=connection_info["host"],
            port=connection_info["port"],
            database=connection_info["db"],
            user=connection_info["user"],
            password=connection_info["password"],
        )

        print("-" * 5 * 20)
        self.db_engine.connect()
        print("Postgress connection success!")
        print("-" * 5 * 20)

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

        # flag model is loadded
        self.loaded = True

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

    def _predict_text(self, text: str):
        if text:
            r_ = self.model(text)[0]
            return r_["label"], r_["score"]
        else:
            return "neutral", 0

    def _get_data_from_postgress(self, n=1000):

        # Get unpredicted data from postgres
        query = f"""
        SELECT "review"."reviewId"
        , "review"."content"
        FROM review
        LEFT JOIN sentiment
        ON ("review"."reviewId"="sentiment"."reviewId")
        WHERE "sentiment"."sentiment" is null
        LIMIT {n};
        """
        return pd.read_sql(query, self.db_engine)

    def _check_prediction_status(self):
        # create db cursor
        curr = self.db_conn.cursor()

        # print status
        curr.execute("SELECT Count('reviewId') as review_count from sentiment")
        db_length = curr.fetchall()[0][0]

        # get db target
        curr.execute("SELECT Count('reviewId') as review_count from review")
        db_target = curr.fetchall()[0][0]

        # send status
        print(
            f"Prediction Status : {db_length}/{db_target} | {round(db_length/db_target*100, 3)}%"
        )

    def batch_prediction(self, batch_size=1000):

        # do load model if not loaded
        if self.loaded == False:
            self._load_model()

        self._check_prediction_status()
        df = self._get_data_from_postgress(batch_size)

        # while there is a data it will predict
        while len(df) > 0:
            try:
                # get data ad do preprocess
                df["clean_text"] = df["content"].apply(lambda x: self.cleaner(x))
                df["sentiment"], df["pscore"] = zip(
                    *df["clean_text"].apply(lambda x: self._predict_text(x))
                )
                # sent to postgress
                insert_df_to_database(df, db_table="sentiment", engine=self.db_engine)

                # get new data
                df = self._get_data_from_postgress(batch_size)

            except Exception as e:
                print(e)
                print(df)

            self._check_prediction_status()


if __name__ == "__main__":
    preds = SentimentPredictor()
    preds.batch_prediction(batch_size=10)
