# manage_tests.py
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Setup the Google Sheets API client
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client

# Create or open a Google Sheet
def create_or_open_sheet(client, sheet_name):
    try:
        sheet = client.open(sheet_name)
    except gspread.SpreadsheetNotFound:
        sheet = client.create(sheet_name)
    return sheet

# Read the log file and convert it to a DataFrame
def log_to_dataframe(log_file_path):
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
    
    # Process the log file to create a DataFrame
    data = []
    for line in lines:
        if "ERROR" in line:
            level = 'Error'
        elif "INFO" in line:
            level = 'Info'
        else:
            continue

        timestamp, _, message = line.partition(' - ')
        data.append([timestamp, level, message.strip()])

    df = pd.DataFrame(data, columns=['Timestamp', 'Level', 'Message'])
    return df

# Export DataFrame to Google Sheet with conditional formatting
def export_to_sheet(df, sheet_name):
    client = authenticate_google_sheets()
    sheet = create_or_open_sheet(client, sheet_name)
    worksheet = sheet.get_worksheet(0)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    # Optional: Add conditional formatting here using gspread

# Example usage
def main():
    df = log_to_dataframe('test_results.log')
    export_to_sheet(df, 'Test Results')

if __name__ == "__main__":
    main()
