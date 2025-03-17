from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import os

# API endpoint
API_URL = "https://jsonplaceholder.typicode.com/posts"

# Define the output dataset
OUTPUT_FILE = "/opt/airflow/data/jsonplaceholder_data.csv"
DATASET_URI = f"file://{OUTPUT_FILE}"
OUTPUT_DATASET = Dataset(DATASET_URI)

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 14),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'jsonplaceholder_data_pipeline',
    default_args=default_args,
    schedule_interval='0 0 * * *',  # Run daily at midnight
    catchup=False,
    description='Extract, transform, and load JSONPlaceholder data into a dataset.',
)

# Task 1: Extract data from the API
def extract_data(**kwargs):
    """Extracts data from the JSONPlaceholder API."""
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    kwargs['ti'].xcom_push(key='api_data', value=data)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

# Task 2: Transform the data (extract relevant fields)
def transform_data(**kwargs):
    """Extracts relevant fields."""
    api_data = kwargs['ti'].xcom_pull(task_ids='extract_data', key='api_data')
    df = pd.DataFrame(api_data)
    kwargs['ti'].xcom_push(key='transformed_data', value=df.to_json(date_format='iso'))

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

# Task 3: Load the transformed data into a CSV file and produce a dataset
def load_data(**kwargs):
    """Loads the transformed data into a CSV file and updates the dataset."""
    transformed_data_json = kwargs['ti'].xcom_pull(task_ids='transform_data', key='transformed_data')
    df = pd.read_json(transformed_data_json, orient='columns')
    
    output_dir = "/opt/airflow/data"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "jsonplaceholder_data.csv")
    
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
    outlets=[OUTPUT_DATASET],  # Declare the dataset as an output
)

# Define task dependencies
extract_task >> transform_task >> load_task