import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import os

matplotlib.use('Agg')


class Buscas(object):

    def __init__(self):
        self.initial_node = ''
        self.finish_node = ''
        self.nodes = []
        self.edges = []
        self.edges_coust = {}
        self.stack = []
        self.next_node = []
        self.node_sons = {}

        self.G = nx.Graph()

    def is_finish_node(self, node):
        return node == self.finish_node

    def is_node_searched(self, node):
        return node in self.stack

    def generate_node_sons(self):
        for n1, n2 in self.edges:
            if n1 not in self.node_sons:
                self.node_sons[n1] = {n2: self.edges_coust[(n1, n2)]}
            else:
                self.node_sons[n1].update({n2: self.edges_coust[(n1, n2)]})

    def remove_elements(self, list_original, list_elements):
        list_copy = list_original[:]
        for e in list_elements:
            if e in list_original:
                list_copy.remove(e)
        return list_copy

    def busca_amplitude(self, log=False):
        self.generate_node_sons()
        actual_node = self.initial_node  # 1
        next_nodes = []  # 1
        steps = [actual_node]  # 1
        visiteds_locations = []  # 1
        backtrack = {}  # 1
        while actual_node != self.finish_node:  # nk
            if actual_node not in visiteds_locations:  # nk
                sons = self.node_sons[actual_node].keys()  # 3nk
                if log:
                    print("Estou em", actual_node, "e os nós: ", list(sons), "foram inseridos na fila")
                for son in sons:
                    if son not in backtrack:
                        backtrack[son] = []
                    backtrack[son].append(actual_node)
                visiteds_locations.append(actual_node)
                next_nodes += list(sons)
                next_nodes = self.remove_elements(next_nodes, visiteds_locations)
                if log:
                    print("A fila atual: ", next_nodes)
                if len(next_nodes) != 0:
                    actual_node = next_nodes.pop(0)
                    steps.append(actual_node)
            else:
                last_node = actual_node
                if len(next_nodes) != 0:
                    actual_node = next_nodes.pop(0)
                if log:
                    print("Estou em ", last_node, "e irei para", actual_node, "pois já fui visitado")
                steps.append("Pulado " + actual_node)
        if log:
            print("Cheguei em ", actual_node, "e assim termino minha busca. Viva a DEUS VULT")

        backtrack = self.backtrack(self.finish_node, self.initial_node, visiteds_locations, backtrack,
                                   [self.finish_node])
        return list(reversed(backtrack))

    def busca_profundidade(self, log=False):
        self.generate_node_sons()
        actual_node = self.initial_node
        next_nodes = []
        steps = [actual_node]
        visiteds_locations = []
        backtrack = {}
        while actual_node != self.finish_node:
            if actual_node not in visiteds_locations:
                sons = self.node_sons[actual_node].keys()
                if log:
                    print("Estou em", actual_node, "e irei para os próximos nós: ", list(sons))
                for son in sons:
                    if son not in backtrack:
                        backtrack[son] = []
                    backtrack[son].append(actual_node)
                visiteds_locations.append(actual_node)
                next_nodes += list(sons)
                next_nodes = self.remove_elements(next_nodes, visiteds_locations)

                if log:
                    print("A fila atual: ", next_nodes)
                if len(next_nodes) != 0:
                    actual_node = next_nodes.pop()
                    steps.append(actual_node)
            else:
                last_node = actual_node
                if len(next_nodes) > 0:
                    actual_node = next_nodes.pop()
                if log:
                    print("Estou em ", last_node, "e irei para", actual_node, "pois já fui visitado")
                steps.append("Pulado " + actual_node)
        if log:
            print("Cheguei em ", actual_node, "e assim termino minha busca. Viva a DEUS VULT")
        backtrack = self.backtrack(self.finish_node, self.initial_node, visiteds_locations, backtrack,
                                   [self.finish_node])
        return list(reversed(backtrack))

    def generate_next_node(self, node, first_time, jump_node):
        node_name = self.initial_node if first_time else list(node.keys())[0]
        sons_node = self.node_sons[node_name]
        if first_time:
            insert_sons_formated = [{n: (sons_node[n], self.initial_node)} for n in sons_node]
        else:
            if node_name not in jump_node:
                node_value = node[node_name][0]
                path = node[node_name][1]
                insert_sons_formated = [{n: (sons_node[n] + node_value, path + " " + node_name)} for n in sons_node if n not in jump_node]
            else:
                insert_sons_formated = []
        return insert_sons_formated

    def nova_busca_dijkstra(self):
        self.generate_node_sons()
        next_node = self.initial_node
        dict_node = {}
        borda = []
        visiteds = [self.initial_node]
        while next_node != self.finish_node:
            first_time = len(borda) == 0
            node = self.initial_node if first_time else borda.pop(0)
            insert_sons_formated = self.generate_next_node(node, first_time, visiteds)
            borda += insert_sons_formated
            borda = sorted(borda, key=lambda node_aux: node_aux[list(node_aux.keys())[0][0]])
            if not first_time:
                dict_node = node
                next_node = list(node.keys())[0]
                visiteds.append(next_node)
        path = (dict_node[self.finish_node][1]+" "+self.finish_node).split()
        cost = dict_node[self.finish_node][0]
        return path

    def busca_dijkstra(self, initial='*', final='#', percorrer={}, caminho=[]):
        if initial == final:
            caminho_backtrack = self.backtrack_dijkstra(percorrer)
            return caminho_backtrack

        if len(percorrer.keys()) == 0:
            initial = self.initial_node
            final = self.finish_node
            percorrer = {initial: self.node_sons[initial]}
        caminho.append(initial)
        menor_valor, menor_filho = self.menor_valor(ramos=percorrer)
        self.inserir_novo_galho(menor_filho, menor_valor, percorrer, caminho)
        return self.busca_dijkstra(menor_filho, final, percorrer, caminho=caminho)

    def menor_valor(self, menor_valor=9999, menor_filho='', ramos={}):
        for son, value in ramos.items():
            if type(value) == int:
                if value < menor_valor:
                    menor_valor = value
                    menor_filho = son
            else:
                menor_valor, menor_filho = self.menor_valor(menor_valor, menor_filho, ramos[son])
        return menor_valor, menor_filho

    def inserir_novo_galho(self, menor_valor='', valor=0, ramos={}, retirar_filho=[]):
        items_ramos = list(ramos.items())[:]
        for son, value in items_ramos:
            if type(value) == int:
                if son == menor_valor and value == valor:
                    valor = ramos[son]
                    ramos[son] = dict(self.node_sons[son])
                    filhos = list(ramos[son].keys())[:]
                    for s in filhos:
                        if s in retirar_filho:
                            del ramos[son][s]
                        else:
                            ramos[son][s] += valor
            else:
                if ramos[son] == {}:
                    return True
                self.inserir_novo_galho(menor_valor, valor, ramos[son], retirar_filho)
        return True

    def backtrack(self, inicial, final, lista_checagem, lista_pais, acumulativa=[]):
        if inicial == final:
            return acumulativa
        for dad in lista_pais[inicial]:
            if dad in lista_checagem:
                acumulativa.append(dad)
                return self.backtrack(dad, final, lista_checagem, lista_pais, acumulativa)

    def backtrack_dijkstra(self, ramos={}):
        original = dict(ramos)
        caminho = []
        while True:
            keys_filhos = list(ramos.keys())
            for key in keys_filhos:
                caminho.append(key)
                if type(ramos[key]) == dict:
                    ramos = dict(ramos[key])
                else:
                    ramos = ramos[key]
                if ramos == {} or type(ramos) == int:
                    filhotes = original
                    for k in caminho:
                        if (filhotes[k] == {} or type(filhotes[k]) == int) and k != self.finish_node:
                            del filhotes[k]
                        elif k == self.finish_node:
                            if type(filhotes[k]) == dict:
                                return caminho
                            else:
                                del filhotes[k]
                        else:
                            filhotes = filhotes[k]
                    caminho = []
                    ramos = original
                break

    def gerar_grafico(self, caminho, nome):
        nos_resultados = [(caminho[0], caminho[1])]
        for r in range(2, len(caminho), 2):
            nos_resultados.append((caminho[r - 1], caminho[r]))
            nos_resultados.append((caminho[r], caminho[r - 1]))
        for node in self.nodes:
            self.G.add_node(node)
        cores = []
        pular = []
        for n1, n2 in self.edges:
            if (n1, n2) not in pular:
                if n1 in caminho and n2 in caminho:
                    color = 'r'
                    cores.append(color)
                else:
                    color = 'b'
                    cores.append(color)
                self.G.add_edge(n1, n2, color=color, weight=self.edges_coust[(n1, n2)])
            pular.append((n2, n1))
        pos = nx.kamada_kawai_layout(self.G)
        colors = [self.G[u][v]['color'] for u, v in self.G.edges]
        nx.draw(self.G, pos, edge_color=colors, width=1, with_labels=True)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=self.edges_coust)
        if os.path.exists("static/files/" + nome):
            os.remove("static/files/" + nome)
        plt.savefig("static/files/" + nome)
        plt.close()
        self.reset_values()

    def reset_values(self):
        self.G = None
        self.G = nx.Graph()
        self.G.clear()
        self.G.clear_edges()
        self.initial_node = ''
        self.finish_node = ''
        self.nodes = []
        self.edges = []
        self.edges_coust = {}
        self.stack = []
        self.next_node = []
        self.node_sons = {}

