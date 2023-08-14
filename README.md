# music-store-tests
Test automation of a music storage manager

# Test automation of a music storage manager in Python using Pytest

This repo contains test suites of a music storage manager app. The tests cover both the API and the CLI.

To launch those tests you will need pytest, allure, pytest_check and allure-pytest. 

To install those packages:

```console
python -m venv venv
```
On Mac/Linux environement:
```console
source venv/bin/activate
```
On Windows:
```console
venv\Scripts\activate
```

```console
pip install pytest pytest_check allure-pytest
```

To launch those tests:

```console
git clone -b main https://github.com/zeggais/music-store-tests.git
cd music-store-tests
allure generate 
MUSIC_API_EXE=/path/to/music-store-server pytest --alluredir=allure-report/ -s 
```

To generate a test report:

```console
allure serve allure-report/
```

Test Coverage

The tests in this repository cover various scenarios for the Music Service API, including endpoint functionality, 
edge cases, error handling, and CLI behavior. You can find the tests organized into separate classes and methods 
within the test files.

