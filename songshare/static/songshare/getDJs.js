function getDJs() {
    //var last_refersh_cur_time = last_refresh_cur.setMilliseconds(last_ms-5000);
    $.ajax({
        // url: "/socialnetwork/get-posts-json",
        url: "/socialnetwork/refresh-page?last_refresh="+last_refresh,
        dataType : "json",
        success: updateDJs
    });
}


function sanitize(s) {
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}





function updateDJs(djs) {
    // var counterposts = 0;
    // var poo =  (posts.posts).length;
    var len_djs = djs.djs.length
    console.log(djs.djs);
    // var me = 0;
    for (var i = 0; i < len_djs; i++){
        var x = i+1;

        var my_id = "id_dj_search_" + djs.djs[i].pk;
        var live_id = "id_is_live_" + djs.djs[i].pk;
        var dj_cur_status = djs.djs[i].live;
        // console.log(posts.posts, posts.posts.length, my_id);
        document.getElementById(my_id) == null
        if (document.getElementById(live_id) == null && dj_cur_status) 
        {
            $("#"+my_id).attr
        }
        else if (document.getElementById(live_id) != null && !dj_cur_status) 
            $("#"+my_id).
        }
    }
    
}




// function addPost() {
//     var postTextElement = $("#id_post_input_text");
//     var postTextValue   = postTextElement.val();

//     // Clear input box and old error message (if any)
//     postTextElement.val('');
//     displayError('');

//     $.ajax({
//         url: "/socialnetwork/post-create",
//         type: "POST",
//         data: "post="+postTextValue+"&csrfmiddlewaretoken="+getCSRFToken(),
//         dataType : "json",
//         success: function(response) {
//             if (Array.isArray(response)) {
//                 updatePosts(response);
//             } else {
//                 displayError(response.error);
//             }
//         }
//     });
// }



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

function djSearch(name) {
    // var commentTextElement = $("#id_comment_input_text_"+id);
    // var commentTextValue   = commentTextElement.val();

    // // Clear input box and old error message (if any)
    // commentTextElement.val('');
    // displayError('');

    // $.ajax({
    //     url: "/socialnetwork/add-comment"+id,
    //     type: "POST",
    //     data: "comment="+commentTextValue+"&csrfmiddlewaretoken="+getCSRFToken(),
    //     dataType : "json",
    //     success: function(response) {
    //         if (Array.isArray(response)) {
    //             updatePosts(response);
    //         } else {
    //             displayError(response.error);
    //         }
    //     }
    // });

    var url = "{% url 'search-dj' 'QUERYPLACEHOLDER' %}".replace(
        'QUERYPLACEHOLDER', '{name}'
    )
    $('.ui.search').search({ 
        type          : 'standard',
        minCharacters : 2,              
        apiSettings   : {
            onResponse: function(response) {                        
                //DO Something
                return updateDJs(response);
            },
            url: url
        }       
    });
}

function refresh_streams(){
    $.ajax({
        url: window.location.pathname + "/refresh-streams",
        type: "GET",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: add_recently_played,
        error: function(response){
            console.log(response)
        }
    });
}


window.onload = refresh_streams;
window.setInterval(1000); 