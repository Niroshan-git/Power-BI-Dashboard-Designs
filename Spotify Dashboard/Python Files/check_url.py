import pandas as pd
import requests

# Load the CSV file
file_path = 'spotify_with_images.csv'  # Replace with your file path
spotify_data = pd.read_csv(file_path, encoding='latin1')

# Function to check if a URL is valid
def check_url(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

# Columns containing URLs
url_columns = ['artist_image_url', 'album_image_url']

# Check the validity of each URL in the relevant columns
for column in url_columns:
    spotify_data[column + '_valid'] = spotify_data[column].apply(lambda url: check_url(url) if pd.notnull(url) else False)

# Separate valid and invalid URLs
valid_urls = spotify_data[(spotify_data['artist_image_url_valid'] == True) | (spotify_data['album_image_url_valid'] == True)]
invalid_urls = spotify_data[(spotify_data['artist_image_url_valid'] == False) | (spotify_data['album_image_url_valid'] == False)]

# Print valid URLs
print("Valid URLs:")
print(valid_urls[['track_name', 'artist_image_url', 'album_image_url']])

# Print invalid URLs
print("\nInvalid URLs:")
print(invalid_urls[['track_name', 'artist_image_url', 'album_image_url']])

# Optionally save the result to a new CSV file
output_file_path = 'cleaned_spotify_data.csv'
spotify_data.to_csv(output_file_path, index=False)
