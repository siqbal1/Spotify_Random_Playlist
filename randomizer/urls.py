from django.conf.urls import url
from randomizer import views

app_name = 'randomizer'

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^playlist_generator/$', views.playlist_generator, name='playlist_generator'),
    url(r'^add_songs_to_playlist/$', views.add_songs_to_playlist, name='add_songs_to_playlist')
]
 
