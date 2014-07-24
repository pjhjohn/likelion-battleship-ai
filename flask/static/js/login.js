

$(document).ready(function(){


	$('form#form-join').submit(function(data){
		join($(this));
		return false;
	});

	$('form#form-login').submit(function(data){
		login($(this));
		return false;
	});

	$(document).on('click','#btn-sign-up',function(){
		$('#form-login').fadeOut(200,function(){
			$('#form-join').fadeIn(200,function(){
				$(this).find('input:first-child').focus();
			});
		});
		return false;
	});

	$(document).on('click','#btn-sign-in',function(){
		$('#form-join').fadeOut(200,function(){
			$('#form-login').fadeIn(200,function(){
				$(this).find('input:first-child').focus();
			});
		});
		return false;
	});
});


function join(form){
	$.post(
		'join',
		form.serialize(),
		function(data){
			alert(data);
		});
}

function login(form){
	$.post(
		'login_submit',
		form.serialize(),
		function(data){
			if(data == '0'){
				location.reload();
			}else{
				show_toast("Failed to sign in","error");
			}
		});
}