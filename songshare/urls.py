from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home_page, name="home"),
    path('login',views.login_action,name="login"),
    path('register', views.register_action, name="register"),
    path('logout',views.login_action,name="logout"),
    path('dj-stream/<int:id>', views.dj_stream, name="dj-stream"),
    path('dj-search', views.dj_search, name="dj-search"),
    path('song-search/<int:id>', views.song_search, name="song-search"),
    path('photo/<int:id>', views.get_photo, name="photo"),
    path('stream-off', views.stream_off, name="stream-off"),
    path('stream-on', views.stream_on, name="stream-on"),
    path('follow:<int:id>', views.update_follow, name='follow'),
    path('unfollow:<int:id>', views.unfollow, name='unfollow'),
    path('profile-create', views.profile_page_action, name="profile-create"),
    path('profile-view', views.goto_profile, name="profile-view"),
    path('authenticate', views.authenticate_action, name="authenticate"),
]
