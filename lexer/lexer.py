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

    # ==========================================
    # APORTE HENRY OLVERA
    # Operadores relacionales, lógicos y
    # estructuras de control
    # ==========================================



    # ==========================================
    # APORTE ENRIQUE ROSADO
    # Funciones, clases, delimitadores
    # y manejo de impresión
    # ==========================================

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
# APORTE HENRY OLVERA - INICIO
#
# RESPONSABILIDAD:
# Implementar el reconocimiento léxico de:
#
# 1. ESTRUCTURAS DE CONTROL DE FLUJO:
#    - if
#    - else
#    - while
#    - for
#    - switch
#    - case
#    - default
#    - break
#    - continue
#
# 2. OPERADORES RELACIONALES:
#    - >
#    - <
#    - >=
#    - <=
#    - ==
#    - !=
#
# 3. OPERADORES LÓGICOS:
#    - &&
#    - ||
#    - !
#
# TAREAS:
# - Definir los tokens correspondientes.
# - Registrar las palabras reservadas de control.
# - Implementar las expresiones regulares para
#   operadores relacionales y lógicos.
# - Validar que los tokens sean reconocidos
#   correctamente durante el análisis léxico.
# - Realizar pruebas utilizando estructuras
#   condicionales y ciclos en archivos Dart.
#
# EJEMPLOS A VALIDAR:
#
# if (edad >= 18 && activo == true) {
#     print("Acceso permitido");
# }
#
# while (contador < 10) {
#     contador++;
# }
#
# switch(opcion) {
#     case 1:
#         break;
#     default:
#         break;
# }
#
# AUTOR: Henry Olvera
# ==========================================

# ==========================================
# APORTE ENRIQUE ROSADO - INICIO
#
# RESPONSABILIDAD:
# Implementar el reconocimiento léxico de:
#
# 1. PALABRAS RESERVADAS RELACIONADAS CON
#    FUNCIONES, CLASES Y SALIDA DE DATOS:
#    - void
#    - return
#    - class
#    - print
#
# 2. DELIMITADORES Y SÍMBOLOS ESPECIALES:
#    - { }
#    - ( )
#    - [ ]
#    - ;
#    - ,
#    - :
#    - =>
#
# 3. MANEJO DE COMENTARIOS:
#    - Comentarios de línea (//)
#    - Comentarios de bloque (/* */)
#
# 4. CONTROL DE LÍNEAS:
#    - Actualizar correctamente el contador
#      de líneas del lexer.
#
# 5. MANEJO DE ESPACIOS Y TABULACIONES:
#    - Ignorar espacios en blanco y tabuladores.
#
# 6. MANEJO DE ERRORES LÉXICOS:
#    - Detectar caracteres inválidos.
#    - Reportar línea del error.
#    - Continuar el análisis después del error.
#
# TAREAS:
# - Definir tokens para delimitadores.
# - Implementar expresiones regulares para
#   símbolos de agrupación y separación.
# - Implementar reglas para comentarios.
# - Implementar actualización de líneas.
# - Implementar ignorado de espacios.
# - Implementar función de manejo de errores.
#
# EJEMPLOS A VALIDAR:
#
# class Pelicula {
#     void mostrar() {
#         print("Hola");
#     }
# }
#
# // Comentario de línea
#
# /*
#    Comentario
#    multilínea
# */
#
# List<String> nombres = ["A", "B"];
#
# AUTOR: Enrique Rosado
# ==========================================

# Combinación de las palabras reservadas de los tres aportes
palabras_reservadas = {**palabras_reservadas_dome, **palabras_reservadas_henry, **palabras_reservadas_enrique}

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
        log.write('=' * 60 + '\n')
        log.write('ANÁLISIS LÉXICO - ANALIZADOR DART\n')
        log.write(f'Desarrollador: {nombre_desarrollador}\n')
        log.write(f'Archivo analizado: {ruta_archivo}\n')
        log.write(f'Fecha y hora: {datetime.now().strftime("%d/%m/%Y %H:%M")}\n')
        log.write('=' * 60 + '\n\n')
        log.write(f'TOKENS ENCONTRADOS: {len(tokens_encontrados)}\n\n')

        for tok in tokens_encontrados:
            log.write(f'[Línea {tok.lineno}] {tok.type:20} → {tok.value}\n')

        log.write('\n' + '=' * 60 + '\n')
        log.write('ANÁLISIS COMPLETADO\n')
        log.write('=' * 60 + '\n')

    print(f'\nLog generado: {nombre_log}')
    print(f'Total de tokens: {len(tokens_encontrados)}')


if __name__ == '__main__':
    analizar_archivo('algoritmos/algoritmo_dome.dart', 'DomenikaArboleda')