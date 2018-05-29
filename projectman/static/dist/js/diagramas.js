saltos_lineas = function (texto, limite , separador) {

    longitud_texto = texto.length;
    separador = separador == "br" ? "<br>" : "\\n";

    // funcion que reemplaza un caracteres
    function reemplazar(cadena, indice, caracter) {
        return cadena.substr(0, indice) + caracter + cadena.substr(indice + 1);
    }

    //Reemplaza la primera aparicion de un espacio en blanco despues de la posicion 'limite'
    if(longitud_texto > limite){
        espacio = texto.indexOf(" ", limite);
        if(espacio != -1){
            texto = reemplazar(texto, espacio, separador);
        }

        // cuantos saltos de linea cabe en el texto
        cantidad_ciclos = Math.floor(longitud_texto/limite)-1;

        if (cantidad_ciclos > 0){
            // ciclo que busca inserta saltos de lineas despues de haber
            for (var i=0; i<cantidad_ciclos; i++){
                ultimo_salto_linea = texto.lastIndexOf(separador);
                espacio = texto.indexOf(" ", ultimo_salto_linea+limite);
                if(espacio != -1){
                    texto = reemplazar(texto, espacio, separador);
                }
            }
        }
    }
    return texto;
};

titulo = saltos_lineas(titulo,60);
label_footer=[];
label_header=[];
label_header_html=[];
ideas_booleano = false;
valores=[];
for (var i=0; i < datos.length; i++){
    label_header.push(datos[i][0]); // Informacion flotante de cada barra
    label_header_html.push("<span style='font-weight:bold;'>"+saltos_lineas(datos[i][0], 30)+"</span>"); // Informacion flotante de cada barra
    if(datos[i][0].length<=2){
        label_footer.push(datos[i][0].toUpperCase()); //Letra inferior debajo de cada barra
        ideas_booleano = true;
    }else{
        label_footer.push(datos[i][0].charAt(0).toUpperCase()); //Letra inferior debajo de cada barra
    }

    valores.push(datos[i][1]); // Valores asignados a cada barra
}

/* ----------------BARRA----------------------------*/
zingchart.THEME = "classic";
// var initState = null; // Used later to store the chart state before changing the data
var dataBarra = {
    "globals": {
        "font-family": "Helvetica"
    },
    "type": "bar",
    "background-color": "white",
    "title": {
        "color": "#606060",
        "background-color": "white",
        "text": titulo
    },
    "scale-y": {
        "line-color": "none",
        "tick": {
            "line-color": "none"
        },
        "guide": {
            "line-style": "solid"
        },
        "item": {
            "color": "#606060"
        }
    },
    "scale-x": {
        "values": label_footer,
        "line-color": "#C0D0E0",
        "line-width": 1,
        "tick": {
            "line-width": 1,
            "line-color": "#C0D0E0"
        },
        "guide": {
            "visible": false
        },
        "item": {
            "color": "#606060"
        }
    },
    "crosshair-x": {
        "marker": {
            "visible": false
        },
        "line-color": "none",
        "line-width": "0px",
        "scale-label": {
            "visible": false
        },
        "plot-label": {
            "text": "%data-browser",
            "multiple": true,
            "font-size": "12px",
            "color": "#606060",
            "background-color": "white",
            "border-width": 3,
            "alpha": 0.9,
            "callout": true,
            "callout-position": "bottom",
            "shadow": 0,
            "placement": "node-top",
            "border-radius": 4,
            "offsetY": -20,
            "padding": 8
        }
    },
    "plot": {
        "data-browser": label_header_html,
        "cursor": "hand",
        "value-box": {
            "text": "%v",
            "text-decoration": "underline",
            "color": "#606060"
        },
        "tooltip": {
            "visible": false
        },
        "animation": {
            "effect": "7"
        },
        "background-color": "#1976d2"
    },
    "series": [{
        "values": valores
    }]
};
zingchart.render({
    id: 'barra',
    data: dataBarra,
    height: '500',
    width: '100%'
});

/* ----------------CORRELACION----------------------------*/

var dataCorrelacion = {
"graphset":[
    {
        "type":"scatter",
        "background-color":"#fff #fbfbfb",
        "title":{
            "text": titulo,
            "background-color":"#00a679 #33b894"
        },
        "plotarea":{
            "margin":"70 120 dynamic"
            // "margin":"60 40 dynamic dynamic"
        },
        "crosshair-x": {
            "marker": {
                "visible": false
            },
            "line-color": "none",
            "line-width": "0px",
            "scale-label": {
                "visible": false
            },
            "plot-label": {
                "text": "%data-browser: <strong>%v</strong>",
                "multiple": true,
                "font-size": "13px",
                "color": "#606060",
                "background-color": "white",
                "border-width": 3,
                "alpha": 0.9,
                "callout": true,
                "callout-position": "bottom",
                "shadow": 0,
                "placement": "node-top",
                "border-radius": 4,
                "offsetY": -20,
                "padding": 8
            }
        },
        "plot": {
            "data-browser": label_header_html,
            "tooltip": {
                "visible": false
            }
        },
        "scale-x":{
            "offset-start":90,
            "offset-end":90,
            "items-overlap":true,
            // "max-items":16,
            "values": label_footer,
        },
        "scale-y":{
            "min-value":"auto",
            "offset-start":60,
            "offset-end":20,
        },
        "series": [{
            "values": valores,
            // "tooltip":{"text": "%n".replace(/['"]+/g, '')}
            // "tooltip":{"text":"%k / %v"}

        }]
    }
]
};
zingchart.render({
	id : 'correlacion',
	data : dataCorrelacion,
	height: 500,
	width: '100%'
});


/* ----------------PARETO ----------------------------*/

var dataPareto = {
    "type":"pareto",
    "background-color":"rgba(255, 255, 255, 0)",
    "title":{
        "text":titulo,
        "font-family":"Merriweather",
        // "color":"#666666"
    },
    "plotarea":{
        "margin-top":"20%"
    },
    "scale-x":{
        "labels":label_footer
    },
    "options": { //is for the "line"
        "line-plot": {
            "line-width": 2,
            "line-color": "#006064",
            "marker": {
                "size": 3,
                "shadow": false,
                "background-color": "#006064",
                "border-color": "#006064"
            },
            "value-box":{
                "font-color":"#006064",
                "font-family":"Merriweather",
                "font-size":12,
                "font-weight":"bold",
                "background-color":"none",
                "border-width":"none",
                "shadow":false,
                "placement":"top",
                "offset-x":3,
                "offset-y":-5
            }
        },
        "scale-y-2":{
            "guide": {
                "visible": false
            }
        }
    },
    "series": [
        {
            "values": valores,
            "background-color":"#0097A7",
            // "bar-width":"90%",
            "tooltip": {
                "text": "%v",
                "font-family": "arial",
                "shadow-alpha": 0.3
            }
        }
    ]
};

zingchart.render({
    id : 'pareto',
    data : dataPareto,
    height: 500,
    width: '100%'
});
if(ideas_booleano==false){
    for(var i=0;i<label_header.length;i++){
        $(".box-body:has(#pareto)").append('<p style="padding-left: 50px">'+label_header[i]+'</p>');
    }
}

