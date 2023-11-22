# Web Scraping com Python

---

## Resumo

 ---

 Mini projeto de Web Scraping para coletar dados do **[Boletim de Qualidade do Ar da Prefeitura do Rio de Janeiro](https://jeap.rio.rj.gov.br/je-metinfosmac/boletim)**. Este projeto tem o objetivo de facilitar a coleta dos dados no site da prefeitura, eliminando o trabalho manual.
 Atualmente o algoritmo se limita aos dados diários da Estação de Irajá, tendo em vista que é a estação com maior número de medições disponíveis.  
 Os dados se limitam ao ano de **2017 até o ano atual (2023)**, limitação devida ao site.

## Bibliotecas e Frameworks utilizados no projeto

---

`requests` - Para requisição do conteúdo do site
`BeautifulSoup` - Para raspagem e tratamento do conteúdo do site
pandas
`json` - Para armazenamento dos dados coletados
openpyxl
plotly

## Dados Coletados

---

- 'MP10' - Material Particulado [µg/m³]
- 'MP2.5' - Material Particulado [µg/m³]
- 'O3' - Ozônio [µg/m³]
- 'CO' - Monóxido de Carbono [ppm]
- 'NO2' - Dióxido de Nitrogênio [µg/m³]
- 'SO2' - Dixódio de Enxofre [µg/m³]
- 'IQAr' - Índice de Qualidade do Ar [0, 400]
- 'classificacao' - Categorização da Qualidade do Ar

Para mais informações em relação as categorizações da Qualidade do Ar: [Acesse](https://jeap.rio.rj.gov.br/je-metinfosmac/boletim)

## Novas funcionalidades a serem adicionadas e características a serem tratadas

---

- Tratamento de erros

---
