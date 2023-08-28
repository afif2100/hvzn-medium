from logging import exception
from tqdm import trange, tqdm
import pandas as pd
import sqlalchemy
import psycopg2
import datetime
from sqlalchemy import exc
import dateutil


def insert_reviews_to_database(df, db_table=None, engine=None):
    print("-" * 5 * 20)
    print(f"Inserting {len(df)} reviews into the database table '{db_table}'")

    try:
        # Use bulk insert and transaction
        df.to_sql(
            name=db_table, if_exists="append", con=engine, index=False, method="multi"
        )

    except exc.IntegrityError as e:
        pass

    print("Insertion completed.")
    return True


def get_last_date_bq(project_id, app_id=None):
    query = f"""
    SELECT datetime(max(rs.at)) as lst
    FROM `hvzn-development.hvzn_dev.review_sentiment` as rs
    """
    if app_id:
        query += f"WHERE apps = '{app_id}'"

    last_dt = pd.read_gbq(query, project_id=project_id)
    return last_dt["lst"][0]


def get_last_date_db(app_id, conn=None):
    # create query
    date_query = f"""
        SELECT MAX(at)
        FROM review
        WHERE apps = '{app_id}'
        """

    # get dttm from db
    curr = conn.cursor()

    # execute query
    curr.execute(date_query)
    t = curr.fetchall()[0][0]
    if not isinstance(t, datetime.date) and t:
        t = dateutil.parser.parse(t)
    if not t:
        # if null set default date
        t = dateutil.parser.parse("2022-01-01")
    return t
