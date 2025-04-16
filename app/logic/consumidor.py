# Função: Define a classe Consumidor, que representa o consumidor que faz a encomenda.
# A classe guarda o nome do consumidor e as encomendas feitas, além de adicionar novas encomendas.
# Contém o comportamento do consumidor e sua interação com as encomendas.


class Consumidor:
    # Método construtor __init__: é chamado quando um objeto da classe é criado.
    # Ele recebe um parâmetro 'nome', que será utilizado para identificar o consumidor.
    def __init__(self, nome):
        self.nome = nome
        self.encomendas = []

    # Método adicionar_encomenda: Permite adicionar uma nova encomenda à lista de encomendas do consumidor.
    # O parâmetro 'encomenda' é a encomenda a ser adicionada à lista.
    def adicionar_encomenda(self, encomenda):
        self.encomendas.append(encomenda)
