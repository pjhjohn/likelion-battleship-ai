var color = {
    default:'#28324E',
    warning:'#f37934',
    error:'#b8312f',
    success:'#2969b0'
};


function show_confirm(message, level, callback, autohide,  tagId){

    autohide = autohide||true;
    level = level||'default';
    tagId = tagId||'confirm';
    if($('#'+tagId).length > 0) {
        return false;
    }

    $("body").append('<div id="'+tagId+'" style="line-height:2em;padding:10px;position:fixed;z-index:9999;right:20px;top:20px;border-radius:5px;background:'+color[level]+';color:white;font-weight:bold;display:none;box-shadow:0px 0px 2px 2px rgb(100,100,100);">'+message+'<br><div class="pull-right"><button type="button" class="btn btn-default btn-sm btn-cancel">Cancel</button>&nbsp;<button type="button" class="btn btn-primary btn-sm btn-ok">Ok</button></div></div>');

    
    $("#"+tagId).find(".btn-cancel").click(function(){
        if(callback) callback(false);
        $("#"+tagId).fadeOut(300,function(){
            $("#"+tagId).remove();
        });
    });

    $("#"+tagId).find('.btn-ok').click(function(){
        if(callback) callback(true);
        $("#"+tagId).fadeOut(300,function(){
            $("#"+tagId).remove();
        });
    });
    

    $("#"+tagId)
        .fadeIn(300);

    if(autohide){
        setTimeout('$("#'+tagId+'").fadeOut(300,function(){$("#'+tagId+'").remove(); });',3000);
    }

}