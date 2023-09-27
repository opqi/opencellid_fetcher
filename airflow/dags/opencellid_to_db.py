from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models import Variable
from datetime import datetime
import os
import sys

path = os.path.expanduser('/opt/airflow/')

# Add the data folder and ZIP file path to the environment variables
os.environ['PROJECT_PATH'] = path

# Add the data folder to the $PATH so that you can import functions
sys.path.insert(0, path)

from pipelines.opencellid.push_data import push_data_to_clickhouse
from pipelines.opencellid.fetch_data import fetch_opencellid_data

default_args = {
    'owner': 'pdmitriev',
    'start_date': datetime(2023, 9, 20),
    'retries': 1,
}

dag = DAG(
    dag_id='mcc_filtered_dag',
    default_args=default_args,
    description='Load OpenCellId data into ClickHouse using PySpark',
    schedule_interval='0 1 * * *',
    catchup=False,
)

fetch_data_task = PythonOperator(
    task_id='fetch_opencellid',
    python_callable=fetch_opencellid_data,
    dag=dag,
)

# Add a BashOperator to unzip the downloaded data file to the 'data' folder
unzip_data_task = BashOperator(
    task_id='unzip_opencellid_data',
    bash_command='gunzip {{ ti.xcom_pull(task_ids="fetch_opencellid") }}',
    dag=dag,
)

# Add a PythonOperator to push the unzipped data to ClickHouse
push_to_clickhouse_task = PythonOperator(
    task_id='push_to_clickhouse',
    python_callable=push_data_to_clickhouse,
    provide_context=True,
    dag=dag,
)

# Add a BashOperator to clean up the 'data' folder
clean_data_task = BashOperator(
    task_id='clean_data_folder',
    bash_command='rm -rf {{ ti.xcom_pull(task_ids="push_to_clickhouse") }}',
    dag=dag,
)

# Set task dependencies
fetch_data_task >> unzip_data_task >> push_to_clickhouse_task >> clean_data_task
