var initialized = false;
var isHorizontal = true;
var currentShipType = 0;
var shipSizes = [2,3,4,5];
var remainShips = [1,2,1,1];
var currentCell;
var placementCode = 0;
var running = false;

$(document).ready(function(){



    $("#modal-submit-placement").on('shown.bs.modal',function(){
        if (!initialized) {
            $(this).find('table.ship-placement td').css('height',$('table.ship-placement td').width());
            initialized = true;
        }
    });

    $("#placement-list table.ship-placement td").css('height',$("#placement-list table.ship-placement td").width());

    $(document).on('change','input[name=shipType]',function onShipTypeChanged(){
        currentShipType = $(this).val();
        $(this).blur();
    });

    $(document).on('click','table.ship-placement.editable td',function onCellClicked(){
        if (currentCell.hasClass('active') && !currentCell.hasClass('error') && remainShips[currentShipType]>0) {
            $('table.ship-placement.editable td.active')
            .data('shipType',currentShipType)
            .data('isHorizontal',isHorizontal)
            .data('placementCode',placementCode)
            .addClass('placed')
            .removeClass('active');
            placementCode++;

            remainShips[currentShipType]--;
            if (remainShips[currentShipType]==0) {
                $('#ship'+currentShipType).attr('disabled','disabled');
            }

            $('label[for=ship'+currentShipType+']').find('.remainShipCount').text(remainShips[currentShipType]);

            $(this).addClass('startPoint');
        }
    });

    $(document).on('mouseenter','table.ship-placement.editable td',function onMouseEnter(){
        //$('table.ship-placement td.active').removeClass('active');
        //$('table.ship-placement td.error').removeClass('error');
        currentCell = $(this);

        var row = $(this).parent().data('row');
        var col = $(this).data('col')
        var error = false;
        for (var i = 0; i<shipSizes[currentShipType];i++) {
            if (isHorizontal) {
                var target = $(this).parent().find('[data-col='+(col+i)+']');
                if (target.length == 0 || target.hasClass('placed')){
                    error = true;
                    
                }else{
                    target.addClass('active')
                }

            } else {
                var target = $(this).parent().parent().find('[data-row='+(row+i)+']').find('[data-col='+col+']');
                if (target.length == 0 || target.hasClass('placed')){
                    error = true;
                    
                }else{
                    target.addClass('active')
                }
            }
        }
        if (remainShips[currentShipType]<=0){
            error = true;
            
        }
        if (error) {
            $('table.ship-placement td.active').addClass('error');
        }

        $(this).addClass('active');
    });
    $(document).on('mouseleave','table.ship-placement.editable td',function onMouseLeave(){
        $('table.ship-placement td.active').removeClass('active');
        $('table.ship-placement td.error').removeClass('error');
    });

    $(document).on('keydown',function onKeyDown(e){
        if ( (e.which >= 37 && e.which <= 40) || e.which == 82 ) {
            isHorizontal = !isHorizontal;
            if ( typeof currentCell !== 'undefined' ) {
                currentCell.mouseleave();
                currentCell.mouseenter();
            }
        } else if (e.which == 88) {
            var pCode = currentCell.data('placementCode');
            var removedShipType = currentCell.data('shipType');
            console.log(removedShipType);
            $('table.ship-placement.editable td').each(function(){
                if ($(this).data('placementCode') == pCode){
                    $(this).removeClass('placed');
                    $(this)
                    .removeClass('startPoint')
                    .removeData('shipType')
                    .removeData('isHorizontal')
                    .removeData('placementCode');
                }
            });

            currentCell.mouseleave();
            currentCell.mouseenter();

            remainShips[removedShipType]++;

            $('#ship'+removedShipType).removeAttr('disabled');


            $('label[for=ship'+removedShipType+']').find('.remainShipCount').text(remainShips[removedShipType]);

        } else if ( e.which == 192 || e.which == 48 ) {
            $('#ship0').click();
            currentCell.mouseleave();
            currentCell.mouseenter();

        } else if ( e.which >= 49 && e.which <= 52 ) {
            $('#ship'+(e.which-48)).click();
            currentCell.mouseleave();
            currentCell.mouseenter();
        }
    });

    $(document).on('submit','#modal-submit-placement form',function onSubmitPlacement(){
        var sum = 0;
        for (var i in remainShips) {
            sum += remainShips[i];
        }




        if (sum > 0) {
            
            show_toast('You have to place all ships','warning');
            return false;
        }

        if (running) {
            return false;
        }
        $('body').append('<div class="progress" id="progress-ship-submit" style="position:fixed;top:0px;z-index:9999;width:100%;"><div class="progress-bar progress-bar-success progress-bar-striped active" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width:100%;"></div></div>');
        running = true;
        var data = [];
        $(this)
            .find('table.ship-placement.editable td.startPoint')
            .each(function(){
                data.push({
                    location:{
                        x:$(this).data('col'),
                        y:$(this).parent().data('row')
                    },
                    size:shipSizes[$(this).data('shipType')],
                    direction:$(this).data('isHorizontal')?'x':'y'
                });
            });
        data = JSON.stringify(data);
        $.post('submit_placement',{"placement":data},function(data){
                if (data == '0') location.reload();
                else {
                    show_toast('Failed to submit','error');
                    $("#progress-ship-submit").remove();
                }
                running = false;


        });

        return false;
    });

});