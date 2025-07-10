import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os

SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]

creds_json = {
    "type": os.getenv("GCP_TYPE"),
    "project_id": os.getenv("GCP_PROJECT_ID"),
    "private_key_id": os.getenv("GCP_PRIVATE_KEY_ID"),
    "private_key": os.getenv("GCP_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("GCP_CLIENT_EMAIL"),
    "client_id": os.getenv("GCP_CLIENT_ID"),
    "auth_uri": os.getenv("GCP_AUTH_URI"),
    "token_uri": os.getenv("GCP_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("GCP_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("GCP_CLIENT_X509_CERT_URL")
}

CREDS = Credentials.from_service_account_info(creds_json, scopes=SCOPE)
CLIENT = gspread.authorize(CREDS)

# Replace with your Google Sheet name
SHEET_NAME = "CNAM_Schedule"

def get_sheet():
    """Get the worksheet."""
    return CLIENT.open(SHEET_NAME).sheet1

def get_all_courses():
    """Get all courses from the Google Sheet."""
    sheet = get_sheet()
    records = sheet.get_all_records()
    return pd.DataFrame(records)

def get_all_homework():
    """Get all homework from the Google Sheet."""
    # Assuming you have a separate sheet for homework
    try:
        sheet = CLIENT.open(SHEET_NAME).worksheet("Homework")
        records = sheet.get_all_records()
        return pd.DataFrame(records)
    except gspread.exceptions.WorksheetNotFound:
        return pd.DataFrame()
