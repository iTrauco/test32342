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
    file_name = f'marijuana_sales_data{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
    blob = bucket.blob(file_name)
    blob.upload_from_string(csv_data, content_type='text/csv')

    print(f"File {file_name} uploaded to {BUCKET_NAME}.")

    return f"File {file_name} uploaded successfully."
