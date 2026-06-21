import ply.yacc as yacc
from lexer.lexer import tokens

# ==========================================
# APORTE ENRIQUE ROSADO
# Funciones, print, return, class,
# while e ingreso por teclado
# ==========================================

def p_programa(p):
    '''
    programa : elementos
    '''
    print("Programa válido")


def p_elementos(p):
    '''
    elementos : elemento
              | elementos elemento
    '''
    pass


def p_elemento(p):
    '''
    elemento : sentencia_print
             | funcion_void
             | funcion_return
             | declaracion_variable
             | estructura_switch
             | declaracion_map
             | funcion_opcional
             | estructura_while
             | clase
             | ingreso_teclado
    '''
    pass


def p_sentencia_print(p):
    '''
    sentencia_print : PRINT PARENTESIS_IZQ expresion PARENTESIS_DER PUNTOYCOMA
    '''
    print(f"Print reconocido: {p[3]}")


def p_funcion_void(p):
    '''
    funcion_void : VOID IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER bloque
    '''
    print(f"Función void reconocida: {p[2]}")


def p_funcion_return(p):
    '''
    funcion_return : STRING_TYPE IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER bloque_return
    '''
    print(f"Función con retorno reconocida: {p[2]}")


def p_bloque_return(p):
    '''
    bloque_return : LLAVE_IZQ sentencia_return LLAVE_DER
    '''
    pass


def p_sentencia_return(p):
    '''
    sentencia_return : RETURN CADENA PUNTOYCOMA
    '''
    print(f"Return reconocido: {p[2]}")


def p_bloque(p):
    '''
    bloque : LLAVE_IZQ LLAVE_DER
    '''
    pass


def p_expresion_booleana(p):
    '''
    expresion_booleana : expresion MAYOR expresion
                        | expresion MENOR expresion
                        | expresion IGUAL_IGUAL expresion
                        | expresion DISTINTO expresion
                        | TRUE
                        | FALSE
    '''
    pass


def p_estructura_while(p):
    '''
    estructura_while : WHILE PARENTESIS_IZQ expresion_booleana PARENTESIS_DER bloque
    '''
    print("While reconocido")


def p_clase(p):
    '''
    clase : CLASS IDENTIFICADOR LLAVE_IZQ LLAVE_DER
    '''
    print(f"Clase reconocida: {p[2]}")


def p_ingreso_teclado(p):
    '''
    ingreso_teclado : STRING_TYPE IDENTIFICADOR ASIGNACION IDENTIFICADOR PUNTO IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER PUNTOYCOMA
    '''
    print(f"Ingreso por teclado reconocido: {p[2]}")


def p_error(p):
    if p:
        print(f"Error sintáctico en '{p.value}'")
    else:
        print("Error sintáctico al final del archivo")


# ==========================================
# APORTE DOMENIKA ARBOLEDA - INICIO
# Reglas: asignación de variables (todos los tipos),
# estructura de control switch, estructura de datos Map,
# función con parámetros opcionales
# ==========================================

# --- Tipo auxiliar ---
def p_tipo(p):
    '''
    tipo : INT_TYPE
         | DOUBLE_TYPE
         | STRING_TYPE
         | BOOL_TYPE
    '''
    p[0] = p[1]

# --- Expresión simple auxiliar ---
def p_expresion_simple(p):
    '''
    expresion : ENTERO
              | DECIMAL
              | CADENA
              | TRUE
              | FALSE
              | IDENTIFICADOR
    '''
    p[0] = p[1]

# -------------------------
# 1. ASIGNACIÓN DE VARIABLES (todos los tipos)
# -------------------------
def p_declaracion_variable_tipo(p):
    '''
    declaracion_variable : tipo IDENTIFICADOR ASIGNACION expresion PUNTOYCOMA
    '''
    print(f"Declaración válida: {p[1]} {p[2]} = {p[4]};")

def p_declaracion_variable_var(p):
    '''
    declaracion_variable : VAR IDENTIFICADOR ASIGNACION expresion PUNTOYCOMA
    '''
    print(f"Declaración válida (var): {p[2]} = {p[4]};")

def p_declaracion_variable_const(p):
    '''
    declaracion_variable : CONST tipo IDENTIFICADOR ASIGNACION expresion PUNTOYCOMA
    '''
    print(f"Declaración válida (const): {p[2]} {p[3]} = {p[5]};")

def p_declaracion_variable_final(p):
    '''
    declaracion_variable : FINAL tipo IDENTIFICADOR ASIGNACION expresion PUNTOYCOMA
    '''
    print(f"Declaración válida (final): {p[2]} {p[3]} = {p[5]};")

# -------------------------
# 2. ESTRUCTURA DE CONTROL: SWITCH
# -------------------------
def p_estructura_switch(p):
    '''
    estructura_switch : SWITCH PARENTESIS_IZQ IDENTIFICADOR PARENTESIS_DER LLAVE_IZQ lista_casos LLAVE_DER
    '''
    print("Estructura switch reconocida")

def p_lista_casos(p):
    '''
    lista_casos : caso
                | lista_casos caso
                | lista_casos caso_default
                | caso_default
    '''
    pass

def p_caso(p):
    '''
    caso : CASE expresion DOS_PUNTOS sentencia_print BREAK PUNTOYCOMA
    '''
    print(f"Case reconocido: {p[2]}")

def p_caso_default(p):
    '''
    caso_default : DEFAULT DOS_PUNTOS sentencia_print
    '''
    print("Default reconocido")

# -------------------------
# 3. ESTRUCTURA DE DATOS: MAP
# -------------------------
def p_declaracion_map(p):
    '''
    declaracion_map : IDENTIFICADOR MENOR tipo COMA IDENTIFICADOR MAYOR IDENTIFICADOR ASIGNACION LLAVE_IZQ lista_pares LLAVE_DER PUNTOYCOMA
    '''
    print(f"Map reconocido: {p[7]}")

def p_lista_pares(p):
    '''
    lista_pares : par
                | lista_pares COMA par
    '''
    pass

def p_par(p):
    '''
    par : CADENA DOS_PUNTOS expresion
    '''
    print(f"Par clave-valor: {p[1]} : {p[3]}")

# -------------------------
# 4. FUNCIÓN CON PARÁMETROS OPCIONALES
# -------------------------
def p_funcion_parametros_opcionales(p):
    '''
    funcion_opcional : VOID IDENTIFICADOR PARENTESIS_IZQ tipo IDENTIFICADOR COMA CORCHETE_IZQ lista_param_opcionales CORCHETE_DER PARENTESIS_DER bloque
    '''
    print(f"Función con parámetros opcionales reconocida: {p[2]}")

def p_lista_param_opcionales(p):
    '''
    lista_param_opcionales : param_opcional
                            | lista_param_opcionales COMA param_opcional
    '''
    pass

def p_param_opcional(p):
    '''
    param_opcional : tipo IDENTIFICADOR ASIGNACION expresion
    '''
    print(f"Parámetro opcional: {p[1]} {p[2]} = {p[4]}")

# ==========================================
# APORTE DOMENIKA ARBOLEDA - FIN
# ==========================================

parser = yacc.yacc()
# ==========================================
# APORTE DOMENIKA ARBOLEDA - Generación de log
# ==========================================
import os
import io
import sys
from datetime import datetime

def analizar_sintaxis(ruta_archivo, nombre_desarrollador):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        codigo = f.read()

    ahora = datetime.now().strftime('%d-%m-%Y-%Hh%M')
    nombre_log = f'sintactico-{nombre_desarrollador}-{ahora}.txt'
    ruta_log = os.path.join('logs', nombre_log)

    buffer = io.StringIO()
    sys.stdout = buffer

    try:
        parser.parse(codigo)
    except Exception as e:
        print(f"Error: {e}")

    sys.stdout = sys.__stdout__
    resultado = buffer.getvalue()

    with open(ruta_log, 'w', encoding='utf-8') as log:
        log.write('=' * 60 + '\n')
        log.write('ANÁLISIS SINTÁCTICO - ANALIZADOR DART\n')
        log.write(f'Desarrollador: {nombre_desarrollador}\n')
        log.write(f'Archivo analizado: {ruta_archivo}\n')
        log.write(f'Fecha y hora: {datetime.now().strftime("%d/%m/%Y %H:%M")}\n')
        log.write('=' * 60 + '\n\n')
        log.write(resultado)
        log.write('\n' + '=' * 60 + '\n')

    print(f'Log generado: {nombre_log}')
    print(resultado)

if __name__ == '__main__':
    analizar_sintaxis('algoritmos/algoritmo_enrique_sintactico.dart', 'EnriqueRosado')

