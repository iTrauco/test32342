# gcp_cli_tool/test_utils/results_export.py

import pandas as pd
import os
from gspread_utils import get_gspread_client, get_sheet, export_dataframe_to_sheet

def collect_test_results(log_file):
    # Parse the log file and convert it into a DataFrame
    with open(log_file, 'r') as file:
        log_data = file.readlines()
    
    # Assuming log_data is formatted; parse accordingly
    # Example DataFrame creation
    df = pd.DataFrame([line.split('|') for line in log_data], columns=['Test', 'Result', 'Details'])
    return df

def main():
    log_file = 'test_results.log'  # Path to the log file
    json_keyfile = 'path_to_credentials.json'  # Path to Google Sheets API credentials
    spreadsheet_id = 'your_spreadsheet_id'  # Google Sheets spreadsheet ID
    sheet_name = 'Sheet1'  # Name of the sheet to update

    # Collect test results
    df = collect_test_results(log_file)

    # Authorize and get sheet
    client = get_gspread_client(json_keyfile)
    sheet = get_sheet(client, spreadsheet_id, sheet_name)

    # Export to Google Sheets
    export_dataframe_to_sheet(df, sheet)

if __name__ == "__main__":
    main()
