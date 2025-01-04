from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import json

SCOPES = ["https://www.googleapis.com/auth/youtube"]
CLIENT_SECRETS_FILE = "client_secrets.json"
TOKEN_FILE = "token.json"


# flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
# credentials = flow.run_local_server(port=8080)

# with open('token.json', 'w') as token_file:
#     token_file.write(credentials.to_json())


# youtube = build("youtube", "v3", credentials=credentials)

# request = youtube.channels().list(
#     part="snippet,contentDetails,statistics",
#     id="UCexURC626MmhlLJrz_of92g"  
# )

# response = request.execute()

# print(response)



def authenticate():
    """Authenticate the user and return credentials."""
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=8080)
    
    # Save credentials to a file
    with open(TOKEN_FILE, 'w') as token_file:
        token_file.write(credentials.to_json())
    
    return credentials


def get_channel_info(channel_id, credentials):
    """Fetch channel information from YouTube API."""
    youtube = build("youtube", "v3", credentials=credentials)
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()
    return response



def get_video_ids_from_channel(channel_id, credentials):
    """Fetch video IDs from a channel using YouTube API."""
    youtube = build("youtube", "v3", credentials=credentials)
    
    # Get the uploads playlist ID from the channel
    channel_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Fetch videos from the uploads playlist
    video_info = [] 
    next_page_token = None

    while True:
        playlist_items_response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in playlist_items_response["items"]:
            video_id = item["contentDetails"]["videoId"]
            
            video_response = youtube.videos().list(
                part="snippet",  # Only need snippet for title
                id=video_id
            ).execute()
            video_title = video_response["items"][0]["snippet"]["title"]
            video_info.append({"video_id": video_id, "title": video_title})

        next_page_token = playlist_items_response.get("nextPageToken")
        if not next_page_token:
            break

    return video_info


def get_valid_category_ids(credentials):
    """Get the valid video category IDs."""
    youtube = build("youtube", "v3", credentials=credentials)

    # Request to get the list of video categories
    category_response = youtube.videoCategories().list(
        part="snippet",
        regionCode="US"  # You can change this to any region you want, e.g., "IN" for India, "GB" for the UK, etc.
    ).execute()

    categories = category_response["items"]
    valid_category_ids = {category["snippet"]["title"]: category["id"] for category in categories}
    
    # print("Valid Categories:", valid_category_ids)
    return valid_category_ids



def main222():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"
    # CLIENT_SECRETS_FILE = "client_secrets.json"
    scopes_222 = scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes_222)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.i18nLanguages().list(
        
    )
    response = request.execute()

    print(response)



def update_video_localizations(video_id, credentials, localization_data, category_id) :
    """Update the video localizations (title and description) in multiple languages."""
    youtube = build("youtube", "v3", credentials=credentials)
    
    # Get the current video details
    video_response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()
    
    # Retrieve the video snippet
    video_snippet = video_response["items"][0]["snippet"]
    
    # Prepare the localization data
    localizations = video_snippet.get("localized", {})
    
    # Add or update localization data
    for language, data in localization_data.items():
        localizations[language] = {
            "title": data["title"],
            "description": data["description"]
        }
    
    # Prepare the request to update the video
    request_body = {
        "id": video_id,
        "snippet": {
            "categoryId": category_id,
            "title": video_snippet["title"],  # Keep the original title
            "description": video_snippet["description"],  # Keep the original description
            "localized": localizations  # Update localized titles/descriptions
        }
    }
    
    # Update the video
    request = youtube.videos().update(
        part="snippet",
        body=request_body
    )
    
    response = request.execute()
    
    print("Video updated with new localizations:")
    print("API Response: ", response)
    return response


def main():
    """Main function to authenticate and fetch channel information."""
    try:
        # Authenticate and get credentials
        credentials = authenticate()

        # Channel ID to fetch information for
        channel_id = "UCexURC626MmhlLJrz_of92g"

        # Get channel information
        # channel_info = get_channel_info(channel_id, credentials)
        # Print the channel information
        # print(json.dumps(channel_info, indent=4))

        # video_ids = get_video_ids_from_channel(channel_id, credentials)
        # print("Video IDs:", video_ids)


        valid_categories = get_valid_category_ids(credentials)
        # print("Choose a valid category ID from the list:", valid_categories)

        category_id = valid_categories.get("Education")

        localization_data = {
            "vi_VN": {
                "title": "レッスン38：毎日の英会話を学ぼう #面白い #learninghomeenglan #englishspeaking",
                "description": "英会話を楽しく学びましょう！毎日の英語会話でスピーキングを向上させる方法を学びます。"
            }
        }

        video_id = "-Up4XK1EOpI"
        update_video_localizations(video_id, credentials, localization_data, category_id)
  
    except Exception as e:
        print(f"An error occurred: {e}")






if __name__ == "__main__":
    # main()
    main222()


