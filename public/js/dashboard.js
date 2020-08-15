$( document ).ready(function() {
    $('.load_content').each(function (index, item){
        let url = $(item).attr('data-url');
        if (url.length > 0){
            $.ajax({
                url: url,
                data: {'id': $(item).attr('id')},
                success: function(result){
                    $(`#${result['id']}`).html(result['html']);
                }
            });
        }

    })
});