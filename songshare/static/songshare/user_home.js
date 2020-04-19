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

}