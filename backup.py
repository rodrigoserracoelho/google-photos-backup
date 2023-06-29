import os
from pathlib import Path
import requests

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

CURRENT_DIR = os.getcwd()
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
CREDENTIALS_FILE = CURRENT_DIR + '/credentials.json'
TOKEN_FILE_PATH = Path(Path.cwd(), CURRENT_DIR, "token.json")
# Make sure that you authorize this port for redirect on Google Api Console
PORT = 46629
DOWNLOAD_PATH = '/<your>/<directory>/<of>/<preference>/'
TIMESTAMP_FILE_NAME = '/last_timestamp.txt'


def get_token():
    cred_path = Path(CREDENTIALS_FILE)
    cred = None
    if TOKEN_FILE_PATH.exists():
        print("Exists....")
        cred = Credentials.from_authorized_user_file(str(TOKEN_FILE_PATH), SCOPES)
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(cred_path), SCOPES
            )
            cred = flow.run_local_server(port=PORT)
        with open(TOKEN_FILE_PATH, 'w') as file:
            file.write(cred.to_json())
        return cred
    return cred


def download_all_photos(service):
    page_token = None
    last_timestamp = load_last_timestamp()
    new_photos_count = 0
    continue_download = True
    latest_timestamp = None

    while continue_download:
        response = service.mediaItems().list(pageToken=page_token).execute()
        items = response.get('mediaItems', [])

        for item in items:
            photo_id = item['id']
            photo_url = item['baseUrl'] + "=d"
            photo_filename = f"{photo_id}.jpg"
            photo_timestamp = item['mediaMetadata']['creationTime']

            if photo_timestamp > last_timestamp:
                if new_photos_count == 0:
                    latest_timestamp = photo_timestamp

                download_photo(photo_url, DOWNLOAD_PATH + photo_filename)
                new_photos_count += 1

                page_token = response.get('nextPageToken')
                if not page_token:
                    print("Will break...")
                    exit()
            else:
                save_last_timestamp(latest_timestamp)
                print(f"Downloaded {new_photos_count} new photos.")
                exit()


def load_last_timestamp():
    timestamp_file_path = Path(Path.cwd(), CURRENT_DIR + TIMESTAMP_FILE_NAME)
    if timestamp_file_path.exists():
        with open(timestamp_file_path, 'r') as f:
            return f.read().strip()
    else:
        return None


def save_last_timestamp(timestamp):
    timestamp_file_path = Path(Path.cwd(), CURRENT_DIR + TIMESTAMP_FILE_NAME)
    with open(timestamp_file_path, 'w') as f:
        f.write(timestamp)


def download_photo(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded photo: {destination}")
    else:
        print(f"Failed to download photo: {url}")


# Get credentials, this may result on a redirect for authentication
credentials = get_token()
# Build the Google Photos Library API Object with the provided credentials
service = build('photoslibrary', 'v1', credentials=credentials, static_discovery=False)
# Download Files
download_all_photos(service)
