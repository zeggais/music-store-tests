import pytest
import pytest_check as check
import requests

from common import CommonTest
from const import UPLOAD_ENDPOINT


@pytest.mark.usefixtures("setup")
class TestUpload(CommonTest):
    """
    Class testing the uploading functionalities
    """

    def test_upload_valid_wav_file(self) -> None:
        """
        Uploading a valid file
        """
        response = self.add_file("data/file_example_WAV_1MG.wav")
        check.equal(response.status_code, 200, msg="Http return code")
        check.is_true("id" in response.json().keys(), msg="Presence of the id in the response")

    def test_upload_no_file(self) -> None:
        """
        Launching an uploading command but with an empty payload
        """
        files = {}
        response = requests.post(UPLOAD_ENDPOINT, files=files)
        check.equal(response.status_code, 400, msg="Http return code")

    def test_upload_invalid_mime_type(self) -> None:
        """
        Uploading a file with an invalid mime type
        """
        files = {'file': ('invalid_wav.txt', open('data/invalid_wav.txt', 'rb'), 'text/plain')}
        response = requests.post(UPLOAD_ENDPOINT, files=files)
        check.equal(response.status_code, 400, msg="Http return code")

    def test_upload_no_mime_type(self) -> None:
        """
        Uploading a file with no mime type
        """
        files = {'file': ('empy_file.wav', open('data/empy_file.wav', 'rb'))}
        response = requests.post(UPLOAD_ENDPOINT, files=files)
        check.equal(response.status_code, 400, msg="Http return code")

    def test_upload_deleted_file(self) -> None:
        """
        Uploading a previously deleted file
        """
        self.add_file("data/file_example_WAV_1MG.wav")
        self.delete_added_files()
        response = self.add_file("data/file_example_WAV_1MG.wav")
        check.equal(response.status_code, 200, msg="Http return code")


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
