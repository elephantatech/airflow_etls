# tests/test_dag_functions.py
import pytest
import requests
import pandas as pd
from airflow.models import TaskInstance
from airflow.utils.context import Context
from airflow_project.dags.jsonplaceholder_dag import extract_data, transform_data, load_data

API_URL = "https://jsonplaceholder.typicode.com/posts"

def test_extract_data(mocker):
    # Mock the requests.get call
    mock_response = mocker.Mock()
    mock_response.json.return_value = [{"userId": 1, "id": 1, "title": "test", "body": "test body"}]
    mock_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_response)

    # Mock TaskInstance
    ti = TaskInstance(task=None)
    context = Context(ti=ti)

    # Call the function
    extract_data(**context)

    # Assertions
    assert ti.xcom_pull(key='api_data') == [{"userId": 1, "id": 1, "title": "test", "body": "test body"}]
    requests.get.assert_called_once_with(API_URL)

def test_transform_data(mocker):
    # Mock XCom pull
    ti = TaskInstance(task=None)
    ti.xcom_push(key='api_data', value=[{"userId": 1, "id": 1, "title": "test", "body": "test body"}])
    context = Context(ti=ti)
    context['ti'].xcom_pull = mocker.Mock(return_value=[{"userId": 1, "id": 1, "title": "test", "body": "test body"}])

    # Mock TaskInstance
    ti2 = TaskInstance(task=None)
    context2 = Context(ti=ti2)
    context2['ti'].xcom_pull = mocker.Mock(return_value=[{"userId": 1, "id": 1, "title": "test", "body": "test body"}])

    # Call the function
    transform_data(**context2)

    # Assertions
    result = ti2.xcom_pull(key='transformed_data')
    df = pd.read_json(result)
    assert df.shape == (1, 4)

def test_load_data(mocker):
        # Mock XCom pull
    ti = TaskInstance(task=None)
    ti.xcom_push(key='transformed_data', value='[{"userId": 1, "id": 1, "title": "test", "body": "test body"}]')
    context = Context(ti=ti)
    context['ti'].xcom_pull = mocker.Mock(return_value='[{"userId": 1, "id": 1, "title": "test", "body": "test body"}]')

    # Mock pandas to_csv
    mocker.patch("pandas.DataFrame.to_csv")

    # Call the function
    load_data(**context)

    # Assertions
    pd.DataFrame.to_csv.assert_called_once()