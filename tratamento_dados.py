def tratando_dias(mes: int):
    if mes in [1, 3, 5, 7, 8, 10, 12]:
        return 32
    elif mes in [4, 6, 9, 11]:
        return 31
    elif mes == 2:
        return 29


def tratando_dados(lista: list) -> list:
    """Função que trata os dados tirando os espaços em branco e convertendo os dados str para os tipos númericos (quando possível)"""

    for i in range(len(lista)-1):
        if lista[i] == 'ND' or lista[i] == 'NM':
            continue
        elif ',' in lista[i]:
            lista[i] = (lista[i].replace(',', '.'))
            lista[i] = float(lista[i])
        elif i == len(lista) - 1:
            continue

        else:
            lista[i] = int(lista[i])

    return lista


def estacao_indisponivel():
    dicionario = {}

    dicionario['MP10'] = 'ND'
    dicionario['MP2.5'] = 'ND'
    dicionario['O3'] = 'ND'
    dicionario['CO'] = 'ND'
    dicionario['NO2'] = 'ND'
    dicionario['SO2'] = 'ND'
    dicionario['IQAr'] = 'ND'
    dicionario['classificacao'] = 'ND'

    return dicionario


def criando_dicionario(lista: list) -> dict:
    dicionario = {}

    dicionario['MP10'] = lista[0]
    dicionario['MP2.5'] = lista[1]
    dicionario['O3'] = lista[2]
    dicionario['CO'] = lista[3]
    dicionario['NO2'] = lista[4]
    dicionario['SO2'] = lista[5]
    dicionario['IQAr'] = lista[6]
    dicionario['classificacao'] = lista[7]

    return dicionario
