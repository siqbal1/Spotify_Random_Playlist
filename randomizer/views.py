from django.shortcuts import render
from randomizer.models import *
from randomizer.spotify_api_funcs import *
import requests
from django.http import JsonResponse

# Create your views here.
def index(request):
    track_list = get_n_random_tracks(9)

    template_dict = {}
    template_dict['random_tracks'] = []

    i = 0

    track_list_length = len(track_list)

    while i < track_list_length:
        track_dict = {}
        track_dict['album_cover'] = track_list[i]['album_cover']
        track_dict['song_name'] = track_list[i]['name']
        track_dict['album'] = track_list[i]['album']
        track_dict['artists'] = track_list[i]['artists']
        track_dict['preview_url'] = track_list[i]['preview_url']
        track_dict['url'] = track_list[i]['url']

        template_dict['random_tracks'].append(track_dict)
        i += 1

    return render(request, 'randomizer/index.html', context = template_dict)

def playlist_generator(request):

    template_dict = {}

    url = request_account_authorization()

    template_dict['user_auth_url'] = url

    if request.method == 'GET':
        qd = request.GET
        print(qd)
    elif request.method == 'POST':
        qd = request.POST
        print('access_token:' + qd.get('access_token'))
        print('token_type:' + qd.get('token_type'))
        print(qd)
    # http://127.0.0.1:8000/randomizer/playlist_generator/#access_token=BQBgBuIpedQNAWevQQbWC4h6K76g_7znUZLUiRbrQRLQ4Z6WalREbb2_fGtXPucn_836UbHLS3hxBjP6drsOzsZcyKI9hxDGABp9CGl6ugkRFzsyNIAFE98_b4j3I1AN0JWSS0qfWNpYq2Opgrr2JRWAkh_zfsgemkVFH8IVkRwDsQiss5rc&token_type=Bearer&expires_in=3600


    return render(request, 'randomizer/playlist_generator.html', context = template_dict)

def add_songs_to_playlist(request):
    if request.method == 'GET':
        qd = request.GET
        print("GET")
    elif request.method == 'POST':
        qd = request.POST
        print("POST")

    access_token = qd.get('access_token')
    response_status = make_random_playlist(access_token)

    return JsonResponse(response_status)
