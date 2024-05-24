import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._prodotti = DAO.getAllProducts()
        self._idMap = {}
        for prod in self._prodotti:
            self._idMap[prod.Product_number] = prod
        self.colori = set()
        self.edges_added = []
        self.solBest = []

    def buildGraph(self, anno, color):
        self._grafo.clear()
        self._idMap = {}
        for prod in self._prodotti:
            if color == prod.Product_color:
                self._grafo.add_node(prod)
        self.addEdge(anno)
        return self._grafo, self.edges_added

    def getBest(self, prodotto):
        parziale = [prodotto]
        self.ricorsione(parziale)
        return len(self.solBest)

    def pesoCrescente(self, parziale):
        peso = 0
        for par in range(1, len(parziale)):
            if par == 1:
                peso = self._grafo[parziale[par - 1]][parziale[par]]['weight']
            else:
                if peso > self._grafo[parziale[par - 1]][parziale[par]]['weight']:
                    return False
                else:
                    peso = self._grafo[parziale[par - 1]][parziale[par]]['weight']
        return True

    def ricorsione(self, parziale):
        if self.pesoCrescente(parziale) is False and len(parziale) > 1:
            if len(self.solBest) < len(parziale):
                self.solBest = copy.deepcopy(parziale)
        else:
            for neighbor in self._grafo.neighbors(parziale[-1]):
                if neighbor not in parziale:
                    parziale.append(neighbor)
                    self.ricorsione(parziale)
                    parziale.pop()

    def addEdge(self, anno):
        self.edges_added = []
        for v0 in self._grafo.nodes:
            for v1 in self._grafo.nodes:
                if self._grafo.has_edge(v0, v1) is False:
                    if v0.Product_number != v1.Product_number:
                        peso = DAO.getAllPesi(anno, v0.Product_number, v1.Product_number)
                        if peso > 0:
                            self._grafo.add_edge(v0, v1, weight=peso)
                            self.edges_added.append((v0, v1, peso))

    def getColors(self):
        self.colori = set()
        prodotti = DAO.getAllProducts()
        for prod in prodotti:
            self.colori.add(prod.Product_color)
        return self.colori

    def getNumEdges(self):
        return len(self._grafo.edges)

    def getNumVertici(self):
        return len(self._grafo.nodes)
