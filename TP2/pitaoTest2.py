from lark import Lark,Token,Tree, Discard
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter
import lark.tree as lark_tree
import lark.lexer as lark_lexer
from html import gen_html


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

inst: atribuicao | chamar | ler | escreve | imprime | se | repeticao | caso

atribuicao: ID "=" expr
chamar: ID APAR parametros? FPAR
ler: "ler" ID
escreve: "escreve" expr
imprime: "imprime" expr

se: SE se_expr "entao" inst+(SENAO se_expr "entao" inst+)* (DEFEITO inst+)? "fim"
caso: CORRESPONDE expr "com" (CASO expr "=>" inst+ ("break")?)+ (DEFEITO "=>" inst+)? "fim"

repeticao: enq_fazer | repetir_ate

enq_fazer: "enq" se_expr "fazer" inst+
repetir_ate: "fazer" inst+ "ate" se_expr

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

    def start(self, tree):
        self.dic_vars[(None,'Global')] = []
        self.visit_children(tree)
        gen_html(frase, self.finalIfs, self.vars, self.instrucoes, self.estruturas_controlo, self.erros, self.aviso)
        

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
        self.dic_vars[('Funcao',tree.children[0].value)] = []
        self.visit_children(tree)
        # Verificar variáveis declaradas mas não utilizadas
        for values in self.dic_vars.values():
            for lista in values:
                for key in lista.keys():
                    if lista[key][0] is None:
                        self.aviso.append(f"AVISO: Variável declarada mas não utilizada: {key[0]}")
        self.dic_vars.popitem()

    def parametros(self, tree): 
        self.visit_children(tree)

    def parametro(self, tree):
        self.visit_children(tree)

    def decls(self, tree):
        self.visit_children(tree)

    def decl(self, tree):

        # verificar se foi declarado
        for values in reversed(self.dic_vars.values()):
            for lista in values:
                for key in lista.keys():
                    if tree.children[1].value == key[0]:
                        self.erros.append(f"ERRO: Variável já declarada: {key[0]}")
                        return False

        if len(tree.children) == 4:
            criancas = self.visit_children(tree)
            last_key = list(self.dic_vars.keys())[-1] if self.dic_vars else None
            novo = {(tree.children[1].value, criancas[2]): (criancas[3], criancas[0])}
            self.dic_vars[last_key].append(novo)
        else: 
            criancas = self.visit_children(tree)
            last_key = list(self.dic_vars.keys())[-1] if self.dic_vars else None
            novo = {(tree.children[1].value, criancas[2]): (None, criancas[0])}
            self.dic_vars[last_key].append(novo)
        self.vars[criancas[2]] += 1
        self.instrucoes['declaracoes'] += 1

    def var(self, tree):
        return tree.children[0].value

    def tipo(self, tree):
        return tree.children[0].value

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
        self.visit_children(tree)

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
                        return True
        self.erros.append(f"ERRO: Variável não declarada {tree.children[0]}")
        return False

    def chamar(self, tree):
        pass    

    def ler(self, tree):
        self.instrucoes['leitura'] += 1
        pass

    def escreve(self, tree):
        self.instrucoes['escrita'] += 1
        pass

    def imprime(self, tree):
        self.instrucoes['imprime'] += 1

    def se(self, tree):
        
        if self.controlo == True:
            self.estruturas_controlo += 1
        self.instrucoes['condicionais'] += 1
        
        if len(tree.children) == 3:
            self.insideIf_acc.append(self.visit(tree.children[1]))
            self.insideIf= True
            self.controlo = True
            self.visit(tree.children[2])
            self.controlo = False
                
        # se tiver if e else
        elif len(tree.children) == 5:
            if self.insideIf == False:
                self.insideIf_acc.append(self.visit(tree.children[1]))
                self.insideIf = True
                self.controlo = True
                self.visit(tree.children[2])
                self.controlo = False
                self.insideIf_acc = []
                self.insideIf = False
                self.visit(tree.children[4])
            else:
                self.visit_children(tree)

        # se tiver elif's e/ou else
        else:
            # visitar if
            self.insideIf_acc.append(self.visit(tree.children[1]))
            self.insideIf = True
            self.controlo = True
            self.visit(tree.children[2])
            
            # visitar elif's, e se existir else
            for i, child in enumerate(tree.children):
                if isinstance(child,lark_lexer.Token) and child.type == "SENAO":
                    self.insideIf_acc.append(self.visit(tree.children[i+1]))
                    self.insideIf = True
                    self.controlo = True
                    self.visit(tree.children[i+2])

                elif isinstance(child,lark_lexer.Token) and child.type == "DEFEITO":
                    self.insideIf_acc = []
                    self.insideIf = False
                    self.controlo = False
                    self.visit(tree.children[i+1])
        

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
        self.visit_children(tree)


    def repetir_ate(self, tree):
        self.visit_children(tree)


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
classe Principal {
    deixa x: Int = 10
    fun Principal() {
        deixa w: Estringue
        deixa x: Int = 5
        deixa z: Int = 10
    }
    const y: Int = 5
    y = 6
    z = 10
}

"""

frase2 = """

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

frase = frase2
pydot__tree_to_png(p.parse(frase),'lark_test.png')

tree = p.parse(frase)  # retorna uma tree

pydot__tree_to_png(tree,'lark_test.png')
data = MyInterpreter().visit(tree)
