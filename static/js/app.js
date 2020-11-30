var BASE_URL = `${window.location.protocol}//${window.location.host}/`;


function errorCalcular(message) {
    $("#error-calcular").animate({
        height: '+=72px'
    }, 300);
    $('<div class="alert alert-danger">' +
        '<button type="button" class="close" data-dismiss="alert">' +
        '&times;</button>' + message + '</div>').hide().appendTo('#error-calcular').fadeIn(1000);

    $(".alert").delay(2000).fadeOut(
        "normal",
        function () {
            $(this).remove();
        });

    $("#error-calcular").delay(3000).animate({
        height: '-=72px'
    }, 300);

}

function errorConsecucion(message) {

    $("#guardar-consecucion-error").animate({
        height: '+=72px'
    }, 300);
    $('<div class="alert alert-danger">' +
        '<button type="button" class="close" data-dismiss="alert">' +
        '&times;</button>' + message + '</div>').hide().appendTo('#guardar-consecucion-error').fadeIn(1000);

    $(".alert").delay(2000).fadeOut(
        "normal",
        function () {
            $(this).remove();
        });

    $("#guardar-consecucion-error").delay(3000).animate({
        height: '-=72px'
    }, 300);
}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function borrar(elmnt) {
    var id_borrar = elmnt.getAttribute('id');
    var url = `${BASE_URL}api/consecucion/eliminar/${id_borrar}`

    fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    }).then(function () {
        console.log("Eliminado");
        var consecucion_eliminada = document.getElementById(`consecuciones-row-${id_borrar}`);
        consecucion_eliminada.remove();
    })

}

function editar(elmnt) {
    var consecucion_id = elmnt.getAttribute('id');
    document.getElementById("consecucion-id").setAttribute('value', consecucion_id);
    var descripcion = document.getElementById(`descripcion-${consecucion_id}`).innerHTML;
    var meta = document.getElementById(`meta-${consecucion_id}`).innerHTML;
    var porcentaje = document.getElementById(`porcentaje-${consecucion_id}`).innerHTML;

    document.getElementById("agregar-descripcion").value = descripcion;
    document.getElementById("agregar-meta").value = meta;
    document.getElementById("agregar-porcentaje").value = porcentaje;

}

function resetAgregarConsecucionForm() {

    document.getElementById("consecucion-id").value = "0"
    document.getElementById("agregar-descripcion").value = "";
    document.getElementById("agregar-meta").value = "";
    document.getElementById("agregar-porcentaje").value = "";

}

var actualizarObjetivoBtn = document.getElementById('actualizar-objetivo');
actualizarObjetivoBtn.addEventListener("click", function (e) {
    var objetivo = document.getElementById('objetivo-id').value;
    var descripcion = document.getElementById('objetivo').value;
    var metrica = document.getElementById('metrica').value;
    var metaAscendente = document.getElementById('meta-ascendente').checked;

    var url = `${BASE_URL}api/objetivo/actualizar/${objetivo}`;

    fetch(url, {
        method: 'PUT',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'descripcion': descripcion,
            'metrica': metrica,
            'meta_ascendente': metaAscendente,
        })
    }).then(response => response.json())
        .then(function (data) {
            console.log(data);
        })



})


var calcularBtn = document.getElementById('calcular-btn');
calcularBtn.addEventListener("click", function (e) {

    var url = `${BASE_URL}api/consecucion/calcular`;
    var objetivo = document.getElementById('objetivo-id').value;
    var resultado = document.getElementById('resultado').value;

    if (resultado == "") {
        errorCalcular("Debe especificar un valor");
        return;
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'resultado': resultado,
            'objetivo': objetivo
        })
    }).then(response => response.json())
        .then(function (data) {

            if (data.error && data.error != null) {
                errorCalcular(data.message);
            }
            else {
                document.getElementById("consecucion-porcentaje").value = data.consecucion;
            }
        })

})



var agregarBtn = document.getElementById('agregar-btn');
agregarBtn.addEventListener("click", function (e) {

    var consecucion_id = document.getElementById('consecucion-id').value

    if (consecucion_id === "0" || consecucion_id === null) {
        crearConsecucion();
    }
    else {
        editarConsecucion(consecucion_id);
    }

    resetAgregarConsecucionForm();
})

function validarConsecucion(descripcion, meta, porcentaje) {

    if (descripcion == "" || meta == "" || porcentaje == "") {
        errorConsecucion("Debe completar todos los campos");
        return false;
    }

    if(porcentaje > 100 || porcentaje < 0){
        errorConsecucion("Digitar un porcentaje entre 0% a 100%");
        return false;
    }

    if(meta < 0){
        errorConsecucion("La meta debe ser mayor a 0");
        return false;
    }

    return true;
}

function crearConsecucion() {
    var url = `${BASE_URL}api/consecucion/crear`;
    var objetivo = document.getElementById('objetivo-id').value;
    var descripcion = document.getElementById('agregar-descripcion').value;
    var meta = document.getElementById('agregar-meta').value;
    var porcentaje = document.getElementById('agregar-porcentaje').value;

    if (!validarConsecucion(descripcion, meta, porcentaje)) {
        return;
    }

    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'descripcion': descripcion,
            'meta': meta,
            'porcentaje': porcentaje,
            'objetivo': objetivo
        })
    })
        .then(response => response.json())
        .then(function (data) {
            addRowConsecucion(data);
        })



}

function editarConsecucion(consecucion_id) {

    var url = `${BASE_URL}api/consecucion/actualizar/${consecucion_id}`;
    var objetivo = document.getElementById('objetivo-id').value;
    var descripcion = document.getElementById('agregar-descripcion').value;
    var meta = document.getElementById('agregar-meta').value;
    var porcentaje = document.getElementById('agregar-porcentaje').value;
    var consecucion_id = document.getElementById('consecucion-id').value

    if (!validarConsecucion(descripcion, meta, porcentaje)) {
        return;
    }

    fetch(url, {
        method: 'PUT',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'id': consecucion_id,
            'descripcion': descripcion,
            'meta': meta,
            'porcentaje': porcentaje,
            'objetivo': objetivo
        })
    })
        .then(response => response.json())
        .then(function (data) {
            document.getElementById(`descripcion-${consecucion_id}`).innerHTML = data.descripcion;
            document.getElementById(`meta-${consecucion_id}`).innerHTML = data.meta;
            document.getElementById(`porcentaje-${consecucion_id}`).innerHTML = data.porcentaje

        })



}


function addRowConsecucion(data) {

    var consecucion = document.getElementById('consecucion-wrapper');
    var item = `
    <div id=consecuciones-row-${data.id} class="consecucion-row">
    <div style="flex:2">
        <p id="descripcion-${data.id}">${data.descripcion}</p>
    </div>
    <div style="flex:1">
        <p id="meta-${data.id}">${data.meta}</p>
    </div>
    <div style="flex:1">
        <p id="porcentaje-${data.id}">${data.porcentaje}</p>
    </div>
    <div style="flex:2">
        <button type="button" onclick="editar(this)" class="btn btn-primary id="${data.id}">Editar</button>
        <button type="button" onclick="borrar(this)" class="btn btn-danger" id="${data.id}">Borrar</button>
    </div>
    </div>`
    var new_item = document.createElement('div');
    new_item.innerHTML = item;
    consecucion.appendChild(new_item);
}

function editRowConsecucion(data) {

    var consecucion = document.getElementById(`consecuciones-row-${data.id}`);
    var item = `
    <div style="flex:2">
        <p id="descripcion-${data.id}">${data.descripcion}</p>
    </div>
    <div style="flex:1">
        <p "id="meta-${data.id}">${data.meta}</p>
    </div>
    <div style="flex:1">
        <p id="porcentaje-${data.id}>${data.porcentaje}</p>
    </div>
    <div style="flex:2">
        <button type="button" onclick="editar(this)" class="btn btn-primary id="${data.id}">Editar</button>
        <button type="button" onclick="borrar(this)" class="btn btn-danger" id="${data.id}">Borrar</button>
    </div>
    `
    consecucion.innerHTML = item;
}
