import json
import requests

# Put API Key here
API_KEY = ""

# YouTube API Search Endpoint
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

# Channel IDs (Replace/Add more if needed)
informative_channels = [
]
timewaste_channels = [
]

def get_video_links(channel_id):
    """Fetch video links for a given channel ID."""
    params = {
        "part": "snippet",
        "channelId": channel_id,
        "maxResults": 10, # Set it
        "type": "video",
        "order": "date",
        "key": API_KEY
    }
    try:
        response = requests.get(SEARCH_URL, params=params)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network or Request Error for {channel_id}: {e}")
        return []
    except json.JSONDecodeError:
        print(f"Invalid JSON response from API for {channel_id}.")
        return []

    # Check for errors in API response
    if "error" in data:
        print(f"API Error for {channel_id}: {data['error']['message']}")
        return []

    video_links = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        video_links.append(f"https://www.youtube.com/watch?v={video_id}")

    print(f"Extracted {len(video_links)} links from {channel_id}")
    return video_links

def save_to_json(filename, links):
    """Save video links to a JSON file."""
    with open(filename, "w") as f:
        json.dump(links, f, indent=4)
    print(f"📁 Saved {len(links)} links to {filename}")

if __name__ == "__main__":
    # Fetch and save video links for informative channels
    informative_links = []
    for channel in informative_channels:
        informative_links.extend(get_video_links(channel))
    save_to_json("informative.json", informative_links)
    
    # Fetch and save video links for time-waste channels
    timewaste_links = []
    for channel in timewaste_channels:
        timewaste_links.extend(get_video_links(channel))
    save_to_json("timewaste.json", timewaste_links)