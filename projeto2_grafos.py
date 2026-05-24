"""
=============================================================
UNIVERSIDADE PRESBITERIANA MACKENZIE
Teoria dos Grafos - Projeto 2

Lucas Bacil Karam - 10434396
Israel Marcos Seixas Zibordi - 10444694

Tema:
    Malha aérea brasileira

Dataset:
    OpenFlights

Arquivos usados:
    - airports.dat.txt
    - routes.dat.txt

Conceitos aplicados:
    1. Árvore Geradora Mínima (AGM) - Algoritmo de Kruskal
    2. Coloração de Grafos - Algoritmo guloso

Ideia do projeto:
    Modelar aeroportos brasileiros como vértices e rotas aéreas
    como arestas. Depois, analisar o mesmo grafo usando dois
    conceitos diferentes da disciplina.

Modelagem:
    Vértices:
        Aeroportos brasileiros, identificados pelo código IATA.

    Arestas:
        Rotas diretas entre aeroportos brasileiros.

    Peso da aresta:
        Distância aproximada em quilômetros entre os aeroportos,
        calculada a partir da latitude e longitude.

    Grafo:
        Embora o dataset possua rotas direcionais, neste projeto
        as rotas são tratadas como não direcionadas, pois o foco é
        analisar conectividade e agrupamento dos aeroportos.
=============================================================
"""

# ============================================================
# IMPORTAÇÕES
# ============================================================

# Biblioteca padrão para ler arquivos CSV ou .dat separados por vírgula
import csv

# Biblioteca padrão para funções matemáticas
import math

# defaultdict facilita criar listas automaticamente dentro de dicionários
from collections import defaultdict

# NetworkX será usado apenas para gerar as imagens dos grafos
import networkx as nx

# Matplotlib será usado para salvar as imagens em .png
import matplotlib.pyplot as plt


# ============================================================
# 1. FUNÇÃO PARA CALCULAR DISTÂNCIA ENTRE AEROPORTOS
# ============================================================

def calcular_distancia_km(lat1, lon1, lat2, lon2):
    """
    Calcula a distância aproximada entre dois pontos da Terra.

    Os aeroportos possuem latitude e longitude no dataset.
    Com esses valores, usamos a fórmula de Haversine para calcular
    a distância aproximada entre os dois pontos.

    Essa distância será usada como peso da aresta no grafo.

    Parâmetros:
        lat1, lon1:
            Latitude e longitude do primeiro aeroporto.

        lat2, lon2:
            Latitude e longitude do segundo aeroporto.

    Retorno:
        Distância aproximada em quilômetros.
    """

    # Raio médio da Terra em quilômetros
    raio_terra = 6371

    # Converte graus para radianos, pois as funções trigonométricas usam radianos
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Diferença entre as latitudes e longitudes
    diferenca_lat = lat2 - lat1
    diferenca_lon = lon2 - lon1

    # Fórmula de Haversine
    a = (
        math.sin(diferenca_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(diferenca_lon / 2) ** 2
    )

    c = 2 * math.asin(math.sqrt(a))

    # Arredonda para deixar o resultado mais simples no relatório
    return round(raio_terra * c)


# ============================================================
# 2. LEITURA DOS AEROPORTOS BRASILEIROS
# ============================================================

def ler_aeroportos_brasil(nome_arquivo):
    """
    Lê o arquivo airports.dat.txt e filtra apenas aeroportos do Brasil.

    No arquivo airports.dat, os campos principais são:
        linha[1] -> nome do aeroporto
        linha[2] -> cidade
        linha[3] -> país
        linha[4] -> código IATA
        linha[6] -> latitude
        linha[7] -> longitude

    O código IATA é aquele código de 3 letras, como:
        GRU, CGH, GIG, BSB etc.

    Retorno:
        Um dicionário no formato:

        {
            "GRU": {
                "nome": "Guarulhos - Governador André Franco Montoro International Airport",
                "cidade": "Sao Paulo",
                "latitude": -23.435556,
                "longitude": -46.473057
            },
            ...
        }
    """

    aeroportos = {}

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)

        for linha in leitor:
            # Evita erro caso alguma linha esteja incompleta
            if len(linha) < 8:
                continue

            pais = linha[3]
            codigo_iata = linha[4]

            # Queremos apenas aeroportos do Brasil
            # Também ignoramos aeroportos sem código IATA válido
            if pais == "Brazil" and codigo_iata != "\\N":
                nome = linha[1]
                cidade = linha[2]
                latitude = float(linha[6])
                longitude = float(linha[7])

                aeroportos[codigo_iata] = {
                    "nome": nome,
                    "cidade": cidade,
                    "latitude": latitude,
                    "longitude": longitude
                }

    return aeroportos


# ============================================================
# 3. LEITURA DAS ROTAS ENTRE AEROPORTOS BRASILEIROS
# ============================================================

def ler_rotas_brasileiras(nome_arquivo, aeroportos):
    """
    Lê o arquivo routes.dat.txt e pega apenas rotas brasileiras.

    No arquivo routes.dat, os campos principais são:
        linha[2] -> aeroporto de origem
        linha[4] -> aeroporto de destino

    O objetivo é manter apenas as rotas em que:
        - a origem está no dicionário de aeroportos brasileiros;
        - o destino também está no dicionário de aeroportos brasileiros;
        - origem e destino são diferentes.

    Para cada rota válida, calculamos a distância entre os aeroportos.

    Retorno:
        Lista de rotas no formato:

        [
            ("GRU", "GIG", 338),
            ("GRU", "BSB", 854),
            ...
        ]
    """

    rotas = []

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)

        for linha in leitor:
            # Evita erro caso alguma linha esteja incompleta
            if len(linha) < 5:
                continue

            origem = linha[2]
            destino = linha[4]

            # Mantém apenas rotas em que origem e destino são aeroportos brasileiros
            if origem in aeroportos and destino in aeroportos and origem != destino:
                lat1 = aeroportos[origem]["latitude"]
                lon1 = aeroportos[origem]["longitude"]
                lat2 = aeroportos[destino]["latitude"]
                lon2 = aeroportos[destino]["longitude"]

                distancia = calcular_distancia_km(lat1, lon1, lat2, lon2)

                rotas.append((origem, destino, distancia))

    return rotas


# ============================================================
# 4. MONTAGEM DO GRAFO NÃO DIRECIONADO
# ============================================================

def montar_grafo_nao_direcionado(rotas):
    """
    Monta um grafo não direcionado a partir das rotas.

    O dataset de rotas é direcionado.
    Ou seja, ele pode ter:
        GRU -> GIG
        GIG -> GRU

    Para simplificar o projeto, vamos considerar isso como uma única aresta:
        GRU - GIG

    Isso faz sentido porque os conceitos escolhidos aqui são:
        - AGM, que normalmente trabalha com grafo não direcionado;
        - coloração, que também fica mais simples em grafo não direcionado.

    Retorno:
        grafo:
            Dicionário de adjacência.

            Exemplo:
            {
                "GRU": [("GIG", 338), ("BSB", 854)],
                "GIG": [("GRU", 338)]
            }

        arestas:
            Lista de arestas únicas.

            Exemplo:
            [
                ("GRU", "GIG", 338),
                ("GRU", "BSB", 854)
            ]
    """

    grafo = defaultdict(list)
    arestas_unicas = {}

    for origem, destino, distancia in rotas:
        # Ordena os nomes para evitar duplicação.
        # Assim, GRU-GIG e GIG-GRU viram a mesma chave.
        a = min(origem, destino)
        b = max(origem, destino)

        chave = (a, b)

        # Se essa aresta ainda não existe, adiciona.
        # Se já existe, ignora a repetição.
        if chave not in arestas_unicas:
            arestas_unicas[chave] = distancia

    # Monta a lista de adjacência do grafo
    for (origem, destino), distancia in arestas_unicas.items():
        grafo[origem].append((destino, distancia))
        grafo[destino].append((origem, distancia))

    # Monta a lista simples de arestas
    arestas = []

    for (origem, destino), distancia in arestas_unicas.items():
        arestas.append((origem, destino, distancia))

    return grafo, arestas


# ============================================================
# 5. FUNÇÕES AUXILIARES DO KRUSKAL - UNION-FIND
# ============================================================

def encontrar_pai(pai, vertice):
    """
    Encontra o representante do conjunto de um vértice.

    Essa função faz parte da estrutura Union-Find, usada no Kruskal
    para saber se dois vértices já estão conectados.

    Se dois vértices já têm o mesmo pai/representante, adicionar
    uma aresta entre eles formaria ciclo.
    """

    if pai[vertice] != vertice:
        pai[vertice] = encontrar_pai(pai, pai[vertice])

    return pai[vertice]


def unir(pai, v1, v2):
    """
    Une os conjuntos de dois vértices.

    Isso significa que, depois de adicionar uma aresta entre v1 e v2,
    eles passam a fazer parte do mesmo componente conectado.
    """

    raiz1 = encontrar_pai(pai, v1)
    raiz2 = encontrar_pai(pai, v2)

    if raiz1 != raiz2:
        pai[raiz2] = raiz1


# ============================================================
# 6. ALGORITMO DE KRUSKAL - ÁRVORE GERADORA MÍNIMA
# ============================================================

def kruskal(vertices, arestas):
    """
    Aplica o algoritmo de Kruskal.

    Objetivo:
        Encontrar uma Árvore Geradora Mínima, ou seja, uma seleção
        de arestas que conecta todos os vértices com o menor custo
        total possível, sem formar ciclos.

    Como funciona:
        1. Ordena todas as arestas pelo menor peso.
        2. Percorre as arestas nessa ordem.
        3. Adiciona uma aresta se ela não formar ciclo.
        4. Para quando todos os vértices estiverem conectados.

    No projeto:
        As arestas são rotas aéreas.
        O peso é a distância entre aeroportos.

    Interpretação:
        A AGM representa uma rede mínima de rotas que mantém os
        aeroportos conectados usando a menor distância total.
    """

    # Ordena as arestas da menor distância para a maior distância
    arestas_ordenadas = sorted(arestas, key=lambda x: x[2])

    # Inicialmente, cada vértice é pai dele mesmo
    pai = {}

    for vertice in vertices:
        pai[vertice] = vertice

    agm = []
    custo_total = 0

    for origem, destino, distancia in arestas_ordenadas:
        raiz_origem = encontrar_pai(pai, origem)
        raiz_destino = encontrar_pai(pai, destino)

        # Se as raízes são diferentes, a aresta não forma ciclo
        if raiz_origem != raiz_destino:
            agm.append((origem, destino, distancia))
            custo_total += distancia
            unir(pai, origem, destino)

    return agm, custo_total


# ============================================================
# 7. COLORAÇÃO GULOSA
# ============================================================

def coloracao_gulosa(grafo):
    """
    Aplica uma coloração gulosa no grafo.

    Objetivo:
        Atribuir cores aos vértices de modo que vértices vizinhos
        não tenham a mesma cor.

    Como funciona:
        1. Ordena os vértices pelo grau, do maior para o menor.
           O grau é a quantidade de conexões de um vértice.
        2. Para cada vértice, olha as cores já usadas pelos vizinhos.
        3. Escolhe a menor cor disponível.

    Importante:
        O algoritmo guloso é simples e rápido, mas não garante sempre
        o menor número possível de cores.

    No projeto:
        Os vértices são aeroportos.
        Dois aeroportos ligados por rota direta não podem ficar
        no mesmo grupo/cor.

    Interpretação:
        As cores podem representar grupos operacionais, zonas,
        turnos ou categorias diferentes.
    """

    cores = {}

    # Ordena os vértices por grau, do maior para o menor
    vertices = sorted(grafo.keys(), key=lambda v: len(grafo[v]), reverse=True)

    for vertice in vertices:
        cores_vizinhos = set()

        # Pega as cores dos vizinhos que já foram coloridos
        for vizinho, distancia in grafo[vertice]:
            if vizinho in cores:
                cores_vizinhos.add(cores[vizinho])

        # Escolhe a menor cor possível
        cor = 1

        while cor in cores_vizinhos:
            cor += 1

        cores[vertice] = cor

    return cores


# ============================================================
# 8. FUNÇÕES PARA GERAR IMAGENS DO GRAFO
# ============================================================

def criar_grafo_networkx(vertices, arestas):
    """
    Cria um grafo NetworkX apenas para visualização.

    O algoritmo principal do projeto não depende do NetworkX.
    Ele só é usado aqui para gerar as imagens .png.
    """

    G = nx.Graph()

    # Adiciona os vértices
    for vertice in vertices:
        G.add_node(vertice)

    # Adiciona as arestas com o peso/distância
    for origem, destino, distancia in arestas:
        G.add_edge(origem, destino, weight=distancia)

    return G


def obter_posicoes_geograficas(vertices, aeroportos):
    """
    Cria posições para desenhar o grafo usando longitude e latitude.

    Isso deixa a imagem parecida com a posição real dos aeroportos
    no mapa do Brasil.

    No Matplotlib:
        eixo x = longitude
        eixo y = latitude
    """

    posicoes = {}

    for vertice in vertices:
        longitude = aeroportos[vertice]["longitude"]
        latitude = aeroportos[vertice]["latitude"]

        posicoes[vertice] = (longitude, latitude)

    return posicoes


def gerar_imagem_grafo_completo(vertices, arestas, aeroportos):
    """
    Gera uma imagem com o grafo completo.

    Essa imagem mostra todas as rotas brasileiras consideradas.
    Pode ficar um pouco poluída se houver muitas rotas, mas serve
    para mostrar a estrutura geral da malha aérea.
    """

    G = criar_grafo_networkx(vertices, arestas)
    pos = obter_posicoes_geograficas(vertices, aeroportos)

    plt.figure(figsize=(13, 13))

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=450,
        node_color="lightblue",
        edgecolors="black"
    )

    nx.draw_networkx_edges(
        G,
        pos,
        alpha=0.35
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=7,
        font_weight="bold"
    )

    plt.title("Grafo completo - Malha aérea brasileira")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig("grafo_completo.png", dpi=200)
    plt.close()


def gerar_imagem_agm(vertices, arestas, aeroportos, agm):
    """
    Gera uma imagem da Árvore Geradora Mínima.

    A imagem mostra:
        - todas as rotas em cinza claro;
        - as rotas escolhidas pela AGM em destaque.

    Isso ajuda a visualizar o resultado do Kruskal.
    """

    G = criar_grafo_networkx(vertices, arestas)
    pos = obter_posicoes_geograficas(vertices, aeroportos)

    # Pega apenas as arestas da AGM, sem o peso
    arestas_agm = []

    for origem, destino, distancia in agm:
        arestas_agm.append((origem, destino))

    plt.figure(figsize=(13, 13))

    # Desenha todas as arestas em cinza claro
    nx.draw_networkx_edges(
        G,
        pos,
        alpha=0.15
    )

    # Desenha as arestas da AGM mais grossas
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=arestas_agm,
        width=2.5,
        edge_color="blue"
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=450,
        node_color="lightblue",
        edgecolors="black"
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=7,
        font_weight="bold"
    )

    plt.title("Árvore Geradora Mínima - Kruskal")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig("grafo_agm.png", dpi=200)
    plt.close()


def gerar_imagem_coloracao(vertices, arestas, aeroportos, cores):
    """
    Gera uma imagem mostrando a coloração dos aeroportos.

    Cada cor representa um grupo diferente.
    Aeroportos conectados diretamente por uma rota não devem ter
    a mesma cor.
    """

    G = criar_grafo_networkx(vertices, arestas)
    pos = obter_posicoes_geograficas(vertices, aeroportos)

    # Cria uma lista com a cor de cada vértice
    lista_cores = []

    for vertice in G.nodes():
        lista_cores.append(cores.get(vertice, 0))

    plt.figure(figsize=(13, 13))

    nx.draw_networkx_edges(
        G,
        pos,
        alpha=0.25
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=500,
        node_color=lista_cores,
        cmap=plt.cm.Set3,
        edgecolors="black"
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=7,
        font_weight="bold"
    )

    plt.title("Coloração gulosa dos aeroportos")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig("grafo_colorido.png", dpi=200)
    plt.close()


# ============================================================
# 9. PROGRAMA PRINCIPAL
# ============================================================

def main():
    """
    Função principal do programa.

    Ordem de execução:
        1. Lê os aeroportos brasileiros.
        2. Lê as rotas brasileiras.
        3. Monta o grafo não direcionado.
        4. Executa Kruskal.
        5. Executa coloração gulosa.
        6. Mostra os resultados no terminal.
        7. Gera imagens do grafo.
    """

    # Nomes dos arquivos usados no projeto
    arquivo_aeroportos = "airports.dat.txt"
    arquivo_rotas = "routes.dat.txt"

    # Lê os dados
    aeroportos = ler_aeroportos_brasil(arquivo_aeroportos)
    rotas = ler_rotas_brasileiras(arquivo_rotas, aeroportos)

    # Monta o grafo não direcionado
    grafo, arestas = montar_grafo_nao_direcionado(rotas)

    # Lista de vértices realmente usados no grafo
    # Aqui entram apenas aeroportos que aparecem em alguma rota brasileira
    vertices = list(grafo.keys())

    print("=" * 70)
    print("PROJETO 2 - TEORIA DOS GRAFOS")
    print("Tema: Malha aérea brasileira")
    print("Dataset: OpenFlights")
    print("Conceitos: AGM com Kruskal + Coloração gulosa")
    print("=" * 70)

    print()
    print("Quantidade de aeroportos brasileiros encontrados no dataset:", len(aeroportos))
    print("Quantidade de aeroportos usados no grafo:", len(vertices))
    print("Quantidade de rotas brasileiras usadas:", len(arestas))

    # --------------------------------------------------------
    # ALGORITMO 1: ÁRVORE GERADORA MÍNIMA
    # --------------------------------------------------------

    agm, custo_total = kruskal(vertices, arestas)

    print()
    print("=" * 70)
    print("1. ÁRVORE GERADORA MÍNIMA - KRUSKAL")
    print("=" * 70)

    print()
    print("Rotas escolhidas na AGM:")
    for origem, destino, distancia in agm:
        print(f"{origem} - {destino}: {distancia} km")

    print()
    print("Distância total da AGM:", custo_total, "km")
    print("Quantidade de arestas na AGM:", len(agm))

    # --------------------------------------------------------
    # ALGORITMO 2: COLORAÇÃO GULOSA
    # --------------------------------------------------------

    cores = coloracao_gulosa(grafo)

    if cores:
        quantidade_cores = max(cores.values())
    else:
        quantidade_cores = 0

    print()
    print("=" * 70)
    print("2. COLORAÇÃO GULOSA")
    print("=" * 70)

    print()
    print("Quantidade de cores usadas:", quantidade_cores)

    print()
    print("Cores atribuídas aos aeroportos:")
    for aeroporto in sorted(cores):
        cidade = aeroportos[aeroporto]["cidade"]
        print(f"{aeroporto} ({cidade}) -> Cor {cores[aeroporto]}")

    # --------------------------------------------------------
    # INTERPRETAÇÃO DOS RESULTADOS
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("INTERPRETAÇÃO")
    print("=" * 70)

    print()
    print("AGM:")
    print("A Árvore Geradora Mínima mostra uma rede de rotas capaz de conectar")
    print("os aeroportos brasileiros analisados usando a menor distância total possível.")

    print()
    print("Coloração:")
    print("A coloração separa aeroportos conectados diretamente em grupos diferentes.")
    print("Na prática, isso pode representar divisão de zonas, turnos ou grupos operacionais.")

    # --------------------------------------------------------
    # GERAÇÃO DAS IMAGENS
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("GERANDO IMAGENS...")
    print("=" * 70)

    gerar_imagem_grafo_completo(vertices, arestas, aeroportos)
    gerar_imagem_agm(vertices, arestas, aeroportos, agm)
    gerar_imagem_coloracao(vertices, arestas, aeroportos, cores)

    print()
    print("Imagens geradas com sucesso:")
    print("- grafo_completo.png")
    print("- grafo_agm.png")
    print("- grafo_colorido.png")

    print()
    print("=" * 70)
    print("Execução finalizada.")
    print("=" * 70)


# Essa linha faz o programa rodar apenas quando o arquivo é executado diretamente
if __name__ == "__main__":
    main()