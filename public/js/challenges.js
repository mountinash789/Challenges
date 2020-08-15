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
        { "responsivePriority": 1, "targets": [1, 5] },
    ],
    "initComplete": function(settings, json) {
        $('.btn-ajax').click(function(){
            $.ajax({
                url: $(this).attr('data-link'),
                success: function(result){
                    $(`#${result['id']}`).html(result['html']);
                }
            });
        });
    },
}