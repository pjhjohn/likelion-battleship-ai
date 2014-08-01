$(document).ready(function(){
    $("#btn-new-league").click(function(){
        new_league();
    });

    $(document).on('click','.btn-show-battle-results',function(){
        show_battle_list($(this).parent().data('leagueId'), $(this).data('winnerId'), $(this).text().split(" ")[0]);

        return false;
    });


});


function new_league(){
    show_progress();
    $.post(
        '/league',
        function onSuccess(data){
            if (data=='0') {
                location.href="/admin/ranking";
            } else {
                show_toast('Failed to start new league','error');
            }
        }
        ).always(function(){
            hide_progress();
        });
}

function show_battle_list(leagueId, winnerId, winnerMembers) {
    console.log(winnerMembers);
    show_progress();
    $.post(
        '/get_battle_list',
        {
            'leagueId':leagueId,
            'winnerId':winnerId
        },
        function(response) {
            var jsonData = $.parseJSON(response);
            $("#battle-result-list .modal-title").text(winnerMembers);
            var tbody = $("#battle-result-list .modal-body table tbody").empty();
            for ( var i in jsonData ) {
                tbody.append('<tr><td>'+jsonData[i]['teamMembers1']+'</td><td>'+jsonData[i]['teamMembers2']+'</td><td><span class="label '+(jsonData[i]['winnerId'] == winnerId? 'label-success' : 'label-warning')+'">'+(jsonData[i]['winnerId'] == winnerId? 'Win' : 'Lose')+'</span></td><td><a href="/visualize/'+jsonData[i]['ID']+'" target="_blank" class="btn btn-info btn-xs">Visualize</a></td></tr>');
            }
            $("#battle-result-list").modal('show');
        }

        ).always(function(){
            hide_progress();
        });

}