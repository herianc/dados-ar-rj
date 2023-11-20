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
- Criar um método para consulta de dados semestrais 
'''


class ConsultaMensal:
    def __init__(self) -> None:
        self.dados_mes = {}
        self.mes = None
        self.ano = None

    def consulta(self, mes: int, ano: int) -> dict:

        if self.__class__.__name__ == 'ConsultaMensal':
            print(f'Iniciando consulta mensal...\nO procedimento pode demorar alguns segundos. Por favor, aguarde.')
        self.mes = mes
        self.ano = ano

        inicio = None
        fim = None
        data_final = tratamento_dados.tratando_dias(mes)
        for dia in range(1, data_final):
            # Requisitos para o requests.get
            data = f'?data={dia}/{mes}/{ano}'
            url = 'https://jeap.rio.rj.gov.br/je-metinfosmac/boletim'+data

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'}

            site = requests.get(url)  # Caso apresente erro headers=headers
            conteudo = BeautifulSoup(site.content, 'html.parser')

            conteudo_selecionado = conteudo.find_all(
                'td', attrs=('td_st_name', 'td_value_bold', 'td_value'))

            for i, linha in enumerate(conteudo_selecionado):
                if linha.get_text() == 'Irajá':  # Verificando se a estação de Irajá está na tabela
                    # Coletando a posição de inicio e fim do conteúdo desejado
                    inicio = i+1
                    fim = inicio + 8
                else:  # Se não estiver, os dados estão indisponíveis
                    dados_final = tratamento_dados.estacao_indisponivel()

            # Verificando se existe as variaveis inicio e fim (confirmando se a estação realmente foi encontrada)
            if inicio and fim:
                lista_selecionada = conteudo_selecionado[inicio:fim]
                dados_brutos = []
                for dado in lista_selecionada:
                    dados_brutos.append(dado.text.strip())
                    # Verificando se os dados da estação estão disponíveis
                if dados_brutos[0] != 'Temporariamente indisponível' and dados_brutos[0] != 'Temporariamente desativada':
                    dados_tratados = tratamento_dados.tratando_dados(
                        dados_brutos, self.mes, self.ano)
                    dados_final = tratamento_dados.criando_dicionario(
                        dados_tratados, self.mes, self.ano)
                else:
                    dados_final = tratamento_dados.estacao_indisponivel()

            self.dados_mes[f'{dia}-{self.mes}-{self.ano}'] = dados_final
            print(dia, self.dados_mes[f'{dia}-{self.mes}-{self.ano}'])
        return self.dados_mes

    def obter_json(self):
        with open(f'dados{self.mes}-{self.ano}.json', 'w') as arquivo:
            json.dump(self.dados_mes, arquivo, indent=4)

    def obter_csv(self):
        df = pd.DataFrame(self.dados_mes)
        df = df.transpose()
        df.to_csv(f'dados{self.mes}-{self.ano}.csv')

    def obter_excel(self):
        df = pd.DataFrame(self.dados_mes)
        df = df.transpose()
        df.to_excel(f'dados{self.mes}-{self.ano}.xlsx')

    def obter_texto(self):
        df = pd.DataFrame(self.dados_mes)
        df = df.transpose()
        return df.to_string()


class ConsultaAnual(ConsultaMensal):
    def __init__(self):
        super().__init__()
        self.dados_ano = {}
        self.ano = None

    def consulta(self, ano: int):

        self.ano = ano
        print('Iniciando consulta anual... Esse procedimento pode levar alguns minutos\nPor favor, aguarde.')
        for mes in range(1, 13):
            print(f'Consultando mês {mes}...\nPor favor aguarde.')
            match mes:

                case 1:
                    self.dados_ano[f'Jan-{self.ano}'] = ConsultaMensal.consulta(self, mes,
                                                                                self.ano)
                case 2:
                    self.dados_ano[f'Fev-{self.ano}'] = ConsultaMensal.consulta(self, mes,
                                                                                self.ano)
                case 3:
                    self.dados_ano[f'Mar-{self.ano}'] = ConsultaMensal.consulta(self, mes,
                                                                                self.ano)
                case 4:
                    self.dados_ano[f'Abr-{self.ano}'] = ConsultaMensal.consulta(self, mes,
                                                                                self.ano)
                case 5:
                    self.dados_ano[f'Mai-{self.ano}'] = ConsultaMensal.consulta(self, mes,
                                                                                self.ano)
                case 6:
                    self.dados_ano[f'Jun-{self.ano}'] = ConsultaMensal.consulta(self, mes,
                                                                                self.ano)
                case 7:
                    self.dados_ano[f'Jul-{self.ano}'] = ConsultaMensal.consulta(self, mes,
                                                                                self.ano)
                case 8:
                    self.dados_ano[f'Ago-{self.ano}'] = ConsultaMensal.consulta(self, mes,
                                                                                self.ano)
                case 9:
                    self.dados_ano[f'Set-{self.ano}'] = ConsultaMensal.consulta(self, mes,
                                                                                self.ano)
                case 10:
                    self.dados_ano[f'Out-{self.ano}'] = ConsultaMensal.consulta(self, mes,
                                                                                self.ano)
                case 11:
                    self.dados_ano[f'Nov-{self.ano}'] = ConsultaMensal.consulta(self, mes,
                                                                                self.ano)
                case 12:
                    self.dados_ano[f'Dez-{self.ano}'] = ConsultaMensal.consulta(self, mes,
                                                                                self.ano)
        print('Consulta anual finalizada')
        return self.dados_ano

    def obter_json(self):
        with open(f'dados{self.ano}.json', 'w') as arquivo:
            json.dump(self.dados_ano, arquivo, indent=4)
