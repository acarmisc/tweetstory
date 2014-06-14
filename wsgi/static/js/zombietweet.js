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
            $(el).html(data.label);
            $(el).data('action', data.action);
        },
        failure: function(errMsg) {
            console.log(errMsg);
        }
    });
}