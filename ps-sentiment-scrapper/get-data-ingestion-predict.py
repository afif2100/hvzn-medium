from matplotlib.pyplot import table
import pandas as pd
from sqlalchemy import create_engine
from helper import get_review_by_last_date
from helper import SentimentPredictor
from helper.helper import insert_df_to_database, get_last_date_bq, get_last_date_db
import os


def get_review_and_insert(app_id, engine=None, conn=None):
    # get data from playstore

    # get dataframe for each apps
    print(f"Get data from playstore : {app_id}")

    # filter dataframe only for newer apps
    last_date = get_last_date_db(app_id, conn)

    # get apps review
    df = get_review_by_last_date(app_id, last_date)

    # filter df
    df = df[df["at"] > last_date]
    df["apps"] = app_id
    print(f"New data for : {app_id} | {len(df)} | {last_date}")

    # insert df to revuiew database
    if len(df) > 0:
        insert_df_to_database(df, db_table="review", engine=engine)
    else:
        print(f"No new data for {app_id}")


def get_result_data(app, dttm, engine=None):

    query = f"""
        SELECT "review"."reviewId"
        , "review"."apps"
        , "review"."score"
        , "review"."at"
        , "review"."content"
        , "review"."repliedAt"
        , "sentiment"."clean_text"
        , "sentiment"."sentiment"
        FROM review
        LEFT JOIN sentiment
        ON ("review"."reviewId"="sentiment"."reviewId")
        WHERE "sentiment"."sentiment" is not null
        AND "review"."at" > '{dttm}'
        AND "review"."apps" = '{app}'
        ;
    """
    # Read data from sql to pandas
    df = pd.read_sql(query, engine)
    df["repliedDurationHrs"] = (df["repliedAt"] - df["at"]).apply(
        lambda x: round(x.seconds / 3600, 2)
    )

    return df


def ingest_to_bq(app, last_date_app, upload=True, engine=None):
    # sync data to bigquery
    df = get_result_data(app, last_date_app, engine)
    print(f"Data to ingest : {len(df)}")

    # insert to dataframe
    destination_table = "hvzn_dev.review_sentiment"
    if len(df) == 0:
        return True
    if upload:
        df.to_gbq(
            project_id=project_id,
            destination_table=destination_table,
            if_exists="append",
        )
        print(f"BQ Last date Before : {last_date_app}")
        print(f"BQ Last date After : {get_last_date_bq(project_id)}")
    else:
        print("Not uploading to bq, cz this is testing")
    return True


if __name__ == "__main__":
    # get last updated date
    project_id = "hvzn-development"
    preds = SentimentPredictor()

    # insert data
    app_ids = ["id.co.bri.brimo", "com.bca", "id.bmri.livin", "net.myinfosys.PermataMobileX"]
    for app in app_ids:
        # Get App review and insert to LocalDB
        get_review_and_insert(
            app_id=app,
            engine=preds.db_engine,
            conn=preds.db_conn
        )

    # Predict non exist sentiment data
    preds.batch_prediction(batch_size=1000)

    # sync data to bigquery
    # last_date_app = get_last_date_bq(project_id, app)
    # ingest_to_bq(app, last_date_app, upload=True, engine=preds.db_engine)
