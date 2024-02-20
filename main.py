import sys
from node import Node
import itertools

arquivo_entrada = (sys.argv[1])


# Função para ler a primeira linha do arquivo
def ler_primeira_linha_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            linha = arquivo.readline().strip()  # Lê a primeira linha e remove espaços em branco
            if linha.startswith('(') and linha.endswith(')'):
                # Remova os parênteses externos
                linha = linha[1:-1]

                # Divida a linha nos elementos usando ','
                elementos = linha.split(',')

                # Extraia as partes relevantes
                alfabeto = elementos[0].replace("{","").replace("}","")
                estados = elementos[1].replace("{","").replace("}","")
                estado_inicial = elementos[3].replace("{","").replace("}","")
                estados_finais = elementos[4].replace("{","").replace("}","")

                # Converta as strings em listas e retorne os valores
                alfabeto = alfabeto.split(" ")
                estados = estados.split(" ")
                estados_finais = estados_finais.split(" ")

                return alfabeto, estados, estado_inicial, estados_finais

            else:
                print("A primeira linha do arquivo não está no formato esperado.")
                return None
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return None

# Função que inicializa o automato:
def inicializa_automato(nome_arquivo , alfabeto , estados , estados_finais , estado_inicial):
    automato = {}

    for estado in estados:
        if estado == estado_inicial:
            node_atual = Node()
            node_atual.eh_inicial = 1
            if estado in estados_finais:
                node_atual.eh_final = 1
            else:
                node_atual.eh_final = 0

            automato[estado] = node_atual
        else:
            node_atual = Node()
            node_atual.eh_inicial = 0
            if estado in estados_finais:
                node_atual.eh_final = 1
            else:
                node_atual.eh_final = 0

            automato[estado] = node_atual

    with open(nome_arquivo, 'r') as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            if numero_linha >= 2:
                linha = linha.replace(" ","").replace("\n","").split(",")

                estado_atual = linha[0]
                valor_recebido = linha[1]
                proximo_estado = linha[2]

                if valor_recebido in alfabeto:
                    automato[estado_atual].append_value(valor_recebido , proximo_estado)

    return automato


# Gera os novos estados do automato
def gera_lista_novos_estados(estados):
    combinacoes = []

    for r in range(1, len(estados) + 1):
        for combo in itertools.combinations(estados, r):
            combinacoes.append("".join(combo))
    return combinacoes

# Gera novos estados finais
def gera_lista_estados_finais(novos_estados , estados_finais):
    if novos_estados == None or estados_finais == None:
        raise "Erro"

    novos_estados_finais = []
    for estado in novos_estados:
        for antigo_estado_final in estados_finais:
            if antigo_estado_final in estado:
                novos_estados_finais.append(estado)

    return novos_estados_finais

# Concatenar strings do destino do automato
def unir_strings(lista):
    resultado = {}

    for item in lista:
        partes = item.split(' -> ')
        origem, destino = partes[0].split(' , '), partes[1]

        if origem[0] not in resultado:
            resultado[origem[0]] = {}

        if origem[1] not in resultado[origem[0]]:
            resultado[origem[0]][origem[1]] = set()

        resultado[origem[0]][origem[1]].add(destino)

    resultado_final = []
    for origem, destinos in resultado.items():
        for destino, valores in destinos.items():
            valor_final = ''.join(sorted(valores))  # Ordena e combina os valores únicos
            resultado_final.append(f"{origem} , {destino} -> {valor_final}")

    return resultado_final



# Função principal do programa
def main():
    resultado = ler_primeira_linha_arquivo(arquivo_entrada)

    alfabeto, estados, estado_inicial, estados_finais = resultado

    automato = inicializa_automato(arquivo_entrada , alfabeto , estados , estados_finais , estado_inicial)

    #verifica_palavra("acc" , automato)

    # Quais os passo a passos?
    ## 1) Gerar todos os estados possiveis e estados finais
    novos_estados = gera_lista_novos_estados(estados)
    novos_estados_finais = gera_lista_estados_finais(novos_estados , estados_finais)

    ## 2) Gerar a tabela do AFD para todos os estados possíveis
    str_result = []
    for novo_estado in novos_estados:
        # Varre a lista de todos os novos estados
        for letra in alfabeto:
            # Para cada novo estado , verifica todas as letras do alfabeto

            for estado in automato:
                # Para cada estado do automato criado , calcula para qual estados (ou estados) ele vai
                if estado in novo_estado:
                    # Caso seja um resultado com mais de um valor , Join nos resultados
                    estados_calc = "".join(automato[estado].calcula_estado(letra))

                    # Caso o resultado do calculo do automato retorne vazio (não encontrou um destino) então salva o resultado
                    if estados_calc != "":
                        result = f"{novo_estado} , {letra} -> {estados_calc}"
                        str_result.append(result)
    tabela_afd = unir_strings(str_result)


    ## 3) Montar a F' resultante
    string_alfabeto = []
    for letra in alfabeto:
        string_alfabeto.append(letra)
    string_alfabeto = " ".join(string_alfabeto)

    string_novos_estados = []
    for estado_novo in novos_estados:
        string_novos_estados.append(estado_novo)
    string_novos_estados = " ".join(string_novos_estados)

    string_estados_finais = []
    for estado_final in novos_estados_finais:
        string_estados_finais.append(estado_final)
    string_estados_finais = " ".join(string_estados_finais)

    with open("output.txt", "w") as arquivo:
        # Escreve no arquivo
        arquivo.write(f"({ {string_alfabeto} },{ {string_novos_estados} },X,{estado_inicial},{ {string_estados_finais} })\n")
        for i in tabela_afd:
            arquivo.write(f"{i}\n")


# Rodar o programa
main()