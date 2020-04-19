
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.conf import settings

from django.core import serializers
from django.utils import timezone
from datetime import datetime
import spotipy

from songshare.forms import *
from songshare.models import *

# from django.contrib.postgres.search import TrigramSimilarity

import json


# Search functionaily testing
from difflib import SequenceMatcher

from django.db.models import Q
from functools import reduce # Needed only in python 3
from operator import or_




@login_required
def home_page(request):
    context = {}
    c_user = Profile.objects.get(user=request.user)
    context['c_user'] = c_user
    following = list(c_user.following.all())
    context['following'] = list(c_user.following.all())
    context['streams'] = Stream.objects.all().filter(is_streaming=True)
    # pass the spotify registration form if the user is not a dj
    if not c_user.is_dj:
        context['spotify_registration_form'] = SpotifyRegistrationForm()
    elif c_user.is_dj and not c_user.is_live:
        context['stream_creation_form'] = CreateStreamForm()
    return render(request,'songshare/user_home.html', context)

@login_required
def profile_page_action(request):
    """ 
    Renders a user profile page (still missing a lot of info but this displays
    users the current user is following at the very least)
    Parameters
    ----------
    request : HttpRequest
        the django response object containing metadata about the request
    """
    context = {}
    # current user
    try:
        c_user = Profile.objects.get(user=request.user)
        picture_form  = ProfilePictureForm()
    except Profile.DoesNotExist:
        return redirect('home')
    if request.method == 'POST':
        c_user.bio = request.POST['bio']
    # the users that follow the current user
    following = list(c_user.following.all())
    context['c_user'] = c_user
    context['following'] = following


    # Handling pictures
    profile_form = ProfilePictureForm(request.POST, request.FILES)
    # print(profile_form)
    if request.FILES != {} and profile_form.is_valid():
        # I'm so confused apparently this print statement is essential
        # print(profile_form)
        pic = profile_form.cleaned_data['picture']
        c_user.content_type = profile_form.cleaned_data['picture'].content_type
        c_user.picture = pic
        print('picture exists')
        c_user.save()
    context['form']  = ProfilePictureForm()
    context['is_dj'] = c_user.auth_token_code != ''
    c_user.is_dj = c_user.auth_token_code != ''
    print(c_user.is_live)
    print(context)
    print(c_user.bio)

    return render(request, 'songshare/profile.html', context)

@login_required
def goto_profile(request, id):
    """ 
    Renders a user profile page (still missing a lot of info but this displays
    users the current user is following at the very least)
    Parameters
    ----------
    request : HttpRequest
        the django response object containing metadata about the request
    Raises
    ------
    Http404
        If for some reason the page the user is currently on is not available
    """
    context = {}
    try:
        p_user = User.objects.get(id=id)
        profile = Profile.objects.get(user=p_user)
        c_user = Profile.objects.get(user=request.user)
        following = list(c_user.following.all())
        if (profile.user == c_user.user): 
            return redirect(reverse('profile-create'))

        name = profile.fname + ' ' + profile.lname
        context['c_user'] = c_user
        context['profile'] = profile
        if (profile.user in following):
            context['following'] = True
        else:
            context['following'] = False
            print('false')
        context['name'] = name
        return render(request, 'songshare/dj_profile.html', context)
    except:
        raise Http404


# re-renders the page
@login_required
def update_follow(request, id):
    """ 
    Updates follow for the profile the user is currently viewing and re-renders 
    the page with the update
    Parameters
    ----------
    request : HttpRequest
        the django response object containing metadata about the request
    id : models.AutoField
        the id of the page the user wants to follow
    Raises
    ------
    Http404
        If for some reason the page the user is currently on is not available
    """
    context = {}
    try: 
        p_user = User.objects.get(id=id)
        f_user = Profile.objects.get(user=p_user)
        c_user = Profile.objects.get(user=request.user)
        following = list(c_user.following.all())
        context['c_user'] = c_user
        context['profile'] = p_user
        context['following'] = following
        if (f_user.user in following):
            c_user.following.remove(f_user.user)
            c_user.save()
            context['following'] = False
        elif (f_user.user not in following):
            c_user.following.add(f_user.user) 
            c_user.save()
            context['following'] = True
        return goto_profile(request, id)
    except:
        raise Http404

@login_required
def authenticate_action(request):
    try:
        code = request.GET.get('code')
    except:
        print("malformed url. URL should be encoded with the http:.../?code=...")
    current_user_profile = Profile.objects.get(user=request.user)
    current_user_profile.auth_token_code = code
    current_user_profile.is_dj = True
    current_user_profile.save()
    return redirect(reverse('home'))

@login_required
def listener_stream(request, id):
    context = {}
    try:
        p_user = User.objects.get(id=id)
        f_user = Profile.objects.get(user=p_user)
        c_user = Profile.objects.get(user=request.user)
        print(f_user)
        print(c_user)
        if (c_user.user == f_user.user):
            print('here')
            return redirect(reverse('dj-stream'))
        context['dj'] = f_user
        context['c_user'] = c_user
        return render(request, 'songshare/listener_stream.html', context)
    except:
        raise Http404

def clear_stream_action(request):
    context = {}
    c_user = Profile.objects.get(user=request.user)
    context['c_user'] = c_user
    c_user.live = False
    c_user.save()
    return redirect('profile-create')






def get_stream(id):
    stream = Stream.objects.all().filter(dj=Profile.objects.get(pk=id),is_streaming=True)
    if not stream.exists():
        return None
    return stream[0]

@login_required
def dj_stream_action(request, id):
    context = {}

    stream = get_stream(id)
    if stream == None:
        raise Http404
    c_user = Profile.objects.get(user=request.user)
    is_stream_dj = c_user.id == id
    context['c_user'] = c_user
    context['stream'] = stream
    context['is_stream_dj'] = is_stream_dj
    if request.method == "GET":
        # context['currently_playing'] = stream.get_currently_playing()
        # context['recently_played'] = stream.get_recently_played()
        return render(request,'songshare/stream_page.html',context)
    return 42



# https://stackoverflow.com/questions/48603190/django-max-similarity-trigramsimilarity-from-manytomanyfield
def create_query(fulltext):
    profile_names = Profile.objects.values_list('name', flat=True)

    query = []
    THRESHOLD = 0.25
    for name in profile_names:
        score = SequenceMatcher(None, name, fulltext).ratio()
        if score == 1:
            # Perfect Match for name
            return [Q(name=name)]
        if score >= THRESHOLD:
            query.append(Q(name=name))

    return query


@login_required
def dj_search(request):
    context = {}
    c_user = Profile.objects.get(user=request.user)
    context['c_user'] = c_user
    if request.method == "GET":
        return render(request, 'songshare/dj_search.html', context)
    else:
        # print(request.POST)
        search = request.POST['search']
        print(search)
        context['search']=  search
        try:
            queryset = Profile.objects.filter(reduce(or_, create_query(search)))
            context['djs']= queryset
        except:
            context['djs'] = []
        
        
        return render(request, 'songshare/dj_search.html', context)
    
def clean_search_query(result):
    items = result['tracks']['items']
    L = []
    for item in items:
        L.append({'album': item['album'], 'name': item['name'],'artists': item['artists'], 'uri': item['uri']})
    return L

# Returns a json object of the top 10 search terms
# Contains album, name, artists and uri fields
def song_search(request,search_query):
    client_credentials_manager = SpotifyClientCredentials(client_id=settings.SPOTIPY_CLIENT_ID,
                                                        client_secret=settings.SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    results = clean_search_query(sp.search(search_query))
    return HttpResponse(json.dumps(results), content_type='application/json')


@login_required
def get_photo(request, id):
    profile = get_object_or_404(Profile, id=id)
    print('Picture #{} fetched from db: {} (type={})'.format(id, profile.picture, type(profile.picture)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not profile.picture:
        raise Http404
    return HttpResponse(profile.picture, content_type=profile.content_type)


@login_required
def stream_on(request):
    pass

@login_required
def stream_off(request):
    pass

@login_required
def register_user_with_spotify(request):
    if request.method == "GET":
        # should never be the case that this is a get request.
        raise Http404
    context = {}
    spotify_registration_form = SpotifyRegistrationForm(request.POST)
    context['spotify_registration_form'] = spotify_registration_form
    c_user = Profile.objects.get(user=request.user)
    context['c_user'] = c_user
    if not spotify_registration_form.is_valid():
        return render(request,'songshare/user_home.html',context)
    # TODO: need to have some type of safegaud such that a user that has already 
    #       registred with spotify can not try and register again.
    spotify_email = spotify_registration_form.cleaned_data['spotify_email']
    c_user.spotify_email = spotify_email
    c_user.save()
    auth_url = c_user.create_oauth_url(scope=settings.SPOTIFY_SCOPE_ACCESS,
                                    client_id=settings.SPOTIPY_CLIENT_ID,
                                    client_secret=settings.SPOTIPY_CLIENT_SECRET,
                                    redirect_uri=settings.REDIRECT_AUTHENTICATION_URL)
    return redirect(auth_url)


def login_action(request):
    """ Login flow for user authentication.
    Validates login form using username and password fields.
    
    Parameters
    ----------
    request : HttpRequest
        the django response object containing metadata about the request
    """
    context = {}
    #display the registration form on a GET request
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'songshare/login_page.html', context)

    form = LoginForm(request.POST)
    context['form'] = form

    # validate the form
    if not form.is_valid():
        context['message'] = 'invalid login'
        return render(request, 'songshare/login_page.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)

    return redirect(reverse('home'))


@login_required
def logout_action(request):
    """ Logout flow
    Parameters
    ----------
    request : HttpRequest
        the django response object containing metadata about the request
    """
    try: 
        user = request.user
        profile = Profile.objects.get(pk=user.id)
        profile.live = False
        profile.save()
        logout(request)
        return redirect(reverse('login'))
    except:
        raise Http404
    logout(request)
    return redirect(reverse('login'))


@transaction.atomic
def register_action(request):
    """ Register flow
    Validates the User registration form using the appropriate fields, and 
    creates a Profile for the user.
    Parameters
    ----------
    request : HttpRequest
        the django response object containing metadata about the request
    """
    context = {}
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'songshare/register_page.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'songshare/register_page.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['fname'],
                                        last_name=form.cleaned_data['lname'])
    new_user.save()
    new_user = authenticate(username=form.cleaned_data['username'], 
                            password=form.cleaned_data['password'])
    login(request, new_user)
    
    # testing
    dj_status= False
    fname = request.POST['fname']
    lname = request.POST['lname']
    name = fname + ' ' + lname

    new_profile = Profile(user=request.user, 
                          spotify_email=form.cleaned_data['spotify_email'],
                          fname=request.POST['fname'], 
                          lname=request.POST['lname'], 
                          is_dj=dj_status,
                          is_live=False,
                          name=name,
                          picture=None)
    if form.cleaned_data['spotify_email'] != "":
        auth_url = new_profile.create_oauth_url(scope=settings.SPOTIFY_SCOPE_ACCESS,
                                    client_id=settings.SPOTIPY_CLIENT_ID,
                                    client_secret=settings.SPOTIPY_CLIENT_SECRET,
                                    redirect_uri=settings.REDIRECT_AUTHENTICATION_URL)
        new_profile.save()
        return redirect(auth_url)
    new_profile.save()
    return redirect(reverse('home'))

@login_required
def create_stream_action(request):
    if request.method == "GET":
        raise Http404
    context = {}
    stream_creation_form = CreateStreamForm(request.POST)
    context['stream_creation_form'] = stream_creation_form
    c_user = Profile.objects.get(user=request.user)
    context['c_user'] = c_user
    if not stream_creation_form.is_valid():
        return render(request,'songshare/user_home.html',context)
    stream_name = stream_creation_form.cleaned_data['stream_name']
    new_stream = Stream(name=stream_name,
                        dj=c_user,
                        is_streaming=True)
    current_song = new_stream.get_currently_playing()
    if current_song == None:
        context['errors'] = [{'message':'Must currently have an active spotify session'}]
        return render(request,'songshare/user_home.html',context)
    new_stream.save()
    c_user.is_live = True
    c_user.save()
    return redirect(reverse('dj-stream',args=[c_user.id]))

# do not need an id parameter because the button for ending the
# stream will only be available to the DJ this is handled in the 
# dj_stream action with the parameter is_stream_dj
@login_required
def end_stream_action(request):
    if request.method == "GET":
        raise Http404
    c_user = Profile.objects.get(user=request.user)
    stream = get_stream(c_user.id)
    if stream == None:
        raise Http404
    stream.is_streaming = False
    stream.save()
    c_user.is_live = False
    c_user.save()
    return redirect(reverse('home'))

@login_required
def join_stream_action(request, id):
    if request.method == "GET":
        raise Http404
    stream = get_stream(id)
    if stream == None:
        raise Http404
    listener_profile = Profile.objects.get(user=request.user)
    stream.listeners.add(listener_profile)
    stream.save()
    return redirect(reverse('dj-stream',args=[id]))

@login_required
def leave_stream_action(request, id):
    if request.method == "GET":
        raise Http404
    stream = get_stream(id)
    if stream == None:
        raise Http404
    listener_profile = Profile.objects.get(user=request.user)
    stream.listeners.remove(listener_profile)
    stream.save()
    return redirect(reverse('home'))

def get_currently_playing(request,id):
    if request.method == "POST":
        raise Http404
    stream = get_stream(id)
    if stream == None:
        currently_playing = Song(name="No song playing", artist="", album="", uri="", image_url="/static/songshare/default.jpg")
    else:
        currently_playing = stream.get_currently_playing()
        if currently_playing is None:
            currently_playing = Song(name="No song playing", artist="", album="", uri="", image_url="/static/songshare/default.jpg")
    results = currently_playing.to_json()
    return HttpResponse(json.dumps(results), content_type='application/json')

def get_recently_played(request,id):
    if request.method == "POST":
        raise Http404
    stream = get_stream(id)
    if stream == None:
        return HttpResponse(json.dumps([]), content_type='application/json')
    results = stream.get_recently_played()
    response = []
    for item in results:
        response.append(item.to_json())
    return HttpResponse(json.dumps(response), content_type='application/json')
    
@login_required
def request_song_action(request,id,song_uri):
    if request.method == "GET":
        raise Http404
    stream = get_stream(id)
    if stream == None:
        return HttpResponse(json.dumps({'success':False}), content_type='application/json')
    client_credentials_manager = SpotifyClientCredentials(client_id=settings.SPOTIPY_CLIENT_ID,
                                                        client_secret=settings.SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    results = sp.track(song_uri)
    requested_song = Song(artist=Song.clean_artists(results['artists']),
                        album=results['album']['name'],
                        name=results['name'],
                        uri=song_uri,
                        image_url=results['album']['images'][2]['url'],
                        request_status='pending',
                        parent=stream,
                        creation_time=timezone.now())
    requested_song.save()
    requested_song.voters.add(request.user.profile_set.all()[0])
    stream.save()
    result = {'is_stream_dj':False, 'requested_songs':[requested_song.to_json(request)], 'success':True}
    return HttpResponse(json.dumps(result), content_type='application/json')

@login_required
def get_requested_songs(request,id):
    if request.method == "POST":
        raise Http404
    stream = get_stream(id)
    if stream == None:
        return HttpResponse(json.dumps({'not_exists':True}), content_type='application/json')
    is_stream_dj = stream.dj == Profile.objects.get(user=request.user)
    results = {'is_stream_dj':is_stream_dj, 'requested_songs':[], 'not_exists':False}
    for item in stream.requested_songs.extra(order_by=['-creation_time']):
        results['requested_songs'].append(item.to_json(request))
    return HttpResponse(json.dumps(results), content_type='application/json')

@login_required
def add_song_to_queue(request,id,song_uri):
    if request.method == "GET":
        raise Http404
    stream = get_stream(id)
    is_stream_dj = stream.dj == Profile.objects.get(user=request.user)
    if stream == None:
        raise Http404
    song = stream.requested_songs.get(uri=song_uri)
    stream.add_to_queue(song)
    song.request_status = 'accepted'
    song.save()
    stream.save()
    return HttpResponse(json.dumps({}), content_type='application/json')

@login_required
def remove_requested_song(request,id,song_uri):
    if request.method == "GET":
        raise Http404
    stream = get_stream(id)
    is_stream_dj = stream.dj == Profile.objects.get(user=request.user)
    if stream == None:
        raise Http404
    song = stream.requested_songs.get(uri=song_uri)
    song.request_status = 'rejected'
    song.save()
    stream.save()
    return HttpResponse(json.dumps({}), content_type='application/json')

@login_required
def vote(request):
    # check that the correct parameters have been sent
    if request.method != 'POST' or ('song' not in request.POST):
        return HttpResponse(json.dumps({"success":False}), content_type='application/json')

    # This checks whether the song is in the stream. Note: each song has only one parent playlist
    song = Song.objects.filter(id=request.POST['song'])
    if not song.exists():
        raise Http404 
    song = song[0]

    # add to voters list
    if song.request_status != 'rejected':
        song.voters.add(request.user.profile_set.all()[0])

    return HttpResponse(json.dumps({"success":True, "song":song.id, "votes":song.voters.all().count()}), content_type='application/json')

@login_required
def unvote(request):
    # check that the correct parameters have been sent
    if request.method != 'POST' or ('song' not in request.POST):
        return HttpResponse(json.dumps({"success":False}), content_type='application/json')

    # This checks whether the song is in the stream. Note: each song has only one parent playlist
    song = Song.objects.filter(id=request.POST['song'])
    if not song.exists():
        raise Http404 
    song = song[0]

    # remove from voters list
    if song.request_status != 'rejected':
        song.voters.remove(request.user.profile_set.all()[0])

    return HttpResponse(json.dumps({"success":True, "song":song.id, "votes":song.voters.all().count()}), content_type='application/json')

def get_currently_streaming(request):
    if request.method == "POST":
        raise Http404
