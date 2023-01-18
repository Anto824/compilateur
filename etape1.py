MNEMONIQUES=["ADD","SUB","MUL","DIV","EQL","NEQ","GTR","LSS","GEQ",
             "LEQ","PRN","INN","INT","LDI","LDA","LDV","STO","BRN",
             "BZE","HLT"]
    
def interpreteur(PCODE):
    memory=[]
    pointeur_pile=0 
    p_instruction=0 
    status="EXECUTION" 
    instru_actuelle="" 
    while status!="END":
        instru_actuelle=PCODE[p_instruction][0]     
        OPERANDE=PCODE[p_instruction][1]
        if p_instruction<(len(PCODE)-1):
            p_instruction+=1
        if instru_actuelle=="ADD":#additionne les deux derniers éléments de la mémoire et remplace leur somme à la place des deux éléments.
            memory[-2]=memory[-1]+memory[-2]
            del memory[-1]
        elif instru_actuelle=="SUB":#soustrait le dernier élément de la mémoire au deuxième dernier élément et remplace la différence à la place des deux éléments.
            memory[-2]=memory[-2]-memory[-1]
            del memory[-1]
        elif instru_actuelle=="MUL":#multiplie les deux derniers éléments de la mémoire et remplace leur produit à la place des deux éléments.
            memory[-2]=memory[-1]*memory[-2]
            del memory[-1]
        elif instru_actuelle=="DIV":#divise le deuxième dernier élément de la mémoire par le dernier élément et remplace le quotient à la place des deux éléments.
            memory[-2]=memory[-2]+memory[-1]
            del memory[-1]
        elif instru_actuelle=="EQL":#vérifie si les deux derniers éléments de la mémoire sont égaux et remplace le résultat (0 ou 1) à la place des deux éléments.
            memory[-2]=int(memory[-1]==memory[-2])
            del memory[-1]
        elif instru_actuelle=="NEQ":#vérifie si les deux derniers éléments de la mémoire sont différents et remplace le résultat (0 ou 1) à la place des deux éléments.
            memory[-2]=int(memory[-1]!=memory[-2])
            del memory[-1]
        elif instru_actuelle=="GTR":#vérifie si le deuxième dernier élément de la mémoire est plus grand que le dernier élément et remplace le résultat (0 ou 1) à la place des deux éléments.
            memory[-2]=int(memory[-2]>memory[-1])
            del memory[-1]
        elif instru_actuelle=="LSS":#vérifie si le deuxième dernier élément de la mémoire est plus petit que le dernier élément et remplace le résultat (0 ou 1) à la place des deux éléments.
            memory[-2]=int(memory[-2]<memory[-1])
            del memory[-1]
        elif instru_actuelle=="GEQ":#vérifie si le deuxième dernier élément de la mémoire est plus grand ou égal au dernier élément et remplace le résultat (0 ou 1) à la place des deux éléments.
            memory[-2]=int(memory[-2]>=memory[-1])
            del memory[-1]
        elif instru_actuelle=="LEQ":#vérifie si le deuxième dernier élément de la mémoire est plus petit ou égal au dernier élément et remplace le résultat (0 ou 1) à la place des deux éléments.
            memory[-2]=int(memory[-2]<=memory[-1])
            del memory[-1]
        elif instru_actuelle=="PRN":#affiche la dernière valeur de la mémoire.
            print("res =",memory[-1])
            del memory[-1]
        elif instru_actuelle=="INN":#demande à l'utilisateur d'entrer une valeur et l'enregistre à l'adresse spécifiée par le dernier élément de la mémoire.
            a=int(input("entrez une valeur: "))
            adresse=memory[-1]
            memory[adresse]=a
            del memory[-1]
        elif instru_actuelle=="INT": #alloue un certain nombre d'espaces vides dans la mémoire pour stocker des données.
            memory+=[0]*OPERANDE
            pointeur_pile+=OPERANDE
        elif instru_actuelle=="LDI":#charge une valeur immédiate dans la mémoire.
            memory+=[OPERANDE]
        elif instru_actuelle=="LDA":#charge l'adresse spécifiée dans la mémoire.
            memory+=[OPERANDE]
        elif instru_actuelle=="LDV":#charge la valeur stockée à l'adresse spécifiée par le dernier élément de la mémoire.
            memory[-1]=memory[memory[-1]]
        elif instru_actuelle=="STO":#stocke la valeur du dernier élément de la mémoire à l'adresse spécifiée par l'avant-dernier élément de la mémoire.
            memory[memory[-2]]=memory[-1]
            del memory[-1]
            del memory[-1]
        elif instru_actuelle=="BRN":#saute à l'instruction spécifiée par l'opérande.
            p_instruction=OPERANDE
        elif instru_actuelle=="BZE":#saute à l'instruction spécifiée par l'opérande si la valeur du dernier élément de la mémoire est égale à zéro.
            if(memory[-1]==0):
                p_instruction=OPERANDE
            del memory[-1]
        elif instru_actuelle=="HLT":#arrête l'exécution du programme.
            status="END"
            
        
PCODE=[("INT",2),("LDA",0),("INN",False),("LDA",1),("LDA",0),("LDV",False),
       ("LDA",1),("LDV",False),("ADD",False),("STO",False),("LDA",0),
       ("LDV",False),("LDI",0),("EQL",False),("BZE",1),("LDA",1),("LDV",False),
       ("PRN",False),("HLT",False)]

interpreteur(PCODE)