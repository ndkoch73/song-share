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

function add_song_to_queue(song_uri){
    $.ajax({
        url: window.location.pathname + "/add-to-queue/" + encodeURIComponent(song_uri),
        type: "POST",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: get_requested_songs,
        error: function(response){
            console.log(response)
        }
    });
}

function update_current_listeners(){
    $.ajax({
        url: window.location.pathname + "/get-listener-count",
        type: "GET",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: update_number_of_listeners,
        error: function(response){
            console.log(response)
        }
    });
}

function update_number_of_listeners(response){
    count_id = "#stream_" + response['id'] + "_count";
    new_count = parseInt(response['count']);
    old_count = parseInt($(count_id).html());
    if(new_count != old_count){
        $(count_id).html(new_count);
    }
}   

function deny_song(song_uri){
    $.ajax({
        url: window.location.pathname + "/remove-requested-song/" + encodeURIComponent(song_uri),
        type: "POST",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: get_requested_songs,
        error: function(response){
            console.log(response)
        }
    });
}

function add_recently_played(response){
    var previously_played_html = $('#recently_played_container').html()
    new_recently_played_html = ""
    $(response).each(function(){
        new_recently_played_html += get_recently_played_html(this);
    });
    previously_played_html = previously_played_html.replace(/\amp;/g,"")
    if(previously_played_html != new_recently_played_html){
        $('#recently_played_container').empty();
        $('#recently_played_container').html(new_recently_played_html)
    }
}

function get_recently_played_html(song){
    return `<div class="ui raised segment">` +
                `<div class="ui two column stackable grid">
                    <div class="three wide column"> ` + 
                        '<div class="ui image">' + 
                            '<img src="'+ song.image_url + '">' + 
                        '</div>' +     
                    `</div>
                    <div class="twelve wide column">` + 
                        '<div class="ui header">' +
                            song.name +
                            '<div class="sub header">' + song.album +
                                '<br>' + 
                                song.artist +
                            '</div>' + 
                        '</div>' +
                    `</div>
                </div>
            </div>`
}

function add_currently_playing(response){
    var currently_playing_html = get_currently_playing_html(response)
    var recent_currently_playing_html = $('#currently_playing_container').html()
    recent_currently_playing_html = recent_currently_playing_html.replace(/\amp;/g,"")
    if (currently_playing_html != recent_currently_playing_html){
        $('#currently_playing_container').empty()
        $('#currently_playing_container').html(currently_playing_html);
    }
}

function request_song(song_uri){
    $.ajax({
        url: window.location.pathname + "/request-song/" + encodeURIComponent(song_uri),
        type: "POST",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: add_one_requested_song,
        error: function(response){
            console.log(response)
        }
    });
}

function vote(song_id){
    $.post(
        "/songshare/vote",
        {csrfmiddlewaretoken:getCSRFToken(), song:song_id},
        update_votes
    );
}

function unvote(song_id){
    $.post(
        "/songshare/unvote",
        {csrfmiddlewaretoken:getCSRFToken(), song:song_id},
        update_votes
    );
}

function update_votes(response){
    if(response.success){
        $("#song_" + response.song.toString() + "_vote_count").html(response.votes.toString());
    }
}

function get_requested_songs(){
    $.ajax({
        url: window.location.pathname + "/get-requested-songs",
        type: "GET",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: update_requested_songs,
        error: function(response){
            console.log(response)
        }
    });
}

function add_requested_song(response){
    var is_stream_dj = response['is_stream_dj']
    new_requested_html = get_requested_song_html(response['requested_songs'][0],is_stream_dj)
    $('#requested_songs_container').append(new_requested_html)
}

function update_requested_songs(response){
    if(response['not_exists']) {
        $("#id_name_of_stream").html("The DJ has stopped the stream. Please visit the home page for live streams.")
        $('#requested_songs_container').empty()
    }
    else {
        var current_requested_html = $('#requested_songs_container').html();
        var new_requested_html = ""
        var is_stream_dj = response['is_stream_dj']
        $(response['requested_songs']).each(function(){
            new_requested_html += get_requested_song_html(this,is_stream_dj)
        });
        current_requested_html = current_requested_html.replace(/\amp;/g,"")
        if(current_requested_html != new_requested_html){
            $('#requested_songs_container').empty()
            $('#requested_songs_container').html(new_requested_html)
        }
    }
}

function add_one_requested_song(response) {
    if(response['success']) {
        var new_requested_html = ""
        var is_stream_dj = response['is_stream_dj']
        $(response['requested_songs']).each(function(){
            new_requested_html += get_requested_song_html(this,is_stream_dj)
        });
        $('#requested_songs_container').prepend(new_requested_html)
    }
}

function votes_html(song,is_stream_dj){
    if(is_stream_dj){
        return '<div class="ui floating blue circular label dj" id="song_' + song.id + '_vote_count">' + song.votes + '</div>'
    }

    if(!song.user_has_voted){
        button = `  <button class="circular mini ui icon button" onclick="vote(` + song.id + `)">
                        <i class="thumbs up icon"></i>
                    </button>
                `
    }
    else {
        button = `  <button class="blue active circular mini ui icon button" onclick="unvote(`+ song.id +`)">
                        <i class="thumbs up icon"></i>
                    </button>
                `
    }
    return '<div class="ui floating blue circular label non-dj" id="song_' + song.id + '_vote_count">' + song.votes + '</div>' + 
            '<div class="ui bottom right attached label" style="background-color: transparent;">' + button + '</div>'
}

function get_requested_song_html(song,is_stream_dj){
    if(song.request_status == 'accepted'){
        button_status_html = `
                    <div class="six wide right aligned column">` +
                        '<button class="disabled circular ui green button" style="opacity: 1 !important"><i class="check icon"></i>Accept</button>' +
                        '<button class="disabled circular ui red button"><i class="close icon"></i>Deny</button>' +
                    `</div>
                </div>
            </div>
            `
        status_label_html = '<span class="ui green right corner label"><i class="check icon"></i></span>'
    } else if(song.request_status == 'rejected'){
        button_status_html = `
                    <div class="six wide right aligned column">` +
                    '<button class="disabled circular ui green button"><i class="check icon"></i>Accept</button>' +
                    '<button class="disabled circular ui red button" style="opacity: 1 !important"><i class="close icon"></i>Deny</button>' +
                `</div>
            </div>
        </div>    
        `
        status_label_html = '<span class="ui red right corner label"><i class="close icon"></i></span>'
    } else {
        button_status_html = `
                    <div class="six wide right aligned column">` +
                    '<button class="circular ui green button" ' + 
                        'onclick="add_song_to_queue(' + "'" + song.uri + "'" + ')"><i class="check icon"></i>Accept</button>' +
                    '<button class="circular ui red button" ' + 
                        'onclick="deny_song(' + "'" + song.uri + "'" + ')"><i class="close icon"></i>Deny</button>' +
                `</div>
            </div>
        </div>
        `
        status_label_html = '<span class="ui grey right corner label"><i class="hourglass half icon"></i></span>'
    }
    if(!is_stream_dj){
        return `
                <div class="ui raised segment">` + 
                    status_label_html + 
                    votes_html(song,is_stream_dj) + 
                    `<div class="ui three column stackable grid">
                        <div class="three wide column"> ` + 
                            '<div class="ui image">' + 
                                '<img src="'+ song.image_url + '">' + 
                            '</div>' +     
                        `</div>
                        <div class="nine wide column">` + 
                            '<div class="ui header">' +
                                song.name +
                                '<div class="sub header">' + song.album +
                                    '<br>' + 
                                    song.artist +
                                '</div>' + 
                            '</div>' +
                        '</div>' + 
                    `</div>
                </div>
        `
    } else {
        main_html = `
                    <div class="ui raised segment"> ` + 
                        votes_html(song,is_stream_dj) + 
                        `<div class="ui four column stackable grid">
                            <div class="two wide column"> ` + 
                                '<div class="ui small image">' + 
                                    '<img src="'+ song.image_url + '">' + 
                                '</div>' +     
                            `</div>
                            <div class="eight wide column">` + 
                                '<div class="ui header">' +
                                    song.name +
                                    '<div class="sub header">' + song.album +
                                        '<br>' + 
                                        song.artist +
                                    '</div>' + 
                                '</div>' +
                            '</div>' + 
                            button_status_html
        return main_html
    }
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
    return `<div class="ui fluid raised card">` +
                `<div class="ui two column stackable grid">
                    <div class="three wide column"> ` + 
                        '<div class="ui image">' + 
                            '<img src="'+ searched_song.album.images[2].url + '">' + 
                        '</div>' +     
                    `</div>
                    <div class="twelve wide column">` + 
                        '<div class="ui header">' +
                            searched_song.name +
                            '<div class="sub header">' + searched_song.album.name +
                                '<br>' + 
                                artists +
                            '</div>' + 
                        '</div>' +
                    `</div>
                </div>` + 
                '<div class="ui bottom attached button" onclick="request_song(' + "'" + searched_song.uri + "'" + ')">' + 
                    '<i class="add icon"></i>' + 
                    'Request Song' + 
                '</div>' + 
            '</div>' + 
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
    get_requested_songs()
}

window.onload = refresh_songs;
window.setInterval(get_currently_playing, 10*1000);
window.setInterval(get_recently_played,15*1000);
window.setInterval(get_requested_songs,2*1000);
window.setInterval(update_current_listeners,1*1000);