import os
import time
import json
import requests
import logging
import zipfile
from google.cloud import functions_v1, storage, bigquery
from google.api_core.exceptions import GoogleAPIError, NotFound
from google.api_core import operation
from google.protobuf.json_format import MessageToDict
from google.longrunning import operations_pb2
from utils.state_manager import read_state, write_state

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to create a zip file
def create_zip_file(zip_filename, files):
    try:
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file in files:
                zipf.write(file, os.path.basename(file))
        logger.info(f"Created zip file: {zip_filename}")
    except Exception as e:
        logger.error(f"Error creating zip file: {e}")

# Function to upload a file to a GCS bucket
def upload_to_bucket(bucket_name, source_file_name, destination_blob_name):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        logger.info(f"Uploaded {source_file_name} to bucket {bucket_name} as {destination_blob_name}")
    except Exception as e:
        logger.error(f"Error uploading file to bucket: {e}")

# Function to delete existing Cloud Function
def delete_cloud_function(function_name, project_id, region):
    client = functions_v1.CloudFunctionsServiceClient()
    try:
        function_path = f'projects/{project_id}/locations/{region}/functions/{function_name}'
        client.delete_function(name=function_path)
        logger.info(f"Deleted existing function: {function_name}")
    except GoogleAPIError as e:
        logger.error(f"Error deleting existing function: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while deleting function: {e}")

# Function to create a bucket if it doesn't exist
def get_or_create_bucket(bucket_name, project_id, region):
    client = storage.Client()
    try:
        bucket = client.get_bucket(bucket_name)
        logger.info(f"Using existing bucket: {bucket_name}")
    except NotFound:
        try:
            bucket = client.create_bucket(bucket_name, location=region)
            logger.info(f"Created new bucket: {bucket_name}")
        except Exception as e:
            logger.error(f"Error creating bucket: {e}")
    return bucket

# Function to create a BigQuery dataset if it doesn't exist
def get_or_create_dataset(dataset_id, project_id, region):
    client = bigquery.Client()
    try:
        dataset = client.get_dataset(dataset_id)
        logger.info(f"Using existing dataset: {dataset_id}")
    except NotFound:
        try:
            dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")
            dataset.location = region
            dataset = client.create_dataset(dataset)
            logger.info(f"Created new dataset: {dataset_id}")
        except Exception as e:
            logger.error(f"Error creating dataset: {e}")
    return dataset

# Function to deploy Cloud Function
def deploy_cloud_function():
    try:
        # Read the configuration
        state = read_state()

        # Collect user inputs for Cloud Function configuration
        function_name = input(f"Enter the Cloud Function name (default: fetchAndUploadCSV): ") or "fetchAndUploadCSV"
        entry_point = input(f"Enter the entry point function name (default: fetch_and_upload_csv): ") or "fetch_and_upload_csv"
        runtime = input(f"Enter the runtime (e.g., python310) (default: python310): ") or "python310"
        region = input(f"Enter the region (default: us-central1): ") or "us-central1"
        memory = int(input(f"Enter the memory allocation (e.g., 128, 256) (default: 256): ") or "256")
        timeout = input(f"Enter the timeout (in seconds, e.g., 60, 300) (default: 60s): ") or "60s"
        trigger = input(f"Enter the trigger type (http, bucket, pubsub) (default: http): ") or "http"
        bucket_name = input(f"Enter your bucket name (default: {state.get('bucket_name', 'your-bucket-name')}): ") or state.get('bucket_name', 'your-bucket-name')
        sheet_url = input(f"Enter your Google Sheet URL (default: {state.get('sheet_url', 'your-sheet-url')}): ") or state.get('sheet_url', 'your-sheet-url')
        project_id = input(f"Enter your project ID (default: {state.get('project_id', 'your-project-id')}): ") or state.get('project_id', 'your-project-id')

        # Update the state
        state.update({
            'function_name': function_name,
            'entry_point': entry_point,
            'runtime': runtime,
            'region': region,
            'memory': memory,
            'timeout': timeout,
            'trigger': trigger,
            'bucket_name': bucket_name,
            'sheet_url': sheet_url,
            'project_id': project_id
        })
        write_state(state)

        # Ensure bucket exists
        get_or_create_bucket(bucket_name, project_id, region)

        # Write the Cloud Function code to main.py
        function_code = f"""
import os
import gspread
import pandas as pd
from google.auth.transport.requests import Request
from google.cloud import storage
from datetime import datetime
import google.auth

# Set environment variables
BUCKET_NAME = os.getenv('BUCKET_NAME')
SHEET_URL = os.getenv('SHEET_URL')
PROJECT_ID = os.getenv('PROJECT_ID')

def fetch_and_upload_csv(request):
    """Fetch data from a Google Sheet, convert it to CSV, and upload it to Cloud Storage."""
    credentials, project = google.auth.default()
    gc = gspread.authorize(credentials)

    # Open the Google Sheet
    sheet = gc.open_by_url(SHEET_URL).get_worksheet(0)
    data = sheet.get_all_records()

    # Convert the data to a DataFrame and then to CSV
    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False)

    # Define the Cloud Storage client and upload the CSV
    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)
    file_name = f'marijuana_sales_data{{datetime.now().strftime("%Y%m%d%H%M%S")}}.csv'
    blob = bucket.blob(file_name)
    blob.upload_from_string(csv_data, content_type='text/csv')

    print(f"File {{file_name}} uploaded to {{BUCKET_NAME}}.")

    return f"File {{file_name}} uploaded successfully."
"""
        with open('main.py', 'w') as f:
            f.write(function_code)
        logger.info('main.py file written locally.')

        # Generate requirements.txt
        requirements = """
gspread
pandas
google-auth
google-cloud-storage
"""
        with open('requirements.txt', 'w') as f:
            f.write(requirements)
        logger.info('requirements.txt file written locally.')

        # Create a zip file containing the function code and requirements
        zip_filename = 'function_deploy.zip'
        create_zip_file(zip_filename, ['main.py', 'requirements.txt'])

        # Upload the zip file to the bucket
        upload_to_bucket(bucket_name, zip_filename, zip_filename)

        # Manually construct the function path
        function_path = f'projects/{project_id}/locations/{region}/functions/{function_name}'

        # Define trigger based on user input
        trigger_config = {}
        if trigger == "http":
            trigger_config = {'https_trigger': {}}
        elif trigger == "bucket":
            bucket_trigger = input(f"Enter the bucket name to trigger the function (default: {bucket_name}): ") or bucket_name
            trigger_config = {'event_trigger': {
                'event_type': 'google.storage.object.finalize',
                'resource': f'projects/_/buckets/{bucket_trigger}'
            }}
        elif trigger == "pubsub":
            pubsub_topic = input(f"Enter the Pub/Sub topic name (default: projects/{project_id}/topics/your-topic): ") or f"projects/{project_id}/topics/your-topic"
            trigger_config = {'event_trigger': {
                'event_type': 'google.pubsub.topic.publish',
                'resource': pubsub_topic
            }}

        # Construct the Cloud Function configuration
        cloud_function = {
            'name': function_path,
            'entry_point': entry_point,
            'runtime': runtime,
            'source_archive_url': f'gs://{bucket_name}/{zip_filename}',
            'environment_variables': {
                'BUCKET_NAME': bucket_name,
                'SHEET_URL': sheet_url,
                'PROJECT_ID': project_id
            },
            'timeout': timeout,
            'available_memory_mb': memory,
            **trigger_config
        }

        # Deploy the function
        client = functions_v1.CloudFunctionsServiceClient()
        try:
            operation = client.create_function(
                request={'location': f'projects/{project_id}/locations/{region}', 'function': cloud_function}
            )
        except GoogleAPIError as e:
            if e.code == 409:  # Function already exists
                logger.info(f"Function {function_name} already exists, updating it...")
                operation = client.update_function(
                    request={'function': cloud_function}
                )
            else:
                raise

        logger.info('Deploying function...')
        logger.info('Waiting for operation to complete...')

        # Handling long-running operations (Corrected)
        while not operation.done():
            logger.info("Deployment in progress...")
            time.sleep(5)

        if operation.exception():
            raise operation.exception()

        response = operation.result()  # Get the result directly
        logger.info('Function deployed successfully!')
        logger.info(MessageToDict(response))

        # Retrieve the function URL dynamically if HTTP trigger is used
        if trigger == "http":
            function_details = client.get_function(request={'name': function_path})
            function_url = function_details.https_trigger.url
            logger.info(f"Function URL: {function_url}")

            # Test the Cloud Function
            response = requests.get(function_url)
            logger.info(f"Function response: {response.text}")

    except GoogleAPIError as e:
        logger.error(f"Error during function deployment or testing: {e}")

    except Exception as e:
        logger.error(f"Unexpected error during function deployment or testing: {e}")

    finally:
        # Clean up local zip file
        if os.path.exists(zip_filename):
            os.remove(zip_filename)
            logger.info(f"Deleted local zip file: {zip_filename}")
        print("
" + "="*50 + "
")

# Call function to deploy Cloud Function
deploy_cloud_function()
