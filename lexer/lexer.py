import ply.lex as lex
import os
from datetime import datetime

tokens = (
    # ==========================================
    # APORTE DOMENIKA ARBOLEDA
    # Tipos primitivos, variables, literales,
    # operadores aritméticos y de asignación
    # ==========================================
    'INT_TYPE',
    'DOUBLE_TYPE',
    'STRING_TYPE',
    'BOOL_TYPE',
    'VAR',
    'CONST',
    'FINAL',
    'TRUE',
    'FALSE',
    'NULL',
    'IDENTIFICADOR',
    'ENTERO',
    'DECIMAL',
    'CADENA',
    'MAS',
    'MENOS',
    'MULTIPLICACION',
    'DIVISION',
    'MODULO',
    'ASIGNACION',
    'MAS_IGUAL',
    'MENOS_IGUAL',
    'MULT_IGUAL',
    'DIV_IGUAL',

    # Aporte de Henry Olvera
    # Operadores relacionales, lógicos y estructuras de control

    'IF',
    'ELSE',
    'WHILE',
    'FOR',
    'SWITCH',
    'CASE',
    'DEFAULT',
    'BREAK',
    'CONTINUE',

    'MAYOR',
    'MENOR',
    'MAYOR_IGUAL',
    'MENOR_IGUAL',
    'IGUAL_IGUAL',
    'DISTINTO',

    'AND',
    'OR',
    'NOT',
    'INCREMENTO',
    'DECREMENTO',



    # ==========================================
    # APORTE ENRIQUE ROSADO
    # Funciones, clases, delimitadores
    # y manejo de impresión
    # ==========================================
    'VOID',
    'RETURN',
    'CLASS',
    'PRINT',

    'LLAVE_IZQ',
    'LLAVE_DER',
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
    'CORCHETE_IZQ',
    'CORCHETE_DER',
    'PUNTOYCOMA',
    'COMA',
    'DOS_PUNTOS',
    'FLECHA',
    'PUNTO',
)

# ==========================================
# APORTE DOMENIKA ARBOLEDA - INICIO
# ==========================================

palabras_reservadas_dome = {
    'int'   : 'INT_TYPE',
    'double': 'DOUBLE_TYPE',
    'String': 'STRING_TYPE',
    'bool'  : 'BOOL_TYPE',
    'var'   : 'VAR',
    'const' : 'CONST',
    'final' : 'FINAL',
    'true'  : 'TRUE',
    'false' : 'FALSE',
    'null'  : 'NULL',
}

t_MAS            = r'\+'
t_MENOS          = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION       = r'/'
t_MODULO         = r'%'
t_MAS_IGUAL      = r'\+='
t_MENOS_IGUAL    = r'-='
t_MULT_IGUAL     = r'\*='
t_DIV_IGUAL      = r'/='
t_ASIGNACION     = r'='

def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CADENA(t):
    r'\"([^\"\\]|\\.)*\"|\'([^\'\\]|\\.)*\''
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = palabras_reservadas.get(t.value, 'IDENTIFICADOR')
    return t

# ==========================================
# APORTE DOMENIKA ARBOLEDA - FIN
# ==========================================

# ==========================================
# APORTE ENRIQUE ROSADO - INICIO
palabras_reservadas_enrique = {
    'void': 'VOID',
    'return': 'RETURN',
    'class': 'CLASS',
    'print': 'PRINT'

    }

# Delimitadores y símbolos especiales
t_LLAVE_IZQ      = r'\{'
t_LLAVE_DER      = r'\}'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_CORCHETE_IZQ   = r'\['
t_CORCHETE_DER   = r'\]'
t_PUNTOYCOMA     = r';'
t_COMA           = r','
t_DOS_PUNTOS     = r':'
t_FLECHA         = r'=>'
t_PUNTO = r'\.'

# Comentarios de una línea
def t_COMENTARIO_LINEA(t):
    r'//.*'
    pass

# Comentarios multilínea
def t_COMENTARIO_BLOQUE(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

# Control de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de errores léxicos
def t_error(t):
    print(
        f"ERROR LÉXICO: Carácter ilegal '{t.value[0]}' "
        f"en línea {t.lineno}"
    )
    t.lexer.skip(1)

# AUTOR: Enrique Rosado
# ==========================================

# Combinación de las palabras reservadas de los tres aportes
# Palabras reservadas del aporte de Henry
palabras_reservadas_henry = {
    'if'     : 'IF',
    'else'   : 'ELSE',
    'while'  : 'WHILE',
    'for'    : 'FOR',
    'switch' : 'SWITCH',
    'case'   : 'CASE',
    'default': 'DEFAULT',
    'break'  : 'BREAK',
    'continue': 'CONTINUE',
}

# Reglas léxicas (operadores relacionales y lógicos) - aporte Henry
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL  = r'<='
t_IGUAL_IGUAL  = r'=='
t_DISTINTO      = r'!='
t_MAYOR         = r'>'
t_MENOR         = r'<'

t_AND          = r'&&'
t_OR           = r'\|\|'
t_NOT          = r'!'

# Incremento / decremento
t_INCREMENTO   = r'\+\+'
t_DECREMENTO   = r'--'

palabras_reservadas = {
    **palabras_reservadas_dome,
    **palabras_reservadas_henry,
    **palabras_reservadas_enrique
}

lexer = lex.lex()

def analizar_archivo(ruta_archivo, nombre_desarrollador):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        codigo = f.read()

    lexer.input(codigo)
    tokens_encontrados = []

    for tok in lexer:
        tokens_encontrados.append(tok)

    ahora = datetime.now().strftime('%d-%m-%Y-%Hh%M')
    nombre_log = f'lexico-{nombre_desarrollador}-{ahora}.txt'
    ruta_log = os.path.join('logs', nombre_log)

    with open(ruta_log, 'w', encoding='utf-8') as log:
        log.write('ANÁLISIS LÉXICO - ANALIZADOR DART\n')
        log.write(f'Desarrollador: {nombre_desarrollador}\n')
        log.write(f'Archivo analizado: {ruta_archivo}\n')
        log.write(f'Fecha y hora: {datetime.now().strftime("%d/%m/%Y %H:%M")}\n')
        log.write(f'TOKENS ENCONTRADOS: {len(tokens_encontrados)}\n\n')

        for tok in tokens_encontrados:
            log.write(f'[Línea {tok.lineno}] {tok.type:20} → {tok.value}\n')
        log.write('\n')
        log.write('ANÁLISIS COMPLETADO\n')

    print(f'\nLog generado: {nombre_log}')
    print(f'Total de tokens: {len(tokens_encontrados)}')


if __name__ == '__main__':
    analizar_archivo('algoritmos/algoritmo_dome.dart', 'DomenikaArboleda')