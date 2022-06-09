import numpy as np
import pickle
from hvzn.utils.gcs_helper import save_pkl_to_gcs, read_pkl_from_gcs, check_gcs_exist


arr = np.array([0, 1, 2, 3, 4, 4, 4, 4, 6, 7, 8])


def test_save_pkl():
    gcs_path = "gs://hvzn-gcs-us-1/tests/array_test2.pkl"
    save_pkl_to_gcs(gcs_path=gcs_path, object=arr)
    assert check_gcs_exist(gcs_path) == True


def test_load_pkl():
    gcs_path = "gs://hvzn-gcs-us-1/tests/array_test2.pkl"
    loaded_array = read_pkl_from_gcs(gcs_path=gcs_path)
    assert np.array_equal(arr, loaded_array) == True
