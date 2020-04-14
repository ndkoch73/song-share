function search_for_song(){
    search_query = $("#song_search_input").val()
    if(search_query == ""){
        return;
    }
    $("#song_search_input").val('')
    $.ajax({
        url: "/songshare/song-search/"+encodeURIComponent(search_query),
        type: "POST",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: add_searched_songs,
        error: function(response){
            console.log(response);
        }
    });
}

function get_currently_playing(){
    $.ajax({
        url: window.location.pathname + "/get-currently-playing",
        type: "GET",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: add_currently_playing,
        error: function(response){
            console.log(response)
        }
    });
}

function get_recently_played(){
    $.ajax({
        url: window.location.pathname + "/get-recently-played",
        type: "GET",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: add_recently_played,
        error: function(response){
            console.log(response)
        }
    });
}

function add_recently_played(response){
    var t = $('#recently_played_container').html().split('<div class="ui segment">');
    t = t.slice(1,t.length)
    current_songs_html = ""
    $(t).each(function(){
        current_songs_html += '<div class="ui segment">' + this;
    });
    new_songs_html = ""
    $(response).each(function(){
        new_songs_html += get_recently_played_html(this);
    });
    if (new_songs_html != current_songs_html){
        $('#recently_played_container').empty();
        $('#recently_played_container').html(new_songs_html)
    }
}

function get_recently_played_html(song){
    return  '<div class="ui segment">' + 
                '<div style="display: flex;flex-direction: row;">' + 
                    '<div class="ui small image">' + 
                        '<img src="'+ song.image_url + '">' + 
                    '</div>' + 
                    '<div class="segment left aligned" style="align-items: flex-end;">' + 
                        '<div class="ui header">' +
                            song.name +
                            '<div class="sub header">' + song.album +
                                '<br>' + 
                                song.artist +
                            '</div>' + 
                        '</div>' +
                    '</div>' +
                '</div>' + 
            '</div>'
}

function add_currently_playing(response){
    var currently_playing_html = get_currently_playing_html(response)
    if (currently_playing_html != $('#currently_playing_container').html()){
        $('#currently_playing_container').empty()
        $('#currently_playing_container').html(currently_playing_html);
    }
}

function request_song(song_uri){
    $.ajax({
        url: window.location.pathname + "/request-song/" + encodeURIComponent(song_uri),
        type: "POST",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json"
    });
}

function clear_search(){
    $('#searched_songs_container').empty();
}

function add_searched_songs(response){
    $('#searched_songs_container').empty();
    $(response).each(function(){
        searched_song_container_id = '#searched_songs_container';
        song_html = get_searched_song_html(this);
        $(searched_song_container_id).append(song_html);
    });
}

function get_currently_playing_html(song){
    return  '<div class="ui card">' + 
                '<div class="ui image">' + 
                    '<img src="' + song.image_url + '">' +
                '</div>' + 
                '<div class="content">' + 
                    '<div class="header">' + song.name + '</div>' + 
                    '<div class="meta">' + 
                        '<span>'+ song.album + '</span>' + 
                        '<br>' + 
                        '<span>'+ song.artist + '</span>' + 
                    '</div>' + 
                '</div>' + 
            '</div>'
}

function get_searched_song_html(searched_song){
    artists = ""
    for(var i = 0; i < searched_song.artists.length; i++){
        artists += searched_song.artists[i].name;
        if(i != searched_song.artists.length - 1){
            artists += ' & ';
        }
    }
    return  '<div class="ui fluid card">' + 
                '<div style="display: flex;flex-direction: row;">' + 
                    '<div class="ui small image">' + 
                        '<img src="' + searched_song.album.images[2].url + '">' +
                    '</div>' + 
                    '<div class="segment left aligned">' + 
                        '<div class="ui small header" style="padding-top: 3%;">' + 
                            searched_song.name + 
                            '<div class="sub header">' + searched_song.album.name + 
                            '<br>' + 
                            artists + 
                        '</div>' + 
                    '</div>' +
                '</div>' +
            '</div>' + 
            '<div class="ui bottom attached button" onclick="request_song(' + "'" + searched_song.uri + "'" + ')">' + 
                '<i class="add icon"></i>' + 
                'Request Song' + 
            '</div>'
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        c = cookies[i].trim();
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length);
        }
    }
    return "unknown";
}

function refresh_songs(){
    get_currently_playing()
    get_recently_played()
}

window.onload = refresh_songs;
window.setInterval(get_currently_playing, 10*1000);
window.setInterval(get_recently_played,15*1000)
