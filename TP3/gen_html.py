def gen_html(frase, ifs, vars, instrucoes, estruturas_controlo, erros, aviso):
    ifs_html = "".join(f"<li>{condition}</li>" for condition in ifs)
    erros_html = "".join(f"<li>{error}</li>" for error in erros)
    aviso_html = "".join(f"<li>{aviso}</li>" for aviso in aviso)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Layout Example with Image in Header</title>
    <style>
        body, html {{
            height: 100%;
            margin: 0;
            font-family: Arial, sans-serif;
        }}
        body.dark-mode {{
            background-color: #000000;
            color: #8BAB92;
        }}
        body.light-mode {{
            background-color: #FFFFFF;
            color: #000000;
        }}
        .header {{
            padding: 20px;
            position: relative;
            text-align: center;
        }}
        .header.dark-mode {{
            background-color: #252525;
        }}
        .header.light-mode {{
            background-color: #f0f0f0;
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
            height: calc(100% - 60px); /* Adjust based on header height */
        }}
        .left-column {{
            flex: 1;
            margin: 10px 5px 5px 10px;
            border-radius: 5px;
            padding: 20px;
            overflow-x: auto;
            white-space: pre;
            font-family: Consolas, Monaco, 'Andale Mono', monospace;
            font-size: 14px;
        }}
        .left-column.dark-mode {{
            background-color: #1E1E1E;
            color: #AADAFA;
        }}
        .left-column.light-mode {{
            background-color: #f5f5f5;
            color: #000000;
        }}
        .left-column.dark-mode .cond {{
            color: #AA7CAB;
        }}
        .left-column.dark-mode .funcla {{
            color: #DCDCAF;
        }}
        .left-column.light-mode .cond {{
            color: #001080;
        }}
        .left-column.light-mode .funcla {{
            color: #A31515;
        }}
        .middle-column {{
            flex: 1;
            display: flex;
            flex-direction: column;
            margin: 10px 5px;
        }}
        .right-column {{
            flex: 1;
            margin: 10px 10px 5px 5px;
            border-radius: 5px;
            padding: 10px;
            display: flex;
            flex-direction: column;
            position: relative;
        }}
        .right-column.dark-mode {{
            background-color: #1E1E1E;
        }}
        .right-column.light-mode {{
            background-color: #f5f5f5;
        }}
        .right-column img {{
            max-width: 100%;
            max-height: 100%;
        }}
        .box {{
            flex: 1;
            margin: 5px;
            border-radius: 5px;
            padding: 20px;
        }}
        .box.dark-mode {{
            background-color: #1E1E1E;
            color: #8BAB92;
        }}
        .box.light-mode {{
            background-color: #f5f5f5;
            color: #000000;
        }}
        .sub-box {{
            display: flex;
            justify-content: space-between;
        }}
        .variables, .instructions {{
            flex: 1;
            margin: 5px;
            border-radius: 5px;
            padding: 10px;
        }}
        .variables.dark-mode, .instructions.dark-mode {{
            background-color: #1E1E1E;
            color: #8BAB92;
        }}
        .variables.light-mode, .instructions.light-mode {{
            background-color: #f5f5f5;
            color: #000000;
        }}
    </style>
    <script>
        function toggleMode() {{
            const body = document.body;
            const header = document.querySelector('.header');
            const leftColumn = document.querySelector('.left-column');
            const rightColumn = document.querySelector('.right-column');
            const boxes = document.querySelectorAll('.box');
            const variables = document.querySelectorAll('.variables');
            const instructions = document.querySelectorAll('.instructions');
            const img = document.querySelector('.right-column img');
            body.classList.toggle('dark-mode');
            body.classList.toggle('light-mode');
            header.classList.toggle('dark-mode');
            header.classList.toggle('light-mode');
            leftColumn.classList.toggle('dark-mode');
            leftColumn.classList.toggle('light-mode');
            rightColumn.classList.toggle('dark-mode');
            rightColumn.classList.toggle('light-mode');

            boxes.forEach(box => {{
                box.classList.toggle('dark-mode');
                box.classList.toggle('light-mode');
            }});
            variables.forEach(variable => {{
                variable.classList.toggle('dark-mode');
                variable.classList.toggle('light-mode');
            }});
            instructions.forEach(instruction => {{
                instruction.classList.toggle('dark-mode');
                instruction.classList.toggle('light-mode');
            }});

            if (body.classList.contains('light-mode')) {{
                img.src = 'static/cfg_light.png';
            }} else {{
                img.src = 'static/cfg.png';
            }}
        }}
    </script>
</head>
<body class="dark-mode">
    <div class="header dark-mode">
        <b>Pitão - O Python Tuga</b>
        <img src="static/cobra_logo.png" alt="Logo">
        <button style="position: absolute; top: 20px; left: 20px;" onclick="toggleMode()">Switch Mode</button>
    </div>
    <div class="container">
        <div class="left-column dark-mode">
<code>{adicionarSpan(frase)}</code>
        </div>
        <div class="middle-column">
            <div class="box top sub-box dark-mode">
                <div class="variables dark-mode">
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
                <div class="instructions dark-mode">
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
            <div class="box middle dark-mode">
                Erros e Avisos:
                <ul>
                    {erros_html}
                    {aviso_html}
                </ul>
            </div>
            <div class="box bottom dark-mode">
                <div class="variables dark-mode">
                    Nº de Estruturas de Controlo aninhadas:
                    {estruturas_controlo}
                </div>
            </div>
            <div class="box sub-bottom sub-box dark-mode">
                <div class="instructions dark-mode">
                    <em>Ifs</em> aninhados que se podiam juntar:
                    <ul>
                        {ifs_html}
                    </ul>
                </div>
            </div>
        </div>
        <div class="right-column dark-mode">
            <div class="box dark-mode">
                <img src="static/cfg.png" alt="CFG">
            </div>
        </div>
    </div>
</body>
</html>'''

    with open("pagHTML.html", "w", encoding="utf-8") as file:
        file.write(html)

def adicionarSpan(frase):
    frase = frase.replace(" fun ", "<span class='funcla'> fun </span>")
    frase = frase.replace(" classe ", "<span class='funcla'> classe </span>")
    frase = frase.replace(" seja ", "<span class='funcla'> seja </span>")
    frase = frase.replace(" const ", "<span class='funcla'> const </span>")
    frase = frase.replace(" entao ", "<span class='cond'> entao </span>")
    frase = frase.replace(" senao ", "<span class='cond'> senao </span>")
    frase = frase.replace(" omissao ", "<span class='cond'> omissao </span>")
    frase = frase.replace(" corresponde ", "<span class='cond'> corresponde </span>")
    frase = frase.replace(" enq ", "<span class='cond'> enq </span>")
    frase = frase.replace(" ler ", "<span class='funcla'> ler </span>")
    frase = frase.replace(" escreve ", "<span class='funcla'> escreve </span>")
    frase = frase.replace(" imprime ", "<span class='funcla'> imprime </span>")
    frase = frase.replace(" fim ", "<span class='cond'> fim </span>")
    frase = frase.replace(" se ", "<span class='cond'> se </span>")
    return frase
