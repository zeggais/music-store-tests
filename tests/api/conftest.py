import pytest
import subprocess
import os


@pytest.fixture(scope="module")
def setup():
    # Setup
    path_to_exe = os.environ["MUSIC_API_EXE"]
    p = subprocess.Popen([path_to_exe], stdout=subprocess.DEVNULL)

    # Tests execution
    yield

    # Teardown
    p.kill()
