def tratando_dias(mes: int) -> int:
    # Função que retorna o número de dias do mês + 1
    if mes in [1, 3, 5, 7, 8, 10, 12]:
        return 32
    elif mes in [4, 6, 9, 11]:
        return 31
    elif mes == 2:
        return 29


def tratando_dados(lista: list, mes: int, ano: int) -> list:
    if ano > 2019 or (ano == 2019 and mes == 12):
        for i in range(len(lista)-1):
            if lista[i] == 'ND' or lista[i] == 'NM':  # Poluente não medido no dia
                lista[i] = 'NA'

            elif ',' in lista[i]:  # Dados decimais
                lista[i] = (lista[i].replace(',', '.'))
                lista[i] = float(lista[i])

            elif i == len(lista) - 1:  # Classificação EX: "Bom ou Moderado"
                continue

            else:
                lista[i] = int(lista[i])  # String de dígito inteiro
    else:
        for i in range(len(lista)-2):

            if lista[i] == 'ND' or lista[i] == 'NM':  # Poluente não medido no dia
                lista[i] = 'NA'

            elif ',' in lista[i]:  # Dados decimais
                lista[i] = (lista[i].replace(',', '.'))
                lista[i] = float(lista[i])

            elif i == len(lista) - 1:  # Classificação Ex: Bom ou Péssimo
                continue

            else:
                lista[i] = int(lista[i])  # String de digito inteiro
    return lista


def estacao_indisponivel() -> dict:
    '''Função que cria um dicionário com os dados NA quando a estação não está disponível'''
    dicionario = {}

    dicionario['MP10'] = 'NaN'
    dicionario['MP2.5'] = 'NaN'
    dicionario['O3'] = 'NaN'
    dicionario['CO'] = 'NA'
    dicionario['NO2'] = 'NA'
    dicionario['SO2'] = 'NA'
    dicionario['IQAr'] = 'NA'
    dicionario['classificacao'] = 'NA'

    return dicionario


def criando_dicionario(lista: list, mes, ano) -> dict:
    '''Função que cria dicionário de acordo com o ano da consulta'''
    dicionario = {}
    if ano >= 2020 or (ano == 2019 and mes == 12):
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
        dicionario['MP2.5'] = 'NA'  # MP2.5 não era medido
        dicionario['O3'] = lista[1]
        dicionario['CO'] = lista[2]
        dicionario['NO2'] = lista[3]
        dicionario['SO2'] = lista[4]
        dicionario['IQAr'] = lista[5]
        # Entre 2017 a 11/2019 a quantidade de colunas era menor
        dicionario['classificacao'] = lista[-2]

    return dicionario
