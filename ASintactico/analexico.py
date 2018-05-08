import ply.lex as lex
import re
import codecs
from colorama import Fore

resultado_lexema=[]
tabla=[]
cadena =''

reservada = (
    # Palabras Reservadas
    'SELECT','INSERT','DELETE','UPDATE',
    'VALUES',
    'FROM',
    'WHERE',
    'SET',
    'INTO',
    'JOIN',
    'ON'
)
tokens = reservada + (
    'ID',
    'INTEGER',
    'DOUBLE',
    'CADENA',
    'FECHA',
    'BOOL',
    'ASIGNAR',
    #aritmeticos
    'OP_A',
    #logica
    'OP_L', # and | or 
    'NOT',
    #relacional
    'OP_R',
    'DISTINTO',

    'TIPO_JOIN', # inner| right | left
    'GROUP_BY', # group_by
    'OP_M', # count| max | min | sum | avg

    # Simbolos
    'ALL',

    # Otros
    'PUNTOCOMA',
    'PUNTO',
    'COMA',
    'PARENTESIS_A',
    'PARENTESIS_C',    
)

# Reglas de Expresiones Regualres para token de Contexto simple

t_OP_A= r'\+|-|/|\*'

t_ASIGNAR = r'='
# Expresiones Logicas
t_OP_R = r'<=?|>=?|=='

#t_COMILLA = r'(\'|")'
t_PUNTOCOMA = r';'
t_COMA = r','
t_PUNTO = r'\.'
t_PARENTESIS_A = r'\('
t_PARENTESIS_C = r'\)'
t_ignore =' \t'
t_INTEGER = r'-?\d+'
t_DOUBLE = r'-?\d+\.\d+'
t_CADENA = r'(\'|")[\w ]+[\w\W\d\D\s]*(\'|")'

def t_OP_L(t):
    r'((and|\&\&)|(\|{2}|or))'
    return t
def t_ALL(t):
    r'all'
    return t
def t_NOT(t):
    r'not'
    return t
def t_ON(t):
    r'on'
    return t
def t_INTO(t):
    r'into'
    return t
def t_FECHA(t):
    r'([0-2][0-9]|3[0-1])(-|/)(0[1-9]|1[0-2])(-|/)(\d{4})'
    return t
def t_BOOL(t):
    r'(true|false)'
    return t
def t_OP_M(t):
    r'(count|max|min|sum|avg)'
    return t

def t_TIPO_JOIN(t):
    r'(inner|right|left)'
    return t
def t_GROUP_BY(t):
    r'group_by'
    return t

def t_ID(t):
    r'[a-zA-Z_]+\w*'
    if t.value.upper() in reservada:
        t.value = t.value.upper()
        t.type = t.value
    return t


def t_DISTINTO(t):
    r'<>'
    return t

def t_comentario_block(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    print("Comentario de multiple linea")

def t_comentario(t):
     r'--(.)*'
     t.lexer.lineno += 1
     print("Comentario de una linea")

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error( t):
    #global resultado_lexema
    print("** Token no valido en la Linea {:4} Valor {:16} Posicion {:4}".format(str(t.lineno), str(t.value),str(t.lexpos)))
    #resultado_lexema.append(estado)
    t.lexer.skip(1)

def agregar_tabla_simbolos(t,val):
    if(t=='ID'):
        tabla.append("|{:4}\t|{:5}\t\t|{:4}\t\t|".format(t,val, 'string'))

def imprimir(res):
    for i in res:
        if(i[:2]=="**"):
            print(Fore.RED+i)
        else:
            print(Fore.BLACK+i)

########## Analisis Sintactico ###############

noTerminales =['P','S','A','AP','AN','M','MP','T','B','BP',
            'W','G','C','F','Z','FP','R','V','Q','QP',
            'U','J','JP','E','N','NP','Y','YP','VO','O']
Terminales = list(tokens)
Terminales.append('$')

gramatica ={
    'P':[['SELECT','DELETE','UPDATE','INSERT','$'],[
        ['S','PUNTOCOMA','P'],
        ['S','PUNTOCOMA','P'],
        ['S','PUNTOCOMA','P'],
        ['S','PUNTOCOMA','P'],
        ['e']
        ]],
    'S':[['SELECT','DELETE','UPDATE','INSERT'],[
        ['SELECT','A','FROM','T','B'],
        ['DELETE','FROM','T','BP'],
        ['UPDATE','T','SET','N','W'],
        ['INSERT','INTO','T','PARENTESIS_A','AP','PARENTESIS_C','VALUES','Y'],
        ]],
    'A':[['ALL','OP_M','ID'],[
        ['ALL'],
        ['M'],
        ['AP'],
        ]],
    'AP':[['ID'],[
        ['T','PUNTO','T','AN']
        ]],
    'AN':[['FROM','COMA','PARENTESIS_C'],[
        ['e'],
        ['COMA','AP'],
        ['e']
        ]],
    'M':[['OP_M'],[
        ['OP_M']
        ]],
    'MP':[['ALL','ID'],[
        ['ALL'],
        ['T','PUNTO','T']
        ]],
    'T':[['ID'],[
        ['ID']
        ]],
    'B':[['PUNTOCOMA','GROUP_BY','WHERE','TIPO_JOIN'],[
        ['e'],
        ['GROUP_BY','T','PUNTO','T'],
        ['BP'],
        ['J','T','ON','E']
        ]],
    'BP':[['PUNTOCOMA','WHERE'],[
        ['e'],
        ['W']
        ]],
    'W':[['WHERE'],[
        ['WHERE','C','G']
        ]],
    'G':[['PUNTOCOMA','GROUP_BY'],[
        ['e'],
        ['GROUP_BY','T','PUNTO','T']
        ]],
    'C':[['ID','NOT'],[
        ['F'],
        ['NOT','PARENTESIS_A','F','PARENTESIS_C']
        ]],
    'F':[['ID'],[
        ['FP','Z']
        ]],
    'Z':[['PUNTOCOMA','GROUP_BY','PARENTESIS_C','OP_L'],[
        ['e'],
        ['e'],
        ['e'],
        ['OP_L','F']
        ]],
    'FP':[['ID'],[
        ['T','PUNTO','T','R','V']
        ]],
    'R':[['OP_R','DISTINTO'],[
        ['OP_R'],
        ['DISTINTO']
        ]],
    'V':[['INTEGER','DOUBLE','CADENA','FECHA','BOOL'],[
        ['Q'],
        ['Q'],
        ['CADENA'],
        ['FECHA'],
        ['BOOL']
        ]],
    'Q':[['INTEGER','DOUBLE'],[
        ['INTEGER','QP'],
        ['DOUBLE','QP'],
        ]],
    'QP':[['COMA','PARENTESIS_C','OP_A','OP_L'],[
        ['e'],
        ['e'],
        ['U','Q'],
        ['e'],
        ]],
    'U':[['OP_A'],[
        ['OP_A']
        ]],
    'J':[['TIPO_JOIN'],[
        ['JP','JOIN']
        ]],
    'JP':[['TIPO_JOIN'],[
        ['TIPO_JOIN']
        ]],
    'E':[['ID'],[
        ['T','PUNTO','T','OP_R','T','PUNTO','T']
        ]],
    'N':[['ID'],[
        ['T','PUNTO','T','ASIGNAR','V','NP']
        ]],
    'NP':[['COMA','WHERE'],[
        ['COMA','N'],
        ['e']
        ]],
    'Y':[['PARENTESIS_A'],[
        ['PARENTESIS_A','VP','PARENTESIS_C','YP']
        ]],
    'YP':[['COMA','PUNTOCOMA'],[
        ['COMA','Y'],
        ['e']
        ]],
    'VP':[['INTEGER','DOUBLE','CADENA','FECHA','BOOL'],[
        ['V','O'],
        ['V','O'],
        ['V','O'],
        ['V','O'],
        ['V','O'],
        ]],
    'O':[['COMA','PARENTESIS_C'],[
        ['COMA','VP'],
        ['e']
        ]],
}   

def find(end_pila, first_lt):
    if(end_pila in gramatica): # si es un NO terminal
        if( first_lt in gramatica[end_pila][0]):
            #print('en mi ',end_pila, ' si hay ',first_lt)
            index = gramatica[end_pila][0].index(first_lt)
            lista = gramatica[end_pila][1][index]
            alreves=[]
            for i in range(len(lista)-1, -1, -1):
                alreves.append(lista[i])
            return alreves
        else:
            #print('en mi ',end_pila, ' no hay ',first_lt)
            return False
    elif(end_pila in Terminales and end_pila == first_lt): #si es un Terminal
        #print(end_pila, first_lt)
        return True
    else:  # error
        return False

def pila_Sintac(l_tokens):
    l_tokens.append('$')
    pila = ['$','P']
    print(pila)
    #print(pila,'\n',l_tokens)
    while len(pila)>0 or len(l_tokens)>0:
        end = len(pila)-1 
        if(pila[end] == 'e'):
            pila.pop(len(pila)-1)
            end-=1
        #print('--------\n busco ',pila[end],' ',l_tokens[0])
        gram = find(pila[end],l_tokens[0])
        #print('--------\n')
        if(gram != False and gram != True): #lista
            pila.pop(len(pila)-1) # ultimo
            pila= pila + gram
            print(pila)
            #print(pila,'\n',l_tokens)
        elif(gram == True): # terminal igual en pila y l_tokens
            pila.pop(len(pila)-1)
            l_tokens.pop(0)
            print(pila)
            #print(pila,'\n',l_tokens)
        elif(gram == False):
            print('error:', pila[end],' - ',l_tokens[0])
            if(pila[end] in gramatica):
                l_tokens[0]= gramatica[pila[end]][0][0]
            print(pila)
            #print(pila,'\n',l_tokens)
            if(l_tokens[0]=='$'):
                return
        #print('itero',len(pila))
        #input('Enter your input:') 


# instanciamos el analizador lexico
analizador = lex.lex()

def a_lexico():
    directorio = '../ASintactico/'
    archivo = 'test2.vye'
    test = directorio+archivo
    fp =codecs.open(test,'r','utf-8')
    cadena = fp.read()
    fp.close()
    analizador.input(cadena)
    ### lee tokens ###
    cadena_result=''
    lista_tokens=[]
    while True:
        tok = analizador.token()
        if not tok:
            break
        # print("lexema de "+tok.type+" valor "+tok.value+" linea "tok.lineno)
        estado = "Linea {:40} Tipo {:16} Valor {:16} Posicion {:4}".format(str(tok.lineno),str(tok.type) ,str(tok.value), str(tok.lexpos))
        resultado_lexema.append(estado)
        cadena_result+= str(tok.type)+" "
        agregar_tabla_simbolos(str(tok.type) ,str(tok.value))
        lista_tokens.append(str(tok.type))
    
    imprimir(resultado_lexema)
    print(Fore.YELLOW+"\nANALISIS LEXICO:\n"+Fore.BLUE + cadena_result)
    print(Fore.BLACK+"TABLA DE SIMBOLOS\n"+"|Id\t|Nombre\t\t|Tipo\t\t|")
    tabla_simb = set(tabla)
    imprimir(tabla_simb)

    return lista_tokens

list_tokens = a_lexico()
print('\nPILA')
pila_Sintac(list_tokens)
print('termine')
