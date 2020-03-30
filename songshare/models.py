from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

"""
Note:
    These are the preliminary classes we are thinking of using in the songshare
    model. The attributes are not final, and we will find that we may need to 
    add more or remove some attributes in certain classes to accomplish the
    goal of the songshare app
"""

class Profile(models.Model):
    """
    A class used to represent a user Profile using songshare app
    ...
    Attributes
    ----------
    user : models.ForeignKey(User)
        the user who owns the profile
    is_dj : models.BooleanField
        is the user a dj?
    fname, lname : models.CharField
        the first and last name of the user (may delete later as the User 
        should have this information already)
    bio : models.CharField
        a short bio for the profile (may not need but will include in case
        we want to make songshare more social)
    following : models.ManyToManyField(User)
        the Users followed by user 
    picture : models.FileField(blank=True)
        the user's profile picture
    content_type: models.CharField
        used to verify that the user's profile picture is indeed a picture
    """
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    auth_token = models.CharField(max_length=200)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    bio = models.CharField(max_length=200)
    following = models.ManyToManyField(User, related_name='following')
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return 'Profile(user=' + str(self.user) + \
               ' bio=' + str(self.bio) + ')'

# Song class (essential)
class Song(models.Model):
    """
    A class used to encapsulate a song provided by Spotify API
    ...
    Attributes
    ----------
    artist : models.CharField
        the artist of the song (might need an additional field to reference
        an artist profile via uri)
    album : models.CharField
        the album of the song (might need an additional field to reference
        an album profile via uri)
    vote_count : models.IntegerField
        vote count for the song
    uri : models.CharField
        reference to the song provided by the Spotify API
    """
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    vote_count = models.IntegerField(blank=True, null=True)
    uri = models.CharField(max_length=200)
    def __str__(self):
        return 'Song(artist=' + str(self.artist) + ' album=' + str(self.album) + ')'

# Playlist class (essential)
class Playlist(models.Model):
    """
    A class used to represent a user Playlist created using songshare app
    ...
    Attributes
    ----------
    user : models.ForeignKey(User)
        the owner of the playlist
    profile : models.ForeignKey(Profile)
        reference to the playlist owner's profile for a user to view
    songs : models.ForeignKey(Song)
        the songs in the playlist
    bio : models.CharField
        a playlist should have a description (maybe?)
    followers : models.ManyToManyField(Profile)
        the followers of the playlist used to reference their profile
    picture : models.FileField(blank=True)
        the playlist's picture
    content_type: models.CharField
        used to verify that the user's profile picture is indeed a picture
    """
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, default=None, on_delete=models.PROTECT)
    songs = models.ForeignKey(Song, default=None, on_delete=models.PROTECT)
    picture = models.FileField(blank=True)
    bio = models.CharField(max_length=200)
    content_type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return 'Playlist(user=' + str(self.user) + ' songs=' + str(self.songs) + ')'
      
# Post Model (optional for now)
class Post(models.Model):
    """
    A class used to represent a Post created by a User
    ...
    Attributes
    ----------
    text : models.CharField
        the text of the Post
    user : models.ForeignKey(User)
        the user who made the Post
    fname, lname : models.CharField
        the first and last name of the user (may delete later as the User 
        should have this information already)
    date : models.models.DateTimeField
        the creation time date of the Post
    """
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    date = models.DateTimeField()

    def __str__(self):
        return 'Post(user=' + str(self.user) + ' text=' + str(self.text) + ')'


# Comment Model (optional for now)
class Comment(models.Model):
    """
    A class used to represent a Comment on a Post created by a User
    ...
    Attributes
    ----------
    post: models.ForeignKey(Post)
        the post on which the Comment was made
    text : models.CharField
        the text of the Comment
    user : models.ForeignKey(User)
        the User who made the Comment
    fname, lname : models.CharField
        the first and last name of the user (may delete later as the User 
        should have this information already)
    date : models.models.DateTimeField
        the creation time date of the Comment
    """
    post = models.ForeignKey(Post, default=None, on_delete=models.PROTECT)
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    date = models.DateTimeField()

    def __str__(self):
        return 'Comment(user=' + str(self.user) + ' text=' + str(self.text) + ')'

"""
Note:
    These encapsulate profiles that cannot be followed, but the information
    might be useful for adding multiple songs by an artist to a playlist, 
    for example


"""

"""
class Artist(models.Model):
    profile = models.ForeignKey(Profile, default=None, on_delete=models.PROTECT)
    uri = models.CharField(max_length=200)
    albums = models.ForeignKey(Album, default=None, on_delete=models.PROTECT)
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50, blank=True)



class Album(models.Model):
    profile = models.ForeignKey(Profile, default=None, on_delete=models.PROTECT)
    uri = models.CharField(max_length=200)
    songs = models.ForeignKey(Song, default=None, on_delete=models.PROTECT)
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50, blank=True)
"""
