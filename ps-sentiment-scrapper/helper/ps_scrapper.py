import pandas as pd
from time import sleep
from google_play_scraper import Sort, reviews
from tqdm import tqdm


MAX_COUNT_EACH_FETCH = 200


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

    df = pd.DataFrame(result)
    print(
        f"Downloaded : {len(result)} | Oldest Date : {min(df['at'])} | Latest Date : {max(df['at'])}"
    )

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
