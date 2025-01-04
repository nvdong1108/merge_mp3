from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow



SCOPES = ["https://www.googleapis.com/auth/youtube"]

# Đường dẫn tới file OAuth2 JSON
CLIENT_SECRETS_FILE = "client_secrets.json"

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_local_server(port=8080)

with open('token.json', 'w') as token_file:
    token_file.write(credentials.to_json())


