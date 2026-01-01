import io
import os
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']
TOKEN_FILE = Path.home() / ".omr_app" / "token.pickle"
CREDENTIALS_FILE = Path.home() / ".omr_app" / "credentials.json"
LOCAL_JSON = Path("data/question_bank.json")
DRIVE_FILE_NAME = "question_bank.json"

def authenticate():
    creds = None
    TOKEN_FILE.parent.mkdir(exist_ok=True)

    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    service = build('drive', 'v3', credentials=creds)
    return service

def download_json():
    service = authenticate()
    # search file in Drive
    results = service.files().list(
        q=f"name='{DRIVE_FILE_NAME}'",
        spaces='drive',
        fields="files(id, name)"
    ).execute()
    files = results.get('files', [])
    if not files:
        print("Drive file not found, creating new local JSON")
        return False
    file_id = files[0]['id']

    request = service.files().get_media(fileId=file_id)
    LOCAL_JSON.parent.mkdir(exist_ok=True)
    fh = io.FileIO(LOCAL_JSON, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        # Optional: print(f"Download {int(status.progress() * 100)}%")
    return True

def upload_json():
    service = authenticate()
    # check if file exists
    results = service.files().list(
        q=f"name='{DRIVE_FILE_NAME}'",
        spaces='drive',
        fields="files(id, name)"
    ).execute()
    files = results.get('files', [])
    media = MediaFileUpload(LOCAL_JSON, mimetype='application/json', resumable=True)
    if files:
        file_id = files[0]['id']
        service.files().update(fileId=file_id, media_body=media).execute()
    else:
        file_metadata = {'name': DRIVE_FILE_NAME}
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()

