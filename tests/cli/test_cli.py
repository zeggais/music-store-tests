import subprocess
import time

import pytest
import os
import requests
import pytest_check as check

cli_executable = os.environ["MUSIC_API_EXE"]
exe_name = os.path.basename(cli_executable)
exe_path = os.path.dirname(cli_executable)


class TestCLI:

    @pytest.fixture
    def run_cli_command(self):
        def run_command(*args):
            proc = subprocess.Popen([cli_executable, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                output, err = proc.communicate(timeout=1)
            except subprocess.TimeoutExpired:
                proc.terminate()
                proc.wait()
                output, err = proc.communicate()
            return str(output), str(err)
        return run_command

    def test_cli_help(self, run_cli_command):
        """
        Testing if the help message is displayed
        """
        output, _ = run_cli_command("--help")
        check.is_true(f"{exe_name} [OPTIONS] [storage-location]" in output, msg="Help message displayed")

    def test_cli_default_port(self, run_cli_command):
        """
        Verifying the default port
        """
        output, _ = run_cli_command()
        check.is_true("localhost:5555" in output, msg="Right default port selected")

    def test_cli_custom_port(self, run_cli_command):
        """
        Launching the api on a custom port
        """
        output, _ = run_cli_command("--port", "8080")
        check.is_true("localhost:8080" in output, msg="Right default port selected")

    def test_cli_invalid_port(self, run_cli_command):
        """
        Launching the api on an invalid port
        """
        output, _ = run_cli_command("--port", "abc")
        check.is_false("localhost:5555" in output, msg="Right default port selected")

    def test_cli_missing_port_value(self, run_cli_command):
        """
        Launching the api without a port value
        """
        output, _ = run_cli_command("--port")
        check.is_false("localhost:5555" in output, msg="Right default port selected")

    def test_cli_custom_storage_location(self):
        """
        Launching the api with a custom storage location
        """
        p = subprocess.Popen([cli_executable, "./tests"], stdout=subprocess.DEVNULL)
        time.sleep(1)  # Waiting for execution
        payload = {"file": ("file.wav", open("data/empy_file.wav", "rb"), "audio/wav")}
        requests.post("http://localhost:5555/upload", files=payload)
        check.is_true(sum(file.endswith('.wav') for file in os.listdir("tests/")) > 0, msg="Wav file stored")
        os.system("rm tests/*.wav")
        p.kill()

    def test_cli_default_storage_location(self):
        """
        Launching the api without the default storage location
        """
        p = subprocess.Popen([cli_executable], stdout=subprocess.DEVNULL)
        time.sleep(1)  # Waiting for execution
        payload = {"file": ("file.wav", open("data/empy_file.wav", "rb"), "audio/wav")}
        requests.post("http://localhost:5555/upload", files=payload)
        check.is_true(sum(file.endswith('.wav') for file in os.listdir(".")) > 0, msg="Wav file stored")
        os.system("rm *.wav")
        p.kill()

    def test_cli_nonexistent_storage_location(self, run_cli_command):
        """
        Launching the api with an invalid storage location
        """
        _, err = run_cli_command("./toto")
        check.is_not_none(err, msg="Error on storing folder")


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
