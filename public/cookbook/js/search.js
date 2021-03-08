let config = {
    "dom": "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
           "<'row'<'col-sm-12'tr>>" +
           "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
    "processing": true,
    "serverSide": true,
    "fixedHeader": true,
    "pageLength": 25,
    "ajax": AJAX_URL,
    "order": [[ 1, "desc" ]],
    "columnDefs": [
        { "orderable": false, "searchable": false,  "targets": [0,2,4] },
    ],
    "initComplete": function(settings, json) {
    },
}
$(document).ready(function() {
    $('#id_tag_select').on('change',function(){
        AJAX_URL = `${BASE_URL}?${$('#id_tag_select').serialize()}`;
        $(`#${table_id}`).DataTable().ajax.url(AJAX_URL).load();
    });
} );