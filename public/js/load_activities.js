$( document ).ready(function() {

    $.ajax({
        url: GET_ACTIVITES_URL,
        success: function(result){
            $(`#${result['id']}`).html(result['html']);
        }
    });

});