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
    streams.forEach(stream => {
        var stream_followers_id = "id_stream_follower" + x;
        if (document.getElementById(stream_followers_id)) 
        {

        }
    });
}
window.onload = get_currently_streaming();
window.setInterval(5000);


