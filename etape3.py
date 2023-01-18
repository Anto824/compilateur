import re

TOKENS=["programme","begin","end","read","write","if","while","(",")","var"]
i=0 #indice du token actuel
regex_lit='[a-zA-Z][a-zA-Z_0-9]*'
regex_num='[0-9]+'

PROGRAM=["programme",'abc',';','const','C','=','10',';','D','=','8',';',
         'var','A',',','B',';',
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

token=PROGRAM[0]

offset=0
TABLESYM=[]

def symEntree(classe,value): #cette fonction ajoute une entrée à la table des symboles (TABLESYM) avec le nom, la classe (constant, variable, etc.) et la valeur (offset) donnés en entrée.
    global TABLESYM,offset
    if classe=='constant':
        value=PROGRAM[i+1]
    TABLESYM+=[(PROGRAM[i-1],classe,value)]
    offset+=1
    
def symChercher(sym): #cette fonction cherche dans la table des symboles (TABLESYM) l'entrée correspondant au symbole donné en entrée. Si elle existe, elle retourne l'entrée, sinon elle appelle la fonction erreur_decla.
    global TABLESYM
    res=False
    for s in TABLESYM:
        if s[0]==sym:
            res=s
    if res:
        return res
    else:
        erreur_decla(sym)

length=len(PROGRAM)

def token_suivant(): #cette fonction passe au token suivant
    global i,token
    if i<(len(PROGRAM)-1):
        i+=1
        token=PROGRAM[i]
    
    
def erreur_decla(sym): #cette fonction affiche un message d'erreur si une variable n'est pas déclarée
    print("variable {} not declared".format(sym))
    
def erreur(exp_token,given_token): #cette fonction affiche un message d'erreur si le token donné en entrée n'est pas celui attendu
    print("ERREUR ", "expected: ",exp_token, " given: ",given_token)
    
def test(test_token): #cette fonction teste si le token donné en entrée est le même que le token actuel. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    if test_token==token or re.match(test_token,token):
        token_suivant()
        return 1
    else:
        erreur(test_token, token)
        token_suivant()
        return 0
        
def test_entre(test_token, classe): #cette fonction teste si le token donné en entrée est le même que le token actuel. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    global offset
    if test(test_token)==1:
        symEntree(classe,value=offset)
        
def test_cherche(test_token): #cette fonction teste si le token donné en entrée est le même que le token actuel. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    tok=token
    if test(test_token)==1:
        symChercher(tok)
    
        
def constantes(): #cette fonction teste si le token actuel est une constante. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    test("const")       
    while re.match(regex_lit,token) and token!='var':
        test_entre(regex_lit,"constant")
        test("=")
        test(regex_num)
        test(";")

def variables(): #cette fonction teste si le token actuel est une variable. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    test("var")
    test_entre(regex_lit,'variable')
    while token==",":
        token_suivant()
        test_entre(regex_lit,'variable')
    test(";")
    
def factor(): #cette fonction teste si le token actuel est un facteur. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    if re.match(regex_lit,token):
        test_cherche(regex_lit)
    elif re.match(regex_num, token):
        token_suivant()
    else:
        test("(")
        expression()
        test(")")
    
def termine(): #cette fonction teste si le token actuel est un terme. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.  
    factor()
    while token in ["*","/"]:
        token_suivant()
        factor()
    
def expression(): #cette fonction teste si le token actuel est une expression. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    termine()
    while token in ["+","-"]:
        token_suivant()
        termine()

def condition(): #cette fonction teste si le token actuel est une condition. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    expression()
    if token in ["==","<>","<",">","<=",">="]:
        token_suivant()
        expression()
    
def affectation(): #cette fonction teste si le token actuel est une affectation. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    test_cherche(regex_lit)
    test(":=")
    expression()

def si(): #cette fonction teste si le token actuel est un si. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    test("if")
    condition()
    test("then")
    instance()

def tant_que(): #cette fonction teste si le token actuel est un tant que. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    test("while")
    condition()
    test("do")
    instance()

def ecrire(): #cette fonction teste si le token actuel est un ecrire. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    test("write")
    test("(")
    expression()
    while token==",":
        token_suivant()
        expression()
    test(")")

def lire(): #cette fonction teste si le token actuel est un lire. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    test("read")
    test("(")
    test_cherche(regex_lit)
    while token==",":
        token_suivant()
        test(regex_lit)
    test(")")

def instances(): #cette fonction teste si le token actuel est une instance. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    test("begin")
    instance()  
    while token==";":
        token_suivant()
        #print("instances:",token)
        instance()
    test("end")
    
def instance(): #cette fonction teste si le token actuel est une instance. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    if token=="if":
        si()
    elif token=="while":
        tant_que()
    elif token=="begin":
        instances()
    elif token=="write":
        ecrire()
    elif token=="read":
        lire()
    elif re.match(regex_lit,token) and token not in TOKENS:        
        affectation()

        
def block(): #cette fonction teste si le token actuel est un block. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    if token=="const":
        constantes()
    if token=="var":
        variables()
    instances()
    
def programme(): #cette fonction teste si le token actuel est un programme. Si c'est le cas, elle passe au token suivant, sinon elle appelle la fonction erreur.
    test("programme")
    test_entre(regex_lit, 'programme')
    test(";")
    block()
    if token != ".":
        erreur(".",token)
    
programme()