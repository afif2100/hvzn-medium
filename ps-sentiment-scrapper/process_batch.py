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

    project_id = "hvzn-development"
    preds = SentimentPredictor()

    # Get review data and insert data
    app_ids = [
        "id.co.bri.brimo",
        "com.bca",
        "id.bmri.livin",
        "net.myinfosys.PermataMobileX",
        "id.co.btn.mobilebanking.android",
        "com.jago.digitalBanking",
        "id.co.cimbniaga.mobile.android",
    ]
    for app in app_ids:
        # Get App review and insert to LocalDB
        get_review_and_insert(app_id=app, engine=preds.db_engine, conn=preds.db_conn)

    # Predict non exist sentiment data
    preds.batch_prediction(batch_size=1000)

    # Sync data to bigquery
    # last_date_app = get_last_date_bq(project_id, app)
    # ingest_to_bq(app, last_date_app, upload=True, engine=preds.db_engine)
