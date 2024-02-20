class Node:
    eh_inicial = 0
    eh_final = 0
    valor_recebido = []
    destino = []

    def __init__(self):
        self.eh_inicial = 0
        self.valor_recebido = []
        self.destino = []

    def append_value(self , letra , destino):
        if len(self.valor_recebido) == len(self.destino):
            self.valor_recebido.append(letra)
            self.destino.append(destino)
        else:
            raise "Erro"

    def set_inicial(self , inicial):
        if(inicial == 0 | inicial == 1):
            self.eh_inicial = inicial
        else:
            raise "Erro"

    def set_final(self , final):
        if(final == 0 | final == 1):
            self.eh_final = final
        else:
            raise "Erro"

    def get_eh_inicial(self):
        return self.eh_inicial

    def get_eh_final(self):
        return self.eh_final

    def get_valores_recebidos(self):
        return self.valor_recebido

    def get_destinos(self):
        return self.destino

    def get_infos(self):
        if self.eh_inicial == 1:
            print("O node é estado inicial")
        else:
            print("O node NÃO é estado inicial")

        if self.eh_final == 1:
            print("O node é estado final")
        else:
            print("O node NÃO é estado final")

        if len(self.valor_recebido) == len(self.destino):
            for i in range(len(self.valor_recebido)):
                letra = self.valor_recebido[i]
                destino = self.destino[i]
                print(f"Com a letra '{letra}' vai para o estado '{destino}'")
            print("------------------------")
        else:
            raise "Erro"

    def calcula_estado(self , valor):
        estados_finais = []
        for i in range(len(self.valor_recebido)):
            if self.valor_recebido[i] == valor:
                estados_finais.append(self.destino[i])

        return estados_finais