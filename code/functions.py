import requests
import pandas as pd
import lyricsgenius
from auth import *
import re
from sklearn.feature_extraction.text import CountVectorizer
import requests
from dotenv import load_dotenv
from functions import *
from bs4 import BeautifulSoup
from pprint import pprint
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import seaborn as sns
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from matplotlib import colormaps as cm
from scipy.interpolate import splprep, splev 
from collections import Counter

genius = lyricsgenius.Genius("access_token2")

# Returns an artist's ID, name, popularity, etc.
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

# Returns a playlist's items
def get_playlist_items(playlist_id, fields, market, limit, offset, access_token):
    
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_token()

    params = {
        'market': market,
        'fields': fields,
        'limit': limit,
        'offset': offset
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Returns an artist's top 10 tracks
def get_top_tracks(artist_id, token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "market": "US"
    }
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()  

# Returns the URL of a song page on Genius, used to fetch lyrics in function get_song_lyrics
def search_song(query, token):
   
    base_url = 'https://api.genius.com'
    search_url = f'{base_url}/search'
    
    params = {
        'q': query  
    }

    headers = get_token2()
    
    response = requests.get(search_url, headers=headers, params=params)
    
    if response.status_code == 200:
        search_results = response.json()['response']['hits']
        if search_results:
            song_path = search_results[0]['result']['path']
            return f"https://genius.com{song_path}"
        else:
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

# Returns song lyrics for a given song title and artist
def get_song_lyrics(song_title, artist_name):
    
    try:
        song = genius.search_song(song_title, artist_name)
        if song:
          
            return song.lyrics
        else:
            return f"Lyrics for '{song_title}' by {artist_name} not found."
    except Exception as e:
        
        return f"Error fetching lyrics for '{song_title}' by {artist_name}: {e}"
    
# Searches for songs on Genius, using different variations of the song title and artist name
# To ensure lyrics are found, despite not using the exact song title or artist name    
def get_song_lyrics_with_variations(song_title, artist_name):
    
    variations = [
        song_title,
        song_title.split(" - ")[0],  
        f"{song_title} {artist_name}",  
        f"{song_title.split(' - ')[0]} {artist_name}",  
        artist_name,  
    ]

    for variation in variations:
        print(f"Searching for: {variation}")
        song = genius.search_song(variation, artist_name)
        if song:
            print(f"Found lyrics for: {variation}")
            return song.lyrics

    return f"No results found for: {song_title} by {artist_name}"

# Searches for a song on Genius by its first word + artist name and returns its lyrics
# This was an attempt at getting the lyrics to some songs which would print in translated languages, or were not found due to specific names
def get_song_lyrics_with_first_word(song_title, artist_name):

    first_word = song_title.split(" ")[0]
    
    song = genius.search_song(f"{first_word} {artist_name}", artist_name)
    
    if song:
        lyrics = song.lyrics
        
        cleaned_lyrics = re.sub(r'(\d+ Contributors|Translations.*?)(\n|$)', '', lyrics)
      
        cleaned_lyrics = re.sub(r'\[.*?\]', '', cleaned_lyrics)  
        
        return cleaned_lyrics
    else:
        return f"No lyrics found for: {song_title} by {artist_name}"


indices_to_refetch = [85, 86, 72, 68, 65, 53, 49, 45, 41, 33, 31, 26, 8, 0]

# Refetching lyrics for the top tracks that were not fetched successfully (see above)
def refetch_lyrics_for_top_tracks(df, indices):
    for index in indices:
        
        if index < len(df):
            song_title = df.loc[index, 'name']  
            artist_name = df.loc[index, 'artist']  
            
            new_lyrics = get_song_lyrics_with_first_word(song_title, artist_name)
            
            df.loc[index, 'lyrics'] = new_lyrics
        else:
            print(f"Index {index} is out of range.")
    
    return df

# Fetching lyrics and handling exceptions
def safe_get_song_lyrics(row):
    try:
        return get_song_lyrics(row['name'], row['artist'])
    except Exception as e:
        print(f"Failed to fetch lyrics for {row['name']} by {row['artist']}: {e}")
        return None  

# Preprocessing the lyrics by removing non-alphabetic characters and converting them to lowercase
def preprocess_lyrics(lyrics):

    lyrics = re.sub(r"[^a-zA-Z\s']", '', lyrics)
   
    lyrics = lyrics.lower()
    return lyrics

# Fetching lyrics
def fetch_lyrics(row):
    try:
        return get_song_lyrics(row['name'], row['artist'])
    except Exception as e:
        print(f"Error fetching lyrics for {row['name']} by {row['artist']}: {e}")
        return None
    
# Fetching the most frequent words from the lyrics of the top tracks    
def get_most_frequent_words(text):
    
    words = re.findall(r'\b\w+\b', text.lower())  
    return dict(Counter(words))  

# Here I created a list of "stop words" that I wanted to remove from the lyrics before visualising and analysing them
# The main reason why these were removed was irrelevancy: they were either non-words like "boom" or "la", or lyric annotations such as "chorus" or "verse"
words_to_remove = ['don', 'chorus', 'll', 'la', 'nicki', 'verse', 'pre', 'minaj', 'ayy', 'boom', 'oh', 'ain', 'ah', 'wanna', 'cause', 'like', 'yeah', 'ooh', 'rihanna', 'bout', 'rida', 'just', 'flo', 'got', 'feat', 'remix', 'em', 'badoom', 'outchea', 'prechorus']

# Removing the stop words from the lyrics, alongside normalizing and standardizing them
def preprocess_lyrics_final(lyrics):

    pattern = r'\b(?:' + '|'.join(words_to_remove) + r')\b'
    lyrics = re.sub(pattern, '', lyrics, flags=re.IGNORECASE)
    lyrics = re.sub(r"[^a-zA-Z\s']", '', lyrics)
    lyrics = lyrics.lower()
    
    return lyrics

# Clean both 'Track Name' and 'Artists' columns
def clean_columns(df, columns):
    return df.assign(**{col: df[col].str.strip().str.lower() for col in columns})

# Fetching the most frequent words from the lyrics of the top tracks, where stop words and other noise is removed
def get_most_frequent_words_final(lyrics_list):

    cleaned_lyrics = [preprocess_lyrics_final(lyric) for lyric in lyrics_list]
 
    vectorizer = CountVectorizer(stop_words='english', max_features=20)
    
    word_counts = vectorizer.fit_transform(cleaned_lyrics)
    
    word_freq = dict(zip(vectorizer.get_feature_names_out(), word_counts.sum(axis=0).A1))
    return word_freq

# Combines main artists and featured artists into a single string
def combine_artists(artist_column):
    if 'feat' in artist_column:
        
        artists = artist_column.split('feat')
        main_artist = artists[0].strip()
        featured_artists = artists[1].strip()
        combined_artists = main_artist + ' feat ' + ', '.join(sorted(set(featured_artists.split(','))))
    else:
        combined_artists = artist_column
    return combined_artists

# Bar plotting top 10 most frequent words in lyrics
def plot_word_frequencies(male_word_freq, female_word_freq, top_n=10):
   
    male_words, male_counts = zip(*male_word_freq[:top_n])
    female_words, female_counts = zip(*female_word_freq[:top_n])

    male_df = pd.DataFrame({'word': male_words, 'count': male_counts, 'gender': 'Male'})
    female_df = pd.DataFrame({'word': female_words, 'count': female_counts, 'gender': 'Female'})
 
    combined_df = pd.concat([male_df, female_df])

    plt.figure(figsize=(10, 6))
    sns.barplot(x='count', y='word', hue='gender', data=combined_df, palette='muted')
    
    plt.title('Top 10 Most Frequent Words in Lyrics (Male vs Female Artists)', fontsize=16)
    plt.xlabel('Word Frequency', fontsize=12)
    plt.ylabel('Word', fontsize=12)
    plt.show()

# Plotting a word cloud with the given word frequency
def plot_word_cloud(word_freq, title="Word Cloud", save_path=None):
    
    word_dict = dict(word_freq)
    
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='spring_r').generate_from_frequencies(word_dict)
    
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  
    plt.title(title, fontsize=16)
    
    if save_path:
        plt.savefig(save_path, format='png', dpi=300, bbox_inches='tight')
    
    plt.show()
    
    plt.close()

# Creating a word cloud based on the shape and colours of a mask/image
def plot_shaped_word_cloud(word_freq, mask_path, title="Word Cloud", max_words=1000):
    
    word_dict = dict(word_freq)
    
    mask = np.array(Image.open(mask_path).convert("RGB"))
    
    wc = WordCloud(
        background_color="white",
        max_words=max_words,  
        mask=mask,
        stopwords=STOPWORDS,
        contour_width=3,  
        contour_color="slategrey",
        colormap="spring_r"  
    ).generate_from_frequencies(word_dict)
    
    image_colors = ImageColorGenerator(mask)
    
    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation="bilinear")  
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")  
    plt.axis("off")  
    plt.title(title, fontsize=16, weight='bold', pad=20)
    plt.show()



