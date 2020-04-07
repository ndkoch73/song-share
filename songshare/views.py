
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

@login_required
def home_page(request):
    c_user = Profile.objects.get(user=request.user)
    print(c_user)
    context = {'c_user': c_user}
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
    print(context)
    print(Profile.objects.all())
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
    current_user_profile.save()
    return redirect(reverse('home'))

def listener_stream(request, id):
    context = {}
    try:
        p_user = User.objects.get(id=id)
        f_user = Profile.objects.get(user=p_user)
        c_user = Profile.objects.get(user=request.user)
        if (c_user.user == f_user.user):
            return redirect(reverse('dj_stream'))
        context['dj'] = f_user
        context['c_user'] = c_user
        return render(request, 'songshare/listener_stream.html', context)
    except:
        raise Http404


# Starts the stream sets flags such as is live
def dj_stream(request):
    context = {}
    user = request.user
    user_id = user.id
    try:
        profile = Profile.objects.get(pk=user_id)
        c_user = Profile.objects.get(user=request.user)
        profile.live =  True
        profile.save()
        context['c_user'] = c_user
        return render(request, 'songshare/dj_stream.html', context)
    except:
        raise Http404

def clear_stream_action(request):
    context = {}
    return render(request, 'songshare/dj_stream.html', context)


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
        context['djs'] = Profile.objects.filter(name=search)
        try: 
            print("hit")
            similarity = Profile.objects.annotate(similarity=TrigramSimilarity('name', search),).filter(similarity__gt=0.1).order_by('-similarity')
            print("hit")
            # context['djs'] = similarity
        except:
            print("whoops")
        
        return render(request, 'songshare/dj_search.html', context)
    

def song_search(request,id):
    pass

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




def login_action(request):
    """ Login flow for user authentication.
    Validates login form using username and password fields.
    
    Parameters
    ----------
    request : HttpRequest
        the django response object containing metadata about the request
    """
    context = {}
    # try:
    #     Profile.objects.get(pk=1)
    #     new_user = User.objects.create_user(username=form.cleaned_data['username'], 
    #                                     password=form.cleaned_data['password'],
    #                                     email=form.cleaned_data['email'],
    #                                     first_name=form.cleaned_data['first_name'],
    #                                     last_name=form.cleaned_data['last_name'])
    #     new_user.save()
    #     new_user = authenticate(username=form.cleaned_data['username'], 
    #                         password=form.cleaned_data['password'])
    #     login(request, new_user)
    #     new_profile = Profile(user=request.user, 
    #                       is_dj=False,
    #                       live=False,
    #                       auth_token="",
    #                       fname=request.POST['first_name'], 
    #                       lname=request.POST['last_name'], 
    #                       picture=None)
    # except:
    #     Profile

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
                          spotify_username=form.cleaned_data['spotify_username'],
                          fname=request.POST['fname'], 
                          lname=request.POST['lname'], 
                          is_dj=dj_status,
                          live=False,
                          name=name,
                          picture=None)
    if form.cleaned_data['spotify_username'] != "":
        auth_url = new_profile.create_oauth_url(scope=settings.SPOTIPY_MODIFY_PLAYBACK_SCOPE,
                                    client_id=settings.SPOTIPY_CLIENT_ID,
                                    client_secret=settings.SPOTIPY_CLIENT_SECRET,
                                    redirect_uri=settings.REDIRECT_AUTHENTICATION_URL)
        new_profile.save()
        return redirect(auth_url)
    new_profile.save()
    return redirect(reverse('home'))

DUMMY_LIVEDJ ={
    'id': 1,
    'is_dj': True,
    'live': True,
    'auth_token': None,
    'fname': 'dummy',
    'lname': 'dj',
    'bio': 'DUMMY',
}

"""
NOTE: - I think it's a good idea to seperate the current user's profile page and 
        the profile pages of other users. The profile_page_action method redirects
        a user to their own profile. The goto_profile method will redirect the user
        to their own profile if they click their own link, or to other user profiles.
        Obviously we will work on the names of the html once we decide on urls.py
"""

