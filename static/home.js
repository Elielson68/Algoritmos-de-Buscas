container_image = document.getElementById("container-image")
column_image = document.getElementById("column-image")
container_select = document.getElementById("container-select")
let namespace = '/';
let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
socket.on('connect', () => { socket.send('conectado') } );
socket.on('dado_gerado', (nome) => {
    container_select.style = "margin-top: 25%;"
    column_image.removeAttribute("hidden")
    img = document.getElementById("img")
    img.remove()
    img = document.createElement("img")
    img.setAttribute("id", "img")
    img.setAttribute("class", "rounded mx-auto d-block")
    container_image.appendChild(img)
    img.src = "static/files/"+nome
})
socket.emit('teste', 'ola');
button = document.getElementById("enviar")
button.addEventListener('click', Enviar)
select_busca = document.getElementById("busca")
select_initNode = document.getElementById("init_node")
select_finishNode = document.getElementById("finish_node")

function Enviar(){
    data = {"busca": select_busca.value, "init_node": select_initNode.value, "finish_node": select_finishNode.value}
    socket.emit('gerarGrafo', data)
}