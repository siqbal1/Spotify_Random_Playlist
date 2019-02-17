import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spotify_random_playlist.settings')

import django
django.setup()

from randomizer.models import *
from randomizer.spotify_api_funcs import *
import requests

# def add_track(track_id):
#     track = Track.objects.get_or_create(id = track_id)[0]
#     track.save()
#     return track
#
# #read all track ids from the text file
# with open("track_ids.txt") as f:
#     track_ids = f.readlines()
#
# #strip the \n from all track ids
# track_ids =  [track.strip() for track in track_ids]
#
# for track_id in track_ids:
#     track = add_track(track_id)
#     print("Added " + track.id)

# def add_track_genres(track_tuple, track_id, auth_header):
#     """
#     INPUT: Single Track Model object, track id, and the auth_header
#
#     To get the genres for the track we have to get
#     the artist and artist id. Also adds new music genres
#     to the Music_Genre model.
#
#     Then use a seperate api call to get the genress that the
#     artist is usually associated with
#     """
#
#     track_json = requests.get("	https://api.spotify.com/v1/tracks/" + track_id, headers=auth_header)
#     track_json = track_json.json()
#
#
#     if 'artists' in track_json:
#         artist_id = track_json['artists'][0]['id']
#         artist_json = requests.get("https://api.spotify.com/v1/artists/"+artist_id,
#                             headers=auth_header)
#         artist_json = artist_json.json()
#
#         if 'genres' in artist_json and len(artist_json['genres']) > 0:
#
#             genres = ""
#
#             for single_genre in artist_json['genres']:
#                 if not Music_Genre.objects.filter(name=single_genre):
#                     new_genre = Music_Genre(name=single_genre)
#                     new_genre.save()
#                     print("Added New Genre: " + single_genre)
#
#                 genres += single_genre + ","
#
#             genres = genres[:-1]
#
#         else:
#             genres = "N/A"
#     else:
#         genres="N/A"
#
#     track_tuple.genres = genres
#     track_tuple.save()
#
#     print("Track_id: " + track_tuple.id)
#     print("Genres: " + track_tuple.genres + "\n")
#
# def write_genres_to_file():
#     all_genres = Music_Genre.objects.all()
#     f = open("genre_list.txt", "w+")
#
#     for single_genre in all_genres:
#         f.write(single_genre.name + "\n")


def save_track_id(track_id):
    """
    INPUT: TRack id string

    saves track id in django model

    """

    new_track = Track(id=track_id)
    new_track.save()
    print("Saved: " + new_track.id)

def get_track_info(tracks_dict):
    """
    Takes in json from api search requests
    -print song ids and name
    -saves ids to model
    """
    #tracks_dict['tracks']['items'] is a list type
    #each index is a dict with the track info

    tracks_list = tracks_dict['tracks']['items']
    print(tracks_list)

    for track in tracks_list:
        track_id = track['id']
        save_track_id(track_id)


def get_track_id_from_word_list():
    """
    Does a search on items in a word list on spotify api to get
    track ids
    """
    auth_header = get_auth_header()

    file = open("Spotify_Random_Playlist_Generator\search_list.txt", 'r')
    count = 0
    #last failed index = 43, 108, 301, 458
    #tracks saved =  5822, 10019, ?, 3228
    index = 458

    #get words without \n
    file_lines = file.read().splitlines()
    file_len = len(file_lines)


    try:
        while index < file_len:
            word = file_lines[index]


            print("Search Param:" + word)
            offset = 0
            has_more_results = True

            ## TODO: split words into halfs to get more tracks
            ## based on smaller word lists

            while offset <= 1000 and has_more_results:
                search_params = {
                    "q" : word,
                    "type" : "track",
                    "limit" : str(50),
                    "offset" : offset,
                }

                search_results =  requests.get("https://api.spotify.com/v1/search", search_params,
                                        headers=auth_header)
                # print(search_results.json())
                search_results = search_results.json()

                #check if there are any more results
                if 'tracks' in search_results and search_results['tracks']['items']:
                    print("Running.")
                    get_track_info(search_results)
                else:
                    has_more_results = False

                if count % 2000 == 0:
                    auth_header = get_auth_header()

                offset += 50
                count += 1

            index += 1

    finally:
        print("Last word before failure: " + file_lines[index])
        print("Last word index before failure: " + str(index))
        print("Track ids saved:" + str(count))
        # print(search_results)


def read_track_ids_from_file(file=open('track_id_backup.txt')):
    tracks_list = file.readlines()
    count = 0

    for track in tracks_list:
        track = track.strip()
        save_track_id(track)
        count += 1


    file.close()

    print("Finished reading file.")


def delete_track_model():
    Track.objects.all().delete()




if __name__ == "__main__":
    # read_track_ids_from_file()
    delete_track_model();
    # remaining_tracks = Track.objects.filter(genres="none")
    #
    # index = 0
    # last_id = ""
    # auth_header = get_auth_header()
    #
    # try:
    #
    #     for track_tuple in remaining_tracks:
    #         add_track_genres(track_tuple, str(track_tuple.id), auth_header)
    #
    #         if index % 1500 == 0:
    #             auth_header = get_auth_header()
    #
    #         index += 1
    #         last_id = str(track_tuple.id)
    #
    # finally:
    #     print("Last index modified: " + str(index))
    #     print("Last id: " + last_id)
