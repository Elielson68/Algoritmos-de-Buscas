
var container_image = document.getElementById("container-image")
var column_image = document.getElementById("column-image")
var container_select = document.getElementById("container-select")
var button = document.getElementById("enviar")
var img = document.getElementById("img")
var checkbox_digraph = document.getElementById("use_digraph")
var first_time = true;
var p_cost = document.getElementById("custo")
let namespace = '/';
let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

socket.on('connect', () => { socket.send('conectado') } );

socket.on('dado_gerado', (dado) => {
    if(first_time){
        container_select.removeAttribute("class")
        container_select.setAttribute("class", "p-3 border bg-light descer")
        container_select.addEventListener("animationend", listener, false);
        img.setAttribute("class", "expandir")
        column_image.removeAttribute("hidden")
        first_time = false
    }
    else{
        img.setAttribute("class", "desaparecer");
        img.addEventListener("animationend", listener_img, false);

    }
    img.src = "static/files/"+dado.nome
    p_cost.innerHTML = "Custo: "+dado.custo
})

socket.emit('teste', 'ola');

button.addEventListener('click', Enviar)
select_busca = document.getElementById("busca")
select_initNode = document.getElementById("init_node")
select_finishNode = document.getElementById("finish_node")

function Enviar(){
    data = {"busca": select_busca.value, "init_node": select_initNode.value, "finish_node": select_finishNode.value,
    "use_digraph": checkbox_digraph.checked}
    socket.emit('gerarGrafo', data)
}

function listener(e) {
  switch(e.type) {
    case "animationend":
      container_select.style = "margin-top: 25%;"
      break;
  }
  container_select.removeEventListener("animationend", listener, false);
}

function listener_img(e) {
  switch(e.type) {
    case "animationend":
      img.setAttribute("class", "aparecer")
      break;
  }
  container_select.removeEventListener("animationend", listener, false);
}