// $(document).ready(function () {
//Evitar varios Submit/envios de formularios
$("button[type=submit]").click(function (e) {
    // var icono = '<i class="fa fa-spinner fa-spin"></i> ';
    var valor = $(this).text();
    var puntos = '...';
    $(this).addClass(" noevent");
    $(this).html(valor + puntos);
    // $(this).html(icono+valor);
    // e.preventDefault();
});

var activar_clase = function () {
    var url = window.location;
    var element = $("ul.nav a").filter(function () {
        return this.href == url;
    });
    if (element) {
        var p = "li:has(a[href='" + url.pathname + "'])";
        $(p).addClass('active treeview');
    }
};
activar_clase();
// $(".sidebar").click(function (e) {
//     activar_clase();
// });

// Limpiar los formularios al salir de un modal
$('.modal:has(input)').on('hidden.bs.modal', function () {
    $(this).find('form')[0].reset(); //para borrar todos los datos que tenga los input, textareas, select.
});

origin = window.location.origin;
url_dataTable = origin + "/static/plugins/datatables/spanish.json";
$('.datatable-active').DataTable({
    responsive: true,
    language: {
        "url": url_dataTable
    }
});

$('.datatable-active-small').DataTable({
    responsive: true,
    language: {
        "url": url_dataTable
    },
    "displayLength": 1,
    "lengthMenu": [1, 3, 5, 10, 15],
    ordering: false
});

deleteModalForm = function (url, message, table_id = null, name = '') {
    let form = $("#form-eliminar");
    form.attr("action", url);
    $("#span-ms").html(message + " <strong>" + name + "</strong>");
    //Ajax
    form.submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            success: function (response) {
                $('#modal-eliminar').modal('toggle');
                if (table_id) {
                    const urlHref = location.href + " #" + table_id + ">*";
                    let table = $("#" + table_id);
                    table.load(urlHref, 2000);
                    // Notificacion
                    $.notify({message: message+' fue eliminada con éxito'},
                        {
                            type: 'success',
                            timer: 2500,
                            placement: {
                                from: 'top',
                                align: 'right'
                            }
                        }
                    );
                }
            },
            error: function (response) {
                console.error(response);
                $('#modal-eliminar').modal('toggle');
            }
        });
    });
};

// });