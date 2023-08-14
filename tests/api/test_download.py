import pytest
import pytest_check as check
import requests

from common import CommonTest
from const import DOWNLOAD_ENDPOINT


@pytest.mark.usefixtures("setup")
class TestDownload(CommonTest):
    """
    Class test the download functionalities
    """

    @pytest.mark.parametrize("valid_id", [True, False])
    def test_download_music_id(self, valid_id: bool) -> None:
        """
        Testing if we can download a file following the validity of the id
        :param valid_id: file id validity
        """
        if valid_id:
            # Upload a file first to get a music_id
            upload_response = self.add_file("data/file_example_WAV_1MG.wav")
            music_id = upload_response.json().get('id')
        else:
            music_id = 999999

        # Test downloading the uploaded file
        response = requests.get(f"{DOWNLOAD_ENDPOINT}/{music_id}")
        if not valid_id:
            check.equal(response.status_code, 404, msg="Http return code")
        else:
            check.equal(response.status_code, 200, msg="Http return code")
            check.equal(response.headers["Content-Type"], "audio/x-wav", msg="Content type")
            check.is_true(len(response.content) > 0, msg="Non empty content")


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
