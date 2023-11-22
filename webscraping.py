import requests
import json
from bs4 import BeautifulSoup
import tratamento_dados
import pandas as pd

'''TRATAR EXCEÇÕES
- Limitar os anos de requisição
    - [2017, 2023] Consulta Mensal
    - [2017, 2022] Consulta Anual
- Tratar possíveis erros de conexão na requisição
'''


class ConsultaMensal:
    def __init__(self) -> None:
        self.dados_mes = {}
        self.mes = None
        self.ano = None

    def consulta(self, mes: int, ano: int) -> dict:

        try:
            if self.__class__.__name__ == 'ConsultaMensal':
                print(
                    f'Iniciando consulta mensal...\nO procedimento pode demorar alguns segundos. Por favor, aguarde.')
            self.mes = mes
            self.ano = ano

            if mes == 6 and ano == 2020:
                # Período que nenhuma estação esteve disponível
                dados_final = tratamento_dados.estacao_indisponivel()

            inicio = None
            fim = None
            data_final = tratamento_dados.tratando_dias(mes)

            # For para requisição dos dados dia a dia
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
                        dados_final = tratamento_dados.estacao_indisponivel()

                ## REALIZANDO O TRATAMENTO DOS DADOS##

                # Verificando se existe as variaveis inicio e fim (confirmando se a estação realmente foi encontrada)
                if inicio and fim:
                    lista_selecionada = conteudo_selecionado[inicio:fim]
                    dados_brutos = []
                    for dado in lista_selecionada:
                        dados_brutos.append(dado.text.strip())
                        # Verificando se os dados da estação estão disponíveis
                    if len(dados_brutos) > 0:
                        if dados_brutos[0] != 'Temporariamente indisponível' and dados_brutos[0] != 'Temporariamente desativada':
                            dados_tratados = tratamento_dados.tratando_dados(
                                dados_brutos, self.mes, self.ano)
                            dados_final = tratamento_dados.criando_dicionario(
                                dados_tratados, self.mes, self.ano)
                        else:
                            dados_final = tratamento_dados.estacao_indisponivel()

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
        for mes in range(1, 13):
            print(f'Consultando mês {mes}...\nPor favor aguarde.')
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
            print(
                'Iniciando consulta anual... Esse procedimento pode levar alguns minutos\nPor favor, aguarde.')
            for mes in range(1, 7):
                print(f'Consultando mês {mes}...\nPor favor aguarde.')
                self.dados_semestre = ConsultaMensal.consulta(
                    self, mes, self.ano)

            print('Consulta semestral finalizada')
            return self.dados_semestre
        if semestre == 2:
            self.semestre = 2
            self.ano = ano
            print(
                'Iniciando consulta anual... Esse procedimento pode levar alguns minutos\nPor favor, aguarde.')
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
