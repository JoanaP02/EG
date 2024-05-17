def gen_html(frase, ifs, vars, instrucoes, estruturas_controlo, erros, aviso):
    # Transforma a lista de condições em itens de lista HTML para a seção "Outros"
    ifs_html = "".join(f"<li>{condition}</li>" for condition in ifs)
    # Transforma a lista de erros em itens de lista HTML
    erros_html = "".join(f"<li>{error}</li>" for error in erros)
    # Transforma a lista de avisos em itens de lista HTML
    aviso_html = "".join(f"<li>{aviso}</li>" for aviso in aviso)

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
            color: #8BAB92;
        }}
        .header {{
            background-color: #252525;
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
            background-color: #000000;
        }}
        .left-column {{
            background-color: #1E1E1E;
            flex: 1;
            margin-left: 10px;
            margin-top: 10px;
            margin-bottom: 5px;
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
        .middle-column {{
            flex: 1;
            display: flex;
            flex-direction: column;
        }}
        .right-column{{
            background-color: #1E1E1E;
            flex: 1;
            margin-left: 5px;
            margin-top: 10px;
            margin-bottom: 5px;
            margin-right: 10px;
            border-radius: 5px;
            padding: 10px;
            display: flex;
            flex-direction: column;
        }}
        .right-column img {{
            position: absolute;
            max-width: 100%;
            max-height: 100%;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }}
        .right-box {{
            flex: 1;
            margin-left: 5px;
            margin-right: 5px;
            border-radius: 5px;
            padding: 10px;
            color: #8BAB92;
            position: relative;
        }}
        .box {{
            flex: 1;
            margin-left: 5px;
            margin-right: 5px;
            border-radius: 5px;
            padding: 20px;
            color: #8BAB92;
            position: relative;
        }}
        .top {{
            background-color: #1E1E1E;
            margin-top: 10px;
            margin-bottom: 5px;
        }}
        .middle {{
            background-color: #1E1E1E;
            margin-top: 5px;
            margin-bottom: 5px;
        }}
        .bottom {{
            background-color: #1E1E1E;
            margin-top: 5px;
            margin-bottom: 5px;
        }}
        .sub-bottom {{
            background-color: #1E1E1E;
            margin-top: 5px;
            margin-bottom: 5px;
        }}
        .sub-box {{
            display: flex;
            justify-content: space-between;
        }}
        .variables, .instructions {{
            background-color: #1E1E1E;
            flex: 1;
            margin: 5px;
            border-radius: 5px;
            color: #8BAB92;
        }}
    </style>
</head>
<body>
    <div class="header">
        <b>Pitão - O Python Tuga</b>
        <img src="static/cobra_logo.png" alt="Logo">
    </div>
    <div class="container">
        <div class="left-column">
<code>{adicionarSpan(frase)}</code>
        </div>
        <div class="middle-column">
            <div class="box top sub-box">
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
            <div class="box middle">
                Erros e Avisos:
                <ul>
                    {erros_html}
                    {aviso_html}
                </ul>
            </div>
            <div class="box bottom">
                <div class="variables">
                    Nº de Estruturas de Controlo aninhadas:
                    {estruturas_controlo}
                </div>
            </div>
            <div class="box sub-bottom sub-box">
                <div class="instructions">
                    <em>Ifs</em> aninhados que se podiam juntar:
                    <ul>
                        {ifs_html}
                    </ul>
                </div>
            </div>
        </div>
        <div class="right-column">
            <div class="box">
                <img src="static/cfg.png" alt="CFG">
            </div>
        </div>
    </div>
</body>
</html>'''

    # Escreve o conteúdo HTML no arquivo pagHTML.html
    with open("pagHTML.html", "w", encoding="utf-8") as file:
        file.write(html)

def adicionarSpan(frase):
    frase = frase.replace(" fun ", "<span class='funcla'> fun </span>")
    frase = frase.replace(" classe ", "<span class='funcla'> classe </span>")
    frase = frase.replace(" deixa ", "<span class='funcla'> deixa </span>")
    frase = frase.replace(" const ", "<span class='funcla'> const </span>")
    frase = frase.replace(" entao ", "<span class='cond'> entao </span>")
    frase = frase.replace(" senao ", "<span class='cond'> senao </span>")
    frase = frase.replace(" defeito ", "<span class='cond'> defeito </span>")
    frase = frase.replace(" corresponde ", "<span class='cond'> corresponde </span>")
    frase = frase.replace(" enq ", "<span class='cond'> enq </span>")
    frase = frase.replace(" ler ", "<span class='funcla'> ler </span>")
    frase = frase.replace(" escreve ", "<span class='funcla'> escreve </span>")
    frase = frase.replace(" fim ", "<span class='cond'> fim </span>")
    frase = frase.replace(" se ", "<span class='cond'> se </span>")
    return frase