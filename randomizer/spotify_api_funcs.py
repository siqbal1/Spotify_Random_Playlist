import django
django.setup()

import requests
import random
import string
import json
from randomizer.models import *
from datetime import date

#constants
#removed CLIENT_ID, get from spotify api login
#removed SECRET_KEY, get from spotify api login

ID_LENGTH = 22
CHAR_RANGE = string.ascii_lowercase + string.ascii_uppercase + string.digits
NUM_RANGE = string.digits


def get_auth_header():
    """
    INPUT: none

    Returns authorization header for future spotify api calls.
    Does not take any input.

    RETURN: auth_header = {
        "Authorization" : token_type + " " + access_token
    }
    """

    response = requests.post("https://accounts.spotify.com/api/token",
                        data={"grant_type" : "client_credentials"},
                        auth = (CLIENT_ID, SECRET_KEY))

    response_json = response.json()

    access_token = response_json['access_token']
    token_type = response_json['token_type']

    auth_header = {
        "Authorization" : token_type + " " + access_token
    }

    return auth_header


def get_track_info_from_list(tracks_dict):
    """
    INPUT: json returned from spotify api call.

    Takes in a json and extracts track ids from list

    RETURNS: none
    """


    # TODO: edit function to insert objects to django model

    #tracks_dict['tracks']['items'] is a list type
    #each index is a dict with the track info
    if 'tracks' in tracks_dict:
        tracks_list = tracks_dict['tracks']['items']

        for i in range(len(tracks_list)):
            print(tracks_list[i]['id'])
            print(tracks_list[i]['name'])

def get_single_track_info(track_id):
    """
    INPUT: single track id from spotify api

    Takes in a track id and uses the api to find the album name,
    album cover, track name, and artist info

    RETURNS: dict object with the following info: name, album, album_cover,
    artists, url

    ex:
    track_dict = {
        'name' : track_json['name'],
        'album' : track_json['album']['name'],
        #url to the album cover
        'album_cover' : track_json['album']['images'][0]['url'],
        #list of all artists on the track
        'artists' : all_artists,
        #link to the track to be played
        'url' : url,
    }
    """

    auth_header = get_auth_header()

    #get the track
    track_json = requests.get("	https://api.spotify.com/v1/tracks/" + track_id, headers=auth_header)

    #convert into json to get info out of track
    track_json = track_json.json()


    # print("Track Name: " + track_json['name'])
    # print("Album:" + track_json['album']['name'])
    # #get the url of the image and inject into carousel on html page
    # print("Album Image:" + track_json['album']['images'][0]['url'])
    # print("Artist:" + track_json['artists'][0]['name'])

    all_artists = ""

    for artist in track_json['artists']:
        all_artists += artist['name'] + ", "

    all_artists = all_artists[:-2]

    url = "http://open.spotify.com/track/" + track_id

    track_dict = {
        'name' : track_json['name'],
        'album' : track_json['album']['name'],
        'album_cover' : track_json['album']['images'][0]['url'],
        'artists' : all_artists,
        'url' : url,
    }



    return track_dict

def get_group_track_info(id_list):
    """
    INPUT: List of track ids

    Takes input of a list of tracks and
    outputs a list of dict objects with track info

    OUTPUT: list of track_dict (see following)

    track_dict = {
        'name' : track_json['name'],
        'album' : track_json['album']['name'],
        #url to the album cover
        'album_cover' : track_json['album']['images'][0]['url'],
        #list of all artists on the track
        'artists' : all_artists,
        #link to the track to be played
        'url' : url,
    }
    """

    auth_header = get_auth_header()
    id_string = ",".join(id_list)

    #get the track
    print(id_string)
    track_json_list = requests.get("https://api.spotify.com/v1/tracks?ids=" + id_string, headers=auth_header)
    track_json_list = track_json_list.json()

    #get a list of just the tracks
    track_json_list = track_json_list['tracks']


    ret_track_list = []

    for track_json in track_json_list:
        all_artists = ""
        track_id = track_json['id']

        for artist in track_json['artists']:
            all_artists += artist['name'] + ", "

        all_artists = all_artists[:-2]

        url = "http://open.spotify.com/track/" + track_id

        track_dict = {
            'name' : track_json['name'],
            'album' : track_json['album']['name'],
            'artists' : all_artists,
            'preview_url' : track_json['preview_url'],
            'url' : url,
        }

        if track_json['album']['images'][1]:
            track_dict['album_cover'] = track_json['album']['images'][1]['url']
        else:
            track_dict['album_cover'] = "https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwiSnLuk-dbdAhXkIjQIHZtbAQQQjRx6BAgBEAU&url=https%3A%2F%2Farchive.4plebs.org%2Fs4s%2Fthread%2F6014555%2F&psig=AOvVaw2NrU3o7eam_enqI_PsqVZr&ust=1537992035152314"

        ret_track_list.append(track_dict)

    return ret_track_list

def get_n_random_tracks(n=1):
    """
    INPUT: number of random tracks

    Returns n random tracks from the model

    RETURNS: list of tracks

    """
    random_list = Track.objects.random(n)
    random_track_list = get_group_track_info(random_list)
    # return a list of of track dicts

    return random_track_list

def request_account_authorization():
    """
    INPUT: NONE

    Makes a url to request user endpoint authorization

    OUTPUT: returns a string url to get account authorization
    from spotify api
    """
    redirect_uri = "http://spotifyrandomplaylist.com/randomizer/playlist_generator"
    scopes = "playlist-modify playlist-modify-public playlist-modify-private playlist-read-private"

    print("\n" + scopes + "\n")

    url = ("https://accounts.spotify.com/authorize?client_id=" + CLIENT_ID
    + "&response_type=token&redirect_uri=" + redirect_uri
    + "&scope=" + scopes
    + "&show_dialog=true")

    return url

def get_user_auth_header(access_token):
    url_headers = {
        'Authorization' : 'Bearer ' + access_token,
        'Content-Type' : 'application/json',
    }

    return url_headers

def get_user_info(access_token):
    """
    INPUT: access token retrieved from spotify web api

    OUTPUT: json of user info from scopes

    """
    url = 'https://api.spotify.com/v1/me'
    url_headers = {
        'Authorization' : 'Bearer ' + access_token,
    }

    response = requests.get(url, headers=url_headers)

    response = response.json()

    return response


def make_user_playlist(user_id, access_token, name="Random Playlist "):

    """
    INPUT: user_id, access_token, playlist_name (optional)
    Makes a playlist with specified name
    OUTPUT: spotify api json response
    """

    print("Creating playlist...")
    url = "https://api.spotify.com/v1/users/" + user_id + "/playlists"

    url_headers = get_user_auth_header(access_token)

    name += str(date.today()) + " " + str(random.randint(0, 100)) 

    url_parameters = {
        'name' : name,
    }

    url_parameters = json.dumps(url_parameters)


    response = requests.post(url, data=url_parameters, headers=url_headers)

    response = response.json()

    return response


def add_n_random_tracks_to_playlist(playlist_id, access_token, n=30):
    random_tracks = Track.objects.random(n)

    url = "https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks"

    url_headers = get_user_auth_header(access_token)
    random_tracks = make_id_spotify_uri(random_tracks)

    url_parameters = {
        'uris' : random_tracks
    }

    url_parameters = json.dumps(url_parameters)


    response = requests.post(url, data=url_parameters, headers=url_headers)



def make_id_spotify_uri(id_list):
    """
    INPUT: list of track ids

    Adds spotify:track: in front of each track id to turn it
    into spotify uri
    """
    length = len(id_list)
    index = 0

    while index < length:
        id_list[index] = "spotify:track:" + id_list[index]
        index += 1

    return id_list

def add_ids_to_model(search_str="Test"):
    """
    INPUT: string search parameter

    Uses a string search param and does a spotify api search
    and adds the resulting tracks from the search to the model

    OUTPUT: None
    """
    if len(search_str) > 5:
        #split string to get broader search results to add
        #to model
        search_str = search_str[:5]

    tracks_added = False
    attempts = 0
    auth_header = get_auth_header()

    while not tracks_added and attempts < 5:
        offset = randint(0, 1000)

        search_params = {
            "q" : search_str,
            "type" : "track",
            "limit" : 50,
            "offset" : offset,
        }

        search_results =  requests.get("https://api.spotify.com/v1/search", search_params,
                                headers=auth_header)

        search_results = search_results.json()

        if 'tracks' in search_results and search_results['tracks']['items']:
            get_track_info(search_results)
            tracks_added = True

        attempts += 1

    print("New Tracks added.")


def get_track_info(tracks_dict):
    """
    Takes in json from api search requests
    -print song ids and name
    -saves ids to model
    """
    #tracks_dict['tracks']['items'] is a list type
    #each index is a dict with the track info

    tracks_list = tracks_dict['tracks']['items']

    for track in tracks_list:
        track_id = track['id']
        add_track(track_id)

def add_track(track_id):
    """
    INPUT: string track id

    Takes in a string track id and adds the track_id to
    django Track model

    OUTPUT: returns Track object
    """
    track = Track.objects.get_or_create(id = track_id)[0]
    track.save()
    print("Added: " + track.id)
    return track

def make_random_playlist(access_token):
    """
    INPUT: Spotify api access token

    General function to create a playlist of random tracks.
    Uses the following functions:
    get_user_info()
    make_user_playlist()
    add_n_random_tracks_to_playlist()

    OUTPUT: {'status': 'value'}
    status is either success or error

    """
    ret_status = {'status' : 'fail'}

    try:
        user_json = get_user_info(access_token)
        user_id = user_json['id']

        add_ids_to_model(user_id)

        playlist_json = make_user_playlist(user_id, access_token)
        playlist_id = playlist_json['id']
        print("Created Playlist")

        add_n_random_tracks_to_playlist(playlist_id, access_token)
        print("Added songs to playlist")

        ret_status['status'] = 'success'


    except Exception as e:
        print("An unexpected error has occurred.")
        print(e)

    finally:
        return ret_status
