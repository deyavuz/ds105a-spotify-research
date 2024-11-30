import os
import requests
from dotenv import load_dotenv
import base64

def get_token():
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    if not client_id or not client_secret:
        raise ValueError('You need to set CLIENT_ID and CLIENT_SECRET in your .env file')
    
    url = 'https://accounts.spotify.com/api/token'

    auth_string = f'{client_id}:{client_secret}'
    auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': f'Basic {auth_base64}'
    }
    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, headers=headers, data=data)

    if not response.ok:
        raise ValueError('Failed to get token. Status code: {response.status_code}, Response: {response.json()}')
    
    access_token = response.json().get('access_token')

    return {
        'Authorization': f'Bearer {access_token}'
    } 
if __name__ == '__main__':
    print(get_token())

def get_token2():
    client_id = os.getenv('CLIENT_ID_2')
    client_secret = os.getenv('CLIENT_SECRET_2')

    if not client_id or not client_secret:
        raise ValueError('You need to set CLIENT_ID and CLIENT_SECRET in your .env file')
    
    url = 'https://api.genius.com/oauth/token'

    auth_string = f'{client_id}:{client_secret}'
    auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': f'Basic {auth_base64}'
    }
    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, headers=headers, data=data)

    if not response.ok:
        raise ValueError('Failed to get token. Status code: {response.status_code}, Response: {response.json()}')
    
    access_token = response.json().get('access_token')

    return {
        'Authorization': f'Bearer {access_token}'
    } 
if __name__ == '__main__':
    print(get_token())
    
access_token2 = "oErRMop48Zz0HtEVKjle3j-bBmFqQ7bmotcpUsRB5vGuanYIROG0aHDFv46Z7lmT"