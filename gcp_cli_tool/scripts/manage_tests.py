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

# Export DataFrame to Google Sheet with conditional formatting
def export_to_sheet(df, sheet_name):
    client = authenticate_google_sheets()
    sheet = create_or_open_sheet(client, sheet_name)
    worksheet = sheet.get_worksheet(0)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    # Optional: Add conditional formatting here using gspread

# Example DataFrame
def main():
    data = {
        'Test Case': ['Test 1', 'Test 2'],
        'Status': ['Pass', 'Fail'],
        'Details': ['Detail 1', 'Detail 2']
    }
    df = pd.DataFrame(data)
    export_to_sheet(df, 'Test Results')

if __name__ == "__main__":
    main()