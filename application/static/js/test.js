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
function with_toast(message) {
	show_toast(message);
	return false;
}
var dec_digit = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
function run_test(data){
	show_progress();
	$("#btn-form-submit").attr('disabled','disabled');

	// run_test gives back battle result
	$.post('/run_test', data, function(_response_){
		var response = $.parseJSON(_response_);
		if(response[   'my_error'] != 0) return with_toast('ERROR WITH PLAYER1 : ' + response[  'my_error_msg']);
		if(response['enemy_error'] != 0) return with_toast('ERROR WITH PLAYER2 : ' + response['enemy_error_msg']);
		if(response[ 'game_error'] != 0) return with_toast(response['game_error_msg']);
		// response['my_error'] == response['enemy_error'] == response['game_error'] = 0(False)
		console.log(response)
		game_history = response['game_log']['history'];
		latest_log = game_history[game_history.length - 1];
		if (latest_log['player'] == 1){
			if (!latest_log['sink']) {
				if (latest_log['guess']['x'] in dec_digit && latest_log['guess']['y'] in dec_digit) show_toast("You shoot same point twice","error");
				else show_toast('You shoot out of board', 'error');
			} else show_toast('You Win!', 'success');
		} else show_toast('You Lose', 'warning')

		show_confirm('Do you want to visualize this battle?', 'default', function(check) {
			if (check) {
				$('body').append('<form id="form-visualize" action="/visualize" method="post" target="_blank"><textarea name="log" id="" cols="30" rows="10">'
					+ JSON.stringify(response['game_log'])
					+ '</textarea></form>');
				$("#form-visualize").submit();
				$("#form-visualize").remove();
			}
		});
	}).always(function(){
		hide_progress();
		$("#btn-form-submit").removeAttr('disabled');
	}).fail(function(xhr, status, error){
		console.log(xhr)
		console.log(status)
		console.log(error)
		show_toast('Error Has Occured from Server', 'error');
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