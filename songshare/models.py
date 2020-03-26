from django.db import models
from django.contrib.auth.models import User

# Profile class (essential)
class Profile(models.Model):
	user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
	is_dj = models.BooleanField(default=False)
	fname = models.CharField(max_length=20)
	lname = models.CharField(max_length=20)
	bio = models.CharField(max_length=200)
	following = models.ManyToManyField(User, related_name='following')
	picture = models.FileField(blank=True)
	content_type = models.CharField(max_length=50, blank=True)

# Playlist class (essential)
class Playlist(models.Model):
	user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
	profile = models.ForeignKey(Profile, default=None, on_delete=models.PROTECT)
	songs = models.ForeignKey(Song, default=None, on_delete=models.PROTECT)
	picture = models.FileField(blank=True)
	followers = models.ForeignKey(Profile, default=None, on_delete=models.PROTECT)
	content_type = models.CharField(max_length=50, blank=True)

# Song class (essential)
class Song(models.Model):
	artist = models.CharField(max_length=200)
	album = models.CharField(max_length=200)
	vote_count = models.IntegerField(blank=True, null=True)

class Post(models.Model):
	text = models.CharField(max_length=200)
	user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
	fname = models.CharField(max_length=20)
	lname = models.CharField(max_length=20)
	date = models.DateTimeField()

# Comment Model (optional for now)
class Comment(models.Model):
	post = models.ForeignKey(Post, default=None, on_delete=models.PROTECT)
	text = models.CharField(max_length=200)
	user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
	fname = models.CharField(max_length=20)
	lname = models.CharField(max_length=20)
	date = models.DateTimeField()