import ply.yacc as yacc
from lexer.lexer import tokens

# ==========================================
# APORTE ENRIQUE ROSADO
# Funciones, print y return
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
    '''
    pass


# -------------------------
# PRINT
# -------------------------

def p_sentencia_print(p):
    '''
    sentencia_print : PRINT PARENTESIS_IZQ CADENA PARENTESIS_DER PUNTOYCOMA
    '''
    print("Print reconocido")


# -------------------------
# FUNCION VOID
# -------------------------

def p_funcion_void(p):
    '''
    funcion_void : VOID IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER bloque
    '''
    print("Función void reconocida")


# -------------------------
# FUNCION CON RETURN
# -------------------------

def p_funcion_return(p):
    '''
    funcion_return : STRING_TYPE IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER bloque_return
    '''
    print("Función con retorno reconocida")


def p_bloque_return(p):
    '''
    bloque_return : LLAVE_IZQ sentencia_return LLAVE_DER
    '''
    pass


def p_sentencia_return(p):
    '''
    sentencia_return : RETURN CADENA PUNTOYCOMA
    '''
    print("Return reconocido")


# -------------------------
# BLOQUE
# -------------------------

def p_bloque(p):
    '''
    bloque : LLAVE_IZQ LLAVE_DER
    '''
    pass


# -------------------------
# ERROR
# -------------------------

def p_error(p):
    if p:
        print(f"Error sintáctico en '{p.value}'")
    else:
        print("Error sintáctico al final del archivo")


parser = yacc.yacc()