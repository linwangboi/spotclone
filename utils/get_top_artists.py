import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()


def top_artists():
    url = 'https://api.spotify.com/v1/me/top/artists?limit=10&offset=0'
    SPOTIFY_TOKEN = os.getenv("SPOTIFY_TOKEN")
    headers = {
        "Authorization": f'Bearer {SPOTIFY_TOKEN}',
        "Content-Type": 'application/json',
    }
    res = requests.get(url, headers=headers).json()
    artists = []
    for item in res.get('items', []):  # <-- use 'items' not 'artists'
        artist_name = item.get('name', 'Unknown')
        images = item.get('images', [])
        artist_image_url = images[0]['url'] if images else None
        artist_id = item.get('id')
        
        artists.append((
            artist_name,
            artist_image_url,
            artist_id
        ))

    
    return artists

artists = top_artists()
with open('artists_data.py', 'w', encoding='utf-8') as f:
    f.write('top_artists = ')
    f.write(json.dumps(artists, indent=4))
    f.write('\n')