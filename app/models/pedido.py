from .prato import Prato
from .Endereco import Endereco
class Pedido:
    def __init__(self, numero, preco, observacao_p, forma_de_pagamento, status):
        self.__numero = numero
        self.__preco = preco
        self.__observacao_p = observacao_p
        self.__forma_de_pagamento = forma_de_pagamento
        self.__status = status
        self.cliente = None
        self.pratos = []

    @property
    def numero(self):
        return self._numero
    @numero.setter
    def numero(self, value):
        self._numero = value

    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, value):
        self._status = value

    @property
    def endereco_de_entrega(self):
        return self._endereco_de_entrega
    @endereco_de_entrega.setter
    def endereco_de_entrega(self, value):
        self._endereco_de_entrega = value

    @property
    def preco(self):
        return self._preco
    @preco.setter
    def preco(self, value):
        if value >= 0:
            self._preco = value
        else:
            raise ValueError("O preço não pode ser negativo.")
    @property
    def prato(self):
        return self._prato
    @prato.setter
    def prato(self, value):
        self._prato = value
    @property
    def observacao_p(self):
        return self._observacao_p
    @observacao_p.setter
    def observacao_p(self, value):
        self._observacao = value

    @property
    def forma_de_pagamento(self):
        return self._forma_de_pagamento
    @forma_de_pagamento.setter
    def forma_de_pagamento(self, forma):
      if forma in ["dinheiro", "cartão de crédito", "cartão de débito", "pix"]:
         self._forma_de_pagamento = forma
      else:
        print("Forma de pagamento inválida")
    #associação x endereço
    @property
    def endereco(self):
      return self._endereco
    @endereco.setter
    def endereco(self, end):
      if isinstance(end, Endereco):
        self._endereco = end
    #agregação x pratos
    @property
    def pratos(self):
      return self._pratos
    def adicionar_prato(self, prato):
      if isinstance(prato, Prato):
        self._pratos.append(prato)
      else:
        print("O valor atribuído a prato não é um objeto Prato válido.")
    def remover_prato(self, prato):
      if prato in self._pratos:
        self._pratos.remove(prato)
      else:
        print("O prato não está na lista de pratos do pedido.")