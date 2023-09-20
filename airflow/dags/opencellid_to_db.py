from airflow import DAG
from airflow.operators.http_sensor import HttpSensor
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime

path = os.path.expanduser('/opt/airflow/')
# Добавим путь к коду проекта в переменную окружения, чтобы он был доступен python-процессу
os.environ['PROJECT_PATH'] = path
# Добавим путь к коду проекта в $PATH, чтобы импортировать функции
sys.path.insert(0, path)

from pipelines.opencellid.getdata import fetch_opencellid_data 

default_args = dict(
    'owner': 'pdmitriev',
    'start_date': datetime(2023, 9, 20),
    'retries': 1,
)

dag = DAG(
    dag_id = 'mcc_filtered_dag',
    default_args=default_args,
    description='Load OpenCellId data into ClickHouse using PySpark'
    scedule_interval = '0 1 * * *',
    catchup = False,
)

fetch_data_task = PythonOperator(
    task_id='fetch_open_cell_id_data',
    python_callable=fetch_opencellid_data,
    dag=dag,
)

# Add a sensor to check if the OpenCellId API is available
api_sensor = HttpSensor(
    task_id='check_opencellid_api',
    http_conn_id='http_opencellid_api',
    method='GET',
    endpoint=f'cell/get?key={Variable.get("OPENCELLID_API_KEY")}&mcc=262&format=json',
    poke_interval=60,
    timeout=30,
    dag=dag,
)

api_sensor >> fetch_data_task