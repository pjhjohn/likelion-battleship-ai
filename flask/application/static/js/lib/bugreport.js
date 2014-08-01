$(document).ready(function(){
 $('body').append('<!-- Modal -->\
    <div class="modal fade" id="modal-bug-report" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\
    <div class="modal-dialog">\
    <div class="modal-content">\
    <div class="modal-header">\
    <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>\
    <h4 class="modal-title" id="myModalLabel">Bug Report</h4>\
    </div>\
    <div class="modal-body">\
        <form action="" id="form-bug-report"><input type="text" name="title" class="form-control" placeholder = "TITLE" /><br><textarea name="body"  cols="30" rows="10" class="form-control"></textarea></form>\
    </div>\
    <div class="modal-footer">\
    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\
    <button type="button" id="btn-bug-report" class="btn btn-primary">Submit</button>\
    </div>\
    </div>\
    </div>\
    </div>');

    $("#form-bug-report").submit(function(){
        return false;
    })

    $("#btn-bug-report").click(function(){
        show_progress();
        var data = $('#form-bug-report').serialize();
        $.post('/bugreport',data,function(response){
            if (response == '0') {
                show_toast('Submitted','success');
                $("#form-bug-report input, #form-bug-report textarea").val('');
                $("#modal-bug-report").modal('hide');
            } else {
                show_toast('Error','error');
            }
        }).fail(function(){
            show_toast('Error','error');
        }).always(function(){
            hide_progress();
        });
    });

    $(document).on('keydown',function(e){
        if (e.which == 66 && e.ctrlKey) {
            $("#modal-bug-report").modal('show');
        }
    });
});