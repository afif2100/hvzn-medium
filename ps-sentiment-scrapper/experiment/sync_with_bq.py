from sqlalchemy import create_engine
import pandas as pd
import os
import pandas as pd


def get_data(dttm):
    connection_info = {
        "host": os.environ.get("PG_HOST", "localhost"),
        "port": os.environ.get("PG_PORT", 5432),
        "db": os.environ.get("PG_DATABASE", "playstore"),
        "user": os.environ.get("PG_USER", "postgres"),
        "password": os.environ.get("PG_PASS", "postgres"),
    }

    # Sql engine
    db_engine = create_engine(
        "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            connection_info["user"],
            connection_info["password"],
            connection_info["host"],
            connection_info["port"],
            connection_info["db"],
        )
    )

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
        AND "review"."at" > '{dttm}';
        """
    df = pd.read_sql(query, db_engine)
    df["repliedDurationHrs"] = (df["repliedAt"] - df["at"]).apply(
        lambda x: round(x.seconds / 3600, 2)
    )

    return df


if __name__ == "__main__":
    # Insert initial data
    project_id = "hvzn-development"
    destination_table = "hvzn_dev.review_sentiment"
    df = get_data("2020-01-01")

    # full replace data
    df.to_gbq(
        project_id=project_id,
        destination_table=destination_table,
        if_exists="replace",
        chunksize=10000,
        progress_bar=True,
    )
