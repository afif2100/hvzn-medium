import numpy as np
import pickle
from hvzn.utils import GcsHelper


arr = np.array([0, 1, 2, 3, 4, 4, 4, 4, 6, 7, 8])
gcs_path = "gs://hvzn-gcs-us-1/tests/pytest_array.pkl"
gcs = GcsHelper()


def test_save_pkl():
    gcs.save_pkl_to_gcs(gcs_path=gcs_path, object=arr)
    assert gcs.check_gcs_exist(gcs_path) == True


def test_load_pkl():
    loaded_array = gcs.read_pkl_from_gcs(gcs_path=gcs_path)
    assert np.array_equal(arr, loaded_array) == True


def test_delete_file():
    gcs.delete_gcs_file(gcs_path)
    assert gcs.check_gcs_exist(gcs_path) == False
