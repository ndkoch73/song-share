function displayError(message) {
    $("#error").html(message);
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

function update_streams(response){
    var streams = response;
    console.log(streams);
    streams.forEach(stream => {
        var x = stream.id;
        var listeners = stream.listeners;
        var stream_listeners_count_id = "id_stream_listener_count_" + x;
        if (document.getElementById(stream_listeners_count_id).value != listeners) 
        {
            document.getElementById(stream_listeners_count_id).value = listeners;
        }
    });
}



function refresh_streams(){
    $.ajax({
        url: window.location.pathname + "/refresh-streams",
        type: "GET",
        dataType: "json",
        success: update_streams,
        error: function(response){
            console.log(response)
        }
    });
}


window.onload = refresh_streams;
window.setInterval(refresh_streams,10000000000); 