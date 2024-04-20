from lark import Lark,Token,Tree, Discard
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter


# FALTA
# 4- COntar if dentro de if ou se/caso dentro de se/caso
# 5- Ifs aninhados-
#   If ....        /        If ...        \  /
#      If ...  \  /             If ...     \/          
#               \/              Else ...   /\
#                                         /  \

grammar2 = '''
// Regras Sintaticas - Pitão
start: (classe | funcao | decls | insts)+

classe: "classe" ID ACHA (funcao | decls | insts)* FCHA

funcao: "fun" ID APAR parametros? FPAR ("=>" tipo)? ACHA (funcao | decls | insts)* FCHA
parametros: parametro (VIR parametro)*
parametro: ID ":" tipo

decls: decl+
decl: var ID ":" tipo ("=" expr)?

var: DEIXA | CONST
tipo: INT | SET | ARRAY | TUPLO | ESTRINGUE | LISTA

insts: inst+
inst: atribuicao | chamar | ler | escreve | imprime | selecao | repeticao

atribuicao: ID "=" expr
chamar: ID APAR parametros? FPAR
ler: "ler" ID
escreve: "escreve" expr
imprime: "imprime" expr

selecao: se | caso

se: SE se_expr "entao" insts (SENAO se_expr "entao" insts)* (DEFEITO insts)? FIM
caso: CORRESPONDE expr "com" (CASO expr "=>" insts ("break")?)+ (DEFEITO "=>" insts)? FIM

repeticao: enq_fazer | repetir_ate

enq_fazer: "enq" se_expr "fazer" insts
repetir_ate: "fazer" insts "ate" se_expr

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
FIM: "fim"
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
        # dic {(scope_tipo, scope_nome): [(ID, tipo): valor, (ID2, tipo2): valor2]}
        # dic {('Classe', 'Principal'): [(x, Int, 5), (y, Int, None)], ('Classe', 'Secundaria'): [(x, Int, 5)]}
        self.dic = {}

        # Verifica se estamos dentro de uma estrutura de controlo
        self.controlo = False
        self.estruturas_controlo = 0
        
        self.insideIf = False
        
        # dic_info = { variáveis: [somaInt, somaSet, somaArray, somaTuplo, somaEstringue, somaLista],
        #              instrucoes : [declaracoes, atribuicoes, leitura, escrita, condicionais, cíclicas],
        #              erros : [ variáveis não declaradas, variáveis declaradas mas não utilizadas, variáveis declaradas mas não atribuídas]
        #              estruturas_controlo : número
        #            }
        # vars = {Int: 0, Set: 0, Array: 0, Tuplo: 0, Estringue: 0, Lista: 0}
        self.vars = {'Int': 0, 'Set': 0, 'Array': 0, 'Tuplo': 0, 'Estringue': 0, 'Lista': 0}
        self.instrucoes = {'declaracoes': 0, 'atribuicoes': 0, 'leitura': 0, 'escrita': 0, 'imprime': 0, 'condicionais': 0, 'ciclicas': 0}
        #self.erros = {'variaveis_nao_declaradas': 0, 'variaveis_declaradas_nao_utilizadas': 0, 'variaveis_declaradas_nao_atribuidas': 0}

    def start(self, tree):
        self.dic[(None,'Global')] = []
        print(self.dic)

        for child in tree.children:
            print(self.visit(child))

        return f"""Ints {self.vars['Int']}
Set {self.vars['Set']}
Array {self.vars['Array']}
Tuplo {self.vars['Tuplo']}
Estringue {self.vars['Estringue']}
Lista {self.vars['Lista']}
"""

    def classe(self, tree):
        print("Classe")
        #  Token('ID', 'Principal') -  type esquerda, value direita
        # visit children
        self.dic[('Classe',tree.children[0].value)] = []
        print(self.dic)
        self.visit_children(tree)
        # Verificar variáveis declaradas mas não utilizadas
        for values in self.dic.values():
            for lista in values:
                for key in lista.keys():
                    if lista[key] is None:
                        print("AVISO: Variável declarada mas não utilizada:", key[0])
        self.dic.popitem()

    def funcao(self, tree):
        print("Funcao")
        self.dic[('Funcao',tree.children[0].value)] = []
        print(self.dic)
        self.visit_children(tree)
        # Verificar variáveis declaradas mas não utilizadas
        for values in self.dic.values():
            for lista in values:
                for key in lista.keys():
                    if lista[key] is None:
                        print("AVISO: Variável declarada mas não utilizada:", key[0])
        self.dic.popitem()

    def parametros(self, tree): 
        self.visit_children(tree)

    def parametro(self, tree):
        # TO-DO check if parameter is used
        # TO-DO check if there are parameters with the same name
        self.visit_children(tree)

    def decls(self, tree):
        self.visit_children(tree)

    def decl(self, tree):
        # dic {(scope, ID): (tipo, valor)}
        print("Decl")

        # verificar se foi declarado
        for values in reversed(self.dic.values()):
            for lista in values:
                for key in lista.keys():
                    print(key[0])
                    print(tree.children[1])
                    if tree.children[1].value == key[0]:
                        print("ERRO: Variável já declarada")
                        return False

        if len(tree.children) == 4:
        # deixa x: Int = 5
            criancas = self.visit_children(tree)
            last_key = list(self.dic.keys())[-1] if self.dic else None
            novo = {(tree.children[1].value, criancas[2]): (criancas[3], criancas[0])}
            self.dic[last_key].append(novo)
            print(self.dic)
        else: 
            criancas = self.visit_children(tree)
            last_key = list(self.dic.keys())[-1] if self.dic else None
            #self.dic[self.scopes, tree.children[1].value] = (criancas[2], None)
            novo = {(tree.children[1].value, criancas[2]): (None, criancas[0])}
            self.dic[last_key].append(novo)
        self.vars[criancas[2]] += 1
        self.instrucoes['declaracoes'] += 1
        print(self.dic)

    def var(self, tree):
        return tree.children[0].value

    def tipo(self, tree):
        return tree.children[0].value

    def insts(self, tree):
        self.visit_children(tree)

    def inst(self, tree):
        print("Inst")
        print(tree.children)
        self.visit_children(tree)

    def atribuicao(self, tree):
        print("Atribuicao")
        print(tree.children)
        # Iterate over the dictionary values
        for inner_dict in self.dic.values():
            # Check if x is equal to any of the IDs in the keys of the inner dictionary
            for list in inner_dict:
                for key in list.keys():
                    print(key[0])
                    print(tree.children[0])
                    print("AAAAAAAAA")
                    print(list[key])
                    if key[0] == tree.children[0].value:
                        if list[key][0] != None and list[key][1] == 'const':
                            print("ERRO: Variável constante não pode ser alterada")
                            return False
                        list[key] = (self.visit_children(tree)[1], list[key][1])
                        self.instrucoes['atribuicoes'] += 1
                        print(self.dic)
                        return True
        print("ERRO: Variável não declarada " + tree.children[0])
        return False

    def chamar(self, tree):
        pass    

    def ler(self, tree):
        print("Ler")
        self.instrucoes['leitura'] += 1
        pass

    def escreve(self, tree):
        print("Escreve")
        self.instrucoes['escrita'] += 1
        pass

    def imprime(self, tree):
        print("Imprime")
        self.instrucoes['imprime'] += 1

    def selecao(self, tree):
        print("Selecao")
        if self.controlo == True:
            self.estruturas_controlo += 1
        self.controlo = True
        self.visit_children(tree)
        self.instrucoes['condicionais'] += 1
        self.controlo = False

    def se(self, tree):
        print("Se")
        if self.insideIf:
            # ir aos filhos ver se existe um se com else ou elif
            for child in tree.children:
                if child.data == 'senao' or child.data == 'defeito':
                    print("AVISO: Condição Se sem Senao ou Defeito dentro de um Se")
        self.insideIf = True
        self.visit_children(tree)
        self.insideIf = False

    def se_expr(self, tree):
        print("Se_expr")
        variavel = self.visit_children(tree)[0]
        k = []
        for values in reversed(self.dic.values()):
            for lista in values:
                for key in lista.keys():
                    k.append(key[0])
        if variavel not in k:
            print("Variável não declarada " + variavel)
            return True

    def caso(self, tree):
        print("Caso")
        pass

    def repeticao(self, tree):
        print("Repeticao")
        if self.controlo == True:
            self.estruturas_controlo += 1
        self.controlo = True
        self.visit_children(tree)
        self.instrucoes['ciclicas'] += 1
        self.controlo = False

    def enq_fazer(self, tree):
        print("Enq_fazer")
        pass

    def repetir_ate(self, tree):
        print("Repetir_ate")
        pass

    def expr(self, tree):
        expr = ''
        print("Expr")
        for i, child in enumerate(tree.children):
            if i == 0 or i % 2 == 0:
                num = child.children[0]
                expr += num
            else:
                op = child
                expr += op
        return eval(expr)

    def term(self, tree):
        return tree.children[0].value


frase1 = """
classe Principal {
    fun Principal() {
        deixa x: Int = 5
    }
    deixa x: Int
    const y: Int = 5
    const z: Int
    x = 5+6
    y = 6
    z = 10
    se z > 0 entao
        main()
    defeito
        escreve "nope"
    fim

    deixa x: Int = 5
    fun main() {
        escreve "Hello, World!"
    }
}

classe Secundaria {
    fun Principal() {
        deixa x: Int = 5
    }
}
"""

frase2 = """
classe Exemplo {
    const VARIAVEL: Int

    fun soma(a: Int, b: Int) => Int {
        c = a + b
    }

    fun imprime_mensagem() {
        escreve "Olá, mundo!"
    }
}

fun main() {
    const numero: Int = 10
    const texto: Estringue = "Python"

    se numero > 0 entao
        escreve "O número é positivo."
    senao numero < 0 entao
        escreve "O número é negativo."
    defeito
        escreve "O número é zero."
    fim

    enq numero > 0 fazer
        imprime_mensagem()
        numero = numero - 1


    corresponde numero com
        caso 1 =>
            escreve "Número é 1."
        caso 2 =>
            escreve "Número é 2."
        defeito =>
            escreve "Número é diferente de 1 e 2."
    fim
}
    """

ifs = """
se 1 entao
    se 2 entao
        escreve "3"
    defeito
        escreve "naaaaaada"
    fim
fim
"""



p = Lark(grammar2) # cria um objeto parser
pydot__tree_to_png(p.parse(ifs),'ifs.png')

tree = p.parse(ifs)  # retorna uma tree
#print(tree)
#print(tree.pretty())
pydot__tree_to_png(tree,'lark_test.png')
data = MyInterpreter().visit(tree)
print(data)


