# Consultor dos Índices de Poluição do Rio de Janeiro

Trabalho final da disciplina de Computação 2 na UFRJ. O trabalho consiste em criar um projeto que aborde tópicos de Programação Orientada a Objetos aplicados a assuntos do curso do discente (Bacharelado em Ciências Matemáticas e da Terra).<br>

Última atualização: Fev/2024

---
## Sumário 
- [Objetivo](https://github.com/herianc/dados_arRJ#objetivo)
- [Aplicação de POO e Bibliotecas Utilizadas](https://github.com/herianc/dados_arRJ#aplica%C3%A7%C3%A3o-de-poo-no-projeto)
- [Estrutura do Sistema](https://github.com/herianc/dados_arRJ#explicando-a-estrutura-do-sistema)
- [Dados Coletados](https://github.com/herianc/dados_arRJ#dados-coletados)
- [Imagens do Projeto](https://github.com/herianc/dados_arRJ#imagens-do-projeto)
---


## Ideia geral do projeto

Sistema de informação que facilita a obtenção dos dados de poluição do ar na cidade do Rio de Janeiro. A extração da informação é feita através da raspagem de dados do site do [boletim](https://jeap.rio.rj.gov.br/je-metinfosmac/boletim) de qualidade do ar

## Objetivo

Aplicação que realiza a Extração, Tratamento e o Carregamento (Pipeline ETL) dos índices de poluição do Rio. O objetivo principal é facilitar a obtenção dos dados mensais/semestrais/anuais das estações para medição/estudo da poluição nas estações de monitoramento do Rio, tendo em vista que o próprio boletim da Prefeitura do Rio disponibiliza **apenas dados diários**. Ao final de cada consulta um arquivo json é gerado com os dados estruturados e tratados e dando a opção ao usuário de obter uma planilha ou um arquivo csv. Além disso, oferece uma pré visualização dos dados obtidos na consulta.

<img src="https://github.com/herianc/dados_arRJ/blob/main/imagens/consulta.gif.gif?raw=true" width="810" height="480" />

---

## Aplicação de POO no projeto

- **Abstração (classe, objeto e método):**
Abstração de Consulta que tem os atributos (características) mês e/ou ano de consulta.

- **Herança (simples ou múltipla):**
Herança simples entre as classes ConsultaMensal -> ConsultaAnual e ConsultaMensal -> ConsultaSemestral.
- **Encapsulamento:**
O encapsulamento não foi utilizado no código, pois não encontramos aplicação para o conceito.
- **Polimorfismo**
As classes derivadas ConsultaAnual e ConsultaSemestral executam o método consulta() de forma diferente da superclasse ConsultaMensal.
- **Classe abstrata/interface:**  
Classe abstrata Consulta que é o “molde” para as classes ConsultaMensal, ConsultaAnual e ConsultaSemestral.
- **Tratamento de exceções:**  
Diversos tipos de tratamentos de exceções, principalmente na entrada do usuário, durante a execução da consulta e na persistência de dados.
- **Persistência de dados:**
Opções ao usuário de armazenar os dados coletados em arquivos csv, excel. Também foi implementado um “sistema de cache” onde dados consultados pelo usuário geram um json, evitando que consultas já realizadas demandem outra extração no site.
- **Uso de bibliotecas diversas:**
  - `requests`  - Requisição dos dados do site
  - `BeautifulSoup` - Tratamento e raspagem dos dados obtidos na requisição
  - `Pandas` - Manipulação e exportação de dados em formatos excel e csv
  - `Flet` - Interface gráfica
  - `Plotly` - Plotagem do Gráfico de Índice de Qualidade do Ar no Estado do RJ no mês consultado
  - Outras: `os`, `numpy`

---

## Explicando a estrutura do Sistema

O Sistema conta com 3 arquivos Python para diferentes funções.<br>

`interface.py` - É a parte da interface gráfica e de toda a lógica por trás das interações com o usuário.<br>

`webscraping.py` - É o módulo que contém todas as classes criadas para o projeto ConsultaMensal, ConsultaAnual, ConsultaSemestral. É onde ocorre o processo de raspagem de dados, estruturação dos dados coletados e saída dos arquivos em diferentes formatos.

`tratamento_dados.py`- É o módulo que contém funções pontuais para tratamentos de dados: Tratamento dos dados brutos tipo string para valores numéricos `int` e `float`; Criação de dicionários com os poluentes e os seus respectivos índices.

Entendendo o arquivo `webscraping.py`:<br>
A Classe abstrata `Consulta` contém os métodos abstratos `consulta()`, `obter_json()`, `obter_csv()`, `obter_excel()` que serão usadas nas demais subclasses.<br>

A  Super Classe do sistema é a `ConsultaMensal`, onde ocorre a lógica de repetição da raspagem dia a dia durante o mês passado no parâmetro. Através do método `ConsultaMensal.consulta()` que ocorre a raspagem diária durante o mês utilizando uma estrutura de repetição `for` com métodos da biblioteca Request e Beautiful Soup. Além disso, acontece a estruturação dos dados após a extração dos dados do site. <br> 

Os métodos `obter_json()`, `obter_csv()` e `obter_excel()` são métodos que executam funções das bibliotecas json/pandas para obter o os dados em diferentes tipos de arquivos.<br>

As demais classes executam o método `consulta()` da classe `ConsultaMensal` para os respectivos períodos de tempo utilizando o poliformismo para executar essas consultas no respectivo período de tempo.

---

## Dados Coletados

- 'MP10' - Material Particulado [µg/m³]
- 'MP2.5' - Material Particulado [µg/m³]
- 'O3' - Ozônio [µg/m³]
- 'CO' - Monóxido de Carbono [ppm]
- 'NO2' - Dióxido de Nitrogênio [µg/m³]
- 'SO2' - Dixódio de Enxofre [µg/m³]
- 'IQAr' - Índice de Qualidade do Ar [0, 400]
- 'classificacao' - Categorização da Qualidade do Ar

Para mais informações em relação as categorizações da Qualidade do Ar: [Acesse](https://jeap.rio.rj.gov.br/je-metinfosmac/boletim)

**Observações com relação aos dados:**

- MP2.5 passou a ser monitorado a partir de dez/2019.
- 1º Semestre de 2020 há muitos meses com dados indisponíveis (provavelmente devido a pandemia).
- A estação Copacabana esteve fora da listagem do site durante o ano de 2021

---

## Imagens do projeto
Site do Boletim de Qualidade do Ar da Prefeitura do Rio
![Boletim de Qualidade do Ar](https://github.com/herianc/dados_arRJ/blob/main/imagens/site.png?raw=true)

Menu Principal
![Menu Principal](https://github.com/herianc/dados_arRJ/blob/main/imagens/01_menu_principal.png?raw=true)

Página de Consulta Mensal
![Página de Consulta Mensal](https://github.com/herianc/dados_arRJ/blob/main/imagens/02_page_consulta_mensal.png?raw=true)

Página de Carregamento
![Página de Carregamento](https://github.com/herianc/dados_arRJ/blob/main/imagens/03_page_loading.png?raw=true)

Página de Consulta Finalizada
![Página de Consulta Finalizada](https://github.com/herianc/dados_arRJ/blob/main/imagens/04_page_cmensal_realizada.png?raw=true)

Gráfico Detalhado
![Gráfico IQAR](https://github.com/herianc/dados_arRJ/blob/main/imagens/09_gr%C3%A1fico.png?raw=true)

Página de Consulta Anual finalizada
![Página de Consulta Anual finalizada](https://github.com/herianc/dados_arRJ/blob/main/imagens/06_page_canual_realizada.png?raw=true)

Página de erro
![Página de erro](https://github.com/herianc/dados_arRJ/blob/main/imagens/08_page_erro.png?raw=true)



