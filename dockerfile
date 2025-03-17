FROM apache/airflow:2.8.1
USER airflow
RUN pip install --no-cache-dir requests pandas
# No USER root - stay as airflow