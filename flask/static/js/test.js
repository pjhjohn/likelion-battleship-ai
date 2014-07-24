$(document).ready(function(){


	$(document).on('click','button#code-submit',submit_code);

	$(document).on('change','input[type=radio][name=enemy-type]',function(){
		if ($(this).val()=='custom'){
			$('textarea[name=code-enemy]').removeAttr('disabled');
		} else {
			$('textarea[name=code-enemy]').attr('disabled','disabled');
		}
	});
});


function submit_code(){
	if ($('textarea#code-test').val()=='') return false;
	$.post('submit_code',{
		new:$('textarea#code-test').val()
	},
	function onSuccessSubmit(data) {
		if (data == '0') {
			show_toast('Code submitted','success');
		} else {
			show_toast('Failed to submit code','error');
		}
	});
}