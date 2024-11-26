import requests
import pandas as pd

def search_artist(artist_name, token):
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": artist_name,
        "type": "artist",
        "limit": 1
    }
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def get_target_market(target_markets, token):
   url = "https://api.spotify.com/v1/markets"
   headers = {
        "Authorization": f"Bearer {token}"
    }
   response = requests.get(url, headers=headers)
   response.raise_for_status()  # Raise error if the request fails
   all_markets = response.json().get("markets", [])
   
   filtered_markets = [market for market in all_markets if market in target_markets]
   return {
        "requested_markets": target_markets,
        "available_markets": filtered_markets
    }
   response = requests.get(url, headers=headers, params=params)
   return response.json()


def get_featured_playlists(token, country, locale=None, limit=10):
    url = "https://api.spotify.com/v1/browse/featured-playlists"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "country": country,
        "locale": locale,
        "limit": limit
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status() 

    data = response.json()
    playlists = data['playlists']['items']
    
    playlist_data = []
    for playlist in playlists:
        playlist_data.append({
            "playlist_id": playlist['id'],
            "playlist_name": playlist['name'],
            "description": playlist['description'],
            "owner": playlist['owner']['display_name'],
            "num_tracks": playlist['tracks']['total'],
            "url": playlist['external_urls']['spotify']
        })
    
    return pd.DataFrame(playlist_data)