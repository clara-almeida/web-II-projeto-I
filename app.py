import pandas as pd

# Carregar o arquivo CSV com a codificação correta e low_memory desativado
file_path = '/Users/claraalmeida/Documents/Aulas MJD 2024/web-II-projeto-I/MICRODADOS_CADASTRO_CURSOS_2022.CSV'
df = pd.read_csv(file_path, encoding='latin1', sep=';', on_bad_lines='skip', low_memory=False)

# Ajustar a lista de colunas conforme necessário
columns_to_select = ["NU_ANO_CENSO","NO_CURSO","QT_ING","QT_ING_FEM","QT_ING_MASC"]
df_filtered = df[columns_to_select]

# Selecionar os cursos específicos
cursos_interesse = ["Comunicação Social - Jornalismo", "Medicina", "Engenharia Civil", "Tecnologia Da Informação","Administração", "Direito", "Psicologia", "Educação Física"]
df_cursos = df_filtered[df_filtered["NO_CURSO"].isin(cursos_interesse)]

# Agrupar por curso e somar as colunas desejadas
df_agrupado = df_cursos.groupby("NO_CURSO")[["QT_ING", "QT_ING_FEM", "QT_ING_MASC"]].sum().reset_index()

# Calcular os percentuais de mulheres e homens
df_agrupado["PERC_FEM"] = (df_agrupado["QT_ING_FEM"] / df_agrupado["QT_ING"]) * 100
df_agrupado["PERC_MASC"] = (df_agrupado["QT_ING_MASC"] / df_agrupado["QT_ING"]) * 100

# Criar a página HTML
html_file_path = '/Users/claraalmeida/Documents/Aulas MJD 2024/web-II-projeto-I/resultado_cursos.html'
with open(html_file_path, 'w') as file:
    file.write(f'''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resultado dos Cursos</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #000;
                color: #fff;
                margin: 20px;
            }}
            .course-bar {{
                margin: 20px 0;
                width: 100%;
                background-color: #555;
                border-radius: 5px;
                overflow: hidden;
                display: flex;
            }}
            .course-bar .fem {{
                background-color: #cc87ff;
                height: 30px;
                text-align: right;
                padding-right: 10px;
                box-sizing: border-box;
                color: #000;
            }}
            .course-bar .masc {{
                background-color: #90EE90;
                height: 30px;
                text-align: left;
                padding-left: 10px;
                box-sizing: border-box;
                color: #000;
            }}
            .course-label {{
                margin-bottom: 5px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>Resultado dos Cursos</h1>
    ''')

    for _, row in df_agrupado.iterrows():
        file.write(f'''
        <div class="course-label">{row["NO_CURSO"]}</div>
        <div class="course-bar">
            <div class="masc" style="width:{row["PERC_MASC"]}%;">{row["PERC_MASC"]:.2f}% Homens</div>
            <div class="fem" style="width:{row["PERC_FEM"]}%;">{row["PERC_FEM"]:.2f}% Mulheres</div>
        </div>
        ''')

    file.write('''
    </body>
    </html>
    ''')
