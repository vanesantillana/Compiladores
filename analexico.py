import ply.lex as lex
import codecs
resultado_lexema=[]

reservada = (
    # Palabras Reservadas
    'SELECT','INSERT','DELETE','UPDATE',
    'VALUES',
    'FROM',
    'WHERE',
    'SET',
    'JOIN',
    'INT',
    'DOUBLE',
    'VARCHAR',
    'DATE',
    'BOOLEAN'
)
tokens = reservada + (
    'ID',
    'NUMERO',
    'FECHA',
    'BOOL',
    'ASIGNAR',
    #aritmeticos
    'OP_A',
    #logica
    'OP_L', # and | or |not
    #relacional
    'OP_R',
    'DISTINTO',
    
    'TIPO_JOIN', # inner| right | left
    'GROUP_BY', # group_by
    'COUNT',
    'OP_M', # max | min | sum | avg

    # Simbolos
    'TODO',

    # Otros
    'PUNTOCOMA',
    'PUNTO',
    'COMA',
    'PARENTESIS',
    'LLAVE',
    'COMENTARIO',
    'COMENTARIO_BLOCK'

)

# Reglas de Expresiones Regualres para token de Contexto simple

t_OP_A= r'\+|-|/|\^'
t_ASIGNAR = r'='
# Expresiones Logicas
t_OP_R = r'((<|>|=)=?)'
t_TODO = r'\*'

t_PUNTOCOMA = ';'
t_COMA = r','
t_PARENTESIS = r'(\(|\))'
t_LLAVE= r'({|})'

def t_FECHA(t):
    r'([0-2][0-9]|3[0-1])(-|/)(0[1-9]|1[0-2])(-|/)(\d{4})'
    return t;
def t_BOOL(t):
    r'(true|false)'
    return t
def t_OP_M(t):
    r'(max|min|sum|avg)'
    return t
def t_COUNT(t):
    r'count'
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

def t_NUMERO(t):
    r'[0-9]+([,][0-9]+)?'
    t.value = int(t.value)
    return t

def t_OP_L(t):
    r'((and|\&\&)|(\|{2}|or)|(not|!))'
    return t

def t_DISTINTO(t):
    r'<>'
    return t

def t_COMENTARIO_BLOCK(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    print("Comentario de multiple linea")

def t_COMENTARIO(t):
     r'--(.)*'
     t.lexer.lineno += 1
     print("Comentario de una linea")
t_ignore =' \t'

def t_error( t):
    global resultado_lexema
    estado = "** Token no valido en la Linea {:4} Valor {:16} Posicion {:4}".format(str(t.lineno), str(t.value),str(t.lexpos))
    resultado_lexema.append(estado)
    t.lexer.skip(1)

def imprimir(res):
    for i in resultado_lexema:
        print(i)

# Prueba de ingreso
def prueba(data):
    analizador = lex.lex()
    analizador.input(data)

    resultado_lexema.clear()
    while True:
        tok = analizador.token()
        if not tok:
            break
        # print("lexema de "+tok.type+" valor "+tok.value+" linea "tok.lineno)
        estado = "Linea {:4} Tipo {:16} Valor {:16} Posicion {:4}".format(str(tok.lineno),str(tok.type) ,str(tok.value), str(tok.lexpos) )
        resultado_lexema.append(estado)
    return resultado_lexema

 # instanciamos el analizador lexico
analizador = lex.lex()

if __name__ == '__main__':
    while True:
        data = input("Ingrese: ")
        prueba(data)
        imprimir(resultado_lexema)