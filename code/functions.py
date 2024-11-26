import requests

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


def get_market(markets, token):
    url = "https://api.spotify.com/v1/markets"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": markets,
        "type": "market",
        "limit": 1
    }
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()