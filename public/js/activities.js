let config = {
    "dom": "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
           "<'row'<'col-sm-12'tr>>" +
           "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
    "processing": true,
    "serverSide": true,
    "fixedHeader": true,
    "pageLength": 25,
    "ajax": AJAX_URL,
    "order": [[ 2, "desc" ]],
    "columnDefs": [
        { "orderable": false, "searchable": false,  "targets": 5 }
    ],
    "initComplete": function(settings, json) {
    },
}
$(document).ready(function() {
    $('#id_activity_type_select').on('change',function(){
        var selectedValue = $(this).val();
        $(`#${table_id}`).dataTable().fnFilter(selectedValue)
    });
} );