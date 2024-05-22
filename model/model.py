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

    def buildGraph(self, anno, color):
        self._grafo.clear()
        self._idMap = {}
        for prod in self._prodotti:
            if color == prod.Product_color:
                self._grafo.add_node(prod)
        self.addEdge(anno)
        return self._grafo, self.edges_added

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
