import requests
import os
from loguru import logger
from airflow.models import Variable


def fetch_opencellid_data():
    api_key = Variable.get("OPENCELLID_API_KEY")

    # Define the URL to download the data
    download_url = f"https://opencellid.org/ocid/downloads?token={api_key}&type=full&file=cell_towers.csv.gz"

    # Define the local file path where the data will be saved
    data_folder = os.path.expanduser('/opt/airflow/data/')  # Adjust the folder path as needed
    file_path = os.path.join(data_folder, 'cell_towers.csv.gz')

    # Create the data folder if it doesn't exist
    os.makedirs(data_folder, exist_ok=True)
    logger.info(f"Created temporary data folder {data_folder}")

    try:
        logger.info(f"Downloading data")
        # Send an HTTP GET request to the URL
        response = requests.get(download_url, stream=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open the local file and write the content of the response to it
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            logger.info(f"Downloaded data to {file_path}")
            Variable.set("opencellid_zip_file_path", file_path)
        else:
            logger.error(f"Failed to download data. Status code: {response.status_code}")

    except Exception as e:
        logger.error(f"Error occurred while downloading data: {str(e)}")

    return file_path

# Example usage
if __name__ == "__main__":
    from loguru import logger

    # Configure Loguru to log to a file
    log_file_path = '/opt/airflow/logs/fetch_data.log'
    logger.add(log_file_path, rotation='10 MB')

    fetch_opencellid_data()
