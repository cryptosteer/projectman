$("select#usuario").change(function () {
    $("#cuerpo-tabla").html("");
    actualizarTabla();
});

actualizarTabla = function () {
    var x = document.getElementById("usuario");
    for (var i = 0; i < x.options.length; i++) {
        if (x.options[i].selected) {
            $("#tabla_usuarios").append(
                "<tr>" +
                    "<td>" +
                        "<input type='text' value='" + x.options[i].text + "' disabled>" +
                    "</td>" +
                "</tr>"
            );
        }
    }
};

actualizarTabla();