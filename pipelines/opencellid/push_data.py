from airflow.models import Variable
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime
from loguru import logger
import os

# MCC codes you want to filter
mcc_codes = [262, 460, 310, 208, 510, 404, 250, 724, 234, 311]
mcc_param = ",".join(str(code) for code in mcc_codes)

api_key = Variable.get("OPENCELLID_API_KEY")
clickhouse_username = Variable.get("CLICKHOUSE_AIRFLOW_USER")
clickhouse_password = Variable.get("CLICKHOUSE_AIRFLOW_PASS")
clickhouse_server_url = Variable.get("CLICKHOUSE_SERVER_URL")
clickhouse_server_url = f"{clickhouse_server_url}?user={clickhouse_username}&password={clickhouse_password}"
clickhouse_table = "opencellid.cell_tower"

def push_data_to_clickhouse(**kwargs):
    # Initialize SparkSession
    spark = SparkSession.builder.appName("DataIngestion").getOrCreate()
    ti = kwargs['ti']
    unpacked_path = ti.xcom_pull(task_ids='tmp_opencellid_data')
    logger.info(unpacked_path)
    unpacked_path = '.'.join(unpacked_path.split('.')[:-1])
    logger.info(f'Read csv file: {unpacked_path}')
    df = spark.read.csv(unpacked_path, header=True, inferSchema=True)

    filtered_df = df.filter(col('mcc').isin(mcc_codes))

    filtered_df = filtered_df.withColumn('cell', col('cell').cast('string'))
    filtered_df = filtered_df.withColumn('created_at', from_unixtime(col('created')))
    filtered_df = filtered_df.drop('created')
    filtered_df = filtered_df.withColumn('updated_at', from_unixtime(col('updated')))
    filtered_df = filtered_df.drop('updated')

    logger.info(f"Filtered data for MCC {mcc_param}.")

    # Write the DataFrame to ClickHouse
    filtered_df.write.format("clickhouse").option("url", clickhouse_server_url).option("dbtable", clickhouse_table).mode("append").save()

    logger.info(f"Inserted data for MCC {mcc_param} into ClickHouse.")
    spark.stop()

    return os.path.dirname(unpacked_path)

# Example usage
if __name__ == "__main__":
    from loguru import logger

    # Configure Loguru to log to a file
    log_file_path = '/opt/airflow/logs/push_data.log'
    logger.add(log_file_path, rotation='10 MB')

    push_data_to_clickhouse()