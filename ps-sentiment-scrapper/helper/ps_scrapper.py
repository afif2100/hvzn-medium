import pandas as pd
from time import sleep
from google_play_scraper import Sort, reviews
from tqdm import tqdm


MAX_COUNT_EACH_FETCH = 200


def _print_info(df):
    print("-" * 5 * 20)
    print(
        f"Downloaded : {len(df)} | Oldest Date : {min(df['at'])} | Latest Date : {max(df['at'])}"
    )
    print("-" * 5 * 20)


def get_review_ps(app_id, n_max=1000):
    continuation_token = None
    result = []

    pbar = tqdm(total=n_max + MAX_COUNT_EACH_FETCH)
    while len(result) <= n_max:
        try:
            _result, continuation_token = reviews(
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

        result += _result
        pbar.update(len(_result))

        if continuation_token.token is None:
            break

    # transform to df
    df = pd.DataFrame(result)
    _print_info(df)

    return df

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
            results_date = results[-1]['at']
            pbar.update(len(results))
        except:
            continue

        # if there is no more data then break loop
        if continuation_token.token is None:
            break
        
        # Print status
        if len(results) % 5000 == 0:
            print(f"\n Last scrap date : {results_date}")

        # If date match then break the loop
        if results[-1]['at'] <= last_date:
            is_date_match = True

    # transform to df
    df = pd.DataFrame(results)
    _print_info(df)
    return df


if __name__ == "__main__":
    continuation_token = None
    result = []

    app_id = "com.bca"
    app_id = "id.bmri.livin"
    app_id = "id.co.bri.brimo"
    version = "v3"

    # df = get_review_ps(app_id=app_id)
    # df.to_csv(f"{app_id}_{version}_playstore_review.csv", sep=";", index=False)

    # print information
    print(f"Downloaded : {len(result)} | Oldest Date : {min(df['at'])}")
