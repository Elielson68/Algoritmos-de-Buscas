import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import os

matplotlib.use('Agg')


class Buscas(object):
    """
        Classe de buscas para utlizar buscas cegas
    """
    def __init__(self):
        self.initial_node = ''
        self.finish_node = ''
        self.nodes = {}
        self.edges_cost = {}
        self.__node_sons = {}

    def __getitem__(self, item):
        return {"largura": self.busca_largura(),
                "profunda": self.busca_profundidade(),
                "dijkstra": self.busca_dijkstra(),
                "gulosa": self.busca_gulosa(),
                "estrela": self.busca_a_estrela()
                }[
            item]

    def reset_values(self):
        self.initial_node = ''
        self.finish_node = ''
        self.nodes = {}
        self.edges_cost = {}
        self.__node_sons = {}

    def __generate_node_sons(self):
        for n1, n2 in list(self.edges_cost.keys()):
            if n1 not in self.__node_sons:
                self.__node_sons[n1] = {n2: self.edges_cost[(n1, n2)]}
            else:
                self.__node_sons[n1].update({n2: self.edges_cost[(n1, n2)]})

    def __generate_next_node(self, node, jump_node):
        node_name = list(node.keys())[0]
        node_childrens = self.__node_sons[node_name]
        if node_name not in jump_node:
            node_value = node[node_name][0]
            path = node[node_name][1]
            insert_sons_formated = [
                {key: (
                    node_childrens[key] + node_value,
                    path + " " + node_name)}
                for key in node_childrens
                if key not in jump_node
            ]
        else:
            insert_sons_formated = []
        return insert_sons_formated

    def busca_largura(self):
        self.__generate_node_sons()
        next_node = self.initial_node
        dict_node = {}
        borda = [{n: (self.__node_sons[next_node][n], self.initial_node)} for n in self.__node_sons[next_node]]
        visiteds = [self.initial_node]
        while next_node != self.finish_node:
            node = borda.pop(0)
            insert_sons_formated = self.__generate_next_node(node, visiteds)
            borda += insert_sons_formated
            dict_node = node
            next_node = list(node.keys())[0]
            visiteds.append(next_node)
        path = (dict_node[self.finish_node][1] + " " + self.finish_node).split()
        cost = dict_node[self.finish_node][0]
        return path, cost

    def busca_profundidade(self):
        self.__generate_node_sons()
        next_node = self.initial_node
        dict_node = {}
        borda = [{n: (self.__node_sons[next_node][n], self.initial_node)} for n in self.__node_sons[next_node]]
        visiteds = [self.initial_node]
        while next_node != self.finish_node:
            node = borda.pop()
            insert_sons_formated = self.__generate_next_node(node, visiteds)
            borda += insert_sons_formated
            dict_node = node
            next_node = list(node.keys())[0]
            visiteds.append(next_node)
        path = (dict_node[self.finish_node][1] + " " + self.finish_node).split()
        cost = dict_node[self.finish_node][0]
        return path, cost

    def busca_dijkstra(self):
        self.__generate_node_sons()
        next_node = self.initial_node
        dict_node = {}
        borda = [{n: (self.__node_sons[next_node][n], self.initial_node)} for n in self.__node_sons[next_node]]
        borda = sorted(borda, key=self.__sort_dijkstra)
        visiteds = [self.initial_node]
        while next_node != self.finish_node:
            node = borda.pop(0)
            insert_sons_formated = self.__generate_next_node(node, visiteds)
            borda += insert_sons_formated
            borda = sorted(borda, key=self.__sort_dijkstra)
            dict_node = node
            next_node = list(node.keys())[0]
            visiteds.append(next_node)
        path = (dict_node[self.finish_node][1] + " " + self.finish_node).split()
        cost = dict_node[self.finish_node][0]
        return path, cost

    def busca_a_estrela(self):
        self.__generate_node_sons()
        next_node = self.initial_node
        dict_node = {}
        borda = [{n: (self.__node_sons[next_node][n], self.initial_node)} for n in
                 self.__node_sons[next_node]]
        borda = sorted(borda, key=self.__sort_a_estrela)
        visiteds = [self.initial_node]
        while next_node != self.finish_node:
            node = borda.pop(0)
            insert_sons_formated = self.__generate_next_node(node, visiteds)
            borda += insert_sons_formated
            borda = sorted(borda, key=self.__sort_a_estrela)
            dict_node = node
            next_node = list(node.keys())[0]
            visiteds.append(next_node)
        path = (dict_node[self.finish_node][1] + " " + self.finish_node).split()
        cost = dict_node[self.finish_node][0]
        return path, cost

    def busca_gulosa(self):
        self.__generate_node_sons()
        next_node = self.initial_node
        dict_node = {}
        borda = [{n: (self.__node_sons[next_node][n], self.initial_node)} for n in
                 self.__node_sons[next_node]]
        borda = sorted(borda, key=self.__sort_gulosa)
        visiteds = [self.initial_node]
        while next_node != self.finish_node:
            node = borda.pop(0)
            insert_sons_formated = self.__generate_next_node(node, visiteds)
            borda += insert_sons_formated
            borda = sorted(borda, key=self.__sort_gulosa)
            dict_node = node
            next_node = list(node.keys())[0]
            visiteds.append(next_node)
        path = (dict_node[self.finish_node][1] + " " + self.finish_node).split()
        cost = dict_node[self.finish_node][0]
        return path, cost

    def __sort_dijkstra(self, node_aux):
        key = list(node_aux.keys())[0]
        return node_aux[key][0]

    def __sort_a_estrela(self, node_aux):
        key = list(node_aux.keys())[0]
        return node_aux[key][0] + self.nodes[key]

    def __sort_gulosa(self, node_aux):
        key = list(node_aux.keys())[0]
        return self.nodes[key]

    def gerar_grafico(self, caminho, nome, use_digraph):
        if use_digraph:
            graph = nx.DiGraph()
        else:
            graph = nx.Graph()
        # Inicia a lista com as duas primeiras edges
        nos_resultados = [(caminho[0], caminho[1])]

        # Continua a lista de edges a partir do terceiro elemento em diante de 2 em 2
        for r in range(2, len(caminho), 2):
            nos_resultados.append((caminho[r - 1], caminho[r]))
            nos_resultados.append((caminho[r], caminho[r - 1]))

        # Insere os n??s no objeto
        for node in list(self.nodes.keys()):
            graph.add_node(node)

        # lista para pular os n??s de mesmo par j?? inseridos na lista de Edges
        # Exemplo: (1, 2) ele ir?? pular o (2, 1)
        pular = []
        for n1, n2 in list(self.edges_cost.keys()):

            # Faz a verifica????o de pulo descrito acima
            if (n1, n2) not in pular:
                # Verifica se o edge ?? um caminho at?? o n?? final, se for colore a linha de vermelho, se n??o colore de
                # azul
                if n1 in caminho and n2 in caminho:
                    color = 'r'
                else:
                    color = 'b'
                graph.add_edge(n1, n2, color=color, weight=self.edges_cost[(n1, n2)]/100)
            pular.append((n2, n1))

        # Cria o layout em que o grafo ser?? plotado

        pos = nx.kamada_kawai_layout(graph)

        # cria um array com as cores de cada edge
        colors = [graph[u][v]['color'] for u, v in graph.edges]
        # desenha o grafo com as configura????es feitas acima
        nx.draw(graph, pos, edge_color=colors, width=1, with_labels=True)
        # realiza umas configura????es adicionais nos edges
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=self.edges_cost)

        # verifica se o arquivo j?? existe com o mesmo nome e se existir exclui e ent??o salva o novo.
        if not os.path.isdir("static/files"):
            os.mkdir("static/files")
        plt.savefig("static/files/" + nome)
        plt.close()
        self.reset_values()

