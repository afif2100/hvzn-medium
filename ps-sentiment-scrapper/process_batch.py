import pandas as pd
from sqlalchemy import create_engine
from helper import SentimentPredictor
from helper import (
    get_last_date_bq,
    get_last_date_db,
    get_review_by_last_date,
    insert_reviews_to_database,
)


def get_review_and_insert(app_id, engine=None, conn=None):
    # Get last updated date from the database
    last_update = get_last_date_db(app_id, conn)

    # Get reviews of the app from the playstore
    print(f"Get data for {app_id}, last updated at: {last_update}")
    reviews = get_review_by_last_date(app_id, last_update)

    # Filter the dataframe to only include newer reviews
    new_reviews = reviews[reviews["at"] > last_update]
    new_reviews["apps"] = app_id
    print(
        f"Found {len(new_reviews)} new reviews for {app_id}, last updated at: {last_update}"
    )

    # Insert the filtered dataframe into the database
    if new_reviews.empty:
        print(f"No new reviews to insert for {app_id}")
    else:
        insert_reviews_to_database(new_reviews, "review", engine)
        print(
            f"Inserted {len(new_reviews)} new reviews for {app_id} into the database."
        )


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
    df.to_gbq(
        project_id=project_id,
        destination_table=destination_table,
        if_exists="append",
    )
    print(f"BQ Last date Before : {last_date_app}")
    print(f"BQ Last date After : {get_last_date_bq(project_id)}")
    print("Not uploading to bq, cz this is testing")


if __name__ == "__main__":

    import logging
    # set log to level info
    logging.basicConfig(level=logging.INFO)

    project_id = "hvzn-development"
    preds = SentimentPredictor()

    app_ids = [
        "id.co.bri.brimo",
        "com.bca",
        "id.bmri.livin",
        "net.myinfosys.PermataMobileX",
        "id.co.btn.mobilebanking.android",
        "com.jago.digitalBanking",
        "id.co.cimbniaga.mobile.android",
        "src.com.bni",
    ]

    # Get review data and insert data
    # for app in app_ids:
    #    get_review_and_insert(app_id=app, engine=preds.db_engine, conn=preds.db_conn)

    # Predict non-existing sentiment data
    run_prediction = input("Run the Sentiment Prediction? [y]es/[n]o : ")
    if run_prediction in ["y", "yes"]:
        preds.batch_prediction(batch_size=500)
    else:
        print("Skipping the Prediction")

    # Sync data to BigQuery
    export_data_tobq = input("Export data to BQ? [y]es/[n]o : ")
    if export_data_tobq in ["y", "yes"]:
        for app in app_ids:
            last_date_app = get_last_date_bq(project_id, app)
            ingest_to_bq(app, last_date_app, upload=True, engine=preds.db_engine)
    else:
        exit(1)
