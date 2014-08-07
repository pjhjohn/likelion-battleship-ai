$(document).ready(function(){
	$('form#form-join').submit(function(data) {
		return join($(this));
	});

	$('form#form-login').submit(function(data) {
		return login($(this));
	});

	$("#btn-add-member").click(function(){
		$('#form-members').append('<br><input type="text" class="form-control members" name="members'+($("input.members").length+1)+'" placeholder="NAME">');
		if ($('input.members').length > 2) $(this).remove();
		$('input.members:last-child').focus();
	});
});

function join(form) {
	if ($('#form-join [name="password"]').val()!=$('[name="password-confirm"]').val()) {
		show_toast("Password not matched", "warning");
		$('#form-join [name="password"]').select();
		return false;
	}

	show_progress();
	$.post('join', form.serialize(), function(response){
		if (response == '0') {
			show_toast("Successfully signed up","success");
			$("#form-join input").val('');
			$("a[href='#sign-in']").click();
		} else show_toast("Failed to sign up","error");
	}).always(function(){
		hide_progress();
	});
	return false;
}

function login(form) {
	show_progress();
	$.post( 'login_submit', form.serialize(), function(data){
		if(data == '0') location.reload();
		else show_toast("Failed to sign in", "error");
	}).always(function(){
		hide_progress();
	});
	return false;
}