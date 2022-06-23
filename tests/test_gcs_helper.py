import os
import numpy as np
import pytest
from hvzn.utils import GcsHelper

from .settings import HOST, PORT, BUCKET
from gcp_storage_emulator.server import create_server

# Start Storage emulator
os.environ["STORAGE_EMULATOR_HOST"] = f"http://{HOST}:{PORT}"
server = create_server(HOST, PORT, default_bucket=BUCKET, in_memory=True)
gcs = GcsHelper()


@pytest.fixture
def payload():
    arr = np.array([0, 1, 2, 3, 4, 4, 4, 4, 6, 7, 8])
    gcs_path = f"gs://{BUCKET}/tests/pytest_array.pkl"
    payload = {"data":arr, "path": gcs_path}
    return payload

def test_start_server():
    server.start()

def test_save_pkl(payload):
    # save pkl
    arr = payload['data']
    gcs_path = payload['path']

    gcs.save_pkl_to_gcs(gcs_path=gcs_path, object=arr)
    assert gcs.check_gcs_exist(gcs_path) == True

def test_load_pkl(payload):
    # load pkl
    arr = payload['data']
    gcs_path = payload['path']

    loaded_array = gcs.read_pkl_from_gcs(gcs_path=gcs_path)
    assert np.array_equal(arr, loaded_array) == True

def test_delete_file(payload):
    # delete file
    arr = payload['data']
    gcs_path = payload['path']

    gcs.delete_gcs_file(gcs_path)
    assert gcs.check_gcs_exist(gcs_path) == False

def test_stop_server():
    server.stop()