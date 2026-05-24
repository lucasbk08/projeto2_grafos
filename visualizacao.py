import networkx as nx
import matplotlib.pyplot as plt


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
