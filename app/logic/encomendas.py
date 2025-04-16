class Encomenda:
    def __init__(self, consumidor, supermercado, frutas):
        self.consumidor = consumidor
        self.supermercado = supermercado
        self.frutas = frutas


class GestorEncomendas:
    def __init__(self):
        self.encomendas = []

    def registar_encomenda(self, encomenda):
        self.encomendas.append(encomenda)
