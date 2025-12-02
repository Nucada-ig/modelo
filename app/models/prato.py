class Prato:
    def __init__(self, restaurante_id, nome, descricao, preco, categoria, disponivel=1, tempo_preparo=None, destaque=0, imagem=None, id_prato=None):
        self.__id_prato = id_prato
        self.__restaurante_id = restaurante_id
        self.__nome = nome
        self.__descricao = descricao
        self.__preco = preco
        self.__categoria = categoria
        self.__disponivel = disponivel
        self.__tempo_preparo = tempo_preparo
        self.__destaque = destaque
        self.__imagem = imagem

    @property
    def id_prato(self):
        return self.__id_prato

    @property
    def restaurante_id(self):
        return self.__restaurante_id

    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, novo_nome):
        self.__nome = novo_nome

    @property
    def descricao(self):
        return self.__descricao
    @descricao.setter
    def descricao(self, nova_descricao):
        self.__descricao = nova_descricao

    @property
    def preco(self):
        return self.__preco
    @preco.setter
    def preco(self, novo_preco):
        if novo_preco >= 0:
            self.__preco = novo_preco
        else:
            raise ValueError("O preço não pode ser negativo.")

    @property
    def categoria(self):
        return self.__categoria
    @categoria.setter
    def categoria(self, nova_categoria):
        self.__categoria = nova_categoria

    @property
    def disponivel(self):
        return self.__disponivel
    @disponivel.setter
    def disponivel(self, novo_disponivel):
        self.__disponivel = 1 if novo_disponivel else 0

    @property
    def tempo_preparo(self):
        return self.__tempo_preparo
    @tempo_preparo.setter
    def tempo_preparo(self, novo_tempo):
        self.__tempo_preparo = novo_tempo

    @property
    def destaque(self):
        return self.__destaque
    @destaque.setter
    def destaque(self, novo_destaque):
        self.__destaque = 1 if novo_destaque else 0

    @property
    def imagem(self):
        return self.__imagem
    @imagem.setter
    def imagem(self, nova_imagem):
        self.__imagem = nova_imagem