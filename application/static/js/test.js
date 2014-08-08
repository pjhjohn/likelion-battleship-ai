$(document).ready(function(){
	$(document).on('click','button#code-submit', submit_code);

	$(document).on('change','input[type=radio][name=enemy_type]',function(){
		if ($(this).val()=='custom') $('textarea[name=enemy_code]').removeAttr('disabled');
		else $('textarea[name=enemy_code]').attr('disabled','disabled');
	});

	$(document).on('submit','form.container', function(){
		if($("#test_code").val()==''){
			show_toast("Please write your code", 'warning');
			$("#test_code").focus();
			return false;
		}
		if(!$("#enemy_code").attr('disabled') && $("#enemy_code").val() == '') {
			show_toast("Please write enemy code", 'warning');
			$("#enemy_code").focus();
			return false;
		}
		run_test($(this).serialize());
		return false;
	});
});

var dec_digit = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
function run_test(data){
	show_progress();
	$("#btn-form-submit").attr('disabled','disabled');

	// run_test gives back battle result
	$.post('/run_test', data, function(response){
		if (response == '1') {
			show_toast('You have to place ship first', 'error');
			return false;
		}
		var log = $.parseJSON(response);
		if (log['my_error'] != 0) {
			show_toast('ERROR WITH PLAYER1\n' + log['my_error_msg']);
			return false;
		} else if(log['enemy_error'] != 0) {
			show_toast('ERROR WITH PLAYER2\n' + log['enemy_error_msg']);
			return false;
		} else if(log['game_error'] != 0) {
			show_toast('ERROR DURING GAME\n' + log['game_error_msg']);
			return false;
		} else {
			latest_log = log['game_log']['history'][log['game_log']['history'].length - 1];
			if (latest_log['player'] == 1) {
				if (!latest_log['sink']) {
					if (latest_log['guess']['x'] in dec_digit && latest_log['guess']['y'] in dec_digit) show_toast("You shoot same point twice","error");
					else show_toast("You shoot out of board","error")
				} else show_toast('You win','success');
			} else show_toast('You lose','warning');

			show_confirm('Do you want to visualize this battle?','default',function(check){
				if (check) {
					console.log(log['game_log'])
					$('body').append('<form id="form-visualize" action="/visualize" method="post" target="_blank"><textarea name="log" id="" cols="30" rows="10">'
						+ JSON.stringify(log['game_log'])
						+ '</textarea></form>');
					$("#form-visualize").submit();
					$("#form-visualize").remove();
				}
			});
		}
	}).always(function(){
		hide_progress();
		$("#btn-form-submit").removeAttr('disabled');
	}).fail(function(xhr, status, error){
		show_toast('Python syntax error or other exception','error');
	});
}

function submit_code(){
	show_progress();
	$("#code-submit").attr('disabled','disabled');
	if ($('textarea#test_code').val()=='') return false;

	$.post('submit_code', { new : $('textarea#test_code').val() }, function onSuccessSubmit(data) {
		if (data == '0') show_toast('Code submitted','success');
		else show_toast('Failed to submit code','error');
	}).always(function(){
		hide_progress();
		$("#code-submit").removeAttr('disabled');
	});
}