$(function() {
    /* false buttons in dashboard */

    $('.running-el').live('click', function(){
        window.location = '/show/'+$(this).data('id');
    });

    $('.schedule-el').live('click', function(){
        window.location = '/show/'+$(this).data('id');
    });

});

