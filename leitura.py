import csv

from distancia import calcular_distancia_km


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
