import math


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
