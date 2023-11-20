from webscraping import ConsultaMensal, ConsultaAnual

'''
Métodos disponíveis em ConsultaMensal
consulta_mes.consulta(mes, ano) mes e ano são numeros inteiros correspondentes a data
consulta_mes.obter_json()
consulta_mes.obter_csv()
consulta_mes.obter_excel()

Métodos de ConsultaAnual:
consulta_ano.consulta(ano) permite consulta entre 2017 e 2022
consulta_ano.obter_json()


As consultas serão mostradas dia a dia até o fim.

para chamar os métodos obter é preciso realizar a consulta antes.
'''


consulta_mes = ConsultaMensal()  # Instânciando a classe.
consulta_ano = ConsultaAnual()  # Instânciando a classe.


# Fazendo a requisição de Fev, 2023 e armazenando em uma variável.
dados = consulta_mes.consulta(10, 2022)
print()
print(consulta_mes.obter_texto())

#
