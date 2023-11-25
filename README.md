# Consultor dos Índices de Poluição do Rio de Janeiro (Irajá)

---
Projeto final da disciplina de Computação 2 na UFRJ. O trabalho consiste em criar um projeto que aborde tópicos de Programação Orientada a Objetos aplicados à assuntos do curso do discente (Ciências da Terra).

## Ideia geral do projeto

Sistema de informação que facilita a obtenção dos dados de poluição do ar na cidade do Rio de Janeiro, especificamente para o Bairro de Irajá. A obtenção da informação é feita através da raspagem de dados do site do [boletim](https://jeap.rio.rj.gov.br/je-metinfosmac/boletim) de qualidade do ar

---

## Objetivo

Aplicação que realiza a Extração, Tratamento e o Carregamento (Pipeline ETL) dos índices de poluição da estação de monitoramento de Irajá. O objetivo principal é facilitar a obtenção dos dados mensais/semestrais/anuais da estação para medição/estudo da poluição no bairro, tendo em vista que o próprio boletim **não disponibiliza** os dados de forma conjunta por períodos.

![Boletim de Qualidade do Ar](https://github.com/herianc/dados_arRJ/blob/main/imagens/site.png?raw=true)

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
`requests`  - Requisição dos dados do site
`BeautifulSoup` - tratamento e raspagem dos dados obtidos na requisição
`Pandas` - Manipulação de dados e exportação de dados em formatos excel e csv
`Flet` - Interface gráfica
`Plotly` - Plotagem do Gráfico de Índice de Qualidade do Ar no Estado do RJ no mês consultado
Outras: `os`, `numpy`

---

## Explicando a estrutura do Sistema

O Sistema conta com 3 arquivos Python para diferentes funções.

`main.py` - É a parte da interface gráfica e de toda a lógica por trás das interações com o usuário.

`webscraping.py` - É o módulo que contém todas as classes criadas para o projeto ConsultaMensal, ConsultaAnual, ConsultaSemestral. É onde ocorre o processo de raspagem de dados, estruturação dos dados coletados e saída dos arquivos em diferentes formatos.

`tratamento_dados.py`- É o módulo que contém funções pontuais para tratamentos de dados: Tratamento dos dados brutos tipo string para valores numéricos `int` e `float`; Criação de dicionários com os poluentes e os seus respectivos índices.

Entendendo o arquivo `webscraping.py`:
A Classe abstrata `Consulta` contém os métodos abstratos `consulta()`, `obter_json()`, `obter_csv()`, `obter_excel()` que serão usadas nas demais subclasses.

A  Super Classe do sistema é a `ConsultaMensal`, onde ocorre a lógica de repetição da raspagem dia a dia durante o mês passado no parâmetro. É neste método que ocorre a raspagem diária durante o mês utilizando uma estrutura de repetição for. Além disso, acontece a estruturação dos dados após a extração dos dados do site.  

Os métodos `obter_json()`, `obter_csv()`, `obter_excel()` e `obter_texto()` (este último para obter a tabela dos dados consultados no prompt) são métodos que executam funções das bibliotecas json/pandas para obter o os dados em diferentes tipos de arquivos.

As demais classes apenas aplicam o método `consulta()` da classe `ConsultaMensal` para os respectivos períodos de tempo, porém utilizando o poliformismo para executar essas consultas, tendo em vista que a consulta mensal é realizada por outro for para indicar o número de meses que serão consultados.  

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

---

## Imagens do projeto

Menu Principal
![Menu Principal](https://github.com/herianc/dados_arRJ/blob/main/imagens/01_menu_principal.png?raw=true)

Página de Consulta Mensal
![Página de Consulta Mensal](https://github.com/herianc/dados_arRJ/blob/main/imagens/02_page_consulta_mensal.png?raw=true)

Página de Carregamento
![Página de Carregamento](https://github.com/herianc/dados_arRJ/blob/main/imagens/03_page_loading.png?raw=true)

Página de Consulta Finalizada
![Página de Consulta Finalizada](https://github.com/herianc/dados_arRJ/blob/main/imagens/04_page_consulta_mensal_realizada.png?raw=true)

Página de Consulta Anual/Semestral
![Página de Consulta Anual/Semestral](https://github.com/herianc/dados_arRJ/blob/main/imagens/05_page_consulta_anual.png?raw=true)

Página de Carregamento
![Página de Carregamento](https://github.com/herianc/dados_arRJ/blob/main/imagens/06_page_loading_anual.png?raw=true)

Página de Consulta Anual finalizada
![Página de Consulta Anual finalizada](https://github.com/herianc/dados_arRJ/blob/main/imagens/07_page_consulta_anual_realizada.png?raw=true)

Página de Consulta Semestral finalizada
![Página de Consulta Semestral finalizada](https://github.com/herianc/dados_arRJ/blob/main/imagens/07_page_consulta_semestral_realizada.png?raw=true)

Página de erro
![Página de erro](https://github.com/herianc/dados_arRJ/blob/main/imagens/08_page_error.png?raw=true)

![Terminal consulta mensal finalizada](https://github.com/herianc/dados_arRJ/blob/main/imagens/09_consulta_mensal_terminal.png?raw=true)

Saída no terminal após consulta mensal.
