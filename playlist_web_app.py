from flask import Flask, render_template, request
import requests
from youtube_search import YoutubeSearch

app = Flask(__name__)

# Spotify credentials
client_id = "c04a49be17b04016af725b42fd9c5037"
client_secret = "fbd08ed84fbc4bbd88a45b8a80af238f"

# Function to get YouTube URL for a track
def get_youtube_url(query):
    search_results = YoutubeSearch(query, max_results=1).to_dict()
    return 'https://youtube.com' + search_results[0]['url_suffix']

# Function to get Spotify access token
def get_spotify_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    spotify_client = response.json()
    return spotify_client['access_token']

# Function to get playlist data from Spotify
def get_playlist_data(playlist_id, token):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Route for displaying playlist results
@app.route('/', methods=['GET', 'POST'])
def display_results():
    if request.method == 'POST':
        playlist_id = request.form['playlist_id']
        token = get_spotify_token()
        playlist_data = get_playlist_data(playlist_id, token)
        
        # Extract track info and search on YouTube
        results = []
        for item in playlist_data['tracks']['items']:
            query = ''
            for artist in item['track']['artists']:
                query += artist['name'] + ' '
            query += item['track']['name']
            youtube_url = get_youtube_url(query)
            results.append({'query': query, 'youtube_url': youtube_url})
        
        return render_template('results.html', results=results)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
