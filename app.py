from flask import Flask, render_template, request, send_file
from buscas import Buscas
from Node import nodes, edges, edges_labels
from flask_socketio import SocketIO
import random
app = Flask(__name__)
socketio = SocketIO(cors_allowed_origins="*")
socketio.init_app(app)
busca = Buscas()
busca_app = {"largura": busca.busca_amplitude, "profunda": busca.busca_profundidade, "dijkstra": busca.nova_busca_dijkstra}

@app.route("/")
def home():
    return render_template("home.html", nos=nodes)

@app.route("/imagem")
def imagem():
    return send_file("static/files/graph.jpg", mimetype='image/gif')

@socketio.on("gerarGrafo")
def gerarGrafo(input):
    configure_busca()
    tipo_busca = input["busca"]
    busca.initial_node = input["init_node"]
    busca.finish_node = input["finish_node"]
    busca.generate_node_sons()
    resultado = busca_app[tipo_busca]()
    name = generate_random_names()
    busca.gerar_grafico(resultado, name)
    socketio.emit("dado_gerado", name)

def configure_busca():
    busca.nodes = nodes
    busca.edges = edges
    busca.edges_coust = edges_labels

def generate_random_names():
    name = ""
    letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'm', 'n', 'o', 'p']
    numeros = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for x in range(10):
        n = random.randint(0, 1)
        if n == 0:
            name += random.choice(letras)
        else:
            name += random.choice(numeros)
    return name+".jpg"

socketio.run(app, debug=True)