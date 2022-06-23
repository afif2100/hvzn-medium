import gcsfs
import pickle


class GcsHelper:
    def __init__(self) -> None:
        self.fs = gcsfs.GCSFileSystem()

    def save_pkl_to_gcs(self, gcs_path, object) -> None:
        with self.fs.open(gcs_path, "wb") as f:
            pickle.dump(object, f)

    def read_pkl_from_gcs(self, gcs_path) -> None:
        with self.fs.open(gcs_path, "rb") as f:
            return pickle.load(f)

    def check_gcs_exist(self, gcs_path) -> bool:
        return self.fs.exists(gcs_path)

    def delete_gcs_file(self, gcs_path) -> bool:
        self.fs.rm(gcs_path)
        return self.check_gcs_exist(gcs_path) == False
