from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models import Variable
from datetime import datetime
import os
import sys

path = os.path.expanduser('/opt/airflow/')
data_folder = os.path.join(path, 'data')  # Define the data folder path

# Define the path to the ZIP file using an Airflow Variable
zip_file_path = os.path.join(data_folder, 'cell_towers.csv.gz')

# Add the data folder and ZIP file path to the environment variables
os.environ['PROJECT_PATH'] = path
os.environ['DATA_FOLDER'] = data_folder
os.environ['ZIP_FILE_PATH'] = zip_file_path

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
    task_id='fetch_opencellid_data',
    python_callable=fetch_opencellid_data,
    dag=dag,
)

# Add a BashOperator to unzip the downloaded data file to the 'data' folder
unzip_data_task = BashOperator(
    task_id='unzip_opencellid_data',
    bash_command=f'gzip -d $ZIP_FILE_PATH',
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
    bash_command='rm -rf $DATA_FOLDER',
    dag=dag,
)

# Set task dependencies
fetch_data_task >> unzip_data_task >> push_to_clickhouse_task >> clean_data_task
