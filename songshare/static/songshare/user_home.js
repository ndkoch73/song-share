function get_currently_streaming(){
    $.ajax({
        url: "/songshare/get-currently-streaming",
        type: "GET",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: update_streams,
        error: function(response){
            console.log(response)
        }
    });
}

function update_streams(response){
    stream_html = "";
    $(response.streams).each(function(){
        stream_html += get_stream_html(this,response.c_user)
    });
    previous_stream_html = $('#currently-streaming-container').html();
    if(previous_stream_html != stream_html){
        $('#currently-streaming-container').html(stream_html);
    }
}

function is_user_listener(user,listeners){
    result = false;
    listeners.forEach(function(item){
        if(item.id == user.id){
            result = true
        }
    });
    return result;
}

function get_stream_html(stream,c_user){
    photo_url = stream.picture_avaliable ? "/songshare/photo/" + stream.dj.id : "https://cdn1.iconfinder.com/data/icons/user-pictures/100/unknown-512.png";
    stream_action_button = ""
    if(c_user.id != stream.dj.id){
        if(is_user_listener(c_user,stream.listeners)){
            stream_action_button = `
                <a class="fluid positive ui button" href="/songshare/dj-stream/` + stream.dj.id + `">
                    <i class="spotify icon"></i>
                    Go To Stream
                </a>`
        } else {
            stream_action_button = `
                <form method="POST" action="/songshare/join-stream/` + stream.dj.id + `">
                    <button class="fluid positive ui button">
                    <i class="spotify icon"></i>
                        Join Stream
                    </button>` + 
                '<input type="hidden" name="csrfmiddlewaretoken" value="' + getCSRFToken() + '">' +
                '</form>'
        }
    }
    return `
            <div class="four wide column">
                <div class="ui card">
                    <div class="content">
                        <span class="header">` + stream.name + '</span>' + 
                `       <img src="` + photo_url + `" style="height: 64px; width: 64px;">
                        <br><br>
                        <div class="meta">
                            <span>Hosted by <a href="/songshare/profile-view/` + stream.dj.id + `">DJ ` + stream.dj.username + `</a></span>
                        </div>
                        <div class="meta">
						    <i class="users icon"></i>
						    <span>` + stream.total_listening + ` listeners</span>
                        </div>` + 
                        stream_action_button + 
                    `</div>
                </div>
            </div>`
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

function refresh_streams(){
    update_streams()
}

window.onload = get_currently_streaming;
window.setInterval(get_currently_streaming,2*1000)
