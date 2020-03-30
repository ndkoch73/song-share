
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.core import serializers

from django.utils import timezone
from datetime import datetime

from songshare.forms import *
from songshare.models import *

import json

def home_page(request):
    return render(request,'songshare/user_home.html', {})
# renders current user's profile page


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
    except Profile.DoesNotExist:
        return redirect('home')
    
    
    # the users that follow the current user
    following = list(c_user.following.all())
    context['c_user'] = c_user
    context['following'] = following
    context['form']  = ProfilePictureForm()
    print(context)
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
            return redirect(reverse('user_profile_page'))

        name = profile.fname + ' ' + profile.lname
        context['c_user'] = c_user
        context['profile'] = profile
        context['following'] = following
        if (profile.user in following):
            context['following'] = True
        else:
            context['following'] = False
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

def authenticate_action(request):
    context = {}
    if request.method == "GET":
        return render(request, 'songshare/authenticate.html', context)
    return redirect('authenticate')




def profile_view(request):
    pass

def dj_stream(request, id):
    pass

def dj_search(request):
    context = {}
    return render(request, 'songshare/dj_search.html', context)

def song_search(request,id):
    pass

@login_required
def get_photo(request, id):
    profile = get_object_or_404(Profile, id=id)
    # print('Picture #{} fetched from db: {} (type={})'.format(id, profile.profile_picture, type(profile.profile_picture)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not profile.profile_picture:
        raise Http404

    return HttpResponse(profile.profile_picture, content_type=profile.content_type)


@login_required
def stream_on(request):
    pass

@login_required
def stream_off(request):
    pass



@login_required
def follow(request, id):
    pass

@login_required
def unfollow(request, id):
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
    #display the registration form on a GET request
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'songshare/login_page.html', context)

    form = LoginForm(request.POST)
    context['form'] = form

    # validate the form
    if not form.is_valid():
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
    logout(request)
    return redirect(reverse('login'))




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
        return render(request, 'songshare/register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'songshare/register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        fname=form.cleaned_data['fname'],
                                        lname=form.cleaned_data['lname'])
    new_user.save()
    new_user = authenticate(username=form.cleaned_data['username'], 
                            password=form.cleaned_data['password'])
    login(request, new_user)
    new_profile = Profile(user=request.user, 
                          is_dj=False,
                          fname=request.POST['fname'], 
                          lname=request.POST['lname'], 
                          picture=None)
    new_profile.save()
    return redirect(reverse('home'))


"""
NOTE: - I think it's a good idea to seperate the current user's profile page and 
        the profile pages of other users. The profile_page_action method redirects
        a user to their own profile. The goto_profile method will redirect the user
        to their own profile if they click their own link, or to other user profiles.
        Obviously we will work on the names of the html once we decide on urls.py
"""

# renders current user's profile page
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
    c_user = Profile.objects.get(user=request.user)
    # the users that follow the current user
    following = list(c_user.following.all())
    context['c_user'] = c_user
    context['following'] = following
    context['form']  = ProfilePictureForm()
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
            return redirect(reverse('user_profile_page'))

        name = profile.fname + ' ' + profile.lname
        context['c_user'] = c_user
        context['profile'] = profile
        context['following'] = following
        if (profile.user in following):
            context['following'] = True
        else:
            context['following'] = False
        context['name'] = name
        return render(request, 'songshare/profile.html', context)
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

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'songshare/login_page.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'songshare/login_page.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))

def logout_action(request):
    logout(request)
    return redirect(reverse('login'))

def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'songshare/register_page.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
    	return render(request, 'songshare/register_page.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    p = Profile(user=new_user)
    p.save()
  

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)


    return redirect(reverse('home'))