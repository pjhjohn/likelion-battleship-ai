var color = {
    default:'#28324E',
    warning:'#f37934',
    error:'#b8312f',
    success:'#2969b0'
};

function show_confirm(message, level, callback, autohide,  tag_id){
    autohide= autohide||false 
    level   =    level||'default';
    tag_id  =   tag_id||'confirm';
    if($('#'+tag_id).length > 0) return false;

    $("body").append('<div id="'+tag_id+'" style="line-height:2em;padding:10px;position:fixed;z-index:9999;right:20px;top:20px;border-radius:5px;background:'+color[level]+';color:white;font-weight:bold;display:none;box-shadow:0px 0px 2px 2px rgb(100,100,100);">'+message+'<br><div class="pull-right"><button type="button" class="btn btn-default btn-sm btn-cancel">Cancel</button>&nbsp;<button type="button" class="btn btn-primary btn-sm btn-ok">Ok</button></div></div>');
    $("#"+tag_id).find(".btn-cancel").click(function(){
        if(callback) callback(false);
        $("#"+tag_id).fadeOut(300,function(){
            $("#"+tag_id).remove();
        });
    });
    $("#"+tag_id).find('.btn-ok').click(function(){
        if(callback) callback(true);
        $("#"+tag_id).fadeOut(300,function(){
            $("#"+tag_id).remove();
        });
    });
    $("#"+tag_id).fadeIn(300);
    if(autohide) setTimeout('$("#'+tag_id+'").fadeOut(300,function(){$("#'+tag_id+'").remove(); });', 3000);
}