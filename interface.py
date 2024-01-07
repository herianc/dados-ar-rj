import plotly.express as px
import flet as ft
import pandas as pd
import json
import webbrowser as wb
import numpy as np
from flet.plotly_chart import PlotlyChart
from flet import Page, AppBar, ElevatedButton, Text, TextField, Image
from flet import CrossAxisAlignment, MainAxisAlignment, ProgressRing
from webscraping import ConsultaAnual, ConsultaMensal, ConsultaSemestral
from os import system
from datetime import date
from datetime import datetime


consulta_anual = ConsultaAnual()
consulta_mensal = ConsultaMensal()
consulta_semestral = ConsultaSemestral()

mes_atual = datetime.today().month
ano_atual = datetime.today().year


def abrir_site(e):
    wb.open('https://jeap.rio.rj.gov.br/je-metinfosmac/boletim')


def app(page: Page):

    # Estilização da janela da aplicação
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = 768
    page.window_width = 1080
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.window_center()
    page.title = 'Boletim de Poluição do Rio'
    FONTE = 'comfortaa'

    # Estações disponíveis para consulta
    estacoes = ['Centro', 'Copacabana', 'São Cristóvão',
                'Tijuca', 'Irajá', 'Bangu', 'Campo Grande', 'Pedra de Guaratiba']

    # Menu dropdown com as estações
    estacao = ft.Dropdown(
        label="Estações",
        hint_text="Estação",
        width=200,
        options=[
            ft.dropdown.Option('Centro'),
            ft.dropdown.Option('Copacabana'),
            ft.dropdown.Option('São Cristóvão'),
            ft.dropdown.Option('Tijuca'),
            ft.dropdown.Option('Irajá'),
            ft.dropdown.Option('Bangu'),
            ft.dropdown.Option('Campo Grande'),
            ft.dropdown.Option('Pedra de Guaratiba')
        ],
    )

    ## Página de consulta anual ##
    def page_consulta_anual(e):
        estacao.error_text = ''
        consulta_anual.dados_ano.clear()
        consulta_semestral.dados_semestre.clear()
        consulta_mensal.dados_mes.clear()
        estacao.value = ''

        page.clean()
        global ano
        ano = TextField(label='Ano', value='', width=200)
        estacao
        botao_consulta = ElevatedButton(text='Consultar',
                                        on_click=page_consulta_anual_click
                                        )
        botao_semestre1 = ElevatedButton(text='Dados do 1º Semestre',
                                         on_click=page_consulta_semestral1_click
                                         )
        botoa_semestre2 = ElevatedButton(text='Dados do 2º Semestre',
                                         on_click=page_consulta_semestral2_click
                                         )

        botao_voltar = ElevatedButton(text='Voltar',
                                      on_click=lambda _: main()
                                      )

        page.add(
            AppBar(title=Text('Consulta Anual', font_family=FONTE)),
            Text(value='Dados disponíveis de 2017 a 2022', font_family=FONTE),
            ft.Row(controls=[ano, estacao],
                   alignment='center'),
            ft.Row(
                controls=[botao_consulta,
                          botao_semestre1,
                          botoa_semestre2,
                          botao_voltar
                          ],
                alignment='center'
            ),
        )
        page.update()

    ## Página de consulta anual após o click no botão ##
    def page_consulta_anual_click(e):
        # Verificando os inputs do usuário
        try:
            if not ano.value:
                ano.error_text = 'Digite ano'
                page.update()
            if not int(ano.value) in range(2017, ano_atual):
                ano.error_text = 'Ano inválido ❌'
                page.update()
            if not ano.value.isdigit():
                ano.error_text = 'Digite apenas números'
                page.update()
            if int(ano.value) == ano_atual:
                ano.error_text = 'Ano não disponível no momento'
            if int(ano.value) in range(2017, ano_atual):
                if estacao.value in estacoes:
                    ano_consulta = int(ano.value)
                    page.clean()
                    page.add(

                        Text(value='Realizando consulta...\nPode levar alguns minutos. Vá tomar uma água e depois volte. 🥸🤏⏳',
                             size=20, font_family=FONTE
                             ),
                        Text('A consulta anual pode durar cerca de 3-4 minutos',
                             font_family=FONTE, size=14),
                        ProgressRing()
                    )

                # Inputs OK! Obtendo os dados
                try:
                    # Verificando se o usuário já tem os dados
                    nome_arquivo = estacao.value.replace(' ', '_').lower()
                    caminho = f'./dados/{nome_arquivo}{ano_consulta}.json'
                    with open(caminho, 'r') as arquivo:
                        consulta_anual.dados_ano = json.load(arquivo)
                        consulta_anual.ano = ano_consulta
                    consulta_anual.estacao = estacao.value
                except FileNotFoundError:
                    # Caso não tenha os dados, executa a raspagem no site
                    try:
                        consulta_anual.consulta(estacao.value, ano_consulta)
                        consulta_anual.obter_json()
                    except Exception:
                        # Ocorreu algum erro durante a raspagem
                        page.clean()
                        page.add(Text(value='Erro durante a consulta 🥴',
                                      font_family=FONTE, size=25),
                                 ElevatedButton(text='Voltar',
                                                on_click=lambda _: main()),
                                 )
                        raise Exception

                # Consulta OK!
                tabela = pd.DataFrame.from_dict(consulta_anual.dados_ano,
                                                orient='index')

                fig = px.line(tabela, y='IQAr', x=tabela.index,
                              title=f'Índice de Qualidade do Ar de {ano_consulta} - Estação {estacao.value}'
                              )
                fig.update_yaxes(title='Índice')
                fig.update_xaxes(title='Meses', )

                dados_iqar = tabela[['IQAr']].replace('NA', np.nan)
                dias_indisponivel = dados_iqar.isnull().sum().to_string()[7:]
                tabela = tabela.replace('NA', np.nan)
                mp10 = tabela[['MP10']].mean().round(2).to_string()[7:].strip()
                mp25 = tabela[['MP2.5']].mean().round(
                    2).to_string()[7:].strip()
                o3 = tabela[['O3']].mean().round(2).to_string()[4:].strip()
                co = tabela[['CO']].mean().round(2).to_string()[5:].strip()
                no2 = tabela[['NO2']].mean().round(2).to_string()[6:].strip()
                so2 = tabela[['SO2']].mean().round(2).to_string()[6:].strip()
                iqar = tabela[['IQAr']].mean().round(2).to_string()[7:].strip()
                dias_prejudiciais = tabela['IQAr'].loc[tabela['IQAr'] > 80].count(
                )

                def grafico_detalhes(e):
                    fig.show()
                page.clean()
                page.add(Text(value='Consulta realizada 🤓👌',
                              size=30, font_family=FONTE),
                         ft.Row(controls=[
                             ElevatedButton(on_click=lambda _: consulta_anual.obter_excel(),
                                            text='Obter Planilha'),
                             ElevatedButton(on_click=lambda _: consulta_anual.obter_csv(),
                                            text='Obter .csv'),
                             ElevatedButton(on_click=grafico_detalhes,
                                            text='Gráfico detalhado'),
                             ElevatedButton(text='Voltar',
                                            on_click=lambda _: main())],
                                alignment='center'
                                ),
                         Text(value=f'Médias dos índices no ano de {ano_consulta} - Estação {estacao.value}',
                              font_family=FONTE),
                         Text(value=f'MP10: {mp10}  |  MP2.5: {mp25}  |  O3: {o3}  |  CO: {co}  |  NO2: {no2}  |  SO2: {so2}  |  IQAr: {iqar}',
                              font_family=FONTE),
                         Text(value=f'Dias com a Qualidade do Ar prejudicial à saúde:  {dias_prejudiciais}',
                              font_family=FONTE),
                         Text(value=f'\tA estação esteve indisponível {dias_indisponivel} dias.',
                              font_family=FONTE),

                         PlotlyChart(fig, expand=True),
                         )
        except ValueError:
            pass
        except:
            raise Exception

    ## Página de consulta semestral 1 após apertar o click no botão ##
    def page_consulta_semestral1_click(e):
        # Verificando os inputs do usuário
        try:
            if not ano.value:
                ano.error_text = 'Digite ano'
            if not int(ano.value) in range(2017, ano_atual+1):
                ano.error_text = 'Ano inválido ❌'
                page.update()
            if not ano.value.isdigit():
                ano.error_text = 'Digite apenas números'
                page.update()
            if int(ano.value) in range(2017, ano_atual+1) and int(mes_atual >= 7):
                if estacao.value in estacoes:
                    ano_consulta = int(ano.value)
                    page.clean()
                    page.add(
                        Text(value='Realizando consulta...\nPode levar alguns minutos. Vá tomar uma água e depois volte. 🤏🥸⏳',
                             size=20, font_family=FONTE
                             ),
                        ProgressRing()
                    )

                # Inputs OK! Obtendo os dados
                try:
                    # Verificando se o usuário já tem os dados
                    nome_arquivo = estacao.value.replace(' ', '_').lower()
                    caminho = f'./dados/{nome_arquivo}{ano_consulta}-semestre{1}.json'
                    with open(caminho, 'r') as arquivo:
                        consulta_semestral.dados_semestre = json.load(arquivo)
                        consulta_semestral.ano = ano_consulta
                        consulta_semestral.semestre = 1
                    consulta_semestral.estacao = estacao.value
                except FileNotFoundError:
                    # Caso não tenha os dados, executa a raspagem no site
                    try:
                        consulta_semestral.consulta(
                            estacao.value, 1, ano_consulta)
                        consulta_semestral.obter_json()
                    except Exception:
                        # Ocorreu algum erro durante a raspagem
                        page.clean()
                        page.add(Text(value='Erro durante a consulta 🥴',
                                      font_family=FONTE, size=30),
                                 ElevatedButton(text='Voltar',
                                                on_click=lambda _: main()),
                                 )
                        raise Exception

                # Consulta OK! Plotando o Gráfico
                tabela = pd.DataFrame.from_dict(consulta_semestral.dados_semestre,
                                                orient='index')
                fig = px.line(tabela, y='IQAr', x=tabela.index,
                              title=f'Índice de Qualidade do Ar do 1º Semestre de {ano_consulta}'
                              )
                fig.update_yaxes(title='Índice')
                fig.update_xaxes(title='Meses', )

                # Obtendo as medidas resumo

                dados_iqar = tabela[['IQAr']].replace('NA', np.nan)
                dias_indisponivel = dados_iqar.isnull().sum().to_string()[7:]
                tabela = tabela.replace('NA', np.nan)
                mp10 = tabela[['MP10']].mean().round(2).to_string()[7:].strip()
                mp25 = tabela[['MP2.5']].mean().round(
                    2).to_string()[7:].strip()
                o3 = tabela[['O3']].mean().round(2).to_string()[4:].strip()
                co = tabela[['CO']].mean().round(2).to_string()[5:].strip()
                no2 = tabela[['NO2']].mean().round(2).to_string()[6:].strip()
                so2 = tabela[['SO2']].mean().round(2).to_string()[6:].strip()
                iqar = tabela[['IQAr']].mean().round(2).to_string()[7:].strip()
                dias_prejudiciais = tabela['IQAr'].loc[tabela['IQAr'] > 80].count(
                )

                def grafico_detalhes(e):
                    fig.show()

                page.clean()
                page.add(Text(value='Consulta realizada 🤓👌',
                              size=30, font_family=FONTE),
                         ft.Row(controls=[
                             ElevatedButton(on_click=lambda _: consulta_semestral.obter_excel(),
                                            text='Obter Planilha'),
                             ElevatedButton(on_click=lambda _: consulta_semestral.obter_csv(),
                                            text='Obter .csv'),
                             ElevatedButton(on_click=grafico_detalhes,
                                            text='Gráfico detalhado'),
                             ElevatedButton(text='Voltar',
                                            on_click=lambda _: main())],
                                alignment='center'
                                ),
                         Text(value=f'Médias no 1º Semestre de {ano_consulta} - Estação {estacao.value}',
                              font_family=FONTE),
                         Text(value=f'MP10: {mp10}  |  MP2.5: {mp25}  |  O3: {o3}  |  CO: {co}  |  NO2: {no2}  |  SO2: {so2}  |  IQAr: {iqar}',
                              font_family=FONTE),
                         Text(value=f'Dias com a qualidade do ar prejudiciais à saúde: {dias_prejudiciais}',
                              font_family=FONTE),
                         Text(value=f'Neste período a estação {estacao.value} esteve indisponível {dias_indisponivel} dias.',
                         font_family=FONTE),
                         PlotlyChart(fig, expand=True)
                         )
        except ValueError:
            pass
        except:
            raise Exception

    ## Página de consulta semestral 2 após apertar o botão ##
    def page_consulta_semestral2_click(e):
        try:
            # Verificando os inputs do usuário
            if not ano.value:
                ano.error_text = 'Digite ano'
            if not int(ano.value) in range(2017, ano_atual):
                ano.error_text = 'Ano inválido ❌'
                page.update()
            if not ano.value.isdigit():
                ano.error_text = 'Digite apenas números'
                page.update()

            if int(ano.value) in range(2017, ano_atual):
                if estacao.value in estacoes:
                    ano_consulta = int(ano.value)
                    page.clean()
                    page.add(
                        Text(value='Realizando consulta...\nPode levar alguns minutos. Vá tomar uma água e depois volte. 🥸🤏⏳',
                             size=20, font_family=FONTE
                             ),
                        ProgressRing()
                    )

                # Inputs OK! Obtendo os dados
                try:
                    # Verificando se o usuário já tem os dados
                    nome_arquivo = estacao.value.replace(' ', '_').lower()
                    caminho = f'./dados/{nome_arquivo}{ano_consulta}-semestre{2}.json'
                    with open(caminho, 'r') as arquivo:
                        consulta_semestral.dados_semestre = json.load(arquivo)
                        consulta_semestral.ano = ano_consulta
                        consulta_semestral.semestre = 2

                    consulta_semestral.estacao = estacao.value
                except FileNotFoundError:
                    # Usuário ainda não tem os dados, executando a consulta
                    try:
                        consulta_semestral.consulta(
                            estacao.value, 2, ano_consulta)
                        consulta_semestral.obter_json()
                    except Exception:
                        # Ocorreu algum erro durante a raspagem
                        page.clean()
                        page.add(Text(value='Erro durante a consulta 🥴',
                                      font_family=FONTE, size=30),
                                 ElevatedButton(text='Voltar',
                                                on_click=lambda _: main()),
                                 )
                        raise Exception

                # Consulta OK! Plotando o Gráfico

                tabela = pd.DataFrame.from_dict(consulta_semestral.dados_semestre,
                                                orient='index')

                fig = px.line(tabela, y='IQAr', x=tabela.index,
                              title=f'Índice de Qualidade do Ar no semestre'
                              )
                fig.update_yaxes(title='Índice')
                fig.update_xaxes(title='Meses')

                dados_iqar = tabela[['IQAr']].replace('NA', np.nan)
                dias_indisponivel = dados_iqar.isnull().sum().to_string()[7:]
                tabela = tabela.replace('NA', np.nan)
                mp10 = tabela[['MP10']].mean().round(2).to_string()[7:].strip()
                mp25 = tabela[['MP2.5']].mean().round(
                    2).to_string()[7:].strip()
                o3 = tabela[['O3']].mean().round(2).to_string()[4:].strip()
                co = tabela[['CO']].mean().round(2).to_string()[5:].strip()
                no2 = tabela[['NO2']].mean().round(2).to_string()[6:].strip()
                so2 = tabela[['SO2']].mean().round(2).to_string()[6:].strip()
                iqar = tabela[['IQAr']].mean().round(2).to_string()[7:].strip()
                dias_prejudiciais = tabela['IQAr'].loc[tabela['IQAr'] > 80].count(
                )

                def grafico_detalhes(e):
                    fig.show()

                page.clean()
                page.add(Text(value='Consulta realizada 🤓👌',
                              size=30, font_family=FONTE),
                         ft.Row(controls=[
                             ElevatedButton(on_click=lambda _: consulta_semestral.obter_excel(),
                                            text='Obter Planilha'),
                             ElevatedButton(on_click=lambda _: consulta_semestral.obter_csv(),
                                            text='Obter .csv'),
                             ElevatedButton(on_click=grafico_detalhes,
                                            text='Gráfico detalhado'),
                             ElevatedButton(text='Voltar',
                                            on_click=lambda _: main())],
                                alignment='center'
                                ),
                         Text(value=f'Médias no 2º Semestre de {ano_consulta} - Estação {estacao.value}',
                              font_family=FONTE),
                         Text(value=f'MP10: {mp10}  |  MP2.5: {mp25}  |  O3: {o3}  |  CO: {co}  |  NO2: {no2}  |  SO2: {so2}  |  IQAr: {iqar}',
                              font_family=FONTE),
                         ft.Row(controls=[Text(value=f'Dias com a qualidade do ar prejudiciais à saúde: {dias_prejudiciais}',
                                               font_family=FONTE),
                                          Text(value=f'Neste período a estação {estacao.value} esteve indisponível {dias_indisponivel} dias.',
                                               font_family=FONTE)]),

                         PlotlyChart(fig, expand=True)
                         )
        except ValueError:
            pass
        except:
            raise Exception

    ## Página de consulta mensal ##
    def page_consulta_mensal(e):
        consulta_mensal.dados_mes.clear()
        estacao.value = ''
        estacao.error_text = ''

        page.clean()
        global mes, ano
        mes = TextField(label='Mês', value='', width=200)
        ano = TextField(label='Ano', value='', width=200)
        botao_consulta = ElevatedButton(
            text='Consultar',
            on_click=page_consulta_mensal_click
        )
        voltar = ElevatedButton(text='Voltar',
                                on_click=lambda _: main()
                                )

        page.add(
            AppBar(title=Text('Consulta Mensal', font_family=FONTE)),
            Text(value='Dados disponíveis de 2017 a 2023', font_family=FONTE),
            ft.Row(controls=[
                mes, ano, estacao], alignment='center'),
            ft.Row(controls=[
                botao_consulta, voltar
            ],
                alignment='center'
            )
        )
        page.update()

    ## Página de consulta mensal após executar a consulta ##
    def page_consulta_mensal_click(e):
        try:
            # Verificando os inputs do usuário
            if not int(mes.value) in range(1, 13):
                mes.error_text = 'Mês inválido ❌'
                page.update()
            if not int(ano.value) in range(2017, ano_atual + 1):
                ano.error_text = 'Ano inválido ❌'
                page.update()

            if int(ano.value) == datetime.today().year:
                if int(mes.value) >= datetime.today().month:
                    mes.error_text = 'Mês ainda não disponível'
                    page.update()

            elif int(mes.value) in range(1, 13) and int(ano.value) in range(2017, ano_atual + 1):
                if estacao.value in estacoes:
                    mes_consulta = int(mes.value)
                    ano_consulta = int(ano.value)
                    page.clean()
                    page.add(Text(value='Realizando consulta...\nPode levar alguns instantes. Por favor, aguarde. 🙂⏳',
                                  size=25, font_family=FONTE
                                  ),
                             ft.ProgressRing()
                             )

                # Inputs OK! Obtendo os dados
                try:
                    # Verificando se o usuário já tem os dados
                    nome_arquivo = estacao.value.replace(' ', '_').lower()
                    caminho = f'./dados/{nome_arquivo}{ano_consulta}-{mes_consulta}.json'
                    with open(caminho, 'r') as arquivo:
                        consulta_mensal.dados_mes = json.load(arquivo)
                        consulta_mensal.mes = mes_consulta
                        consulta_mensal.ano = ano_consulta

                    consulta_mensal.estacao = estacao.value
                except FileNotFoundError:
                    try:
                        # Caso não tenha os dados, executa a raspagem no site
                        consulta_mensal.consulta(estacao.value,
                                                 mes_consulta, ano_consulta)
                        consulta_mensal.obter_json()
                    except Exception:
                        # Ocorreu algum erro durante a raspagem
                        page.clean()
                        page.add(Text(value='Erro durante a consulta 🥴',
                                      font_family=FONTE, size=25),
                                 ElevatedButton(text='Voltar',
                                                on_click=lambda _: main()),
                                 )
                        raise Exception

                # Consulta OK! Plotando o gráfico
                tabela = pd.DataFrame.from_dict(
                    consulta_mensal.dados_mes, orient='index')

                data = date(ano_consulta, mes_consulta, 1)

                fig = px.line(tabela, y='IQAr', x=tabela.index,
                              title=f'Índice de Qualidade do Ar de {data.month}/{data.year} - Estação {estacao.value}'
                              )
                fig.update_yaxes(title='Índice')
                fig.update_xaxes(title='Dias', )

                # Obtendo a media de cada parametro
                tabela = tabela.replace('NA', np.nan)
                mp10 = tabela[['MP10']].mean().round(2).to_string()[7:].strip()
                mp25 = tabela[['MP2.5']].mean().round(
                    2).to_string()[7:].strip()
                o3 = tabela[['O3']].mean().round(2).to_string()[4:].strip()
                co = tabela[['CO']].mean().round(2).to_string()[5:].strip()
                no2 = tabela[['NO2']].mean().round(2).to_string()[6:].strip()
                so2 = tabela[['SO2']].mean().round(2).to_string()[6:].strip()
                iqar = tabela[['IQAr']].mean().round(2).to_string()[7:].strip()
                dias_prejudiciais = tabela['IQAr'].loc[tabela['IQAr'] > 80].count(
                )

                def grafico_detalhes(e):
                    fig.show()

                page.clean()
                page.add(Text(value='Consulta realizada 🤓👌',
                              size=30, font_family=FONTE
                              ),
                         ft.Row(
                    controls=[
                        ElevatedButton(text='Obter Planilha',
                                       on_click=lambda _: consulta_mensal.obter_excel()),
                        ElevatedButton(text='Obter .csv',
                                       on_click=lambda _: consulta_mensal.obter_csv()),
                        ElevatedButton(on_click=grafico_detalhes,
                                       text='Gráfico Detalhado'),
                        ElevatedButton(text='Voltar',
                                       on_click=lambda _: main()),
                    ],
                    alignment='center'
                ),
                    Text(value=f'Médias dos índices no mês',
                         font_family=FONTE),
                    Text(
                        value=f'MP10: {mp10}  |  MP2.5: {mp25}  |  O3: {o3}  |  CO: {co}  |  NO2: {no2}  |  SO2: {so2}  |  IQAr: {iqar}'),
                    Text(value=f'Dias com a qualidade do ar prejudiciais à saúde: {dias_prejudiciais}',
                         font_family=FONTE),
                    ft.Divider(),
                    Text(
                        value=f'DADOS DE {estacao.value.upper()} {mes_consulta}/{ano_consulta}', size=16, width='w900'),
                    ft.Markdown(
                    tabela.replace(np.nan, 'ND').to_markdown(),
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
                    on_tap_link=lambda e: page.launch_url(e.data),
                )
                )
                page.scroll = 'auto'
                page.padding = ft.padding.only(left=100, right=100, top=50)
                page.update()
        except ValueError:
            pass
        except:
            raise Exception

    ## Menu Principal ##
    def main():
        page.scroll = None
        page.clean()
        page.add(
            AppBar(title=Text('Menu Principal', font_family=FONTE)),
            Image('minerva_logo.png',
                  width=300, height=150),
            Text(value='Dados de Poluição do Rio'.upper(),
                 font_family=FONTE, size=30),
            ElevatedButton(text='Consulta Mensal',
                           width=200,
                           on_click=page_consulta_mensal),
            ElevatedButton(text='Consulta Anual', width=200,
                           on_click=page_consulta_anual),
            ElevatedButton(text='Boletim', width=200,
                           on_click=abrir_site),
            ElevatedButton(text='Sair',
                           width=200,
                           on_click=lambda _: page.window_close()))

    main()


if __name__ == '__main__':
    ft.app(target=app,
           assets_dir='./assets')
