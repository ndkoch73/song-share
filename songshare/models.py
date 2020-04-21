from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import spotipy.util as spotipyutil
import spotipy.oauth2 as oauth2
import spotipy


class Profile(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    spotify_email = models.EmailField(max_length=200)
    is_dj = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    name = models.CharField(max_length=42)
    bio = models.CharField(max_length=200)
    following = models.ManyToManyField(User, related_name='following')
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50, blank=True)
    auth_token_code = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return str(self.fname) + " " + str(self.lname) + " with spotify email: "\
            + str(self.spotify_email) + " and is_dj: " + str(self.is_dj) + "\n"
    def create_oauth_url(self,scope=None, client_id=None,
                          client_secret=None, redirect_uri=None,
                          cache_path=None):
        cache_path = cache_path or ".cache-" + self.spotify_email
        sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
                                    scope=scope, cache_path=cache_path)
        token_info = sp_oauth.get_cached_token()
        if not token_info:
            auth_url = sp_oauth.get_authorize_url()
            return auth_url
        else:
            return token_info

    def get_auth_token(self,scope=None, client_id=None,
                          client_secret=None, redirect_uri=None,
                          cache_path=None):
        cache_path = cache_path or ".cache-" + self.spotify_email
        sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
                                    scope=scope, cache_path=cache_path)
        token_info = sp_oauth.get_cached_token()
        if not token_info:
            token = sp_oauth.get_access_token(self.auth_token_code, as_dict=False)
        else:
            return token_info["access_token"]
        if token:
            return token
        else:
            return None

    def to_json(self):
        picuture_available = bool(self.picture)
        return {'spotify_email':self.spotify_email,'is_dj':self.is_dj,'id':self.id,
            'is_live':self.is_live,'fname':self.fname,'lname':self.lname,'name':self.name,
            'bio':self.bio, 'picture_avaliable':picuture_available,'username':self.user.username}




class Post(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    date = models.DateTimeField()

    def __str__(self):
        return 'Post(user=' + str(self.user) + ' text=' + str(self.text) + ')'


class Stream(models.Model):
    name = models.CharField(max_length=256)
    dj = models.ForeignKey(Profile, default=None, on_delete=models.PROTECT)
    listeners = models.ManyToManyField(Profile, related_name="listening")
    is_streaming = models.BooleanField(default=True)
    
    def get_recently_played(self):
        sp = spotipy.Spotify(auth=self.dj.get_auth_token(scope=settings.SPOTIFY_SCOPE_ACCESS,
                                            client_id=settings.SPOTIPY_CLIENT_ID,
                                            client_secret=settings.SPOTIPY_CLIENT_SECRET,
                                            redirect_uri=settings.REDIRECT_AUTHENTICATION_URL))
        recently_played = sp.current_user_recently_played(limit=settings.RECENT_SONG_LIMIT)
        recently_played = recently_played['items']
        results = []
        for song in recently_played:
            artists = Song.clean_artists(song['track']['artists'])
            recent_song = Song(artist=artists,
                            album=song['track']['album']['name'],
                            name=song['track']['name'],
                            uri=song['track']['uri'],
                            image_url=song['track']['album']['images'][2]['url'])
            results.append(recent_song)
        return results

    def get_currently_playing(self):
        sp = spotipy.Spotify(auth=self.dj.get_auth_token(scope=settings.SPOTIFY_SCOPE_ACCESS,
                                            client_id=settings.SPOTIPY_CLIENT_ID,
                                            client_secret=settings.SPOTIPY_CLIENT_SECRET,
                                            redirect_uri=settings.REDIRECT_AUTHENTICATION_URL))
        result = sp.currently_playing()
        if result == None:
            return None
        result = result['item']
        artists = Song.clean_artists(result['artists'])
        current_song = Song(artist=artists,
                        album=result['album']['name'],
                        name=result['name'],
                        uri=result['uri'],
                        image_url=result['album']['images'][1]['url'])
        return current_song
    
    def to_json(self):
        result = {'name': self.name, 'dj':self.dj.to_json(),'is_streaming':self.is_streaming}
        listeners = []
        for listener in self.listeners.all():
            listeners.append(listener.to_json())
        result['listeners'] = listeners
        result['total_listening'] = len(listeners)
        return result
    
    def add_to_queue(self,song):
        sp = spotipy.Spotify(auth=self.dj.get_auth_token(scope=settings.SPOTIFY_SCOPE_ACCESS,
                                            client_id=settings.SPOTIPY_CLIENT_ID,
                                            client_secret=settings.SPOTIPY_CLIENT_SECRET,
                                            redirect_uri=settings.REDIRECT_AUTHENTICATION_URL))
        sp.add_to_queue(song.uri)

    def clear_queue(self):
        sp = spotipy.Spotify(auth=self.dj.get_auth_token(scope=settings.SPOTIFY_SCOPE_ACCESS,
                                            client_id=settings.SPOTIPY_CLIENT_ID,
                                            client_secret=settings.SPOTIPY_CLIENT_SECRET,
                                            redirect_uri=settings.REDIRECT_AUTHENTICATION_URL))
        for x in range(self.requested_songs.count()):
            sp.next_track()
        sp.pause_playback()


class Song(models.Model):
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    voters = models.ManyToManyField(Profile)
    num_votes = models.IntegerField(blank=True, null=True)
    uri = models.CharField(max_length=200)
    image_url = models.CharField(max_length=500)
    # can take three values 'accepted','denied','pending'
    request_status = models.CharField(max_length=10) 
    parent = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name="requested_songs")
    creation_time = models.DateTimeField()

    @classmethod
    def clean_artists(cls,artists):
        result = ""
        for i in range(0,len(artists)):
            result += artists[i]['name']
            if i != len(artists) - 1:
                artists += " & "
        return result
    def __str__(self):
        return 'Song(artist=' + str(self.artist) + ' album=' + str(self.album) + ')'
    def to_json(self, request=None):
        if request is not None:
            user_has_voted = self.voters.filter(user=request.user).exists()
            votes = self.voters.all().count()
            ID = self.id
        else:
            user_has_voted = False
            votes = 0
            ID = -1
        if self.request_status:
            return {'artist':self.artist,'album':self.album,'name':self.name, 'votes':self.voters.all().count(),
                    'uri':self.uri,'image_url':self.image_url, 'request_status':self.request_status, 
                    'user_has_voted':user_has_voted, 'id':ID}
        return {'artist':self.artist,'album':self.album,'name':self.name,'uri':self.uri,'image_url':self.image_url,
                'votes':votes, 'user_has_voted':user_has_voted, 'id':ID}

