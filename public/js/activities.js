let config = {
    "processing": true,
    "serverSide": true,
    "ajax": AJAX_URL,
    "order": [[ 2, "desc" ]],
    "columnDefs": [
        { "orderable": false, "searchable": false,  "targets": 5 }
    ],
    "initComplete": function(settings, json) {
        feather.replace();
    },
}