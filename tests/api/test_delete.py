import pytest
import pytest_check as check
import requests

from common import CommonTest
from const import DELETE_ENDPOINT, LIST_ENDPOINT


@pytest.mark.usefixtures("setup")
class TestDelete(CommonTest):
    """
    Class testing the deletion functionalities
    """

    @pytest.mark.parametrize("valid_id", [True, False])
    def test_delete_music_id(self, valid_id: bool) -> None:
        """
        Testing the deletion of a file following the validity of the id
        :param valid_id: id_ validity
        """
        if valid_id:
            # Upload a file first to get a music_id
            upload_response = self.add_file("data/file_example_WAV_1MG.wav")
            music_id = upload_response.json().get('id')
        else:
            music_id = 999999

        # Test downloading the uploaded file
        response = requests.delete(f"{DELETE_ENDPOINT}/{music_id}")
        expected_status_code = 200 if valid_id else 404
        check.equal(response.status_code, expected_status_code, msg="Http return code")

        if valid_id:
            response = requests.get(LIST_ENDPOINT)
            check.equal(len(response.json()), 0, msg="File is deleted")


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
