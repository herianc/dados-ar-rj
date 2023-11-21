def tratando_dias(mes: int) -> int:
    # Função que retorna o número de dias do mês + 1
    if mes in [1, 3, 5, 7, 8, 10, 12]:
        return 32
    elif mes in [4, 6, 9, 11]:
        return 31
    elif mes == 2:
        return 29


def tratando_dados(lista: list, mes: int, ano: int) -> list:
    """Função que trata os dados tirando os espaços em branco e convertendo os dados str para os tipos númericos (quando possível).
    A estrutura da lista recebida muda com o ano da consulta"""
    if ano > 2019:
        for i in range(len(lista)-1):
            if lista[i] == 'ND' or lista[i] == 'NM':
                lista[i] = 'NA'
            elif ',' in lista[i]:
                lista[i] = (lista[i].replace(',', '.'))
                lista[i] = float(lista[i])
            elif i == len(lista) - 1:
                continue
            else:
                lista[i] = int(lista[i])
    elif ano <= 2019:
        if ano == 2019 and mes == 12:
            for i in range(len(lista)-1):
                if lista[i] == 'ND' or lista[i] == 'NM':
                    lista[i] = 'NA'
                elif ',' in lista[i]:
                    lista[i] = (lista[i].replace(',', '.'))
                    lista[i] = float(lista[i])
                elif i == len(lista) - 1:
                    continue

                else:
                    lista[i] = int(lista[i])
        else:
            for i in range(len(lista)-2):

                if lista[i] == 'ND' or lista[i] == 'NM':
                    lista[i] = 'NA'
                elif ',' in lista[i]:
                    lista[i] = (lista[i].replace(',', '.'))
                    lista[i] = float(lista[i])
                elif i == len(lista) - 1:
                    continue

                else:
                    lista[i] = int(lista[i])

    return lista


def estacao_indisponivel() -> dict:
    '''Função que cria um dicionário com os dados faltantes quando a estação não está disponível '''
    dicionario = {}

    dicionario['MP10'] = 'NA'
    dicionario['MP2.5'] = 'NA'
    dicionario['O3'] = 'NA'
    dicionario['CO'] = 'NA'
    dicionario['NO2'] = 'NA'
    dicionario['SO2'] = 'NA'
    dicionario['IQAr'] = 'NA'
    dicionario['classificacao'] = 'NA'

    return dicionario


def criando_dicionario(lista: list, mes, ano) -> dict:
    '''Função que cria dicionário de acordo com o ano da consulta'''
    dicionario = {}
    if ano >= 2020:
        dicionario['MP10'] = lista[0]
        dicionario['MP2.5'] = lista[1]
        dicionario['O3'] = lista[2]
        dicionario['CO'] = lista[3]
        dicionario['NO2'] = lista[4]
        dicionario['SO2'] = lista[5]
        dicionario['IQAr'] = lista[6]
        dicionario['classificacao'] = lista[7]
    elif ano <= 2019:
        if ano == 2019 and mes == 12:
            dicionario['MP10'] = lista[0]
            dicionario['MP2.5'] = lista[1]
            dicionario['O3'] = lista[2]
            dicionario['CO'] = lista[3]
            dicionario['NO2'] = lista[4]
            dicionario['SO2'] = lista[5]
            dicionario['IQAr'] = lista[6]
            dicionario['classificacao'] = lista[7]
        else:
            dicionario['MP10'] = lista[0]
            dicionario['MP2.5'] = 'NA'
            dicionario['O3'] = lista[1]
            dicionario['CO'] = lista[2]
            dicionario['NO2'] = lista[3]
            dicionario['SO2'] = lista[4]
            dicionario['IQAr'] = lista[5]
            dicionario['classificacao'] = lista[-2]

    return dicionario
