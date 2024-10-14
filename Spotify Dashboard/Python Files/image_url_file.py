import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time


# Set up Spotify API credentials
client_id =  '' # Replace with your Spotify client_id 
client_secret =  '' # Replace with your Spotify client_secret


# Authentication with Spotify
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Load your dataset
file_path = 'spotify-2023.csv'  # The file you uploaded
df = pd.read_csv(file_path, encoding='latin1')

# Assuming the dataset has a column with artist names and album names
# Adjust column names as per your dataset (e.g., 'artist_name' and 'album_name')
artists = df['artist(s)_name'].tolist()
albums = df['track_name'].tolist()

# Create lists to store image URLs
artist_images = []
album_images = []

# Fetch images using Spotify API
for artist, album in zip(artists, albums):
    try:
        # Fetch artist info
        artist_info = sp.search(q=f'artist:{artist}', type='artist')
        if artist_info['artists']['items']:
            artist_image_url = artist_info['artists']['items'][0]['images'][0]['url']
        else:
            artist_image_url = None  # No artist image found
        
        # Fetch album info
        album_info = sp.search(q=f'album:{album} artist:{artist}', type='album')
        if album_info['albums']['items']:
            album_image_url = album_info['albums']['items'][0]['images'][0]['url']
        else:
            album_image_url = None  # No album image found

        # Append URLs to lists
        artist_images.append(artist_image_url)
        album_images.append(album_image_url)

        # Print success message
        print(f"Successfully fetched data for {artist}, {album}")

    except Exception as e:
        # Handle any errors and continue with the next artist/album
        print(f"Error fetching data for {artist}, {album}: {e}. Trying next artist.")
        artist_images.append(None)
        album_images.append(None)
    
    # Sleep for a short time to avoid hitting API rate limits
    time.sleep(1)

# Add new columns to the DataFrame
df['artist_image_url'] = artist_images
df['album_image_url'] = album_images

# Save the updated dataset to a new CSV file
output_file_path = 'spotify_with_images.csv'  # Replace with your desired output file path
df.to_csv(output_file_path, index=False)

print(f"Updated dataset saved to {output_file_path}")
