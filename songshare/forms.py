from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from songshare.models import Profile
from songshare.models import Playlist

#from songshare.models import Artist
#from songshare.models import Album

MAX_UPLOAD_SIZE = 2500000

# login form 
class LoginForm(forms.Form):
	username = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'placeholder': 'username'}))
	password = forms.CharField(max_length = 200, widget = forms.PasswordInput(), label='password')

	def clean(self):
			cleaned_data = super().clean()
			username = cleaned_data.get('username')
			password = cleaned_data.get('password')
			user = authenticate(username=username, password=password)

			if not user:
				raise forms.ValidationError("Invalid username/password")

			return cleaned_data

# user registration form
class RegistrationForm(forms.Form):
		username = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'placeholder': 'username'}))
		password = forms.CharField(max_length = 200, 
								   widget = forms.PasswordInput(), 
								   label='password')
		confirm_password = forms.CharField(max_length = 200, 
								  		   widget = forms.PasswordInput(), 
								  		   label='confirm password')
		email = forms.CharField(max_length = 50, widget = forms.EmailInput())
		first_name = forms.CharField(max_length = 20)
		last_name = forms.CharField(max_length = 20)

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



MAX_UPLOAD_SIZE = 2500000

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

class PlaylistPictureForm(forms.ModelForm):
    class Meta:
        model = Playlist
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