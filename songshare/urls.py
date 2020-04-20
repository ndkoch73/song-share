from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home_page, name="home"),
    path('login',views.login_action,name="login"),
    path('register', views.register_action, name="register"),
    path('logout',views.logout_action,name="logout"),
    path('listener-stream/<int:id>', views.listener_stream, name="listener-stream"),
    path('dj-search', views.dj_search, name="dj-search"),
    path('song-search/<str:search_query>', views.song_search, name="song-search"),
    path('photo/<int:id>', views.get_photo, name="photo"),
    path('follow:<int:id>', views.update_follow, name='follow'),
    path('profile-create', views.profile_page_action, name="profile-create"),
    path('profile-view/<int:id>', views.goto_profile, name="profile-view"),
    path('authenticate', views.authenticate_action, name="authenticate"),
    path('register-user-spotify',views.register_user_with_spotify,name="spotify-user-spotify"),
    path('create-stream',views.create_stream_action,name="create-stream"),
    path('dj-stream/<int:id>',views.dj_stream_action,name="dj-stream"),
    path('end-stream',views.end_stream_action,name='end-stream'),
    path('join-stream/<int:id>',views.join_stream_action,name='join-stream'),
    path('leave-stream/<int:id>',views.leave_stream_action,name='leave-stream'),
    path('dj-stream/<int:id>/request-song/<str:song_uri>',views.request_song_action,name="request-song"),
    path('dj-stream/<int:id>/get-currently-playing',views.get_currently_playing,name="get-currently-playing"),
    path('dj-stream/<int:id>/get-recently-played',views.get_recently_played,name="get-recently-played"),
    path('dj-stream/<int:id>/get-requested-songs',views.get_requested_songs,name="get-requested-songs"),
    path('dj-stream/<int:id>/add-to-queue/<str:song_uri>',views.add_song_to_queue,name="add-to-queue"),
    path('dj-stream/<int:id>/remove-requested-song/<str:song_uri>',views.remove_requested_song,name='remove-requested-song'),
    path('vote',views.vote,name="vote"),
    path('unvote',views.unvote,name="unvote"),
    path('get-currently-streaming',views.get_currently_streaming,name="get-currently-streaming"),
    # path('dj-search/refresh-streams', views.refresh_stream, name="refresh-stream"),
]