$(document).ready(function(){
    $("#btn-new-league").click(function(){
        new_league();
    });
});


function new_league(){
    show_progress();
    $.post(
        'league',
        function onSuccess(data){
            if (data=='0') {
                location.reload();
            } else {
                show_toast('Failed to start new league','error');
            }
        }
        ).always(function(){
            hide_progress();
        });
}

