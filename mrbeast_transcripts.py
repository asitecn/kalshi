import os
import requests
from youtube_transcript_api import YouTubeTranscriptApi

# Replace with your own YouTube API key
API_KEY = "YOUR_YOUTUBE_API_KEY"
CHANNEL_ID = "UCX6OQ3DkcsbYNE6H8uQQuVA"

def get_all_video_ids(api_key, channel_id):
    video_ids = []
    
    # First get the uploads playlist ID
    url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={api_key}"
    r = requests.get(url).json()
    uploads_playlist_id = r["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Paginate through playlist items
    next_page_token = None
    while True:
        playlist_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={uploads_playlist_id}&maxResults=50&key={api_key}"
        if next_page_token:
            playlist_url += f"&pageToken={next_page_token}"
        r = requests.get(playlist_url).json()
        
        for item in r["items"]:
            video_ids.append(item["contentDetails"]["videoId"])
        
        next_page_token = r.get("nextPageToken")
        if not next_page_token:
            break
    return video_ids


def download_transcripts(video_ids, output_folder="transcripts"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    for vid in video_ids:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(vid)
            with open(f"{output_folder}/{vid}.txt", "w", encoding="utf-8") as f:
                for entry in transcript:
                    f.write(entry["text"] + "\n")
            print(f"Downloaded transcript for {vid}")
        except Exception as e:
            print(f"No transcript for {vid} ({e})")


if __name__ == "__main__":
    video_ids = get_all_video_ids(API_KEY, CHANNEL_ID)
    download_transcripts(video_ids)
