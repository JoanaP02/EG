def gen_html(ifs, vars, instrucoes, estruturas_controlo, erros, aviso):
    # Transforma a lista de condições em itens de lista HTML para a seção "Outros"
    ifs_html = "".join(f"<li>{condition}</li>" for condition in ifs)
    # Transforma a lista de erros e avisos em itens de lista HTML
    erros_html = "".join(f"<li>{error}</li>" for error in erros)

    # Cria o conteúdo HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Layout Example with Image in Header</title>
    <style>
        body, html {{
            background-color: #000000;
            height: 100%;
            margin: 0;
            font-family: Arial, sans-serif;
            color: #f0f0f0;
        }}
        .header {{
            background-color: #4a4a4a;
            padding: 20px;
            position: relative;
            text-align: center;
        }}
        .header img {{
            position: absolute;
            top: 50%;
            right: 20px;
            transform: translateY(-50%);
            max-height: 100%;
        }}
        .container {{
            display: flex;
            flex-direction: column;
            height: 100%;
            background-color: #000000;
        }}
        .container2 {{
            display: flex;
            height: 100%;
            background-color: #000000;
        }}
        .left-column {{
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
        }}
        .left-column .cond {{
            color: #AA7CAB;
        }}
        .left-column .funcla {{
            color: #DCDCAF;
        }}
        .right-column {{
            flex: 2;
            display: flex;
            flex-direction: column;
        }}
        .box {{
            flex: 1;
            margin-left: 5px;
            margin-right: 10px;
            border-radius: 5px;
            padding: 20px;
            color: #f0f0f0;
            position: relative;
        }}
        .red {{
            background-color: #2b0b00;
            margin-top: 10px;
            margin-bottom: 5px;
        }}
        .blue {{
            background-color: #000035;
            margin-top: 5px;
            margin-bottom: 5px;
        }}
        .sub-box {{
            display: flex;
            justify-content: space-between;
            padding: 10px;
        }}
        .variables, .instructions {{
            background-color: #2b0b00;
            flex: 1;
            margin: 5px;
            border-radius: 5px;
            padding: 10px;
            color: #f0f0f0;
        }}
        .footer {{
            background-color: #4a4a4a;
            padding: 20px;
            text-align: center;
            margin-top: 10px;
            width: 100%;
        }}
        .purple {{
            background-color: #2a002a;
            margin-top: 5px;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        Pitão - O Python Tuga
        <img src="static/cobra_logo.png" alt="Logo">
    </div>
    <div class="container">
        <div class="container2">
            <div class="left-column">
                <!-- Substitua por seu trecho de código real -->
                <code>deixa x: <span class="funcla">Int</span> = 5
                <span class="cond">se</span> x + 2 <span class="cond">entao</span>
                    <span class="cond">se</span> 2 <span class="cond">entao</span>
                        escreve "3"
                    <span class="cond">fim</span>
                <span class="cond">senao</span> 3 <span class="cond">entao</span>   
                    <span class="cond">se</span> 4 <span class="cond">entao</span>
                        escreve "4"
                    <span class="cond">fim</span>
                escreve "naaaaaada"
                <span class="cond">defeito</span>
                escreve "naaaaaada"
                <span class="cond">fim</span>
                </code>
            </div>
            <div class="right-column">
                <div class="box red sub-box">
                    <div class="variables">
                        Variáveis:
                        <ul>
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
                <div class="box blue">
                    Erros e Avisos:
                    <ul>
                        {erros_html}
                    </ul>
                </div>
            </div>
        </div>
        <div class="footer">
            <div class="box purple">
                Outros:
                <ul>
                    {ifs_html}
                </ul>
            </div>
        </div>
    </div>
</body>
</html>'''

    # Escreve o conteúdo HTML no arquivo pagHTML.html
    with open("pagHTML.html", "w", encoding="utf-8") as file:
        file.write(html)
