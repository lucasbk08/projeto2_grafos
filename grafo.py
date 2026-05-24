from collections import defaultdict


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
