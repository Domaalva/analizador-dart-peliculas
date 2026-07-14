#Aporte de Henry Olvera
import ply.yacc as yacc
from lexer.lexer import tokens

#Precedencia de operadores para evitar conflictos
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUAL_IGUAL', 'DISTINTO'),
    ('left', 'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    ('right', 'NOT'),
)

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
             | sentencia_if
             | sentencia_control
             | sentencia_incremento
             | sentencia_asignacion
             | sentencia_return
             | funcion_void
             | funcion_return
             | declaracion_variable
             | estructura_switch
             | declaracion_map
             | funcion_opcional
             | estructura_while
             | estructura_for
             | declaracion_list
             | declaracion_set
             | funcion_nombrada
             | declaracion_lambda
             | clase
    '''
    pass


def p_sentencia_print(p):
    '''
    sentencia_print : PRINT PARENTESIS_IZQ expresion_general PARENTESIS_DER PUNTOYCOMA
    '''
    print(f"Print reconocido: {p[3]}")


def p_sentencia_if(p):
    '''
    sentencia_if : IF PARENTESIS_IZQ expresion_booleana PARENTESIS_DER bloque_no_vacio else_opcional
    '''
    print("If reconocido")


def p_else_opcional(p):
    '''
    else_opcional :
                  | ELSE bloque_no_vacio
    '''
    pass


def p_bloque_no_vacio(p):
    '''
    bloque_no_vacio : LLAVE_IZQ elementos LLAVE_DER
    '''
    pass


def p_sentencia_control(p):
    '''
    sentencia_control : BREAK PUNTOYCOMA
                      | CONTINUE PUNTOYCOMA
    '''
    print(f"Sentencia de control reconocida: {p[1]}")


def p_sentencia_incremento(p):
    '''
    sentencia_incremento : incremento PUNTOYCOMA
    '''
    print("Incremento/decremento reconocido")


def p_sentencia_asignacion(p):
    '''
    sentencia_asignacion : IDENTIFICADOR ASIGNACION expresion_general PUNTOYCOMA
    '''
    print(f"Asignación reconocida: {p[1]} = {p[3]}")


def p_funcion_void(p):
    '''
    funcion_void : VOID IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER bloque
    '''
    print(f"Función void reconocida: {p[2]}")


def p_funcion_return(p):
    '''
    funcion_return : tipo IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER bloque_return
    '''
    print(f"Función con retorno reconocida: {p[2]}")


def p_bloque_return(p):
    '''
    bloque_return : LLAVE_IZQ sentencia_return LLAVE_DER
    '''
    pass


def p_sentencia_return(p):
    '''
    sentencia_return : RETURN expresion_general PUNTOYCOMA
    '''
    print(f"Return reconocido: {p[2]}")


def p_bloque(p):
    '''
    bloque : LLAVE_IZQ LLAVE_DER
          | LLAVE_IZQ elementos LLAVE_DER
    '''
    pass


def p_expresion_booleana(p):
    '''
    expresion_booleana : expresion MAYOR expresion
                        | expresion MENOR expresion
                        | expresion IGUAL_IGUAL expresion
                        | expresion DISTINTO expresion
                        | expresion MAYOR_IGUAL expresion
                        | expresion MENOR_IGUAL expresion
                        | TRUE
                        | FALSE
                        | NOT expresion_booleana
                        | PARENTESIS_IZQ expresion_booleana PARENTESIS_DER
                        | expresion_booleana AND expresion_booleana
                        | expresion_booleana OR expresion_booleana
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3 and p[1] == '!':
        p[0] = ('not', p[2])
    elif len(p) == 4 and p[1] == '(':
        p[0] = p[2]
    elif len(p) == 4 and p[2] in ('&&', '||'):
        p[0] = ('logic', p[2], p[1], p[3])
    elif len(p) == 4:
        p[0] = ('comp', p[2], p[1], p[3])


#Henry Olvera - Expresiones aritméticas
def p_expresion_aritmetica(p):
    '''
    expresion : expresion MAS termino
              | expresion MENOS termino
              | termino
    '''
    if len(p) == 4:
        p[0] = ('binop', p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_termino(p):
    '''
    termino : termino MULTIPLICACION factor
            | termino DIVISION factor
            | factor
    '''
    if len(p) == 4:
        p[0] = ('binop', p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_factor_primary(p):
    '''
    factor : ENTERO
           | DECIMAL
           | CADENA
           | IDENTIFICADOR
           | PARENTESIS_IZQ expresion PARENTESIS_DER
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_factor_booleano(p):
    '''
    factor : TRUE
           | FALSE
    '''
    p[0] = p[1]


def p_factor_call(p):
    '''
    factor : factor PARENTESIS_IZQ lista_args PARENTESIS_DER
    '''
    p[0] = ('call', p[1], p[3])


def p_factor_member(p):
    '''
    factor : factor PUNTO IDENTIFICADOR
    '''
    p[0] = ('member', p[1], p[3])


def p_factor_index(p):
    '''
    factor : factor CORCHETE_IZQ expresion CORCHETE_DER
    '''
    p[0] = ('index', p[1], p[3])


#Henry Olvera - for
def p_incremento(p):
    '''
    incremento : IDENTIFICADOR INCREMENTO
               | IDENTIFICADOR DECREMENTO
               | IDENTIFICADOR ASIGNACION expresion
    '''
    pass


def p_estructura_for(p):
    '''
    estructura_for : FOR PARENTESIS_IZQ for_init PUNTOYCOMA expresion_booleana PUNTOYCOMA incremento PARENTESIS_DER bloque
    '''
    print("For reconocido")


def p_for_init(p):
    '''
    for_init :
             | tipo IDENTIFICADOR ASIGNACION expresion
             | VAR IDENTIFICADOR ASIGNACION expresion
    '''
    pass



#Henry Olvera - Declaraciones List y Set
def p_declaracion_list(p):
    '''
    declaracion_list : IDENTIFICADOR MENOR tipo MAYOR IDENTIFICADOR ASIGNACION CORCHETE_IZQ lista_elementos CORCHETE_DER PUNTOYCOMA
    '''
    print(f"List reconocida: {p[5]}")

def p_declaracion_set(p):
    '''
    declaracion_set : IDENTIFICADOR MENOR tipo MAYOR IDENTIFICADOR ASIGNACION LLAVE_IZQ lista_elementos LLAVE_DER PUNTOYCOMA
    '''
    print(f"Set reconocido: {p[5]}")

def p_lista_elementos(p):
    '''
    lista_elementos : expresion
                    | lista_elementos COMA expresion
    '''
    pass


#Henry Olvera -Parámetros opcionales por nombre (llaves {})
def p_funcion_parametros_nombrados(p):
    '''
    funcion_nombrada : VOID IDENTIFICADOR PARENTESIS_IZQ LLAVE_IZQ lista_param_nombrados LLAVE_DER PARENTESIS_DER bloque
    '''
    print(f"Función con parámetros nombrados reconocida: {p[2]}")

def p_lista_param_nombrados(p):
    '''
    lista_param_nombrados : param_nombrado
                          | lista_param_nombrados COMA param_nombrado
    '''
    pass

def p_param_nombrado(p):
    '''
    param_nombrado : tipo IDENTIFICADOR ASIGNACION expresion
    '''
    print(f"Parámetro nombrado: {p[1]} {p[2]} = {p[4]}")



#Henry Olvera - Funciones lambda (forma simplificada)
def p_declaracion_lambda(p):
    '''
    declaracion_lambda : tipo IDENTIFICADOR ASIGNACION PARENTESIS_IZQ lista_params PARENTESIS_DER FLECHA expresion PUNTOYCOMA
    '''
    print(f"Lambda/función anónima reconocida: {p[2]}")


def p_lista_params(p):
    '''
    lista_params :
                | param_simple
                | lista_params COMA param_simple
    '''
    pass

def p_param_simple(p):
    '''
    param_simple : tipo IDENTIFICADOR
    '''
    pass


def p_lista_args(p):
    '''
    lista_args :
              | expresion
              | lista_args COMA expresion
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
         | IDENTIFICADOR
    '''
    p[0] = p[1]

# (Se usa 'factor' y 'expresion' aritmética para manejar literales y identificadores)

# -------------------------
# 1. ASIGNACIÓN DE VARIABLES (todos los tipos)
# -------------------------
def p_declaracion_variable_tipo(p):
    '''
    declaracion_variable : tipo IDENTIFICADOR ASIGNACION expresion_general PUNTOYCOMA
    '''
    print(f"Declaración válida: {p[1]} {p[2]} = {p[4]};")

def p_declaracion_variable_var(p):
    '''
    declaracion_variable : VAR IDENTIFICADOR ASIGNACION expresion_general PUNTOYCOMA
    '''
    print(f"Declaración válida (var): {p[2]} = {p[4]};")

def p_declaracion_variable_const(p):
    '''
    declaracion_variable : CONST tipo IDENTIFICADOR ASIGNACION expresion_general PUNTOYCOMA
    '''
    print(f"Declaración válida (const): {p[2]} {p[3]} = {p[5]};")

def p_declaracion_variable_final(p):
    '''
    declaracion_variable : FINAL tipo IDENTIFICADOR ASIGNACION expresion_general PUNTOYCOMA
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
    caso_default : DEFAULT DOS_PUNTOS lista_sentencias
    '''
    print("Default reconocido")


def p_lista_sentencias(p):
    '''
    lista_sentencias : sentencia_print
                    | sentencia_control
                    | sentencia_incremento
                    | sentencia_asignacion
                    | lista_sentencias sentencia_print
                    | lista_sentencias sentencia_control
                    | lista_sentencias sentencia_incremento
                    | lista_sentencias sentencia_asignacion
    '''
    pass

# -------------------------
# 3. ESTRUCTURA DE DATOS: MAP
# -------------------------
def p_declaracion_map(p):
    '''
    declaracion_map : IDENTIFICADOR MENOR tipo COMA tipo MAYOR IDENTIFICADOR ASIGNACION LLAVE_IZQ lista_pares_opt LLAVE_DER PUNTOYCOMA
    '''
    print(f"Estructura de datos Map reconocida: {p[7]}")

def p_lista_pares_opt(p):
    '''
    lista_pares_opt :
                    | lista_pares
    '''
    pass

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


def p_expresion_general(p):
    '''
    expresion_general : expresion
                      | expresion_booleana
    '''
    p[0] = p[1]

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

