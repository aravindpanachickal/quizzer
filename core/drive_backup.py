import os
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

APP_DIR = Path.home() / ".omr_quiz"
APP_DIR.mkdir(exist_ok=True)

TOKEN_FILE = APP_DIR / "token.json"
CRED_FILE = Path("credentials.json")

BACKUP_NAME = "omr_question_bank.json"


def get_drive_service():
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE, SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CRED_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("drive", "v3", credentials=creds)


def find_existing_file(service):
    response = service.files().list(
        q=f"name='{BACKUP_NAME}' and trashed=false",
        spaces="drive",
        fields="files(id, name)"
    ).execute()

    files = response.get("files", [])
    return files[0]["id"] if files else None


def backup_to_drive(local_file):
    try:
        service = get_drive_service()

        file_id = find_existing_file(service)

        media = MediaFileUpload(
            local_file, mimetype="application/json"
        )

        if file_id:
            service.files().update(
                fileId=file_id,
                media_body=media
            ).execute()
        else:
            service.files().create(
                body={"name": BACKUP_NAME},
                media_body=media,
                fields="id"
            ).execute()

    except Exception:
        # Silent failure — never crash quiz
        pass
