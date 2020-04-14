function search_for_song(){
    search_query = $("#song_search_input").val()
    // TODO: sanitize the search query and handle errors here
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

function clear_search(){
    $('#searched_songs_container').empty();
}

function add_searched_songs(response){
    console.log(response)
    $(response).each(function(){
        searched_song_container_id = '#searched_songs_container';
        song_html = get_searched_song_html(this);
        $(searched_song_container_id).append(song_html);
    });
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
            '<div class="ui bottom attached button">' + 
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