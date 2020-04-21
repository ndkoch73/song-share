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
    var streams = response.streams;
    console.log(streams);
    streams.forEach(stream => {
        var x = stream.id;
        var listeners = stream.total_listening;
        console.log(x);
        var stream_id = "id_stream_" + x;
        
        // console.log(document.getElementById(stream_listeners_count_id));
        if (document.getElementById(stream_id) != null) 
        {
            console.log(('#'+stream_listeners_count_id))
            // console.log(document.getElementById(stream_listeners_count_id).textContent);
            // document.getElementById(stream_listeners_count_id).textContent(listeners);
            doc_html =  "<i class=\"users icon\"></i>"+ "<span>"+ listeners + " listeners</span>"
            var stream_listeners_count_id = "id_stream_listener_count_"+x;
            var live_status = "id_stream_live_"+x;
            console.log(listeners)
            $('#'+stream_listeners_count_id).html(doc_html);
            if (stream.is_streaming){
                live_html = "<i class=\"circle red icon\"></i>"
            }
            else{
                live_html = "<i class=\"circle outline icon\"></i>"
            }
            $('#'+live_status).html(live_html);
        }
    });
}






function refresh_streams(){
    $.ajax({
        url: window.location.pathname + "/refresh-search",
        type: "GET",
        dataType: "json",
        success: update_streams,
        error: function(response){
            console.log(response)
        }
    });
}

function refresh_search(){
    refresh_streams()
    // refresh_djs()
}

window.onload = refresh_search;
window.setInterval(refresh_streams,10000); 
// window.setInterval(refresh_djs, 10000); 