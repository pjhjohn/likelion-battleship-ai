function show_progress(progressClass, progressId){
    progressId = progressId||"progress";
    progressClass = progressClass||'success';
    if ($('#progress').length==0) {
        $('body').append('<div class="progress" id="'+progressId+'" style="position:fixed;top:0px;z-index:9999;width:100%;"><div class="progress-bar progress-bar-'+progressClass+' progress-bar-striped active" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width:100%;"></div></div>');    
        
    }
    
}


function hide_progress(progressId){
    progressId = progressId||'progress';
    $("#"+progressId).remove();
}