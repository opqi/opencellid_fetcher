# opencellid_fetcher

## Create .env file and run Airflow
cd airflow/
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker-compose up -d

## Create .env file for ClickHouse
cd clickhouse/
touch .env

### .env file should contain
CLICKHOUSE_LISTEN_HOST=your_host
CLICKHOUSE_LISTEN_PORT=your_listen_port
CLICKHOUSE_HTTP_PORT=your_http_port
CLICKHOUSE_NATIVE_PORT=your_native_port
CLICKHOUSE_NATIVE_TCP_PORT=your_tcp_port
CLICKHOUSE_DATA_PATH=/var/lib/clickhouse
CLICKHOUSE_TMP_PATH=/var/lib/clickhouse/tmp
CLICKHOUSE_USER_FILES_PATH=/var/lib/clickhouse/user_files
CLICKHOUSE_FORMAT_SCHEMA_PATH=/var/lib/clickhouse/format_schemas
CLICKHOUSE_LOG_PATH=/var/log/clickhouse-server/clickhouse-server.log
CLICKHOUSE_ERROR_LOG_PATH=/var/log/clickhouse-server/clickhouse-server.err.log
CLICKHOUSE_PART_LOG_PATH=/var/lib/clickhouse/ctries
CLICKHOUSE_AIRFLOW=your_username
CLICKHOUSE_AIRFLOW_PASS=your_pass

## Run ClickHouse
docker-compose up -d

## Set Variables in Airflow UI
airflow variables -s OPENCELLID_API_KEY your_api_key
airflow variables -s CLICKHOUSE_AIRFLOW your_username
airflow variables -s CLICKHOUSE_AIRFLOW_PASSWORD your_password
