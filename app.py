"""
Медицинская система мониторинга - Версия с загрузкой файлов
Dash приложение с функцией загрузки Excel файлов
"""

import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import base64
import io

# Инициализация приложения
app = dash.Dash(__name__)
app.title = "Медицинская система мониторинга"

# Макет приложения
app.layout = html.Div([
    html.H1("Медицинская система мониторинга", 
             style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    # Блок загрузки файлов
    html.Div([
        html.H3("Загрузка данных"),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Перетащите файл сюда или ',
                html.A('выберите файл')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
                'cursor': 'pointer'
            },
            multiple=False
        ),
        html.Div(id='output-data-upload')
    ], style={'margin': '20px'}),
    
    # Информационный блок
    html.Div([
        html.H4("Поддерживаемые форматы"),
        html.P("Excel файлы (.xlsx, .xls) с колонками:"),
        html.Ul([
            html.Li("Имя - имя пациента"),
            html.Li("Пол - пол пациента (М/Ж)"),
            html.Li("Возраст - возраст в годах"),
            html.Li("Пульс - частота сердечных сокращений"),
            html.Li("Давление - артериальное давление"),
            html.Li("ЭКГ - показатели электрокардиограммы"),
            html.Li("Сатурация - уровень кислорода в крови")
        ])
    ], style={'margin': '20px', 'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '5px'}),
    
    html.Div([
        html.H4("Версия 2.0 - Загрузка файлов"),
        html.P("Добавлена возможность загрузки и предварительного просмотра Excel файлов.")
    ], style={'margin': '20px', 'textAlign': 'center', 'backgroundColor': '#e8f4fd', 'padding': '20px', 'borderRadius': '5px'})
])

def parse_contents(contents, filename):
    """Парсинг содержимого загруженного файла"""
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename:
            # CSV файл
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename or 'xlsx' in filename:
            # Excel файл
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return html.Div([
                'Неподдерживаемый формат файла. Пожалуйста, загрузите Excel файл.'
            ], style={'color': 'red'})
    except Exception as e:
        return html.Div([
            f'Ошибка при обработке файла: {str(e)}'
        ], style={'color': 'red'})
    
    return html.Div([
        html.H5(f'Файл "{filename}" загружен успешно!'),
        html.P(f'Количество записей: {len(df)}'),
        html.P(f'Колонки: {", ".join(df.columns)}'),
        
        html.H6('Предварительный просмотр данных:'),
        dash_table.DataTable(
            data=df.head(10).to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_cell={'textAlign': 'left'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
        )
    ], style={'marginTop': '20px'})

@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is not None:
        return parse_contents(contents, filename)
    return html.Div('Выберите файл для загрузки...')

if __name__ == '__main__':
    app.run(debug=True, port=8050)
