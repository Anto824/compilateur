import re

mots_cles=["programme","begin","end","read","write","if","while","(",")"]
i = 0 #indice du token actuel
regex_lit = '[a-zA-Z][a-zA-Z_0-9]*' #regex pour les litteraux
regex_num = '[0-9]+' #regex pour les nombres
 
PROGRAM = ["programme",'abc',';','const','C','=','10',';','var','A',',','B',';',
         'begin',
         'A',':=','0',';',
         'B',':=','0',';',
         'while','A','<>','0','do',
         'begin',
         'read','(','A',')',';',
         'B',':=','A','+','B',';',
         'end',';',
         "write",'(','B',')',';', 
         'end','.']

token = PROGRAM[0]

taille_code = len(PROGRAM)



def token_suivant():#avance le token courant
    global i,token
    if i < (len(PROGRAM)-1):
        i += 1
        token = PROGRAM[i]
    
def erreur(exp_token,given_token):#affiche une erreur
    print("ERREUR ", "expected: ", exp_token, " given: ", given_token)
    
def test(test_token):#test si le token courant est le token attendu
    if test_token == token or re.match(test_token,token):
        token_suivant()
        return 1
    else:
        erreur(test_token, token)
        token_suivant()
        
def constantes(): #analyse les constantes
    test("const")    
    while re.match(regex_lit,token) and token!='var':
        test(regex_lit)
        test("=")
        test(regex_num)
        test(";")
    

def variables(): #analyse les variables
    test("var")
    test(regex_lit)
    while token == ",":
        token_suivant()
        test(regex_lit)
    test(";")
    
def factor(): #analyse les facteurs
    if re.match(regex_lit,token) or re.match(regex_num, token):
        token_suivant()
    else:
        test("(")
        expression()
        test(")")
    
def termine(): #analyse les termes
    factor()
    while token in ["*","/"]:
        token_suivant()
        factor()
    
def expression(): #analyse les expressions
    termine()
    while token in ["+","-"]:
        token_suivant()
        termine()

def condition(): #analyse les conditions
    expression()
    if token in ["==","<>","<",">","<=",">="]:
        token_suivant()
        expression()
    
def affectation(): #analyse les affectations
    test(regex_lit)
    test(":=")
    expression()

def si(): #analyse les si
    test("if")
    condition()
    test("then")
    instance()

def tant_que(): #analyse les tant que
    test("while")
    condition()
    test("do")
    instance()

def ecrire():  #analyse les ecrire
    test("write")
    test("(")
    expression()
    while token == ",":
        token_suivant()
        expression()
    test(")")

def lire():  #analyse les lire
    test("read")
    test("(")
    test(regex_lit)
    while token == ",":
        token_suivant()
        test(regex_lit)
    test(")")

def instances(): #analyse les instances
    test("begin")
    instance()  
    while token == ";":
        token_suivant()
        instance()
    test("end")
    
def instance():     #analyse les instances
    if token == "if":
        si()
    elif token == "while":
        tant_que()
    elif token == "begin":
        instances()
    elif token == "write":
        ecrire()
    elif token == "read":
        lire()
    elif re.match(regex_lit,token) and token not in mots_cles:        
        affectation()

        
def block(): #analyse les blocs
    if token == "const":
        constantes()
    if token == "var":
        variables()
    instances()
    
def programme(): #analyse les programmes
    test("programme")
    test(regex_lit)
    test(";")
    block()
    if token != ".":
        erreur(".",token)
    
programme()
