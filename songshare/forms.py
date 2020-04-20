from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.validators import validate_email

from songshare.models import Profile
from songshare.models import Stream

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

#from songshare.models import Artist
#from songshare.models import Album

MAX_UPLOAD_SIZE = 2500000

class CreateStreamForm(forms.Form):
    stream_name = forms.CharField(max_length=256, label="Stream Name", 
                widget=forms.TextInput(attrs={'placeholder': 'stream name'}))
    def clean_stream_name(self):
        stream_name = self.cleaned_data.get('stream_name')
        try:
            s = Stream.objects.get(name=stream_name)
            if s.is_streaming:
                raise forms.ValidationError("Stream is currently live with the same name")
        except:
            return stream_name

# spotify registration form
# TODO: this copies code from the registration form, if possible it would be 
#       ideal to use the code from the registration form but only use the spotify_email
#       field
class SpotifyRegistrationForm(forms.Form):
    spotify_email = forms.EmailField(max_length=100, label="Spotify Email",
                        widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    def clean_spotify_email(self):
        spotify_email = self.cleaned_data.get('spotify_email')
        try:
            validate_email(spotify_email)
            return spotify_email
        except:
            raise forms.ValidationError("Please enter a valid email address")

# login form 
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder':'username'}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username,password=password)

        if not user:
            raise forms.ValidationError('Invalid username or password')
        return cleaned_data

# user registration form
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length = 200, 
                                widget = forms.PasswordInput(), 
                                label='Password')
    confirm_password = forms.CharField(max_length = 200, 
                                        widget = forms.PasswordInput(), 
                                        label='Confirm Password')
    email = forms.CharField(max_length = 50, widget = forms.EmailInput())
    fname = forms.CharField(max_length = 20, label="First Name")
    lname = forms.CharField(max_length = 20, label="Last Name")
    spotify_email = forms.CharField(max_length=100, label="Spotify Email",
                        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
                        required=False)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken")
        return username
    
    def clean_spotify_email(self):
        spotify_email = self.cleaned_data.get('spotify_email')
        if spotify_email == "":
            return spotify_email
        try:
            validate_email(spotify_email)
            return spotify_email
        except:
            raise forms.ValidationError("Please enter a valid email address")


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ( 'picture',)

    def clean_picture(self):
        picture = self.cleaned_data['picture']
        if not picture:
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture

class SpotifyUsernameForm(forms.Form):
    username = forms.CharField(max_length=400, label="Spotify Username")

"""
class ArtistPictureForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ( 'picture',)

    def clean_picture(self):
        picture = self.cleaned_data['picture']
        if not picture:
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture


class AlbumPictureForm(forms.ModelForm):
    class Meta:
        model = Album
        model = Profile
        fields = ( 'picture',)

    def clean_picture(self):
        picture = self.cleaned_data['picture']
        if not picture:
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture
 """