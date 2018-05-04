import ply.yacc as yacc
import re
import codecs
from analexico import tokens
from sys import stdin
from colorama import Fore

# resultado del analisis
resultado_gramatica = []

precedence =(
    ('right','ASIGNAR'),
    ('right','DISTINTO'),
)
def p_P1(p):
    '''P : S PUNTOCOMA'''
    print("P1")
def p_P2(p):
    '''P : S PUNTOCOMA P'''
    print("P2")

def p_S1(p):
    '''S : SELECT A FROM T B'''
    print("S 1")
def p_S2(p):
    '''S : DELETE FROM T Bp'''
    print('S 2')
def p_S3(p):
    '''S : UPDATE T SET N W'''
    print('S 3')
def p_S4(p):
    '''S : INSERT INTO T PARENTESIS Ap PARENTESIS VALUES Y'''
    print('S 4')

def p_A1(p):
    '''A : TODO'''
    print("A 1")
def p_A2(p):
    '''A : Ap'''
    print("A 2")
def p_A3(p):
    '''A : M'''
    print("A 3")

def p_Ap1(p):
    '''Ap : T PUNTO T'''
    print("Ap 1")
def p_Ap2(p):
    '''Ap : T PUNTO T COMA Ap'''
    print("Ap 2")


def p_M(p):
    '''M : OP_M PARENTESIS Mp PARENTESIS'''
    print("M")

def p_Mp1(p):
    '''Mp : TODO'''
    print("Mp 1")
def p_Mp2(p):
    '''Mp : T PUNTO T'''
    print("Mp 2")


def p_T(p):
    '''T : ID'''
    print('T')

def p_B1(p):
    '''B : Bp'''
    print('B 1')
def p_B2(p):
    '''B : J T ON E'''
    print('B 2')

def p_Bp1(p):
    '''Bp : W'''
    print('Bp 1')
def p_BpEmpty(p):
    '''Bp : empty'''
    print('Bp e') 

def p_W(p):
    '''W : WHERE C'''
    print('W')

def p_C1(p):
    '''C : NOT PARENTESIS F PARENTESIS'''
    print('C 1') 
def p_C2(p):
    '''C : F'''
    print('C 2') 

def p_F1(p):
    '''F : Fp'''
    print('F 1')
def p_F2(p):
    '''F : Fp OP_L F'''
    print('F 2')

def p_Fp(p):
    '''Fp : T PUNTO T R V'''
    print('Fp') 

def p_R1(p):
    '''R : OP_R'''
    print('R 1')
def p_R2(p):
    '''R : DISTINTO'''
    print('R 2')

def p_V1(p):
    '''V : Q'''
    print('V 1')
def p_V2(p):
    '''V : CADENA'''
    print('V 2')
def p_V3(p):
    '''V : FECHA'''
    print('V 3')
def p_V4(p):
    '''V : BOOL'''
    print('V 4')


def p_Q1(p):
    '''Q : INTEGER'''
    print('Q 1')
def p_Q2(p):
    '''Q : DOUBLE'''
    print('Q 2')
def p_Q3(p):
    '''Q : INTEGER U Q'''
    print('Q 3')
def p_Q4(p):
    '''Q : DOUBLE U Q'''
    print('Q 4')

def p_U1(p):
    '''U : OP_A_S'''
    print('U 1')
def p_U2(p):
    '''U : OP_A_C'''
    print('U 2')

def p_J(p):
    '''J : Jp JOIN'''
    print('J')

def p_Jp(p):
    '''Jp : TIPO_JOIN'''
    print('Jp')

def p_E(p):
    '''E : T PUNTO T OP_R T PUNTO T'''
    print('E')

def p_N1(p):
    '''N : T PUNTO T ASIGNAR V'''
    print('N 1')
def p_N2(p):
    '''N : T PUNTO T ASIGNAR V COMA N'''
    print('N 2')

def p_Vp1(p):
    '''Vp : V'''
    print('Vp 1')
def p_Vp2(p):
    '''Vp : V COMA Vp'''
    print('Vp 2')
def p_Y1(p):
    '''Y : PARENTESIS Vp PARENTESIS'''
    print('Y 1')

def p_Y2(p):
    '''Y : PARENTESIS Vp PARENTESIS COMA Y'''
    print('Y 2')

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print("Error de sintaxis",p)
    print("Error en la linea",str(p.lineno))

directorio = '../ASintactico/'
archivo = 'test2.vye'
test = directorio+archivo
fp =codecs.open(test,'r','utf-8')
cadena = fp.read()
fp.close()

# instanciamos el analizador sintactico
print(Fore.MAGENTA+"---ANALISIS SINTACTICO---")
parser = yacc.yacc()
result = parser.parse(cadena)

#print("Resultado ", result)
