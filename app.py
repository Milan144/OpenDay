import requests
from flask import Flask, jsonify
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
app = Flask(__name__)

@app.route('/addition', methods=['GET'])
def addition():
    return jsonify({"result": 1+1})

# Spotify API credentials
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

def get_spotify_token():
    """
    Fonction pour obtenir un token d'accès OAuth à l'API de Spotify.
    """
    auth_url = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    if auth_response.status_code == 200:
        return auth_response.json().get('access_token')
    else:
        return None


def get_top_tracks():
    """
    Fonction pour obtenir le top 10 des chansons populaires depuis l'API Spotify.
    """
    token = get_spotify_token()
    if not token:
        return {"error": "Impossible d'obtenir le token d'accès à Spotify"}

    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Spotify API pour les chansons populaires (playlist Global Top 50)
    url = 'https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF/tracks'  # Global Top 50

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Impossible de récupérer les chansons populaires"}

    tracks_data = response.json().get('items', [])

    # On extrait les 10 premières chansons avec une meilleure présentation
    top_tracks = []
    for index, track in enumerate(tracks_data[:10], start=1):
        track_info = track['track']
        top_tracks.append({
            'position': index,
            'title': track_info['name'],
            'artist': ', '.join([artist['name'] for artist in track_info['artists']]),
            'album': track_info['album']['name'],
            'popularity': track_info['popularity']  # Popularité de la chanson
        })

    return top_tracks


@app.route('/', methods=['GET'])
def top_songs():
    """
    Route Flask qui renvoie le top 10 des chansons populaires.
    """
    top_tracks = get_top_tracks()
    # Retourner les résultats sous forme de liste structurée
    return jsonify({"top_songs": top_tracks})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
