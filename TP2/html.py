def gen_html(ifs, vars, instrucoes, estruturas_controlo, erros, aviso):
    html = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Layout Example with Image in Header</title>
    <style>
        body, html {
            background-color: #000000;
            height: 100%;
            margin: 0;
            font-family: Arial, sans-serif;
            color: #f0f0f0;
        }
        .header {
            background-color: #4a4a4a;
            padding: 20px;
            position: relative;
            text-align: center;
        }
        .header img {
            position: absolute;
            top: 50%;
            right: 20px;
            transform: translateY(-50%);
            max-height: 100%;
        }
        .container {
            display: flex;
            height: 100%;
            background-color: #000000;
        }
        .left-column {
            background-color: #1E1E1E;
            flex: 1;
            margin-left: 10px;
            margin-top: 10px;
            margin-bottom: 10px;
            margin-right: 5px;
            border-radius: 5px;
            padding: 20px;
            color: #AADAFA;
            overflow-x: auto;
            white-space: pre;
            font-family: Consolas, Monaco, 'Andale Mono', monospace;
            font-size: 14px;
        }
        .left-column .cond {
            color: #AA7CAB;
        }
        .left-column .funcla {
            color: #DCDCAF;
        }
        .right-column {
            flex: 2;
            display: flex;
            flex-direction: column;
        }
        .box {
            flex: 1;
            margin-left: 5px;
            margin-right: 10px;
            border-radius: 5px;
            padding: 20px;
            color: #f0f0f0;
            position: relative;
        }
        .red {
            background-color: #2b0b00;
            margin-top: 10px;
            margin-bottom: 5px;
        }
        .blue {
            background-color: #000035;
            margin-top: 5px;
            margin-bottom: 5px;
        }
        .sub-box {
            display: flex;
            justify-content: space-between;
            padding: 10px;
        }
        .variables, .instructions {
            background-color: #2b0b00;
            flex: 1;
            margin: 5px;
            border-radius: 5px;
            padding: 10px;
            color: #f0f0f0;
        }
        .footer {
            background-color: #4a4a4a;
            padding: 20px;
            text-align: center;
            margin-top: 10px;
            width: 100%;
        }
        .purple {
            background-color: #2a002a;
            margin-top: 5px;
            margin-bottom: 10px;
        }
    </style>
</head>

<body>

    <div class="header">
        Pitão - O Python Tuga
        <img src="static/cobra_logo.png" alt="Logo">
    </div>

    <div class="container">
        <div class="right-column">
            <div class="box red sub-box">
                <div class="variables">
                    Variáveis:
                    <ul>'''
    html += f'''
                        <li>'Int': {vars['Int']}</li>
                        <li>'Set': {vars['Set']}</li>
                        <li>'Array': {vars['Array']}</li>
                        <li>'Tuplo': {vars['Tuplo']}</li>
                        <li>'Estringue': {vars['Estringue']}</li>
                        <li>'Lista': {vars['Lista']}</li>
                    </ul>
                </div>
                <div class="instructions">
                    Instruções:
                    <ul>
                        <li>Declarações: {instrucoes['declaracoes']}</li>
                        <li>Atribuições: {instrucoes['atribuicoes']}</li>
                        <li>Leitura: {instrucoes['leitura']}</li>
                        <li>Escrita: {instrucoes['escrita']}</li>
                        <li>Imprime: {instrucoes['imprime']}</li>
                        <li>Condicionais: {instrucoes['condicionais']}</li>
                        <li>Cíclicas: {instrucoes['ciclicas']}</li>
                    </ul>
                </div>
            </div>
            <div class="box blue">Erros</div>
        </div>
        <div class="footer">
            <div class="box purple">Outros</div>
        </div>
'''
    f = open("pagHTML.html", "w")
    f.write(html)