import plotly.express as px
import flet as ft
import pandas as pd
import json
from flet.plotly_chart import PlotlyChart
from flet import Page, AppBar, ElevatedButton, Text, TextField, Image
from flet import CrossAxisAlignment, MainAxisAlignment
from webscraping import ConsultaAnual, ConsultaMensal

fonte = 'Comfortaa'
consulta_ano = ConsultaAnual()
consulta_mes = ConsultaMensal()


def app(page: Page):

    # Estilização da janela da aplicação
    page.title = 'Consulta'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = 720
    page.window_width = 1024
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    fonte = 'comfortaa'  # Fonte usada nos textos

    ## Página de consulta anual ##

    def consulta_anual(e):
        page.clean()
        global ano
        ano = TextField(label='Ano', value='', width=200, max_length=4)
        botao_consulta = ElevatedButton(text='Consultar',
                                        on_click=consulta_anual_click
                                        )
        botao_semestre1 = ElevatedButton(text='Dados do 1º Semestre',
                                         on_click=consulta_semestre1_click
                                         )
        botoa_semestre2 = ElevatedButton(text='Dados do 2º Semestre',
                                         on_click=consulta_semestre2_click
                                         )
        botao_voltar = ElevatedButton(text='Voltar',
                                      on_click=lambda _: main()
                                      )

        page.add(
            AppBar(title=Text('Consulta Anual', font_family=fonte)),
            Text(value='Dados disponíveis de 2017 a 2022', font_family=fonte),
            ano,
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

    def consulta_anual_click(e):
        try:
            if not int(ano.value) in range(2017, 2022):
                ano.error_text = 'Ano inválido ❌'
                page.update()
            if not ano.value.isdigit():
                ano.error_text = 'Digite apenas números'
                page.update()

            if int(ano.value) in range(2017, 2024):
                ano_consulta = int(ano.value)
                page.clean()
                page.add(
                    Text(value='Realizando consulta...\nPode levar alguns minutos. Vá tomar uma água e depois volte. 🤏🥸⏳',
                         size=25, font_family=fonte
                         )
                )

                # Realizando a consulta anual
                try:
                    consulta_ano.consulta(ano_consulta)
                except Exception:
                    page.clean()
                    page.add(Text(value='Erro na consulta 🥴',
                                  font_family=fonte, size=25),
                             ElevatedButton(text='Voltar',
                                            on_click=lambda _: main()),
                             )
                    raise Exception

                # Consulta feita com sucesso
                page.clean()
                page.add(Text(value='Consulta realizada ☝️🤓',
                              size=25, font_family=fonte),
                         ft.Row(controls=[
                             ElevatedButton(on_click=lambda _: consulta_ano.obter_json(),
                                            text='Obter json'),
                             ElevatedButton(text='Voltar',
                                            on_click=lambda _: main())],
                                alignment='center'
                                )
                         )

        except:
            ...

    def consulta_semestre1_click(e):
        try:
            if not int(ano.value) in range(2017, 2022):
                ano.error_text = 'Ano inválido ❌'
                page.update()
            if not ano.value.isdigit():
                ano.error_text = 'Digite apenas números'
                page.update()

            if int(ano.value) in range(2017, 2024):
                ano_consulta = int(ano.value)
                page.clean()
                page.add(
                    Text(value='Realizando consulta...\nPode levar alguns minutos. Vá tomar uma água e depois volte. 🤏🥸⏳',
                         size=25, font_family=fonte
                         )
                )

                # Realizando a consulta anual
                try:
                    consulta_ano.consulta_semestral1(ano_consulta)
                except Exception:
                    page.clean()
                    page.add(Text(value='Erro na consulta 🥴',
                                  font_family=fonte, size=25),
                             ElevatedButton(text='Voltar',
                                            on_click=lambda _: main()),
                             )
                    raise Exception

                # Consulta feita com sucesso
                page.clean()
                page.add(Text(value='Consulta realizada ☝️🤓',
                              size=25, font_family=fonte),
                         ft.Row(controls=[
                             ElevatedButton(on_click=lambda _: consulta_ano.obter_json_semestre1(),
                                            text='Obter json'),
                             ElevatedButton(text='Voltar',
                                            on_click=lambda _: main())],
                                alignment='center'
                                )
                         )
        except:
            raise Exception

    def consulta_semestre2_click(e):
        try:
            if not int(ano.value) in range(2017, 2022):
                ano.error_text = 'Ano inválido ❌'
                page.update()
            if not ano.value.isdigit():
                ano.error_text = 'Digite apenas números'
                page.update()

            if int(ano.value) in range(2017, 2024):
                ano_consulta = int(ano.value)
                page.clean()
                page.add(
                    Text(value='Realizando consulta...\nPode levar alguns minutos. Vá tomar uma água e depois volte. 🤏🥸⏳',
                         size=25, font_family=fonte
                         )
                )

                # Realizando a consulta anual
                try:
                    consulta_ano.consulta_semestral2(ano_consulta)
                except:
                    page.clean()
                    page.add(Text(value='Erro na consulta 🥴',
                                  font_family=fonte, size=25),
                             ElevatedButton(text='Voltar',
                                            on_click=lambda _: main()),
                             )

                # Consulta feita com sucesso
                page.clean()
                page.add(Text(value='Consulta realizada ☝️🤓',
                              size=25, font_family=fonte),
                         ft.Row(controls=[
                             ElevatedButton(on_click=lambda _: consulta_ano.obter_json_semestre2(),
                                            text='Obter json'),
                             ElevatedButton(text='Voltar',
                                            on_click=lambda _: main())],
                                alignment='center'
                                )
                         )
        except:
            raise Exception

    ## Página de consulta mensal ##

    def consulta_mensal(e):
        page.clean()
        global mes, ano
        mes = TextField(label='Mês', value='', width=200, max_length=2)
        ano = TextField(label='Ano', value='', width=200, max_length=4)
        botao_consulta = ElevatedButton(
            text='Consultar',
            on_click=consulta_mensal_click
        )

        page.add(
            AppBar(title=Text('Consulta Mensal', font_family=fonte)),
            Text(value='Dados disponíveis de 2017 a 2023', font_family=fonte),
            ft.Row(controls=[mes, ano], alignment='center'),
            ft.Row(controls=[
                botao_consulta,
                ElevatedButton(text='Voltar',
                               on_click=lambda _: main()
                               )],
                   alignment='center'
                   )
        )
        page.update()

    ## Página de consulta mensal após executar a consulta ##
    def consulta_mensal_click(e):
        try:
            if not int(mes.value) in range(1, 13):
                mes.error_text = 'Mês inválido ❌'
                page.update()
            if not int(ano.value) in range(2017, 2024):
                ano.error_text = 'Ano inválido ❌'
                page.update()
            if int(ano.value) == 2023 and int(mes.value) >= 11:
                ano.error_text = 'Consulta ainda não disponível'  # Tratando temporariamente
                page.update()
            if int(mes.value) in range(1, 13) and int(ano.value) in range(2017, 2024):
                mes_consulta = int(mes.value)
                ano_consulta = int(ano.value)
                page.clean()
                page.add(Text(value='Realizando consulta...\nPode levar alguns instantes. Por favor, aguarde. 🙂🙃⏳',
                              size=25, font_family=fonte
                              )
                         )

                # Fazendo a raspagem dos dados
                try:
                    with open(f'dados{mes_consulta}-{ano_consulta}.json', 'r') as arquivo:
                        dados = json.load(arquivo)
                except FileNotFoundError:
                    try:
                        dados = consulta_mes.consulta(
                            mes_consulta, ano_consulta)
                    except Exception:
                        page.clean()
                        page.add(Text(value='Erro na consulta 🥴',
                                      font_family=fonte, size=25),
                                 ElevatedButton(text='Voltar',
                                                on_click=lambda _: main()),
                                 )
                        raise Exception

                # Plotando o gráfico
                tabela = pd.DataFrame(dados)
                tabela = tabela.transpose()
                fig = px.line(tabela[['IQAr']],
                              title=f'Índice de Qualidade do Ar de {mes_consulta}-{ano_consulta}'
                              )

                # APÓS A CONSULTA #
                page.clean()
                page.add(Text(value='Consulta realizada 🤓👌',
                              size=30, font_family=fonte
                              ),
                         ft.Row(
                    controls=[
                        ElevatedButton(text='Obter Excel',
                                       on_click=lambda _: consulta_mes.obter_excel()),
                        ElevatedButton(text='Obter csv',
                                       on_click=lambda _: consulta_mes.obter_csv()),
                        ElevatedButton(text='Obter json',
                                       on_click=lambda _: consulta_mes.obter_json()),
                        ElevatedButton(text='Voltar',
                                       on_click=lambda _: main())
                    ],
                    alignment='center'
                ),
                    PlotlyChart(fig, expand=True)
                )
                page.update()
        except:
            page.update()

    ## Menu Principal ##

    def main():
        page.clean()
        page.add(
            AppBar(title=Text('Menu Principal', font_family=fonte)),
            Image('ufrj-logo-1-removebg.png',
                  width=200, height=200),
            Text(value='Dados de Poluição de Irajá'.upper(),
                 font_family=fonte, size=30),
            ElevatedButton(text='Consulta Mensal',
                           width=170,
                           on_click=consulta_mensal),
            ElevatedButton(text='Consulta Anual', width=170,
                           on_click=consulta_anual),
            ElevatedButton(text='Sair',
                           width=170,
                           on_click=lambda _: page.window_close()))

    main()

    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER


if __name__ == '__main__':
    ft.app(target=app,
           assets_dir='ufrj-logo-1-removebg.png')
