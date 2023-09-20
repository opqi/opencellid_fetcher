from airflow.models import Variable
from pyspark.sql import SparkSession
from clickhouse_driver import Client
from loguru import logger
import requests


# MCC codes you want to filter
mcc_codes = [262, 460, 310, 208, 510, 404, 250, 724, 234, 311]
mcc_param = ",".join(str(code) for code in mcc_codes)

api_key = Variable.get("OPENCELLID_API_KEY")
clickhouse_username = Variable.get("CLICKHOUSE_AIRFLOW_USER")
clickhouse_password = Variable.get("CLICKHOUSE_AIRFLOW_PASS")
clickhouse_server_url = Variable.get("CLICKHOUSE_SERVER_URL")
    

def fetch_opencellid_data():
    # Fetch data from the OpenCellId API and insert it into ClickHouse using PySpark
    spark = SparkSession.builder.appName("OpenCellId").getOrCreate()
    
    table = 'cell_towers'
    
    clickhouse_client = Client(clickhouse_server_url, user=clickhouse_username, password=clickhouse_password)
    
    url = f"https://api.opencellid.org/cell/get/key={api_key}&mcc={mcc_param}&format=json"
    context = 'cacert.pem'

    response = requests.get(url, verify=context)
    data = response.json()

    if 'error' not in data:
        df = spark.createDataFrame(data)
        df.write.format("clickhouse").option("url", clickhouse_server_url).option("dbtable", table).save()
            
        logger.info(f"Inserted data for MCC {mcc_param} into ClickHouse.")

    spark.stop()