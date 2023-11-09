/*
 Template Name: Dashor - Responsive Bootstrap 4 Admin Dashboard
 Author: Themesdesign
 Website: www.themesdesign.in
 File: Datatable js
 */

$(document).ready(function() {
    $('#datatable').DataTable();

    //Buttons examples
    var table = $('#datatable-buttons').DataTable({
        lengthChange: false,
        "bFilter": false,
        "bInfo": false,
        "language":
                {
                    "url": "//cdn.datatables.net/plug-ins/1.11.5/i18n/tr.json"
                }
    });

    table.buttons().container()
        .appendTo('#datatable-buttons_wrapper .col-md-6:eq(0)');

    $(document).ready(function() {
        $('#datatable2').DataTable();
    } );
} );

