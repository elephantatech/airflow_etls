# Airflow Project Setup

This project sets up a basic Apache Airflow environment using Docker Compose.

## Prerequisites

- Docker
- Docker Compose

## Setup (Docker Environment)

1.   **Clone Repository:**
    `git clone https://github.com/elephantatech/airflow_project.git`
2.  **Navigate to Project:**
    `cd airflow_project`
3.  **Start Airflow:**
    `docker-compose up -d`
4.  **Access Airflow:**
    Open your web browser and go to `http://localhost:8080`. Log in with the username `airflow` and the password `airflow`.
5.  **Stop Airflow:**
    `docker-compose down`

## Setup (Existing Airflow)

If you have an existing Airflow environment, you can copy the `dags` directory into your Airflow's DAGs folder. Also copy the contents of the `config` folder to your airflow config folder. Then install the requirements by running `pip install -r requirements.txt` inside of your airflow python environment.

## Running the DAG as a standalone python script.

The provided dag can also be run as a standalone python script. To do this, first install the required packages:

`pip install requests pandas`

Then run the script:

`python airflow_project/dags/jsonplaceholder_dag.py`

The script will download data from the jsonplaceholder API, transform it, and save it to a CSV file in the /tmp directory.

## Running the data extraction script as a standalone python script.

The data extraction portion of the dag can also be run as a standalone python script, without the airflow components. This is useful for testing, or running the data extraction part of the dag without running the full Airflow environment. To do this, create a new python file called `extract_data.py` in the airflow_project directory, and copy the following contents into it:

```python
import requests
import pandas as pd

API_URL = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(API_URL)
response.raise_for_status()

data = response.json()
df = pd.DataFrame(data)

df.to_csv("/tmp/jsonplaceholder_data.csv", index=False)
print("Data saved to /tmp/jsonplaceholder_data.csv")
```

Then run the script:

`python extract_data.py`

The script will download data from the jsonplaceholder API, and save it to a CSV file in the /tmp directory.


## Developement tools

Install all requirements using pip on venv:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r dev-requirements.txt
```

### Testing

To run the tests for the DAG's Python functions, follow these steps:

1.**Install development requirements:**
    ```bash
    pip install -r dev-requirements.txt
    ```

2.**Navigate to the project root:**
    ```bash
    cd airflow_project
    ```

3.**Run the tests:**
    ```bash
    pytest tests/
    ```

This will execute the test suite located in the `tests/` directory and display the test results.

**Code Coverage:**

To check the code coverage of your tests, you can run:

```bash
pytest --cov-report=term --cov-report=html --cov=./dags tests/
```

This will generate a coverage report in terminal and in a new directory called htmlcov showing the percentage of code lines covered by your tests.

Note: Ensure you have pytest and coverage installed from the dev-requirements.txt file.

### Formatting

To format the code in the project, run:

```bash
black ./dags/ tests/
```

This will format the code using the [Black](https://github.com/psf/black) formatter.

### Linting

To check your code for style errors and potential bugs using flake8, run the following:

```bash
flake8 ./dags/ tests/
```

This will check the code using [flake8](https://github.com/PyCQA/flake8).

## Notes

-   The default admin credentials are username `airflow` and password `airflow`. Change these immediately for production use.
-   The `config` directory contains an example of how to set airflow variables.
-   The `dags` directory is where you will place your Airflow DAG files.

## Licensing

Licensed under the Apache License, Version 2.0 (the "License");

see [LICENSE](./LICENSE) for more information.
