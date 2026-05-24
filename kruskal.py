from union_find import encontrar_pai, unir


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
