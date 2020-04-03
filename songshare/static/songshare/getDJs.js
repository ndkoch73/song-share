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


function updateDJs(posts, comments) {
    // var counterposts = 0;
    // var poo =  (posts.posts).length;
    // console.log(posts.posts);
    // var me = 0;
    for (var i = 0; i < poo; i++){
        var x = i+1;

        var my_id = "id_post_text_" + x;
        var countercomments = 0;
        // console.log(posts.posts, posts.posts.length, my_id);
        if (document.getElementById(my_id) == null ) 
        {
            var dateobj = new Date(posts.posts[i].creation_time);


            $("#id_dj_search").prepend( 
                '<tr><td><ol id="comment-list' + x + '"'+
                '</ol></td> </tr>' + 
                '<tr><td>' + '\n'
                + '<form method="post" action="/socialnetwork/add-comment'+  x + '/global">' +
                '<label>Comment on post:</label>' +
                '<input id="id_comment_input_text_'+ x + '" ' +
                'type="text" name="comment">'+
                '<input type="hidden" name="csrfmiddlewaretoken" value="' + getCSRFToken() +'">' +
                '<button id="id_comment_button_' + x  +'"' +
                x  + ')">Comment</button>' +
                '<span id="error" class="error"></span>' +
                '</form>'+
                '</td></tr>') 
            $("#post-list").prepend( 
                '<tr> <td>' +
                '<span id="id_post_text_' + x + '">' +
                    sanitize(posts.posts[i].post_input_text) + ' post by </span>' +
                    '<a href=\"/socialnetwork/profile-view:' + 
                    posts.posts[i].created_by + '\"' +
                    ' id=id_post_profile_' + x + 
                    '>' +posts.posts[i].p_first_name +' ' 
                    + posts.posts[i].p_last_name+ '</a>'+
                    '-- <span style="font-style: italic;" '+
                    'id=id_post_date_time_' + x + '>' +
                    dateobj.toISOString() + '</span>'
                     +
                '</td> </tr>')
        }
           

    }
    


    var countercomments = 0 
    for (var i = 0; i < posts['comments'].length; i++){
                c = i + 1;
                post_id = posts.comments[i].post_id
                c_id = "id_comment_text_" + c;
                if (document.getElementById(c_id) == null)
                {
                    var dateobj = new Date(posts.comments[i].comment_time);
                    $("#comment-list" + post_id).append(
                    '<tr> <td>' +
                    '<span id="id_comment_text_' + c + '">' +
                    sanitize(posts.comments[i].comment_text) + ' comment by </span>' +
                    '<a href=\"/socialnetwork/profile-view:' + 
                    posts.comments[i].user_id + '\"' +
                    ' id=id_comment_profile_' + c + 
                    '>' + posts.comments[i].c_first_name + ' ' + 
                    posts.comments[i].c_last_name + '</a>'+
                    '-- <span style="font-style: italic;" '+
                    'id=id_comment_date_time_' + c + '>' +
                    dateobj.toISOString() + '</span>'
                     + '</td> </tr>'
                    )
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

function addComment(id) {
    var commentTextElement = $("#id_comment_input_text_"+id);
    var commentTextValue   = commentTextElement.val();

    // Clear input box and old error message (if any)
    commentTextElement.val('');
    displayError('');

    $.ajax({
        url: "/socialnetwork/add-comment"+id,
        type: "POST",
        data: "comment="+commentTextValue+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: function(response) {
            if (Array.isArray(response)) {
                updatePosts(response);
            } else {
                displayError(response.error);
            }
        }
    });
}



// The index.html does not load the list, so we call getList()
// as soon as page is finished loading
window.onload = getPosts;

// causes list to be re-fetched every 5 seconds
window.setInterval(getPosts, 5000);