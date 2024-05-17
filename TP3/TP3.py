from lark import Lark,Token,Tree, Discard
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter
import lark.tree as lark_tree
import lark.lexer as lark_lexer
from gen_html import gen_html
import os
import graphviz


grammar2 = '''
// Regras Sintaticas - Pitão
start: (classe | funcao | decls | inst)+

classe: "classe" ID ACHA (funcao | decls | inst)* FCHA

funcao: "fun" ID APAR parametros? FPAR ("=>" tipo)? ACHA (funcao | decls | inst)* FCHA
parametros: parametro (VIR parametro)*
parametro: ID ":" tipo

decls: decl+
decl: var ID ":" tipo ("=" expr)?

var: DEIXA | CONST
tipo: INT | SET | ARRAY | TUPLO | ESTRINGUE | LISTA

insts: inst+
inst: atribuicao | chamar | ler | escreve | imprime | se | repeticao | caso

atribuicao: ID "=" expr
chamar: ID APAR parametros? FPAR
ler: "ler" ID
escreve: "escreve" expr
imprime: "imprime" expr

se: SE se_expr "entao" insts(SENAO se_expr "entao" insts)* (DEFEITO insts)? "fim"
caso: CORRESPONDE expr "com" (CASO expr "=>" insts ("break")?)+ (DEFEITO "=>" insts)? "fim"

repeticao: enq_fazer | repetir_ate

enq_fazer: "enq" se_expr "fazer" insts "fim"
repetir_ate: "fazer" insts "ate" se_expr "fim"

expr: term (OP term)*
se_expr: term (OP term)* (OUTRO term (OP term)*)*
term: NUM | STRING | ID

// Regras Lexicográficas
NUM: /[0-9]+(,[0-9]+)?/
STRING: /"([^"]+)"/
ID: /[a-zA-Z_]\w*/
DEIXA: "deixa"
CONST: "const"
INT: "Int"
SET: "Set"
ARRAY: "Array"
TUPLO: "Tuplo"
ESTRINGUE: "Estringue"
LISTA: "Lista"
SE: "se"
SENAO: "senao"
DEFEITO: "defeito"
CORRESPONDE: "corresponde"
CASO: "caso"
OP: "+" | "-" | "*" | "/" | "%" | "^" 
OUTRO: "==" | "!=" | "<" | "<=" | ">" | ">=" | "e" | "ou"
VIR: ","
APAR: "("
FPAR: ")"
ACHA: "{"
FCHA: "}"

// Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

class MyInterpreter(Interpreter):
    def __init__ (self):

        # {(None, 'Global'): [],
        # ('Classe', 'Exemplo'): [{('VARIAVEL', 'Int'): (None, 'const')}],
        # ('Funcao', 'soma'): [{('d', 'Int'): ('5', 'deixa')}]
        # }
        self.dic_vars= {}

        # Verifica se estamos dentro de uma estrutura de controlo
        self.controlo = False
        
        self.insideIf = False
        self.insideIf_acc = []
        self.finalIfs = []

        self.vars = {'Int': 0, 'Set': 0, 'Array': 0, 'Tuplo': 0, 'Estringue': 0, 'Lista': 0}
        self.instrucoes = {'declaracoes': 0, 'atribuicoes': 0, 'leitura': 0, 'escrita': 0, 'imprime': 0, 'condicionais': 0, 'ciclicas': 0}
        self.estruturas_controlo = 0
        self.erros = []
        self.aviso = []
        
        self.formas = []
        self.ultima_visita = []
        
        self.dot = ''

    def adicionar_grafico(self, estringue):
        condicoes = ["se", "corresponde", "enq", "ate", "senao"]
        
        if self.ultima_visita == []:
            self.dot += f'inicio -> "{estringue}"\n'
            if estringue in condicoes:
                if estringue not in self.formas:
                    self.formas += [estringue]
        else:
            for visita in self.ultima_visita:
                self.dot += f'"{visita}" -> "{estringue}"\n'
                if estringue.split()[0] in condicoes:
                    if estringue not in self.formas:
                        self.formas += [estringue]
        self.ultima_visita = []

    def adicionar_formas(self):
        for estringue in self.formas:
            self.dot += f'"{estringue}" [shape=diamond];\n'

    def start(self, tree):
        self.dic_vars[(None,'Global')] = []
        self.visit_children(tree)
        gen_html(frase, self.finalIfs, self.vars, self.instrucoes, self.estruturas_controlo, self.erros, self.aviso)
        print(self.dot)
        dot_graph = graphviz.Source(self.dot)
        if not os.path.exists("static"):
            os.makedirs("static")

        # Save the graph as an image file (PNG format in this case) in outputs folder
        dot_graph.render(f"cfg",
                        directory="static/",
                        format="png",
                        cleanup=True)

    def classe(self, tree):
        self.dic_vars[('Classe',tree.children[0].value)] = []

        self.visit_children(tree)
        # Verificar variáveis declaradas mas não utilizadas
        for values in self.dic_vars.values():
            for lista in values:
                for key in lista.keys():
                    if lista[key][0] is None:
                        self.aviso.append(f"AVISO: Variável declarada mas não utilizada: {key[0]}")
        self.dic_vars.popitem()

    def funcao(self, tree):
        self.dot += f'''digraph {tree.children[0].value} {{
            beautify = true;
    graph [fontname = "JetBrains Mono", color=\"#8BAB92\", pad=\"0.5\"];
    node [fontname = "JetBrains Mono", color=\"#8BAB92\", fontcolor=\"#000000\", style="filled", fillcolor=\"#8BAB92\"];
    edge [fontname = "JetBrains Mono", color=\"#E94A31\"];
    bgcolor=\"#1E1E1E\";
    inicio [fontcolor="#303030"];
    fim [fontcolor="#303030"];\n\n'''
        self.dic_vars[('Funcao',tree.children[0].value)] = []
        self.visit_children(tree)
        # Verificar variáveis declaradas mas não utilizadas
        for values in self.dic_vars.values():
            for lista in values:
                for key in lista.keys():
                    if lista[key][0] is None:
                        self.aviso.append(f"AVISO: Variável declarada mas não utilizada: {key[0]}")
        self.dic_vars.popitem()
        for visita in self.ultima_visita:
            self.dot += f'"{visita}" -> "fim"\n'
        self.adicionar_formas()
        self.dot += '}'
        

    def parametros(self, tree): 
        self.visit_children(tree)

    def parametro(self, tree):
        self.visit_children(tree)

    def decls(self, tree):
        return self.visit_children(tree)

    def decl(self, tree):
        # verificar se foi declarado
        for values in reversed(self.dic_vars.values()):
            for lista in values:
                for key in lista.keys():
                    if tree.children[1].value == key[0]:
                        self.erros.append(f"ERRO: Variável já declarada: {key[0]}")
                        return False

        criancas = self.visit_children(tree)
        last_key = list(self.dic_vars.keys())[-1] if self.dic_vars else None
        if len(tree.children) == 4:
            novo = {(tree.children[1].value, criancas[2]): (criancas[3], criancas[0])}
            self.dic_vars[last_key].append(novo)
            var, id, tipo, expr = criancas
            estringue = f" {var} {id}: {tipo} = {expr}"
        else:
            novo = {(tree.children[1].value, criancas[2]): (None, criancas[0])}
            self.dic_vars[last_key].append(novo)
            var, id , tipo = criancas
            estringue = f" {var} {id}: {tipo}"
        self.vars[criancas[2]] += 1
        self.instrucoes['declaracoes'] += 1
        self.adicionar_grafico(estringue)
        self.ultima_visita.append(estringue)
        return estringue

    def var(self, tree):
        return tree.children[0].value

    def tipo(self, tree):
        return tree.children[0].value

    def insts(self, tree):
        return self.visit_children(tree)

    def inst(self, tree):
        if self.insideIf and len(tree.children) == 1 and tree.children[0].data == 'se':
            self.insideIf = True
        else:
            if len(self.insideIf_acc) > 1:
                finalResult = " e ".join(self.insideIf_acc)+":"
                before = self.insideIf_acc[0] + " , " + "".join([ i  for i in self.insideIf_acc[1:]])
                self.finalIfs.append(before+" => "+finalResult)
                self.insideIf_acc = []
            self.insideIf = False
        return self.visit_children(tree)[0]

    def atribuicao(self, tree):
        for inner_dict in self.dic_vars.values():
            for list in inner_dict:
                for key in list.keys():
                    if key[0] == tree.children[0].value:
                        if list[key][0] != None and list[key][1] == 'const':
                            self.erros.append(f"ERRO: Variável constante não pode ser alterada: {key[0]}")
                            return False
                        list[key] = (self.visit_children(tree)[1], list[key][1])
                        self.instrucoes['atribuicoes'] += 1
                        self.adicionar_grafico(f"{key[0]} = {list[key][0]}")
                        self.ultima_visita.append(f"{key[0]} = {list[key][0]}")
                        retorno = f"{key[0]} = {list[key][0]}"
                        return retorno
        self.erros.append(f"ERRO: Variável não declarada {tree.children[0]}")
        return False

    def chamar(self, tree):
        pass    

    def ler(self, tree):
        self.instrucoes['leitura'] += 1
        pass

    def escreve(self, tree):
        self.instrucoes['escrita'] += 1
        crianca = self.visit_children(tree)
        crianca = [crianca[0][1:-1]]
        retorno = f"escreve '{crianca[0]}'"
        self.adicionar_grafico(retorno)
        self.ultima_visita.append(retorno)
        return retorno

    def imprime(self, tree):
        self.instrucoes['imprime'] += 1
        crianca = self.visit_children(tree)
        crianca = [crianca[0][1:-1]]
        retorno = f"imprime '{crianca[0]}'"
        self.adicionar_grafico(retorno)
        self.ultima_visita.append(retorno)
        return retorno

    def se(self, tree):
        
        if self.controlo == True:
            self.estruturas_controlo += 1
        self.instrucoes['condicionais'] += 1
        
        if len(tree.children) == 3:
            expr = self.visit(tree.children[1])
            self.adicionar_grafico(f"se {expr}")
            self.ultima_visita.append(f"se {expr}")
            # self.adicionar_grafico(f"{se} {expr} {inst}")
            self.insideIf_acc.append(self.visit(tree.children[1]))
            self.insideIf= True
            self.controlo = True
            self.visit(tree.children[2])
            ultimo = self.ultima_visita[-1]
            self.controlo = False
            self.ultima_visita.append(f"se {expr}")
        
        # se tiver if e else
        elif len(tree.children) == 5:
            if self.insideIf == False:
                expr = self.visit(tree.children[1])
                self.adicionar_grafico(f"se {expr}")
                self.ultima_visita.append(f"se {expr}")
                self.insideIf_acc.append(self.visit(tree.children[1]))
                self.insideIf = True
                self.controlo = True
                self.visit(tree.children[2])
                ultimo = self.ultima_visita
                self.ultima_visita = [f"se {expr}"]
                self.controlo = False
                self.insideIf_acc = []
                self.insideIf = False
                self.visit(tree.children[4])
            else:
                expr = self.visit(tree.children[1])
                self.adicionar_grafico(f"se {expr}")
                self.ultima_visita.append(f"se {expr}")
                self.visit_children(tree)
                ultimo = self.ultima_visita
                self.ultima_visita = [f"se {expr}"]
            self.ultima_visita.extend(ultimo)

        # se tiver elif's e/ou else
        else:
            # visitar if
            expr = self.visit(tree.children[1])
            self.adicionar_grafico(f"se {expr}")
            self.ultima_visita.append(f"se {expr}")
            self.insideIf_acc.append(self.visit(tree.children[1]))
            self.insideIf = True
            self.controlo = True
            self.visit(tree.children[2])
            ultimo = self.ultima_visita
            self.ultima_visita = [f"se {expr}"]
            
            # visitar elif's, e se existir else
            for i, child in enumerate(tree.children):
                if isinstance(child,lark_lexer.Token) and child.type == "SENAO":
                    expr2 = self.visit(tree.children[i+1])
                    self.adicionar_grafico(f"senao {expr2}")
                    self.ultima_visita.append(f"senao {expr2}")
                    self.insideIf_acc.append(self.visit(tree.children[i+1]))
                    self.insideIf = True
                    self.controlo = True
                    self.visit(tree.children[i+2])
                    ultimoSenao = self.ultima_visita
                    self.ultima_visita = [f"senao {expr2}"]

                elif isinstance(child,lark_lexer.Token) and child.type == "DEFEITO":
                    self.insideIf_acc = []
                    self.insideIf = False
                    self.controlo = False
                    self.visit(tree.children[i+1])
            self.ultima_visita.extend(ultimo)
            self.ultima_visita.extend(ultimoSenao)

    def se_expr(self, tree):
        variavel = self.visit_children(tree)[0]

        list_expr = self.visit_children(tree)
        expressao = [var.value if isinstance(var, lark_lexer.Token) else var for var in list_expr]
        expressao = " ".join(expressao)

        k = []
        for values in reversed(self.dic_vars.values()):
            for lista in values:
                for key in lista.keys():
                    k.append(key[0])
        if variavel not in k:
            self.erros.append(f"ERRO: Variável não declarada: {variavel}")
        return expressao

    def caso(self, tree):
        self.instrucoes['condicionais'] += 1
        if self.controlo == True:
            self.estruturas_controlo += 1
        self.controlo = True
        self.visit_children(tree)
        self.controlo = False


    def repeticao(self, tree):
        if self.controlo == True:
            self.estruturas_controlo += 1
        self.controlo = True
        self.visit_children(tree)
        self.instrucoes['ciclicas'] += 1
        self.controlo = False

    def enq_fazer(self, tree):
        expr = self.visit(tree.children[0])
        self.adicionar_grafico(f"enq {expr}")
        self.ultima_visita.append(f"enq {expr}")
        self.visit(tree.children[1])
        self.ultima_visita
        self.adicionar_grafico(f"enq {expr}")
        self.ultima_visita.append(f"enq {expr}")

    def repetir_ate(self, tree):
        inst = self.visit(tree.children[0])[0]
        expr = self.visit(tree.children[1])
        self.adicionar_grafico(f"ate {expr}")
        self.ultima_visita.append(f"ate {expr}")
        self.adicionar_grafico(inst)
        self.ultima_visita.append(f"ate {expr}")


    def expr(self, tree):
        expr = ''
        for i, child in enumerate(tree.children):
            if i == 0 or i % 2 == 0:
                num = child.children[0]
                expr += num
            else:
                op = child
                expr += op
        return expr

    def term(self, tree):
        return tree.children[0].value
    
    def OP(self, tree):
        return tree.children[0].value

frase1 = """
fun Principal() {
    deixa x: Int = 5
    deixa z: Int
    deixa y: Int = 0
    fazer
        z = z + 1
        y = 5
        imprime "O número."
        escreve "O número +."
    ate 7 == 7
    fim
    enq 5 > 3 fazer
        z = 5
        x = 4
        enq 2 > 1 fazer
            z = 2
            se 2 > 0 entao
                z = 1
                escreve "O número é positivo."
            defeito
                z = 0
                imprime "O número é negativo."
            fim
        fim
    fim
    deixa y: Int = 5 + 3
}

"""

frase2 = """
fun Principal() {
    deixa x: Int = 5
    deixa z: Int
    deixa y: Int = 0
    se 5 > 3 entao
        z = z + 1
        y = 5
        imprime "O número."
        escreve "O número +."
    senao 7 == 7 entao
        imprime "cenas"
    defeito
        escreve "O número -."
    fim
}
"""

frase3 = """

fun main() {
    deixa numero: Int = 10
    deixa x: Int = 10

    se numero > 0 entao
        se numero > 5 entao
            escreve "O número é positivo e maior que 5."
        fim
    senao numero < 2 entao
        se numero < 0 entao
            escreve "O número é negativo e menor que -5."  
        fim    
    defeito 
        escreve "O número é zero."
    fim 

    enq numero > 0 fazer
        se numero > 5 entao
            imprime "Número é positivo e maior que 5."
        defeito
            imprime "Número é positivo e menor ou igual a 5."
        fim
        imprime_mensagem()
        numero = numero - 1
    
    x = 20


    corresponde numero com
        caso 1 =>
            se numero > 0 entao
                x = 10
            fim
        caso 2 =>
            escreve "Número é 2."
        defeito =>
            escreve "Número é diferente de 1 e 2."
    fim 
}
    """


p = Lark(grammar2) # cria um objeto parser

frase = frase1
tree = p.parse(frase)  # retorna uma tree
pydot__tree_to_png(tree,'frase1.png')
data = MyInterpreter().visit(tree)
