import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from tratamento_dados import criando_dicionario, estacao_indisponivel, tratando_dados, tratando_dias


class ConsultaMensal:
    def __init__(self) -> None:
        self.dados_mes = {}  # dicionário que conterá todos os dados obtidos na consulta
        self.mes = None  # atributo para saber o mês consultado
        self.ano = None  # atributo para saber o ano consultado

    def consulta(self, mes: int, ano: int) -> dict:
        '''Método que realiza a consulta no site do boletim de dados de qualidade do ar'''

        self.mes = mes
        self.ano = ano
        try:
            # Período que nenhuma estação esteve disponível
            if mes == 6 and ano == 2020:
                dados_final = estacao_indisponivel()

            inicio = None
            fim = None
            data_final = tratando_dias(mes)

            # For para requisição dos dados desde o primeiro dia do mês até o ultimo
            for dia in range(1, data_final):
                data = f'?data={dia}/{mes}/{ano}'
                url = 'https://jeap.rio.rj.gov.br/je-metinfosmac/boletim'+data

                site = requests.get(url)  # Caso apresente erro headers=headers
                conteudo = BeautifulSoup(site.content, 'html.parser')

                conteudo_selecionado = conteudo.find_all(
                    'td', attrs=('td_st_name', 'td_value_bold', 'td_value'))

                ## DADOS EM HTML ##

                # For para saber se a Estação de Irajá está disponível no site  (Caso esteja, pega a sua posição na lista)
                for i, linha in enumerate(conteudo_selecionado):
                    if linha.get_text() == 'Irajá':
                        # Coletando a posição de inicio e fim do conteúdo desejado
                        inicio = i+1
                        fim = inicio + 8

                    else:  # Se não estiver, os dados estão indisponíveis
                        dados_final = estacao_indisponivel()

                ## REALIZANDO O TRATAMENTO DOS DADOS##

                # Verificando se existe as variaveis inicio e fim (confirmando se a estação realmente foi encontrada)
                if inicio and fim:
                    lista_selecionada = conteudo_selecionado[inicio:fim]
                    dados_brutos = []
                    for dado in lista_selecionada:
                        dados_brutos.append(dado.text.strip())
                        # Verificando se os dados da estação estão disponíveis
                    if len(dados_brutos) > 0:
                        # A primeira posição da lista indica ou não se a estação está com dados disponíveis
                        # É preciso realizar esta etapa pois nem sempre que a estação está no site os dados estão disponíveis
                        if dados_brutos[0] != 'Temporariamente indisponível' and dados_brutos[0] != 'Temporariamente desativada':

                            # Transformando digistos em int ou float
                            dados_tratados = tratando_dados(
                                dados_brutos, self.mes, self.ano)
                            # Criando o dicionário que armazena cada valor a seu poluente
                            dados_final = criando_dicionario(
                                dados_tratados, self.mes, self.ano)
                        else:
                            # Se nenhuma condição foi verdadeira, a estação está com dados indisponíveis
                            dados_final = estacao_indisponivel()

                # FIM DA REQUISIÇÃO (APENAS UM DIA)

                # Guardando o dicionário dos dados do dia no dicionário do mes
                self.dados_mes[f'{dia}-{self.mes}-{self.ano}'] = dados_final
                print(dia, self.dados_mes[f'{dia}-{self.mes}-{self.ano}'])

        except ConnectionError:
            print('Erro de Conexão/Internet')

        return self.dados_mes

    def obter_json(self):
        with open(f'dados\dados{self.mes}-{self.ano}.json', 'w') as arquivo:
            json.dump(self.dados_mes, arquivo, indent=4)

    def obter_csv(self):
        df = pd.DataFrame(self.dados_mes)
        df = df.transpose()
        df.to_csv(f'dados\dados{self.mes}-{self.ano}.csv')

    def obter_excel(self):
        df = pd.DataFrame(self.dados_mes)
        df = df.transpose()
        df.to_excel(f'dados\dados{self.mes}-{self.ano}.xlsx')

    def obter_texto(self):
        df = pd.DataFrame(self.dados_mes)
        df = df.transpose()
        return df.to_string()


class ConsultaAnual(ConsultaMensal):
    def __init__(self):
        super().__init__()
        self.dados_ano = None
        self.ano = None

    def consulta(self, ano: int):
        self.dados_ano = {}
        self.ano = ano
        print('Iniciando consulta anual... Esse procedimento pode levar alguns minutos\nPor favor, aguarde.')

        # For que realiza a raspagem dos dados durante todo o ano
        for mes in range(1, 13):
            self.dados_ano = ConsultaMensal.consulta(self, mes, self.ano)

        print('Consulta anual finalizada')
        return self.dados_ano

    def obter_json(self):
        with open(f'dados\dados{self.ano}.json', 'w') as arquivo:
            json.dump(self.dados_ano, arquivo, indent=4)

    def obter_csv(self):
        df = pd.DataFrame(self.dados_ano)
        df = df.transpose()
        df.to_csv(f'dados\dados{self.ano}.csv')

    def obter_excel(self):
        df = pd.DataFrame(self.dados_ano)
        df = df.transpose()
        df.to_excel(f'dados\dados{self.ano}.xlsx')


class ConsultaSemestral(ConsultaMensal):
    def __init__(self) -> None:
        super().__init__()
        self.dados_semestre = None
        self.semestre = None

    def consulta(self, semestre: int, ano: int) -> dict:
        self.dados_semestre = {}
        if semestre == 1:
            self.semestre = 1
            self.ano = ano

            # For que realiza a raspagem no primeiro semestre
            for mes in range(1, 7):
                print(f'Consultando mês {mes}...\nPor favor aguarde.')
                self.dados_semestre = ConsultaMensal.consulta(
                    self, mes, self.ano)

            print('Consulta semestral finalizada')
            return self.dados_semestre
        if semestre == 2:
            self.semestre = 2
            self.ano = ano

            # For que realiza a raspagem no segundo semestre
            for mes in range(6, 13):
                print(f'Consultando mês {mes}...\nPor favor aguarde.')
                self.dados_semestre = ConsultaMensal.consulta(
                    self, mes, self.ano)

            print('Consulta anual finalizada')
            return self.dados_semestre

    def obter_json(self):
        with open(f'dados\dados{self.ano}-semestre{self.semestre}.json', 'w') as arquivo:
            json.dump(self.dados_semestre, arquivo, indent=4)

    def obter_csv(self):
        df = pd.DataFrame(self.dados_semestre)
        df = df.transpose()
        df.to_csv(f'dados\dados{self.ano}-semestre{self.semestre}.csv')

    def obter_excel(self):
        df = pd.DataFrame(self.dados_mes)
        df = df.transpose()
        df.to_excel(f'dados\dados{self.ano}-semestre{self.semestre}.xlsx')
