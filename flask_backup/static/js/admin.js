var teamList;

$(document).ready(function(){


    $(document).on('click','#btn-add-league',function(){
        var groupSize = Number(prompt('Enter league group size'));
        if (groupSize) {
            create_group(groupSize);
        }
    });
});


function create_group(groupSize){
    console.log(groupSize);
}

function get_team_list(){
    
}