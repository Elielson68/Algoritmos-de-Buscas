nodes = {'A': 50, 'B': 45, 'C': 40, 'D': 42, 'E': 42, 'F': 32, 'G': 28, 'H': 25, 'I': 30, 'J': 57, 'K': 38, 'L': 29,
         'M': 18, 'N': 20, 'O': 22, 'P': 29, 'Q': 28, 'R': 19, 'S': 10, 'T': 10, 'U': 20, 'V': 0}

edges_labels = {
    ('A', 'B'): 10, ('A', 'C'): 11, ('A', 'D'): 13,
    ('B', 'A'): 10, ('B', 'E'): 14, ('B', 'F'): 14,
    ('C', 'A'): 11, ('C', 'G'): 10, ('C', 'H'): 10,
    ('D', 'A'): 13, ('D', 'I'): 10, ('D', 'J'): 10,
    ('E', 'B'): 14, ('E', 'K'): 11, ('E', 'L'): 14,
    ('F', 'B'): 14, ('F', 'G'): 10, ('F', 'L'): 12, ('F', 'M'): 14,
    ('G', 'C'): 10, ('G', 'F'): 10, ('G', 'M'): 10,
    ('H', 'C'): 10, ('H', 'N'): 10,
    ('I', 'D'): 10, ('I', 'N'): 10, ('I', 'O'): 10,
    ('J', 'D'): 10,
    ('K', 'E'): 11, ('K', 'P'): 10,
    ('L', 'E'): 14, ('L', 'F'): 12, ('L', 'Q'): 10, ('L', 'R'): 11,
    ('M', 'F'): 14, ('M', 'G'): 10, ('M', 'R'): 14, ('M', 'S'): 10,
    ('N', 'H'): 10, ('N', 'I'): 10, ('N', 'T'): 12,
    ('O', 'I'): 10, ('O', 'T'): 13,
    ('P', 'K'): 10, ('P', 'U'): 10,
    ('Q', 'L'): 10, ('Q', 'U'): 10,
    ('R', 'L'): 11, ('R', 'M'): 14, ('R', 'S'): 10,
    ('S', 'M'): 10, ('S', 'R'): 10, ('S', 'V'): 10,
    ('T', 'N'): 12, ('T', 'O'): 13, ('T', 'V'): 10,
    ('U', 'P'): 10, ('U', 'Q'): 10, ('U', 'V'): 21,
    ('V', 'S'): 10, ('V', 'T'): 10, ('V', 'U'): 21,
}

# from buscas import Buscas
#
# busca = Buscas()
# busca.nodes = nodes
# busca.edges_cost = edges_labels
# busca.initial_node = "A"
# busca.finish_node = "V"
# print("Busca em largura: ", busca.busca_largura())
# print("Busca em profundidade: ", busca.busca_profundidade())
# print("Busca gulosa: ", busca.busca_gulosa())
# print("Busca de Dijkstra: ", busca.busca_dijkstra())
# print("Busca A*: ", busca.busca_a_estrela())
