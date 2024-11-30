import requests
import pandas as pd
import lyricsgenius
from auth import *
import sqlite3
import re
from sklearn.feature_extraction.text import CountVectorizer
import requests
from dotenv import load_dotenv
from functions import *
from bs4 import BeautifulSoup
from pprint import pprint
from auth import *
import base64
import os
import pandas as pd
import json
import csv
import string
import lyricsgenius
import sqlite3
from sqlalchemy import create_engine
import re
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
#! pip install nltk
import nltk
from nltk.corpus import stopwords
import seaborn as sns
#! pip install wordcloud
from os import path
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from matplotlib import colormaps as cm
import cv2
from scipy.interpolate import splprep, splev 

genius = lyricsgenius.Genius("access_token2")

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

def get_song_lyrics(song_title, artist_name):
    try:
        # Search for the song by title and artist
        song = genius.search_song(song_title, artist_name)
        if song:
            # If the song is found, return the lyrics
            return song.lyrics
        else:
            return f"Lyrics for '{song_title}' by {artist_name} not found."
    except Exception as e:
        # Catch any errors and return a message
        return f"Error fetching lyrics for '{song_title}' by {artist_name}: {e}"
    

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
            # Take the first result and get its URL
            song_path = search_results[0]['result']['path']
            return f"https://genius.com{song_path}"
        else:
            return None
    else:
        print(f"Error: {response.status_code}")
        return None
    

def get_song_lyrics_with_variations(song_title, artist_name):
    
    # Define variations of the song title
    variations = [
        song_title,
        song_title.split(" - ")[0],  # Remove text after a dash
        f"{song_title} {artist_name}",  # Add artist to the title
        f"{song_title.split(' - ')[0]} {artist_name}",  # Shortened title + artist
        artist_name,  # Search with artist name only
    ]

    # Try each variation
    for variation in variations:
        print(f"Searching for: {variation}")
        song = genius.search_song(variation, artist_name)
        if song:
            print(f"Found lyrics for: {variation}")
            return song.lyrics

    # If no lyrics found, return an error message
    return f"No results found for: {song_title} by {artist_name}"

def get_song_lyrics_with_first_word(song_title, artist_name):
    # Extract the first word from the song title
    first_word = song_title.split(" ")[0]
    
    # Use the first word and artist to search for the song
    song = genius.search_song(f"{first_word} {artist_name}", artist_name)
    
    if song:
        lyrics = song.lyrics
        
        # Clean the lyrics: remove unwanted parts (e.g., contributor info, translations)
        cleaned_lyrics = re.sub(r'(\d+ Contributors|Translations.*?)(\n|$)', '', lyrics)
        
        # Optionally, you can remove any repeated phrases or patterns here
        # e.g., removing any remaining [Chorus] sections or specific patterns
        cleaned_lyrics = re.sub(r'\[.*?\]', '', cleaned_lyrics)  # Remove [Chorus], [Verse 1], etc.
        
        return cleaned_lyrics
    else:
        return f"No lyrics found for: {song_title} by {artist_name}"


conn = sqlite3.connect('../data/spotify_data.db')  # Update with your actual database file
cursor = conn.cursor()
indices_to_refetch = [85, 86, 72, 68, 65, 49, 45, 41, 33, 31, 26, 8, 1]
def refetch_lyrics_for_top_tracks():
    for index in indices_to_refetch:
        try:
            # Get song title and artist from the database
            cursor.execute("SELECT name, artist FROM top_tracks WHERE rowid = ?", (index,))
            result = cursor.fetchone()
            
            if result:
                song_title, artist_name = result
                
                # Call the function to get lyrics with the first word and artist name
                new_lyrics = get_song_lyrics_with_first_word(song_title, artist_name)
                
                # Update the 'lyrics' column with the newly fetched lyrics in the database
                cursor.execute("UPDATE top_tracks SET lyrics = ? WHERE rowid = ?", (new_lyrics, index))
                conn.commit()  # Ensure changes are committed
                print(f"Updated lyrics for song {song_title} by {artist_name} (rowid {index})")
            else:
                print(f"Song with rowid {index} not found in the database.")
        
        except Exception as e:
            print(f"Error while updating row {index}: {e}")
            conn.rollback()  # Rollback in case of error


def preprocess_lyrics(lyrics):
    # Remove non-alphabetic characters except for apostrophes (which are part of contractions)
    lyrics = re.sub(r"[^a-zA-Z\s']", '', lyrics)
    # Convert to lowercase
    lyrics = lyrics.lower()
    return lyrics


def fetch_lyrics(row):
    try:
        return get_song_lyrics(row['name'], row['artist'])
    except Exception as e:
        print(f"Error fetching lyrics for {row['name']} by {row['artist']}: {e}")
        return None
    
def get_most_frequent_words(df):
    # Initialize CountVectorizer
    vectorizer = CountVectorizer(stop_words='english', max_features=20)
    # Fit and transform the lyrics column to get word counts
    word_counts = vectorizer.fit_transform(df['cleaned_lyrics'])
    # Get the words and their corresponding counts
    word_freq = dict(zip(vectorizer.get_feature_names_out(), word_counts.sum(axis=0).A1))
    return word_freq

words_to_remove = ['don', 'chorus', 'll', 'la', 'nicki', 'verse', 'pre', 'minaj', 'ayy', 'boom', 'oh', 'ain', 'ah', 'wanna', 'cause', 'like', 'yeah', 'ooh', 'rihanna', 'bout', 'rida', 'just', 'flo', 'got']
def preprocess_lyrics_final(lyrics):
    # Create a regex pattern to match the words in the list
    pattern = r'\b(?:' + '|'.join(words_to_remove) + r')\b'
    
    # Remove the specific words using the pattern
    lyrics = re.sub(pattern, '', lyrics, flags=re.IGNORECASE)
    
    # Remove non-alphabetic characters except for apostrophes
    lyrics = re.sub(r"[^a-zA-Z\s']", '', lyrics)
    
    # Convert to lowercase
    lyrics = lyrics.lower()
    
    return lyrics

def get_most_frequent_words_final(df):
    # Use .loc to set the cleaned_lyrics column properly
    df.loc[:, 'cleaned_lyrics'] = df['lyrics'].apply(preprocess_lyrics_final)
    
    # Initialize CountVectorizer
    vectorizer = CountVectorizer(stop_words='english', max_features=20)
    
    # Fit and transform the lyrics column to get word counts
    word_counts = vectorizer.fit_transform(df['cleaned_lyrics'])
    
    # Get the words and their corresponding counts
    word_freq = dict(zip(vectorizer.get_feature_names_out(), word_counts.sum(axis=0).A1))
    return word_freq

def combine_artists(artist_column):
    # Check if 'feat' exists, and if so, split and merge artists
    if 'feat' in artist_column:
        # Split the main artist and featured artist(s) and remove any extra spaces
        artists = artist_column.split('feat')
        main_artist = artists[0].strip()
        featured_artists = artists[1].strip()
        # Combine main artist with featured artists, avoiding duplicates
        combined_artists = main_artist + ' feat ' + ', '.join(sorted(set(featured_artists.split(','))))
    else:
        # If no featured artists, return the original
        combined_artists = artist_column
    return combined_artists

def plot_word_frequencies(male_word_freq, female_word_freq, top_n=10):
    # Extract the top N most frequent words
    male_words, male_counts = zip(*male_word_freq[:top_n])
    female_words, female_counts = zip(*female_word_freq[:top_n])

    # Create a DataFrame for plotting
    male_df = pd.DataFrame({'word': male_words, 'count': male_counts, 'gender': 'Male'})
    female_df = pd.DataFrame({'word': female_words, 'count': female_counts, 'gender': 'Female'})
    
    # Combine the DataFrames
    combined_df = pd.concat([male_df, female_df])

    # Create the bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='count', y='word', hue='gender', data=combined_df, palette='muted')
    
    # Set labels and title
    plt.title('Top 10 Most Frequent Words in Lyrics (Male vs Female Artists)', fontsize=16)
    plt.xlabel('Word Frequency', fontsize=12)
    plt.ylabel('Word', fontsize=12)
    plt.show()

def plot_word_frequencies(male_word_freq, female_word_freq, top_n=10):
    # Extract the top N most frequent words
    male_words, male_counts = zip(*male_word_freq[:top_n])
    female_words, female_counts = zip(*female_word_freq[:top_n])

    # Create a DataFrame for plotting
    male_df = pd.DataFrame({'word': male_words, 'count': male_counts, 'gender': 'Male'})
    female_df = pd.DataFrame({'word': female_words, 'count': female_counts, 'gender': 'Female'})
    
    # Combine the DataFrames
    combined_df = pd.concat([male_df, female_df])

    # Create the bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='count', y='word', hue='gender', data=combined_df, palette='muted')
    
    # Set labels and title
    plt.title('Top 10 Most Frequent Words in Lyrics (Male vs Female Artists)', fontsize=16)
    plt.xlabel('Word Frequency', fontsize=12)
    plt.ylabel('Word', fontsize=12)
    plt.show()


def plot_shaped_word_cloud(word_freq, mask_path, title="Word Cloud", max_words=1000):
    """
    Generate and plot a word cloud with a given shape, contour, and more frequent words.
    Uses mask's colors for the word cloud and ensures the contour is visible.
    """
    # Create a dictionary with words and their corresponding frequencies
    word_dict = dict(word_freq)
    
    # Load the mask image and ensure it's in RGB mode
    mask = np.array(Image.open(mask_path).convert("RGB"))
    
    # Generate the word cloud with a contour and more words
    wc = WordCloud(
        background_color="white",
        max_words=max_words,  # Adjust this value to increase the number of words
        mask=mask,
        stopwords=STOPWORDS,
        contour_width=3,  # Thickness of the contour
        contour_color="slategrey",  # Color of the contour
        colormap="spring_r"  # To give color to words, using mask's colors
    ).generate_from_frequencies(word_dict)
    
    # Create coloring from the image to use for word colors
    image_colors = ImageColorGenerator(mask)
    
    # Plot the word cloud
    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation="bilinear")  # Plot word cloud with contour first
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")  # Apply colors from the mask after
    plt.axis("off")  # Turn off the axis
    plt.title(title, fontsize=16, weight='bold', pad=20)
    plt.show()

def plot_word_cloud(word_freq, title="Word Cloud", save_path=None):
    
    word_dict = dict(word_freq)
    
    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='spring_r').generate_from_frequencies(word_dict)
    
    # Plot the word cloud
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Turn off the axis
    plt.title(title, fontsize=16)
    
    # Save the word cloud to a file if save_path is provided
    if save_path:
        plt.savefig(save_path, format='png', dpi=300, bbox_inches='tight')
    
    # Show the plot
    plt.show()
    
    # Close the plot to free memory
    plt.close()

