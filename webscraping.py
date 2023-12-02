from abc import ABC, abstractmethod
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from tratamento_dados import criando_dicionario, estacao_indisponivel, tratando_dados, dias_do_mes
from os import mkdir
import datetime as dt


class Consulta(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def consulta(self):
        pass

    @abstractmethod
    def obter_json(self):
        pass

    @abstractmethod
    def obter_csv(self):
        pass

    @abstractmethod
    def obter_excel(self):
        pass


class ConsultaMensal(Consulta):
    def __init__(self) -> None:
        self.dados_mes = {}  # dicionário que conterá todos os dados obtidos na consulta
        self.mes = None  # atributo para saber o mês consultado
        self.ano = None  # atributo para saber o ano consultado
        self.estacao = None  # atributo para saber a estação que será consultada

        try:
            mkdir('./dados')  # cria o diretório onde os dados serão salvos
        except FileExistsError:
            pass

    def consulta(self, estacao, mes: int, ano: int) -> dict:
        '''Método que realiza a consulta no site do boletim de dados de qualidade do ar'''
        self.mes = mes
        self.ano = ano
        self.estacao = estacao
        print(estacao, mes)
        try:
            dados_do_dia = estacao_indisponivel()

            inicio = None
            fim = None
            fim_do_mes = dias_do_mes(mes)

            # For para requisição dos dados desde o primeiro dia do mês até o ultimo
            for dia in range(1, fim_do_mes):
                data = f'?data={dia}/{mes}/{ano}'
                url = 'https://jeap.rio.rj.gov.br/je-metinfosmac/boletim'+data

                site = requests.get(url)  # Caso apresente erro headers=headers
                conteudo = BeautifulSoup(site.content, 'html.parser')

                conteudo_selecionado = conteudo.find_all(
                    'td', attrs=('td_st_name', 'td_value_bold', 'td_value'))

                ## DADOS EM HTML ##
                # Pré tratamento dos dados
                # For para saber se a Estação de Irajá está disponível no site  (Caso esteja, pega a sua posição na lista)
                for i, linha in enumerate(conteudo_selecionado):
                    if linha.get_text() == estacao:
                        # Coletando a posição de inicio e fim do conteúdo desejado
                        inicio = i+1
                        if ano >= 2020 or (ano == 2019 and mes >= 11 and dia >= 19):
                            fim = inicio + 8
                        else:
                            fim = inicio + 7
                    else:
                        dados_do_dia = estacao_indisponivel()

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
                            dados_do_dia = criando_dicionario(
                                dados_tratados, dia, self.mes, self.ano)
                        else:
                            # Se nenhuma condição foi verdadeira, a estação está com dados indisponíveis
                            dados_do_dia = estacao_indisponivel()

                data = dt.date(ano, mes, dia)

                # FIM DA REQUISIÇÃO (APENAS UM DIA)
                # Guardando o dicionário dos dados do dia no dicionário do mes
                self.dados_mes[f'{data}'] = dados_do_dia
                print(data, self.dados_mes[f'{data}'])

        except ConnectionError:
            print('Erro de Conexão/Internet')
        except:
            raise Exception

        return self.dados_mes

    def obter_json(self):
        estacao = self.estacao.replace(' ', '_').lower()
        with open(f'./dados/{estacao}{self.ano}-{self.mes}.json', 'w') as arquivo:
            json.dump(self.dados_mes, arquivo, indent=4)

    def obter_csv(self):
        try:
            mkdir('./csv')
        except FileExistsError:
            pass
        estacao = self.estacao.replace(' ', '_').lower()
        df = pd.DataFrame(self.dados_mes)
        df = df.transpose()
        df.to_csv(f'./csv/{estacao}{self.ano}-{self.mes}.csv')

    def obter_excel(self):
        try:
            mkdir('./excel')
        except FileExistsError:
            pass
        estacao = self.estacao.replace(' ', '_').lower()
        df = pd.DataFrame(self.dados_mes)
        df = df.transpose()
        df.to_excel(f'./excel/{estacao}{self.ano}-{self.mes}.xlsx')


class ConsultaAnual(ConsultaMensal):
    def __init__(self):
        super().__init__()
        self.dados_ano = {}
        self.ano = None
        self.estacao = None

    def consulta(self, estacao: str, ano: int):
        self.ano = ano
        self.estacao = estacao

        # For que realiza a raspagem dos dados durante todo o ano
        for mes in range(1, 13):
            self.dados_ano = ConsultaMensal.consulta(
                self, estacao, mes, self.ano)

        return self.dados_ano

    def obter_json(self):
        estacao = self.estacao.replace(' ', '_').lower()
        with open(f'./dados/{estacao}{self.ano}.json', 'w') as arquivo:
            json.dump(self.dados_ano, arquivo, indent=4)

    def obter_csv(self):
        try:
            mkdir('./csv')
        except FileExistsError:
            pass

        estacao = self.estacao.replace(' ', '_').lower()
        df = pd.DataFrame(self.dados_ano)
        df = df.transpose()
        df.to_csv(f'./csv/{estacao}{self.ano}.csv')

    def obter_excel(self):
        try:
            mkdir('./excel')
        except FileExistsError:
            ...

        df = pd.DataFrame(self.dados_ano)
        df = df.transpose()
        df.to_excel(f'./excel/dados{self.ano}.xlsx')


class ConsultaSemestral(ConsultaMensal):
    def __init__(self) -> None:
        super().__init__()
        self.dados_semestre = {}
        self.semestre = None

        # Criando a pasta onde os dados serão guardados
        try:
            mkdir('./dados')
        except FileExistsError:
            pass

    def consulta(self, estacao, semestre: int, ano: int) -> dict:
        self.dados_semestre = {}
        if semestre == 1:
            self.semestre = 1
            self.ano = ano

            # For que realiza a raspagem no primeiro semestre
            for mes in range(1, 7):
                print(f'Consultando mês {mes}...\nPor favor aguarde.')
                self.dados_semestre = ConsultaMensal.consulta(
                    self, estacao, mes, self.ano)

            print('Consulta semestral finalizada')
            return self.dados_semestre
        if semestre == 2:
            self.semestre = 2
            self.ano = ano

            # For que realiza a raspagem no segundo semestre
            for mes in range(7, 13):
                print(f'Consultando mês {mes}...\nPor favor aguarde.')
                self.dados_semestre = ConsultaMensal.consulta(
                    self, estacao, mes, self.ano)

            print('Consulta anual finalizada')
            return self.dados_semestre

    def obter_json(self):
        estacao = self.estacao.replace(' ', '_').lower()
        with open(f'./dados/{estacao}{self.ano}-semestre{self.semestre}.json', 'w') as arquivo:
            json.dump(self.dados_semestre, arquivo, indent=4)

    def obter_csv(self):
        try:
            mkdir('.\csv')
        except FileExistsError:
            pass

        estacao = self.estacao.replace(' ', '_').lower()

        df = pd.DataFrame(self.dados_semestre)
        df = df.transpose()
        df.to_csv(f'.\csv\{estacao}{self.ano}-semestre{self.semestre}.csv')

    def obter_excel(self):
        try:
            mkdir('.\excel')
        except FileExistsError:
            ...

        estacao = self.estacao.replace(' ', '_').lower()
        df = pd.DataFrame(self.dados_mes)
        df = df.transpose()
        df.to_excel(
            f'.\excel\{estacao}{self.ano}-semestre{self.semestre}.xlsx')
