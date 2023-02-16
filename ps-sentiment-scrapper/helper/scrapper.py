import pandas as pd
from time import sleep
from google_play_scraper import Sort, reviews
from tqdm import tqdm


MAX_COUNT_EACH_FETCH = 200


def _print_info(df):
    print("\n")
    print("-" * 5 * 20)
    print(f"Downloaded : {len(df)}")
    print(f"Oldest Date : {min(df['at'])}")
    print(f"Latest Date : {max(df['at'])}")
    print("-" * 5 * 20)


def transform_to_df(dict_list: list):

    # Transform the results to a pandas dataframe
    df = pd.DataFrame(dict_list)
    _print_info(df)
    return df


def get_review(app_id, n_max=1000):
    continuation_token = None
    results = []

    pbar = tqdm(total=n_max + MAX_COUNT_EACH_FETCH)
    while len(results) <= n_max:
        try:
            result, continuation_token = reviews(
                app_id,
                count=MAX_COUNT_EACH_FETCH,
                continuation_token=continuation_token,
                lang="id",  # defaults to 'en'
                country="id",  # defaults to 'us'
                sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
                filter_score_with=None,  # defaults to None(means all score)
            )
        except:
            continue

        results += result
        pbar.update(len(result))

        if continuation_token.token is None:
            break

    return transform_to_df(results)


def get_review_by_last_date(app_id, last_date) -> pd.DataFrame:
    results = []
    continuation_token = None
    is_date_match = False

    pbar = tqdm()
    while not is_date_match:
        try:
            result, continuation_token = reviews(
                app_id,
                count=MAX_COUNT_EACH_FETCH,
                continuation_token=continuation_token,
                lang="id",  # defaults to 'en'
                country="id",  # defaults to 'us'
                sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
                filter_score_with=None,  # defaults to None(means all score)
            )
            results += result
            results_date = results[-1]["at"]
            pbar.update(len(results))
        except:
            continue

        # If there is no more data or date match, then break the loop
        if (continuation_token.token is None) or (results[-1]["at"] <= last_date):
            is_date_match = True
            break

        # Print status every 5000 results
        if len(results) % 5000 == 0:
            print(f"\nLast scrap date : {results_date}")

    return transform_to_df(results)
