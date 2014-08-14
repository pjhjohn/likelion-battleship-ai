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
			if (data=='0') location.href="/admin/ranking";
			else show_toast('Failed to start new league','error');
		}
	).always(function(){
		hide_progress();
	});
}

function show_battle_list(league_id, winner_id, winner_members) {
	console.log(winner_members);
	show_progress();
	$.post(
		'/get_battle_list',
		{
			'league_id':league_id,
			'winner_id':winner_id
		},
		function(response) {
			var json_data = $.parseJSON(response);
			$("#battle-result-list .modal-title").text(winner_members);
			var tbody = $("#battle-result-list .modal-body table tbody").empty();
			for ( var i in json_data ) {
				tbody.append('<tr><td>'+json_data[i]['member1']+'</td><td>'+json_data[i]['member2']+'</td><td><span class="label '+(json_data[i]['winner_id'] == winner_id? 'label-success' : 'label-warning')+'">'+(json_data[i]['winner_id'] == winner_id? 'Win' : 'Lose')+'</span></td><td><a href="/visualize/'+json_data[i]['ID']+'" target="_blank" class="btn btn-info btn-xs">Visualize</a></td></tr>');
			}
			$("#battle-result-list").modal('show');
		}
	).always(function(){
		hide_progress();
	});
}
