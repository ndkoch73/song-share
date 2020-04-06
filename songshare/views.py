
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
    
    try:
        c_user = Profile.objects.get(user=request.user)
        print(c_user)
        context = {'c_user': c_user}
        return render(request,'songshare/user_home.html', context)
    except:
        raise Http404
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
    context = {}
    if request.method == "GET":
        return render(request, 'songshare/authenticate.html', context)
    return redirect('authenticate')



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
        context['search']=  request.POST['search']
        context['djs'] = Profile.objects.order_by('live')
        print(context['djs'])
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
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()
    new_user = authenticate(username=form.cleaned_data['username'], 
                            password=form.cleaned_data['password'])
    login(request, new_user)
    
    # testing
    dj_status= False
    if (new_user.id == 2):
        dj_status = True

    new_profile = Profile(user=request.user, 
                          is_dj=dj_status,
                          live=False,
                          auth_token=None,
                          fname=request.POST['first_name'], 
                          lname=request.POST['last_name'], 
                          picture=None)
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

