from logging import exception
from tqdm import trange, tqdm
import pandas as pd
import sqlalchemy
import psycopg2
import datetime
import dateutil


def insert_df_to_database(df, db_table=None, engine=None):
    # Ingest data 1 by 1 prevent error on duplication
    print("-" * 5 * 20)
    print(f"insert_df_to_database : {db_table}")
    for i in trange(len(df)):
        try:
            df.iloc[i : i + 1].to_sql(
                name=db_table, if_exists="append", con=engine, index=False
            )
        except:
            pass

    return True


def get_last_date_bq(project_id, app_id=None):
    query = f"""
    SELECT datetime(max(rs.at)) as lst
    FROM `hvzn-development.hvzn_dev.review_sentiment` as rs
    """
    if app_id:
        query += f"WHERE apps = '{app_id}'"

    # print("-" * 5 * 20)
    # print(query)
    # print("-" * 5 * 20)

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
