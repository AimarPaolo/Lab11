import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []
        self.dizio = {}
        self.lista_ripetuti = []
        self._choiceProdotto = None

    def fillDD(self):
        for i in range(2015, 2019):
            self._view._ddyear.options.append(ft.dropdown.Option(f"{i}"))
        colori = self._model.getColors()
        for col in colori:
            self._view._ddcolor.options.append(ft.dropdown.Option(f"{col}"))

    def handle_graph(self, e):
        self._view.txtOut.controls.clear()
        if self._view._ddyear.value == None or self._view._ddcolor.value == None:
            self._view.txtOut.controls.append(ft.Text("Bisogna selezionare dei valori!!"))
            self._view.update_page()
            return
        anno = self._view._ddyear.value
        colore = self._view._ddcolor.value
        grafo, edges_add = self._model.buildGraph(anno, colore)
        self._view.txtOut.controls.append(ft.Text("Grafo creato correttamente!"))
        nEdges = self._model.getNumEdges()
        nNodi = self._model.getNumVertici()
        self._view.txtOut.controls.append(ft.Text(f"Il grafo creato ha {nEdges} archi e {nNodi} nodi!"))
        top3 = sorted(edges_add, key=lambda x: x[2], reverse=True)
        for vicini in top3[:3]:
            self.find_vicini(vicini)
        self.lista_ripetuti = []
        for key, value in self.dizio.items():
            if value > 1:
                self.lista_ripetuti.append(key)
        self.dizio = {}
        self.fillDDProduct()
        for edge in top3[:3]:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {edge[0].Product_number} a {edge[1].Product_number}, peso={edge[2]}"))
        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {self.lista_ripetuti}"))
        self._view.btn_search.disabled = False
        self._view.update_page()

    def find_vicini(self, vicini):
        if vicini[0].Product_number in self.dizio:
            self.dizio[vicini[0].Product_number] += 1
        else:
            self.dizio[vicini[0].Product_number] = 1
        if vicini[1].Product_number in self.dizio:
            self.dizio[vicini[1].Product_number] += 1
        else:
            self.dizio[vicini[1].Product_number] = 1

    def fillDDProduct(self):
        for prodotto in self._model._grafo.nodes:
            self._view._ddnode.options.append(ft.dropdown.Option(text=prodotto.Product_number, data=prodotto, on_click=self.readDDProdotto))

    def readDDProdotto(self, e):
        if e.control.data is None:
            self._choiceProdotto = None
        else:
            self._choiceProdotto = e.control.data
        print(f"readDDProdotto called -- {self._choiceProdotto}")


    def handle_search(self, e):
        self._view.txtOut2.controls.clear()
        prodotto = self._choiceProdotto
        if self._choiceProdotto is None:
            self._view.txtOut2.controls.append(ft.Text("Bisogna selezionare un prodotto!!", color="red"))
            self._view.update_page()
            return
        path = self._model.getBest(prodotto)
        self._view.txtOut2.controls.append(ft.Text(f"Numero archi percorso più lungo: {path-1}"))
        self._view.update_page()



