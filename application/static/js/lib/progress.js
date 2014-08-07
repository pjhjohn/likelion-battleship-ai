function show_progress(progress_class, progress_id){
    progress_id = progress_id||"progress";
    progress_class = progress_class||'success';
    if ($('#progress').length==0) {
        $('body').append('<div class="progress" id="'+progress_id+'" style="position:fixed;top:0px;z-index:9999;width:100%;"><div class="progress-bar progress-bar-'+progress_class+' progress-bar-striped active" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width:100%;"></div></div>');    
        
    }
    
}

function hide_progress(progress_id){
    progress_id = progress_id||'progress';
    $("#"+progress_id).remove();
}