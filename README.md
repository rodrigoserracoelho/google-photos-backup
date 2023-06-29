# Google Photos Backup

### Requirements:
- Python 3
- PIP
- google-api-core
- google-api-python-client
- google-auth
- google-auth-httplib2
- google-auth-oauthlib
- googleapis-common-protos

### Google Required Steps:
- Access to Google Cloud Console
- Create Project
- Access to project API Library and enable "Photos Library API"
- Go to your project API Credentials and create a Web Application
- In Authorized redirect URIs authorize your http://localhost:46629
- Download JSON and move it to this directory as "credentials.json"
- Run the script for the first time to trigger the login.

### Content:
- last_timestamp.txt (ex: 2022-01-01T00:00:00Z) 
```
All pictures stored after 2022-01-01 will be downloaded. After running the script will change this date with the latest photo date.
```
- credentials.json
```
To generate this file, follow the instructions above in the Google Required Steps section.
```
- token.json
```
This file will be generated after the first "manual" login
```
- backup.py
```
In the Python script change the variable DOWNLOAD_PATH to the path where you want to store the photos.
```