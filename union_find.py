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
