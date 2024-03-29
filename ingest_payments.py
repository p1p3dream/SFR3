from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime, timedelta
import pandas as pd
import requests
import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 25),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def get_dummy_json_data(date):
    # The base URL of the API
    url = 'https://paymentapp.com/payments'

    params = {'date': date.strftime('%Y-%m-%d')}  
    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def process_and_upload_to_s3():
    current_date = datetime.today()
    data = get_dummy_json_data(current_date)
    if data is not None:
        df = pd.json_normalize(data)
        
        # Convert DataFrame to Parquet
        parquet_buffer = df.to_parquet()

        # Upload to S3
        s3_hook = S3Hook(aws_conn_id='your_aws_conn_id')
        s3_hook.load_bytes(parquet_buffer, 
                           key='monthly_payments.parquet', 
                           bucket_name='payments_s3_bucket',
                           replace=True)
    else:
        print("No data received from API.")

def load_into_snowflake():
    copy_sql = """
    COPY INTO payments
    FROM @your_s3_stage/monthly_payments.parquet
    FILE_FORMAT = (TYPE = 'PARQUET');
    """
    return SnowflakeOperator(
        task_id='load_into_snowflake',
        snowflake_conn_id='sf_conn_id',
        sql=copy_sql
    )

with DAG('monthly_payments_pipeline', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:
    process_upload = PythonOperator(
        task_id='process_and_upload_to_s3',
        python_callable=process_and_upload_to_s3
    )

    load_snowflake = load_into_snowflake()

    process_upload >> load_snowflake
