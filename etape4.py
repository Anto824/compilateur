import re

TOKENS=["programme","begin","end","read","write","if","while","(",")","var"]
i=0 #indice du token actuel
regex_lit='[a-zA-Z][a-zA-Z_0-9]*'
regex_num='[0-9]+'

PROGRAM=["programme",'abc',';',
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

def next_inst(compt): #retourne le prochain numero d'instruction
    return False

def getAdresseFromTableSym(nomVar): #retourne l'adresse de la variable
    ADDR=0
    for dec in TABLESYM:
        if dec[0]==nomVar:
            ADDR=dec[2]
    return ADDR

def symEntree(classe,value): #entree dans la table des symboles
    global TABLESYM,offset
    if classe=='constant':
        value=PROGRAM[i+1]
    TABLESYM+=[(PROGRAM[i-1],classe,value)]
    offset+=1
    
def symChercher(sym): #cherche dans la table des symboles
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

def token_suivant(): #passe au token suivant
    global i,token
    if i<(len(PROGRAM)-1):
        i+=1
        token=PROGRAM[i]
    
    
def erreur_decla(sym): #erreur de declaration
    print("variable {} not declared".format(sym))
    
def erreur(exp_token,given_token): #erreur de syntaxe
    print("ERREUR ", "expected: ",exp_token, " given: ",given_token)
    
def test(test_token): #test si le token est correct
    if test_token==token or re.match(test_token,token):
        token_suivant()
        return 1
    else:
        erreur(test_token, token)
        token_suivant()
        return 0
        
def test_entre(test_token, classe): #test si le token est correct et entre dans la table des symboles
    global offset
    if test(test_token)==1:
        symEntree(classe,value=offset)
        
def test_cherche(test_token):#test si le token est dans la table des symboles
    tokenn=token
    if test(test_token)==1:
        symChercher(tokenn)
    
        
def constantes():#analyse des constantes
    test("const")       
    while re.match(regex_lit,token) and token!='var':
        test_entre(regex_lit,"constant")
        test("=")
        test(regex_num)
        test(";")

def variables():#analyse des variables
    test("var")
    test_entre(regex_lit,'variable')
    while token==",":
        token_suivant()
        test_entre(regex_lit,'variable')
    test(";")
    
def factor():#analyse des facteurs
    if re.match(regex_lit,token):#si c'est une variable
        nomVar=token
        test_cherche(regex_lit)
        for line in TABLESYM:#on cherche dans la table des symboles
            if line[1]=='constant':#si c'est une constante
                genere_bis('LDI',TABLESYM.index(line))
            if line[1]=='variable':#si c'est une variable
                genere_bis('LDA',getAdresseFromTableSym(nomVar))
                genere('LDV')
    elif re.match(regex_num, token):#si c'est un nombre
        genere_bis('LDI',token)
        token_suivant()
        
    else:#si c'est une expression
        test("(")
        expression()
        test(")")
    
def termine(): #analyse des termes
    global token
    factor()
    while token in ["*","/"]:
        op=token
        token_suivant()
        factor()
        if op=="*":
            genere('MUL')
        else:
            genere('DIV')
    
def expression(): #analyse des expressions
    global token
    #print("expr_token: ",token)
    termine()
    while token in ["+","-"]:
        op=token
        token_suivant()
        termine()
        if op=="+":
            genere('ADD')
        else:
            genere("SUB")

def condition(): #analyse des conditions
    expression()
    if token in ["==","<>","<",">","<=",">="]:
        token_suivant()
        expression()
    
def affectation():  #analyse des affectations
    global token,PLACESYM
    #recherche de l'adresse de la variable
    ADDR=getAdresseFromTableSym(token)
    test_cherche(regex_lit)
    genere_bis('LDA', ADDR)
    test(":=")
    expression()
    genere('STO')

def si(): #analyse des conditions
    test("if")
    condition()
    test("then")
    genere_bis('BZE',0)
    instance()

def tant_que(): #analyse des boucles
    test("while")
    condition()
    test("do")
    instance()

def ecrire(): #analyse des instructions d'ecriture
    test("write")
    test("(")
    expression()
    genere('PRN')
    while token==",":
        token_suivant()
        expression()
        genere('PRN')
    test(")")

def lire(): #analyse des instructions de lecture
    test("read")
    test("(")
    nomVar=token
    test_cherche(regex_lit)
    genere_bis('LDA',getAdresseFromTableSym(nomVar))
    genere('INN')
    while token==",":
        token_suivant()
        nomVar=token
        test(regex_lit)
        genere_bis('LDA',getAdresseFromTableSym(nomVar))
        genere('INN')
    test(")")

def instances(): 
    instance ()  
    while token==";":
        token_suivant()
        instance()
    test("end")
    
def instance(): 
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

        
def block(): #analyse des blocs
    global offset
    if token=="const":
        constantes()
    if token=="var":
        variables()
    genere_bis('INT', offset)
    instances()
    
def programme(): #analyse du programme
    test("programme")
    test_entre(regex_lit, 'programme')
    test(";")
    block()
    genere('HLT')
    if token != ".":
        erreur(".",token)
    
PCODE=[0]*50#tableau du code
PC=0#compteur du code
        
def genere(m): #generation du code
    global PCODE,PC
    if PC==len(PROGRAM):
        print('Error len')
    PCODE[PC]=m
    PC+=1
    
def genere_bis(m,a): #generation du code
    global PCODE,PC
    if PC==len(PROGRAM):
        print('Error len')
    PCODE[PC]=(m,a)
    PC+=1
    
    
programme()

print(PCODE)