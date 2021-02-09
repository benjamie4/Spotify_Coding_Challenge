import os
import requests
import json


#Benjamin Esquivel, 2/8/2021, benjamiesq@gmail.com

CLIENT_ID = os.environ.get('Spotify_Client_Id')
CLIENT_SECRET = os.environ.get('Spotify_Client_Secret')

grant_type = 'client_credentials'
body_params = {'grant_type' : grant_type}

url='https://accounts.spotify.com/api/token'
response = requests.post(url, data=body_params, auth = (CLIENT_ID, CLIENT_SECRET))

token_raw = json.loads(response.text)
token = token_raw["access_token"]

headers = {
    'Authorization': 'Bearer {token}'.format(token=token)
}

def get_artist_id():
    BASE_URL = 'https://api.spotify.com/v1/'
    q = input('Please type artist name: ')
    r = requests.get(BASE_URL + 'search/',headers=headers,params={'q':q,'type':'artist','limit':1})
    d = r.json()

    for artist in d['artists']['items']:
        artist = artist['id']
        return artist

def query_album():
    BASE_URL = 'https://api.spotify.com/v1/'
    id = input('Please type artist name: ')
    r = requests.get(BASE_URL + 'search/',headers=headers,params={'q':id,'type':'artist','limit':1})
    d = r.json()

    for artist in d['artists']['items']:
        artist_id = artist['id']
        print('Artist Id:'+ artist_id)

    r = requests.get(BASE_URL + 'artists/' + artist_id + '/albums/', headers=headers,params={'limit':10,'include_groups':'album'})
    data = r.json()
    for album in data['items']:
        print(album['name'])

    while data['next'] is not None:
        next_page = data['next']
        result = requests.get(next_page,headers=headers)
        data = result.json()
        for album in data['items']:
            print(album['name'])

        if data['next'] is None:
            break

playlist = []

def query_playlist_songs():
    BASE_URL = 'https://api.spotify.com/v1/playlists'
    r = requests.get(BASE_URL + '/0nBTFnGHg8wj7IhipwGHEz/tracks', headers=headers,params = 'fields=items.track.name')
    data = r.json()

    for i in data['items']:
        i = i['track']['name']
        print(i)
        playlist.append(i)


top_tracks = []
def get_top_tracks():
    artist = get_artist_id()
    BASE_URL = 'https://api.spotify.com/v1/artists/'
    r = requests.get(BASE_URL + artist + '/top-tracks', headers=headers, params={'market':'US'})
    data = r.json()

    for track in data['tracks']:
        top_tracks.append(track['name'])
    query_playlist_songs()

    for i in list(set(playlist).intersection(top_tracks)):
        print('Artist top songs in this playlist:' + i)

# First part of the coding challenge
query_album()
# Second part of the coding challenge
query_playlist_songs()
# Third part of the coding challenge
get_top_tracks()
