$(document).ready(function(){
	$(document).on('click','button#code-submit',submit_code);
	$(document).on('change','input[type=radio][name=enemy-type]',function(){
		if ($(this).val()=='custom') $('textarea[name=code-enemy]').removeAttr('disabled');
		else $('textarea[name=code-enemy]').attr('disabled','disabled');
	});

	$(document).on('submit','form.container',function(){
		if($("#code-test").val()==''){
			show_toast("Please write your code", 'warning');
			$("#code-test").focus();
			return false;
		}
		if(!$("#code-enemy").attr('disabled') && $("#code-enemy").val() == '') {
			show_toast("Please write enemy code", 'warning');
			$("#code-enemy").focus();
			return false;
		}
		run_test($(this).serialize());
		return false;
	});
});

function run_test(data){
	show_progress();
	$("#btn-form-submit").attr('disabled','disabled');
	$.post(
		'/run_test',
		data,
		function(response){
			if (response == '1') {
				show_toast('You have to place ship first','error');
				return false;
			}
			var log = $.parseJSON(response);
			var lastLog = log['history'][log['history'].length-1];

			if (lastLog['player'] == 1) {
				if (!lastLog['sink']) {
					if (between (lastLog["guess"]["x"], 0, 9) && between(lastLog["guess"]["y"],0,9)) {
						show_toast("You shoot same point twice","error");
					} else {
						show_toast("You shoot out of board","error")
					}
				} else {
					show_toast('You win','success');
				}

			} else {
				show_toast('You lose','warning');
			}

			show_confirm('Do you want to visualize this battle?','default',function(check){
				if (check) {
					$('body').append('<form id="form-visualize" action="/visualize" method="post" target="_blank"><textarea name="log" id="" cols="30" rows="10">'+response+'</textarea></form>');
					$("#form-visualize").submit();
					$("#form-visualize").remove();
				}
			});
		}
	).always(function(){
		hide_progress();
		$("#btn-form-submit").removeAttr('disabled');

	}).fail(function(xhr, status, error){
		show_toast('Python syntax error or other exception','error');
		//var errorWindow = window.open("", '_blank');
		//errorWindow.document.write(xhr.responseText);
	});
}

function submit_code(){
	show_progress();
	$("#code-submit").attr('disabled','disabled');

	if ($('textarea#code-test').val()=='') return false;

	$.post(
		'submit_code',
		{
			new:$('textarea#code-test').val()
		},
		function onSuccessSubmit(data) {
			if (data == '0') show_toast('Code submitted','success');
			else show_toast('Failed to submit code','error');
		}
	).always(function(){
		hide_progress();
		$("#code-submit").removeAttr('disabled');
	});
}

function between(x, min, max) {
	return x >= min && x <= max;
}