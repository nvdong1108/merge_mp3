from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Đường dẫn tới file OAuth 2.0
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/youtube"]
TOKEN_FILE = "token.json"

# youtube = build('youtube', 'v3', developerKey='AIzaSyBWJmYywQ8S0OxpJR_lqn4HMfOVfkFSlvQ')

# video_id = 'VIDEO_ID'

# localizations = {
#     'ja': 'Lesson 38 : レッスン12：日常英会話を学ぼう',
#     'ko': 'Lesson 38 : Lesson 12: 일상 영어 회화 배우기'
# }
# request = youtube.videos().update(
#     part='localizations',
#     body={
#         'id': video_id,
#         'localizations': localizations
#     }
# )
# response = request.execute()
# print(response)

def get_video_ids(channel_id):
    
    TOKEN_FILE = "token.json"

    # credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
            
        with open(TOKEN_FILE, 'w') as f:
            f.write(credentials.to_json())
    
    youtube = build("youtube", "v3", credentials=credentials)
    print(f" go here ")

    # request = youtube.search().list(
    #     part='id,snippet',
    #     channelId=channel_id,
    #     type='video',
    #     videoDuration='short'
    # )
    # response = request.execute()
    # video_ids = [item['id']['videoId'] for item in response['items']]
    # return video_ids


def main():
    channel_id = 'UCexURC626MmhlLJrz_of92g'
    video_ids = get_video_ids(channel_id)
    print('Danh sách video_id:', video_ids)


if __name__ == '__main__':
    main()