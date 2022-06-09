import gcsfs
import pickle


def save_pkl_to_gcs(gcs_path, object):
    fs = gcsfs.GCSFileSystem()
    with fs.open(gcs_path, "wb") as f:
        pickle.dump(object, f)


def read_pkl_from_gcs(gcs_path):
    fs = gcsfs.GCSFileSystem()
    with fs.open(gcs_path, "rb") as f:
        return pickle.load(f)


def check_gcs_exist(gcs_path) -> bool:
    fs = gcsfs.GCSFileSystem()
    return fs.exists(gcs_path)
