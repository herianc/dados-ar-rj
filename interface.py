import plotly.express as px
import flet as ft
import pandas as pd
from flet.plotly_chart import PlotlyChart
from flet import Page, AppBar, ElevatedButton, Text, TextField, Image
from flet import CrossAxisAlignment, MainAxisAlignment
from webscraping import ConsultaAnual, ConsultaMensal


fonte = 'comfortaa'


consulta_ano = ConsultaAnual()
consulta_mes = ConsultaMensal()


def app(page: Page):

    # Estilização da janela da aplicação
    page.title = 'Consulta'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = 720
    page.window_width = 720
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    fonte = 'comfortaa'  # Fonte usada nos textos

    # Página de consulta mensal
    def consulta_mensal(e):
        page.clean()
        global mes, ano
        mes = TextField(label='Mês', value='', width=200, max_length=2)
        ano = TextField(label='Ano', value='', width=200, max_length=4)
        botao_consulta = ElevatedButton(
            text='Consultar', on_click=consulta_mensal_clicada)  # colocar ação para o botao

        page.add(
            AppBar(title=Text('Consulta Mensal', font_family=fonte)),
            Text(value='Dados disponíveis de 2017 a 2023', font_family=fonte),
            ft.Row(controls=[mes, ano], alignment='center'),
            botao_consulta
        )
        page.update()

    # Página de consulta mensal após executar a consulta
    def consulta_mensal_clicada(e):
        try:
            if not int(mes.value) in range(1, 13):
                mes.error_text = 'Mês inválido ❌'
                page.update()
            if not int(ano.value) in range(2017, 2024):
                ano.error_text = 'Ano inválido ❌'
                page.update()

            if int(mes.value) in range(1, 13) and int(ano.value) in range(2017, 2024):
                mes_consulta = int(mes.value)
                ano_consulta = int(ano.value)
                page.clean()
                page.add(Text(value='Realizando consulta...\nPode levar alguns instantes. Por favor, aguarde. 😶‍🌫️⏳',
                              size=20,
                              font_family=fonte))

                dados = consulta_mes.consulta(mes_consulta, ano_consulta)
                tabela = pd.DataFrame(dados)
                tabela = tabela.transpose()

                ## APÓS A CONSULTA ##
                fig = px.line(tabela[['IQAr']],
                              title='Índice de Qualidade do Ar no mês consultado'
                              )
                page.clean()
                page.add(Text(value='Consulta realizada ☝️🤓',
                              size=20,
                              font_family=fonte),
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
        except ValueError:
            pass
            page.update()
        except:
            print('Erro desconhecido')

    # Menu Principal
    def main():
        page.clean()
        page.add(
            AppBar(title=Text('Menu Principal', font_family=fonte)),
            Image('ufrj-logo-1-removebg.png', width=200, height=200),
            ElevatedButton(text='Consulta Mensal', on_click=consulta_mensal),
            ElevatedButton(text='Consulta Anual'),
            ElevatedButton(text='Informações'))

    main()

    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER


if __name__ == '__main__':
    ft.app(target=app)
