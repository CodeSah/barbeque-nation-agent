import os
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your service account credentials JSON file
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'creds.json')

# The ID of your Google Sheet (get from the sheet URL)
SPREADSHEET_ID = '13cGks74I6483YfpYqp0H4CVHRpuJ1G24ChcoopKiDnI'

# The sheet name where you want to log the data
SHEET_NAME = 'Sheet1'

# Define the scope for Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Load credentials and build the service client
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('sheets', 'v4', credentials=credentials)

def log_conversation(data):
    """
    Logs conversation data to Google Sheet.
    Expected data keys:
    - Modality
    - Call Time (YYYY-MM-DD HH:MM:SS)
    - Phone Number
    - Call Outcome
    - Room Name (optional)
    - Booking Date (YYYY-MM-DD or 'NA')
    - Booking Time (HH:MM or 'NA')
    - Number of Guests
    - Call Summary
    """
    # Prepare row values in order as per the Google Sheet columns
    row = [
        data.get('Modality', 'NA'),
        data.get('Call Time', 'NA'),
        data.get('Phone Number', 'NA'),
        data.get('Call Outcome', 'NA'),
        data.get('Room Name', 'NA'),
        data.get('Booking Date', 'NA'),
        data.get('Booking Time', 'NA'),
        str(data.get('Number of Guests', 'NA')),
        data.get('Call Summary', 'NA'),
    ]

    body = {
        'values': [row]
    }

    # Append row to the sheet
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{SHEET_NAME}!A1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

    return result
