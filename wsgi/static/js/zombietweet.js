$(function() {
    /* false buttons in dashboard */

    $('.running-el').live('click', function(){
        window.location = '/show/'+$(this).data('id');
    });

    $('.schedule-el').live('click', function(){
        window.location = '/show/'+$(this).data('id');
    });

    $('.btn-following').each(function(){
        checkFollowers(this);
    });

    $('.btn-following').on('click', function(){
        if ($(this).data('action') == 'follow'){
            url = '/user/relate';
        }else{
            url = '/user/unrelate';
        }

        $.ajax({
            context: this,
            type: "POST",
            url: url,
            data: JSON.stringify({username: ''+$(this).data('userid')+''}),
            contentType: "application/json",
            dataType: "json",
            success: function(data){
                newstat = checkFollowers(this);
            },
            failure: function(errMsg) {
                console.log(errMsg);
            }
        });
    });

    // data getters
    if($('.userprofile-head').data('username')){
        //getFromTwitter($('.userprofile-head').data('username'));
        //getFollowing($('.userprofile-head').data('username'));
        applyVague($('.head-background'));
    }

    $('.user-form').on('sumit', function(){
        alert('ciao');
    });

});


function checkFollowers(el){
    console.log("Running checkFollowers for " + $(el).data('userid'));
    $.ajax({
        context: el,
        type: "POST",
        url: "/user/checkFollowing",
        data: JSON.stringify({username: ''+$(el).data('userid')+''}),
        contentType: "application/json",
        dataType: "json",
        success: function(data){
            if (data.label == 'Unfollow'){
                icon = "<i class='glyphicon glyphicon-remove'></i> ";
            }else{
                icon = "<i class='glyphicon glyphicon-plus'></i>";
            }
            $(el).html(icon+data.label);
            $(el).data('action', data.action);
        },
        failure: function(errMsg) {
            console.log(errMsg);
        }
    });
}

function getFromTwitter(username){
    console.log('getFromTwitter for '+username);

    $.ajax({
        context: this,
        type: "POST",
        url: '/user/get_from_twitter',
        data: JSON.stringify({username: ''+username+''}),
        contentType: "application/json",
        dataType: "json",
        success: function(data){
            console.log(data);
            $('#description').html(data.response.description);
            $('.userprofile-head').css('background-color', '#'+data.response.head_color);
            $('.userprofile-head').css('background-image', 'url('+data.response.head_bg+')');
        },
        failure: function(errMsg) {
            console.log(errMsg);
        }
    });
}


function applyVague(item){
    // ̦test item use
    var vague = item.Vague({intensity:50});
    vague.blur();
}
