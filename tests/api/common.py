import os
import requests
from const import UPLOAD_ENDPOINT, LIST_ENDPOINT, DELETE_ENDPOINT


class CommonTest:

    def teardown_method(self) -> None:
        """
        Cleaning files after test
        """
        self.delete_added_files()

    @staticmethod
    def add_multiple_files(nb_file_added: int) -> None:
        """
        Adding multiple wav files
        :param nb_file_added: number of file to create
        """
        for idx in range(nb_file_added):
            payload = {
                "file": (
                    f"file_example_WAV_1MG_{idx}.wav",
                    open("data/file_example_WAV_1MG.wav", "rb"),
                    "audio/wav"
                )
            }
            requests.post(UPLOAD_ENDPOINT, files=payload)

    @staticmethod
    def add_file(filepath: str) -> any:
        """
        Adding a file to the storage
        :param filepath: path to the file
        :return: response to the post request
        """
        filename = os.path.splitext(os.path.basename(filepath))[0]
        payload = {"file": (filename, open(filepath, "rb"), "audio/wav")}
        return requests.post(UPLOAD_ENDPOINT, files=payload)

    def delete_added_files(self) -> None:
        """
        Deleting all the files present in the storage
        """
        list_id = self.get_ids()

        for id_music in list_id:
            requests.delete(f"{DELETE_ENDPOINT}/{id_music}")

    @staticmethod
    def get_ids() -> list:
        """
        Getting all the file id present in the storage
        """
        return list(map(lambda x: os.path.splitext(x)[0], requests.get(LIST_ENDPOINT).json()))
