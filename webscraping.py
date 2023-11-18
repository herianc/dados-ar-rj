import requests
import json
from bs4 import BeautifulSoup
import tratamento_dados


def busca(mes: int, ano: int) -> dict:
    """
        Função que coleta os índices de poluição do ar da estação de Irajá no boletim de qualidade do ar da prefeitura do Rio de Janeiro, no período entre 2017 e 2023
    Args:
        mes (int): numero inteiro entre [1, 12] correspondente ao mês do ano
        ano (int): número inteiro entre [2017, 2023] correspondente ao ano

    Returns:
        dict: dicionário com os dados diários do mês selecionado
    """
    dados = {}
    inicio = None
    fim = None
    data_final = tratamento_dados.tratando_dias(mes)
    for dia in range(1, data_final):
        # Requisitos para o requests.get
        data = f'?data={dia}/{mes}/{ano}'
        url = 'https://jeap.rio.rj.gov.br/je-metinfosmac/boletim'+data

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'}

        requisicao = requests.get(url, headers=headers)
        site = BeautifulSoup(requisicao.content, 'html.parser')

        conteudo_selecionado = site.find_all(
            'td', attrs=('td_st_name', 'td_value_bold', 'td_value'))

        for i, linha in enumerate(conteudo_selecionado):
            if linha.get_text() == 'Irajá':  # Verificando se a estação de Irajá está na tabela
                inicio = i+1
                fim = inicio + 8
            else:  # Se não estiver, os dados estão indisponíveis
                dados_final = tratamento_dados.estacao_indisponivel()

        if inicio and fim:
            lista_selecionada = conteudo_selecionado[inicio:fim]
            dados_brutos = []
            for dado in lista_selecionada:
                dados_brutos.append(dado.text.strip())
            if dados_brutos[1] != 'Temporariamente indisponível':
                dados_tratados = tratamento_dados.tratando_dados(dados_brutos)
                dados_final = tratamento_dados.criando_dicionario(
                    dados_tratados)
            else:
                dados_final = tratamento_dados.estacao_indisponivel()

        dados[f'{dia}-{mes}-{ano}'] = dados_final
        print(dia, dados[f'{dia}-{mes}-{ano}'])

    with open(f'dados_{mes}-{ano}.json', 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

    return dados


dados = busca(5, 2022)
