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
