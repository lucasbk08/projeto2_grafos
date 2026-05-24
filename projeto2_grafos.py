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

from distancia import calcular_distancia_km
from leitura import ler_aeroportos_brasil, ler_rotas_brasileiras
from grafo import montar_grafo_nao_direcionado
from union_find import encontrar_pai, unir
from kruskal import kruskal
from coloracao import coloracao_gulosa
from visualizacao import (
    gerar_imagem_grafo_completo,
    gerar_imagem_agm,
    gerar_imagem_coloracao,
)


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