let config = {
    "processing": true,
    "serverSide": true,
    "fixedHeader": true,
    "pageLength": 25,
    "ajax": AJAX_URL,
    "order": [[ 0, "asc" ]],
    "columnDefs": [
        { "orderable": false, "searchable": false,  "targets": [2, 3, 4, 5] },
        { "orderable": true, "searchable": true,  "targets": [1] },
        { "orderable": true, "searchable": false,  "targets": [0] },
    ],
}


$( document ).ready(function() {
    $(".dataTable").on('click','.btn-ajax', function () {
        $.ajax({
            url: $(this).attr('data-link'),
            success: function(result){
                $(`.${result['id']}`).html(result['html']);
            }
        });
    });
});
