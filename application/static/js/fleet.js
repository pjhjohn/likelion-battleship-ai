var is_initialized  = false;
var is_horizontal   = true;
var is_running      = false;
var ship_size       = [2,3,4,5];
var remaining_ships = [1,2,1,1];
var deployment_code = 0;
var current_ship_type = 0;
var current_cell;

$(document).ready(function(){
	$("#modal-submit-deployment").on('shown.bs.modal',function(){
		if (is_initialized) return;
		is_initialized = true;
		$(this).find('table.fleet-deployment td').css('height',$('table.fleet-deployment td').width());
	});

	$("#deployment-list table.fleet-deployment td").css('height', $("#deployment-list table.fleet-deployment td").width());

	$(document).on('change','input[name=ship_type]', function onShipTypeChanged(){
		current_ship_type = $(this).val();
		$(this).blur();
	});

	$(document).on('click','table.fleet-deployment.editable td', function onCellClicked(){
		if (current_cell.hasClass('active') && !current_cell.hasClass('error') && !current_cell.hasClass('deployed') && remaining_ships[current_ship_type]>0) {
			$('table.fleet-deployment.editable td.active')
			.data('ship_type',current_ship_type)
			.data('is_horizontal',is_horizontal)
			.data('deployment_code',deployment_code)
			.addClass('deployed')
			.removeClass('active');
			deployment_code++;

			remaining_ships[current_ship_type]--;
			if (remaining_ships[current_ship_type]==0) $('#ship'+current_ship_type).attr('disabled','disabled');
			$('label[for=ship'+current_ship_type+']').find('.remaining_ship_count').text(remaining_ships[current_ship_type]);
			$(this).addClass('start_point');
		}
	});

	$(document).on('mouseenter','table.fleet-deployment.editable td', function onMouseEnter(){
		current_cell = $(this);

		var row = $(this).parent().data('row');
		var col = $(this).data('col')
		var error = false;
		for (var i = 0; i<ship_size[current_ship_type];i++) {
			if (is_horizontal) {
				var target = $(this).parent().find('[data-col='+(col+i)+']');
				if (target.length == 0 || target.hasClass('deployed')) error = true;
				else target.addClass('active')
			} else {
				var target = $(this).parent().parent().find('[data-row='+(row+i)+']').find('[data-col='+col+']');
				if (target.length == 0 || target.hasClass('deployed')) error = true;
				else target.addClass('active')
			}
		}
		if (remaining_ships[current_ship_type]<=0) error = true;
		if (error) $('table.fleet-deployment td.active').addClass('error');
		$(this).addClass('active');
	});

	$(document).on('mouseleave','table.fleet-deployment.editable td',function onMouseLeave(){
		$('table.fleet-deployment td.active').removeClass('active');
		$('table.fleet-deployment td.error').removeClass('error');
	});

	$(document).on('keydown',function onKeyDown(e){
		if (e.which == 82/* r */) {
			is_horizontal = !is_horizontal;
			if ( typeof current_cell !== 'undefined' ) {
				current_cell.mouseleave();
				current_cell.mouseenter();
			}
		} else if (e.which == 88/* x */) {
			var fleet_code = current_cell.data('deployment_code');
			var removedship_type = current_cell.data('ship_type');
			//console.log(removedship_type);
			$('table.fleet-deployment.editable td.deployed').each(function(){
				if ($(this).data('deployment_code') == fleet_code){
					$(this).removeClass('deployed');
					$(this)
					.removeClass('start_point')
					.removeData('ship_type')
					.removeData('is_horizontal')
					.removeData('deployment_code');
				}
			});

			current_cell.mouseleave();
			current_cell.mouseenter();
			remaining_ships[removedship_type]++;
			$('#ship'+removedship_type).removeAttr('disabled');
			$('label[for=ship'+removedship_type+']').find('.remaining_ship_count').text(remaining_ships[removedship_type]);

		} else if ( e.which == 192 || e.which == 48 ) {
			$('#ship0').click();
			current_cell.mouseleave();
			current_cell.mouseenter();
		} else if ( e.which >= 49 && e.which <= 52 ) {
			$('#ship'+(e.which-48)).click();
			current_cell.mouseleave();
			current_cell.mouseenter();
		}
	});

	$(document).on('submit','#modal-submit-deployment form', function onSubmitDeployment(){
		var sum = 0;
		for (var i in remaining_ships) sum += remaining_ships[i];
		if (sum > 0) {
			show_toast('You have to deploy all ships','warning');
			return false;
		}
		if (is_running) return false;
		show_progress();
		is_running = true;
		var data = [];
		$(this)
		.find('table.fleet-deployment.editable td.start_point')
		.each(function(){
			data.push({
				location : {
					y : $(this).data('col'),
					x : $(this).parent().data('row')
				},
				size : ship_size[$(this).data('ship_type')],
				direction : $(this).data('is_horizontal')? 'y' : 'x'
			});
		});
		data = JSON.stringify(data);
		$.post('submit_fleet', {'deployment' : data}, function(data){
			if (data == '0') location.reload();
			else			 show_toast('Failed to submit','error');
			is_running = false;
		}).always(function(){
			hide_progress();
		});
		return false;
	});
});