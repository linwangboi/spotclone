import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()


def top_tracks():
    url = 'https://api.spotify.com/v1/me/top/tracks?limit=30&offset=0'
    SPOTIFY_TOKEN = os.getenv("SPOTIFY_TOKEN")
    headers = {
        "Authorization": f'Bearer {SPOTIFY_TOKEN}',
        "Content-Type": 'application/json',
    }

    res = requests.get(url, headers=headers).json()
    tracks = []

    for item in res.get('items', []):
        if item.get('type') == 'track':
            track_id = item.get('id')
            track_name = item.get('name')
            
            # Take first artist's name
            artists_list = item.get('artists', [])
            artist_name = artists_list[0]['name'] if artists_list else 'Unknown'
            
            # Take first image from album
            album_images = item.get('album', {}).get('images', [])
            cover_url = album_images[0]['url'] if album_images else None

            tracks.append({
                "id": track_id,
                "name": track_name,
                "artist": artist_name,
                "cover_url": cover_url
            })

    return tracks

tracks = top_tracks()
with open('tracks_data.py', 'w', encoding='utf-8') as f:
    f.write('top_tracks = ')
    f.write(json.dumps(tracks, indent=4))
    f.write('\n')