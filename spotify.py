import requests
from flask import session
from datetime import datetime

AUTH_URL = 'https://accounts.spotify.com/authorize'
API_BASE_URL = 'https://api.spotify.com/v1/'
TOKEN_URL = 'https://accounts.spotify.com/api/token'


def get_spotify_headers(access_token):
    return {'Authorization': f'Bearer {access_token}'}



def get_top_tracks_short(access_token):
    url = f'{API_BASE_URL}me/top/tracks?limit=50&time_range=short_term'
    response = requests.get(url, headers=get_spotify_headers(access_token))
    return response.json()['items']

def get_top_tracks_med(access_token):
    url = f'{API_BASE_URL}me/top/tracks?limit=50&time_range=medium_term'
    response = requests.get(url, headers=get_spotify_headers(access_token))
    return response.json()['items']


def get_top_tracks_long(access_token):
    url = f'{API_BASE_URL}me/top/tracks?limit=50&time_range=long_term'
    response = requests.get(url, headers=get_spotify_headers(access_token))
    return response.json()['items']


def get_top_artists_short(access_token):
    url = f'{API_BASE_URL}me/top/artists?limit=50&time_range=short_term'
    response = requests.get(url, headers=get_spotify_headers(access_token))
    return response.json()['items']

def get_top_artists_med(access_token):
    url = f'{API_BASE_URL}me/top/artists?limit=50&time_range=medium_term'
    response = requests.get(url, headers=get_spotify_headers(access_token))
    return response.json()['items']

def get_top_artists_long(access_token):
    url = f'{API_BASE_URL}me/top/artists?limit=50&time_range=long_term'
    response = requests.get(url, headers=get_spotify_headers(access_token))
    return response.json()['items']

def get_tracks(access_token, track):
    params = {
    'q': track,
    'type': 'track',
    'market': 'US',
    'limit': 50,
    'offset': 0
    }
    url = f'{API_BASE_URL}search'
    response = requests.get(url, headers=get_spotify_headers(access_token), params=params)
    return response.json()['tracks']['items']


def get_user_profile(access_token):
    url = f"{API_BASE_URL}me"
    response = requests.get(url, headers=get_spotify_headers(access_token))
    return response.json()

def create_playlist(access_token, user_id, playlist_name='new-playlist'):
    url = f"{API_BASE_URL}users/{user_id}/playlists"
    data = {'name': playlist_name, 'public': True}
    response = requests.post(url, headers=get_spotify_headers(access_token), json=data)
    return response.json()

def add_tracks_to_playlist(access_token, playlist_id, track_uris):
    url = f"{API_BASE_URL}playlists/{playlist_id}/tracks"
    data = {'uris': track_uris}
    response = requests.post(url, headers=get_spotify_headers(access_token), json=data)
    success = response.status_code == 201
    return success

def get_recommendations(access_token, seed_tracks):
    url = f"{API_BASE_URL}recommendations?limit=50&seed_tracks={seed_tracks}"
    response = requests.get(url, headers=get_spotify_headers(access_token))
    return response.json()['tracks']

def get_track(access_token, track_id):
    url = f"{API_BASE_URL}tracks/{track_id}"
    response = requests.get(url,headers=get_spotify_headers(access_token) )
    return response.json()['name']


