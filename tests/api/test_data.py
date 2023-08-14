import pytest
import pytest_check as check
import requests

from common import CommonTest
from const import BASE_URL, LIST_ENDPOINT, STAT_ENDPOINT, UPLOAD_ENDPOINT


@pytest.mark.usefixtures("setup")
class TestData(CommonTest):
    """
    Class testing the
    """

    def test_get_table(self) -> None:
        """
        Testing the welcoming message
        """
        response = requests.get(f"{BASE_URL}/")
        check.equal(response.status_code, 200, msg="Http return code")

    @pytest.mark.parametrize("nb_files_added", [0, 3])
    def test_get_list_files(self, nb_files_added) -> None:
        """
        List query verification
        :param nb_files_added: number of file to add
        """
        self.add_multiple_files(nb_files_added)
        response = requests.get(LIST_ENDPOINT)
        check.equal(response.status_code, 200, msg="Http return code")
        check.equal(len(response.json()), nb_files_added, msg="Number of files in list")

    def test_get_list_files_after_failed_upload(self) -> None:
        """
        List query verification after a failed upload. We want to be sure that the file
        is not added.
        """
        payload = {"file": ("dummy.wav", open("data/empy_file.wav", "rb"))}
        requests.post(UPLOAD_ENDPOINT, files=payload)
        response = requests.get(LIST_ENDPOINT)
        check.equal(response.status_code, 200, msg="Http return code")
        check.equal(len(response.json()), 0, msg="Empty list")

    @pytest.mark.parametrize("valid_id", [True, False])
    def test_get_stats(self, valid_id: bool) -> None:
        """
        Verification of the stats query following the validity of the file id
        :param valid_id: validity of the file id
        """
        self.add_multiple_files(1)
        id_music = self.get_ids()[0] if valid_id else -1
        response = requests.get(f"{STAT_ENDPOINT}/{id_music}")
        expected_status_code = 200 if valid_id else 404
        check.equal(response.status_code, expected_status_code, msg="Http return code")
        if valid_id:
            expected_stats = {'sample_count': 1048376, 'sample_rate': 44100, 'channel_count': 2, 'duration': 5.943175}
            check.equal(response.json(), expected_stats, msg="File stats")


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
