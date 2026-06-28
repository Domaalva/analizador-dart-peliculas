"""
Aporte de Henry Olvera
Analizador semántico:
Reglas implementadas:
- Detección de declaraciones con `const`, `final`, tipos básicos y `var`.
- Prohibir asignaciones a identificadores marcados como `const`.
- Verificar compatibilidad exacta de tipos en declaraciones y asignaciones.
- Generar log con resultados de pruebas y errores semánticos.
"""
import re
import os
from datetime import datetime


class Symbol:
    def __init__(self, name, tipo, is_const=False, line=0):
        self.name = name
        self.tipo = tipo  # 'int','double','String','bool' or 'var'
        self.is_const = is_const
        self.line = line


class SemanticAnalyzer:
    def __init__(self):
        # tabla de símbolos: nombre -> Symbol
        self.symbols = {}
        self.errores = []
        self.aprobados = []

    def tipo_literal(self, texto):
        texto = texto.strip()
        # string entre comillas
        if re.match(r'^\".*\"$|^\'.*\'$'.replace("'","'"), texto):
            return 'String'
        if re.match(r"^'.*'$", texto):
            return 'String'
        if re.match(r'^-?\d+$', texto):
            return 'int'
        if re.match(r'^-?\d+\.\d+$', texto):
            return 'double'
        if texto in ('true', 'false'):
            return 'bool'
        # identificador
        if re.match(r'^[A-Za-z_]\w*$', texto):
            sym = self.symbols.get(texto)
            if sym:
                return sym.tipo
            else:
                return None
        return None

    def registrar_declaracion(self, nombre, tipo, is_const, linea):
        self.symbols[nombre] = Symbol(nombre, tipo, is_const, linea)

    def analizar_archivo(self, ruta_codigo, nombre_desarrollador):
        # limpiar estado
        self.symbols = {}
        self.errores = []
        self.aprobados = []

        with open(ruta_codigo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()

        linea_num = 0
        for raw in lineas:
            linea_num += 1
            # eliminar comentarios en linea para que no rompan las reglas regex
            linea = re.sub(r'//.*$', '', raw).strip()
            if not linea:
                continue

            # patrón: const TYPE id = expr;
            m = re.match(r'^const\s+(int|double|String|bool)\s+([A-Za-z_]\w*)\s*=\s*(.+);$', linea)
            if m:
                tipo, nombre, expr = m.group(1), m.group(2), m.group(3)
                self.registrar_declaracion(nombre, tipo, True, linea_num)
                # comprobar tipo RHS
                tipo_rhs = self.tipo_literal(expr)
                if tipo_rhs is None:
                    self.errores.append((linea_num, f"Error semántico [Asignación de tipo]: no se puede determinar el tipo de '{expr}' para la constante '{nombre}'"))
                elif tipo_rhs != tipo:
                    self.errores.append((linea_num, f"Error semántico [Asignación de tipo]: no se puede asignar un valor de tipo {tipo_rhs} a una variable de tipo {tipo} ('{nombre}')."))
                else:
                    self.aprobados.append((linea_num, f"Declaración const válida: {tipo} {nombre} = {expr}"))
                continue

            # patrón: final TYPE id = expr; (registramos pero no permitimos re-asignar por simplicidad)
            m = re.match(r'^final\s+(int|double|String|bool)\s+([A-Za-z_]\w*)\s*=\s*(.+);$', linea)
            if m:
                tipo, nombre, expr = m.group(1), m.group(2), m.group(3)
                self.registrar_declaracion(nombre, tipo, True, linea_num)
                tipo_rhs = self.tipo_literal(expr)
                if tipo_rhs is None:
                    self.errores.append((linea_num, f"Error semántico [Asignación de tipo]: no se puede determinar el tipo de '{expr}' para 'final' '{nombre}'"))
                elif tipo_rhs != tipo:
                    self.errores.append((linea_num, f"Error semántico [Asignación de tipo]: no se puede asignar un valor de tipo {tipo_rhs} a una variable de tipo {tipo} ('{nombre}')."))
                else:
                    self.aprobados.append((linea_num, f"Declaración final válida: {tipo} {nombre} = {expr}"))
                continue

            # patrón: TYPE id = expr;
            m = re.match(r'^(int|double|String|bool)\s+([A-Za-z_]\w*)\s*=\s*(.+);$', linea)
            if m:
                tipo, nombre, expr = m.group(1), m.group(2), m.group(3)
                self.registrar_declaracion(nombre, tipo, False, linea_num)
                tipo_rhs = self.tipo_literal(expr)
                if tipo_rhs is None:
                    self.errores.append((linea_num, f"Error semántico [Asignación de tipo]: no se puede determinar el tipo de '{expr}' para '{nombre}'"))
                elif tipo_rhs != tipo:
                    self.errores.append((linea_num, f"Error semántico [Asignación de tipo]: no se puede asignar un valor de tipo {tipo_rhs} a una variable de tipo {tipo} ('{nombre}')."))
                else:
                    self.aprobados.append((linea_num, f"Declaración válida: {tipo} {nombre} = {expr}"))
                continue

            # patrón: var id = expr;
            m = re.match(r'^var\s+([A-Za-z_]\w*)\s*=\s*(.+);$', linea)
            if m:
                nombre, expr = m.group(1), m.group(2)
                tipo_rhs = self.tipo_literal(expr)
                tipo_reg = tipo_rhs if tipo_rhs else 'var'
                self.registrar_declaracion(nombre, tipo_reg, False, linea_num)
                if tipo_rhs is None:
                    self.aprobados.append((linea_num, f"Declaración var: {nombre} = {expr} (tipo indeterminado)"))
                else:
                    self.aprobados.append((linea_num, f"Declaración var: {nombre} = {expr} (tipo detectado: {tipo_rhs})"))
                continue

            # Asignación simple: id = expr;
            m = re.match(r'^([A-Za-z_]\w*)\s*=\s*(.+);$', linea)
            if m:
                nombre, expr = m.group(1), m.group(2)
                sym = self.symbols.get(nombre)
                if sym and sym.is_const:
                    self.errores.append((linea_num, f"Error semántico [Identificadores]: la constante '{nombre}' no puede ser modificada después de su declaración."))
                    continue
                tipo_rhs = self.tipo_literal(expr)
                if sym is None:
                    # asignación a variable no declarada -> se permite si var no declarado? reportar como error semántico
                    self.errores.append((linea_num, f"Error semántico [Identificadores]: la variable '{nombre}' no fue declarada antes de la asignación."))
                    continue
                if tipo_rhs is None:
                    self.errores.append((linea_num, f"Error semántico [Asignación de tipo]: no se puede determinar el tipo de '{expr}' en la asignación a '{nombre}'."))
                    continue
                if tipo_rhs != sym.tipo:
                    self.errores.append((linea_num, f"Error semántico [Asignación de tipo]: no se puede asignar un valor de tipo {tipo_rhs} a una variable de tipo {sym.tipo} ('{nombre}')."))
                else:
                    self.aprobados.append((linea_num, f"Asignación válida: {nombre} = {expr}"))
                continue

        # generar log
        ahora = datetime.now().strftime('%d%m%Y-%Hh%M')
        nombre_log = f'semantico-{nombre_desarrollador}-{ahora}.txt'
        ruta_log = os.path.join('logs', nombre_log)
        os.makedirs('logs', exist_ok=True)
        with open(ruta_log, 'w', encoding='utf-8') as log:
            log.write('ANÁLISIS SEMÁNTICO - ANALIZADOR DART\n')
            log.write(f'Desarrollador: {nombre_desarrollador}\n')
            log.write(f'Archivo analizado: {ruta_codigo}\n')
            log.write(f'Fecha y hora: {datetime.now().strftime("%d/%m/%Y %H:%M")}\n')
            log.write('\n\n')
            log.write('ERRORES SEMÁNTICOS:\n')
            if not self.errores:
                log.write(' - No se detectaron errores semánticos.\n')
            else:
                for l, msg in self.errores:
                    log.write(f'Linea {l}: {msg}\n')
            log.write('\nPRUEBAS APROBADAS:\n')
            if not self.aprobados:
                log.write(' - Ninguna prueba aprobada.\n')
            else:
                for l, msg in self.aprobados:
                    log.write(f'Linea {l}: {msg}\n')

        return ruta_log

# ==========================================
# APORTE DOMENIKA ARBOLEDA - INICIO
# Reglas semánticas:
# 1. Asignación de tipo: compatibilidad entre tipo declarado y valor asignado
# 2. Identificadores: constante const no puede modificarse
# 3. Operaciones permitidas: operaciones entre tipos compatibles
# ==========================================

class SemanticAnalyzerDome:
    def __init__(self):
        self.tabla_simbolos = {}
        self.errores = []
        self.aprobados = []

    def inferir_tipo(self, expr):
        expr = expr.strip()
        if re.match(r'^\".*\"$', expr) or re.match(r"^'.*'$", expr):
            return 'String'
        if re.match(r'^-?\d+$', expr):
            return 'int'
        if re.match(r'^-?\d+\.\d+$', expr):
            return 'double'
        if expr in ('true', 'false'):
            return 'bool'
        if re.match(r'^[A-Za-z_]\w*$', expr):
            sym = self.tabla_simbolos.get(expr)
            if sym:
                return sym['tipo']
        return None

    def verificar_operacion(self, expr, num):
        m = re.match(r'^(.+?)\s*([\+\-\*\/])\s*(.+)$', expr.strip())
        if not m:
            return True

        izq = m.group(1).strip()
        op  = m.group(2).strip()
        der = m.group(3).strip()

        tipo_izq = self.inferir_tipo(izq)
        tipo_der = self.inferir_tipo(der)

        if tipo_izq is None or tipo_der is None:
            return True

        tipos_numericos = {'int', 'double'}

        if tipo_izq == 'String' or tipo_der == 'String':
            if op != '+':
                self.errores.append((num, f"Error semántico [Operaciones permitidas]: el operador '{op}' no puede aplicarse a valores de tipo String."))
                return False
            if tipo_izq != 'String' or tipo_der != 'String':
                self.errores.append((num, f"Error semántico [Operaciones permitidas]: no es posible realizar '{op}' entre tipo {tipo_izq} y tipo {tipo_der}."))
                return False
            return True

        if tipo_izq == 'bool' or tipo_der == 'bool':
            self.errores.append((num, f"Error semántico [Operaciones permitidas]: no es posible realizar '{op}' con valores de tipo bool."))
            return False

        if tipo_izq in tipos_numericos and tipo_der in tipos_numericos:
            return True

        self.errores.append((num, f"Error semántico [Operaciones permitidas]: operación '{op}' no permitida entre tipos {tipo_izq} y {tipo_der}."))
        return False

    def analizar(self, ruta_codigo, nombre_desarrollador):
        self.tabla_simbolos = {}
        self.errores = []
        self.aprobados = []

        with open(ruta_codigo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()

        for num, raw in enumerate(lineas, start=1):
            linea = re.sub(r'//.*$', '', raw).strip()
            if not linea:
                continue

            # --- REGLA 2: const no puede modificarse ---
            m = re.match(r'^const\s+(int|double|String|bool)\s+([A-Za-z_]\w*)\s*=\s*(.+);$', linea)
            if m:
                tipo, nombre, expr = m.group(1), m.group(2), m.group(3).strip()
                self.tabla_simbolos[nombre] = {'tipo': tipo, 'es_const': True, 'linea': num}
                tipo_valor = self.inferir_tipo(expr)
                if tipo_valor is None:
                    self.errores.append((num, f"Error semántico [Asignación de tipo]: no se puede determinar el tipo de '{expr}' para la constante '{nombre}'."))
                elif tipo_valor != tipo:
                    self.errores.append((num, f"Error semántico [Asignación de tipo]: no se puede asignar un valor de tipo {tipo_valor} a una constante de tipo {tipo} ('{nombre}')."))
                else:
                    self.aprobados.append((num, f"Declaración const válida: {tipo} {nombre} = {expr}"))
                continue

            # Detectar declaración final
            m = re.match(r'^final\s+(int|double|String|bool)\s+([A-Za-z_]\w*)\s*=\s*(.+);$', linea)
            if m:
                tipo, nombre, expr = m.group(1), m.group(2), m.group(3).strip()
                self.tabla_simbolos[nombre] = {'tipo': tipo, 'es_const': True, 'linea': num}
                tipo_valor = self.inferir_tipo(expr)
                if tipo_valor is None:
                    self.errores.append((num, f"Error semántico [Asignación de tipo]: no se puede determinar el tipo de '{expr}' para la variable final '{nombre}'."))
                elif tipo_valor != tipo:
                    self.errores.append((num, f"Error semántico [Asignación de tipo]: no se puede asignar un valor de tipo {tipo_valor} a una variable final de tipo {tipo} ('{nombre}')."))
                else:
                    self.aprobados.append((num, f"Declaración final válida: {tipo} {nombre} = {expr}"))
                continue

            # Detectar declaración con tipo explícito
            m = re.match(r'^(int|double|String|bool)\s+([A-Za-z_]\w*)\s*=\s*(.+);$', linea)
            if m:
                tipo, nombre, expr = m.group(1), m.group(2), m.group(3).strip()
                self.tabla_simbolos[nombre] = {'tipo': tipo, 'es_const': False, 'linea': num}

                # --- REGLA 3: verificar operaciones permitidas ---
                self.verificar_operacion(expr, num)

                # --- REGLA 1: verificar compatibilidad de tipo ---
                tipo_valor = self.inferir_tipo(expr)
                if tipo_valor is None:
                    self.errores.append((num, f"Error semántico [Asignación de tipo]: no se puede determinar el tipo de '{expr}' para '{nombre}'."))
                elif tipo_valor != tipo:
                    self.errores.append((num, f"Error semántico [Asignación de tipo]: no se puede asignar un valor de tipo {tipo_valor} a una variable de tipo {tipo} ('{nombre}')."))
                else:
                    self.aprobados.append((num, f"Declaración válida: {tipo} {nombre} = {expr}"))
                continue

            # Detectar declaración var
            m = re.match(r'^var\s+([A-Za-z_]\w*)\s*=\s*(.+);$', linea)
            if m:
                nombre, expr = m.group(1), m.group(2).strip()
                tipo_rhs = self.inferir_tipo(expr)
                tipo_reg = tipo_rhs if tipo_rhs else 'var'
                self.tabla_simbolos[nombre] = {'tipo': tipo_reg, 'es_const': False, 'linea': num}
                if tipo_rhs is None:
                    self.aprobados.append((num, f"Declaración var: {nombre} = {expr} (tipo indeterminado)"))
                else:
                    self.aprobados.append((num, f"Declaración var: {nombre} = {expr} (tipo detectado: {tipo_rhs})"))
                continue

            # Detectar reasignación
            m = re.match(r'^([A-Za-z_]\w*)\s*=\s*(.+);$', linea)
            if m:
                nombre, expr = m.group(1), m.group(2).strip()
                sym = self.tabla_simbolos.get(nombre)

                # --- REGLA 2: const no puede modificarse ---
                if sym and sym['es_const']:
                    self.errores.append((num, f"Error semántico [Identificadores]: la constante '{nombre}' no puede ser modificada después de su declaración."))
                    continue

                if sym is None:
                    self.errores.append((num, f"Error semántico [Identificadores]: la variable '{nombre}' no fue declarada antes de ser usada."))
                    continue

                # --- REGLA 3: verificar operaciones permitidas en reasignación ---
                self.verificar_operacion(expr, num)

                # --- REGLA 1: verificar compatibilidad de tipo en reasignación ---
                tipo_valor = self.inferir_tipo(expr)
                if tipo_valor is None:
                    self.errores.append((num, f"Error semántico [Asignación de tipo]: no se puede determinar el tipo de '{expr}' en la reasignación a '{nombre}'."))
                elif tipo_valor != sym['tipo']:
                    self.errores.append((num, f"Error semántico [Asignación de tipo]: no se puede asignar un valor de tipo {tipo_valor} a una variable de tipo {sym['tipo']} ('{nombre}')."))
                else:
                    self.aprobados.append((num, f"Reasignación válida: {nombre} = {expr}"))
                continue

        # Generar log
        ahora = datetime.now().strftime('%d%m%Y-%Hh%M')
        nombre_log = f'semantico-{nombre_desarrollador}-{ahora}.txt'
        ruta_log = os.path.join('logs', nombre_log)
        os.makedirs('logs', exist_ok=True)

        with open(ruta_log, 'w', encoding='utf-8') as log:
            log.write('=' * 60 + '\n')
            log.write('ANÁLISIS SEMÁNTICO - ANALIZADOR DART\n')
            log.write(f'Desarrollador: {nombre_desarrollador}\n')
            log.write(f'Archivo analizado: {ruta_codigo}\n')
            log.write(f'Fecha y hora: {datetime.now().strftime("%d/%m/%Y %H:%M")}\n')
            log.write('=' * 60 + '\n\n')
            log.write('ERRORES SEMÁNTICOS:\n')
            if not self.errores:
                log.write('  - No se detectaron errores semánticos.\n')
            else:
                for l, msg in self.errores:
                    log.write(f'  Línea {l}: {msg}\n')
            log.write('\nPRUEBAS APROBADAS:\n')
            if not self.aprobados:
                log.write('  - Ninguna prueba aprobada.\n')
            else:
                for l, msg in self.aprobados:
                    log.write(f'  Línea {l}: {msg}\n')
            log.write('\n' + '=' * 60 + '\n')

        print(f'Log generado: {nombre_log}')
        return ruta_log

# ==========================================
# APORTE DOMENIKA ARBOLEDA - FIN
# ==========================================
# ==========================================
# APORTE ENRIQUE ROSADO - INICIO
# Reglas semánticas:
# 1. Rango de calificación válido entre 0 y 10
# 2. Géneros permitidos dentro de la plataforma de películas
# 3. Retorno de funciones compatible con el tipo declarado
# 4. break y continue usados dentro de estructuras válidas
# ==========================================

class SemanticAnalyzerEnrique:
    def __init__(self):
        self.simbolos = {}
        self.errores = []
        self.aprobados = []
        self.generos_permitidos = {
            "Acción", "Drama", "Comedia", "Terror", "Ciencia ficción",
            "Romance", "Aventura", "Suspenso", "Documental", "Animación",
            "Fantasía", "Musical"
        }

    def quitar_comentario_linea(self, linea):
        en_simple = False
        en_doble = False
        i = 0

        while i < len(linea) - 1:
            c = linea[i]

            if c == '"' and not en_simple:
                en_doble = not en_doble
            elif c == "'" and not en_doble:
                en_simple = not en_simple
            elif c == "/" and linea[i + 1] == "/" and not en_simple and not en_doble:
                return linea[:i]

            i += 1

        return linea

    def inferir_tipo(self, expr):
        expr = expr.strip().rstrip(",")

        if re.match(r'^".*"$', expr) or re.match(r"^'.*'$", expr):
            return "String"

        if re.match(r"^-?\d+\.\d+$", expr):
            return "double"

        if re.match(r"^-?\d+$", expr):
            return "int"

        if expr in ("true", "false"):
            return "bool"

        if re.match(r"^[A-Za-z_]\w*$", expr):
            return self.simbolos.get(expr)

        return None

    def registrar_declaracion_simple(self, linea):
        m = re.match(
            r"^(?:const\s+|final\s+)?(int|double|String|bool)\s+([A-Za-z_]\w*)\s*=\s*(.+);$",
            linea
        )

        if m:
            tipo = m.group(1)
            nombre = m.group(2)
            expr = m.group(3).strip()
            self.simbolos[nombre] = tipo
            return tipo, nombre, expr

        m = re.match(r"^var\s+([A-Za-z_]\w*)\s*=\s*(.+);$", linea)

        if m:
            nombre = m.group(1)
            expr = m.group(2).strip()
            tipo = self.inferir_tipo(expr)

            if tipo:
                self.simbolos[nombre] = tipo

            return tipo, nombre, expr

        return None

    def validar_rango_calificacion(self, linea, num):
        patron_variable = r"(calificacion|calificación|rating|promedio)"

        m = re.search(
            rf"\b[A-Za-z_]*{patron_variable}[A-Za-z_]*\b\s*=\s*(-?\d+(?:\.\d+)?)\s*;",
            linea,
            re.IGNORECASE
        )

        if m:
            valor = float(m.group(2))
            nombre = re.search(
                rf"\b[A-Za-z_]*{patron_variable}[A-Za-z_]*\b",
                linea,
                re.IGNORECASE
            ).group(0)

            if valor < 0 or valor > 10:
                self.errores.append(
                    (num, f"Error semántico [Rango de calificación]: la variable '{nombre}' tiene valor {valor}, pero debe estar entre 0 y 10.")
                )
            else:
                self.aprobados.append(
                    (num, f"Rango de calificación válido: {nombre} = {valor}")
                )

        m = re.search(
            r'["\'](?:calificacion|calificación|rating|promedio)["\']\s*:\s*(-?\d+(?:\.\d+)?)',
            linea,
            re.IGNORECASE
        )

        if m:
            valor = float(m.group(1))

            if valor < 0 or valor > 10:
                self.errores.append(
                    (num, f"Error semántico [Rango de calificación]: el valor {valor} del campo de calificación debe estar entre 0 y 10.")
                )
            else:
                self.aprobados.append(
                    (num, f"Rango de calificación válido en estructura de datos: {valor}")
                )

    def validar_genero(self, linea, num):
        patron_genero = r"(genero|género)"

        m = re.search(
            rf"\b[A-Za-z_]*{patron_genero}[A-Za-z_]*\b\s*=\s*[\"']([^\"']+)[\"']\s*;",
            linea,
            re.IGNORECASE
        )

        if m:
            valor = m.group(2)
            nombre = re.search(
                rf"\b[A-Za-z_]*{patron_genero}[A-Za-z_]*\b",
                linea,
                re.IGNORECASE
            ).group(0)

            if valor not in self.generos_permitidos:
                self.errores.append(
                    (num, f"Error semántico [Géneros permitidos]: el género '{valor}' asignado a '{nombre}' no está permitido.")
                )
            else:
                self.aprobados.append(
                    (num, f"Género permitido válido: {nombre} = '{valor}'")
                )

        m = re.search(
            r'["\'](?:genero|género)["\']\s*:\s*["\']([^"\']+)["\']',
            linea,
            re.IGNORECASE
        )

        if m:
            valor = m.group(1)

            if valor not in self.generos_permitidos:
                self.errores.append(
                    (num, f"Error semántico [Géneros permitidos]: el género '{valor}' no pertenece a la lista permitida.")
                )
            else:
                self.aprobados.append(
                    (num, f"Género permitido válido en estructura de datos: '{valor}'")
                )

    def analizar(self, ruta_codigo, nombre_desarrollador):
        self.simbolos = {}
        self.errores = []
        self.aprobados = []

        with open(ruta_codigo, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        profundidad = 0
        funciones = []
        loops = []
        switches = []
        comentario_bloque = False

        for num, raw in enumerate(lineas, start=1):
            linea_original = raw.rstrip("\n")
            linea_temp = linea_original

            if comentario_bloque:
                if "*/" in linea_temp:
                    linea_temp = linea_temp.split("*/", 1)[1]
                    comentario_bloque = False
                else:
                    continue

            if "/*" in linea_temp:
                antes, despues = linea_temp.split("/*", 1)
                linea_temp = antes

                if "*/" in despues:
                    linea_temp += despues.split("*/", 1)[1]
                else:
                    comentario_bloque = True

            linea = self.quitar_comentario_linea(linea_temp).strip()

            if not linea:
                continue

            self.registrar_declaracion_simple(linea)
            self.validar_rango_calificacion(linea, num)
            self.validar_genero(linea, num)

            m_func = re.match(
                r"^(int|double|String|bool|void)\s+([A-Za-z_]\w*)\s*\([^)]*\)\s*\{?",
                linea
            )

            if m_func:
                tipo_funcion = m_func.group(1)
                nombre_funcion = m_func.group(2)
                profundidad_funcion = profundidad + linea.count("{")

                funciones.append({
                    "tipo": tipo_funcion,
                    "nombre": nombre_funcion,
                    "profundidad": profundidad_funcion
                })

                self.aprobados.append(
                    (num, f"Función registrada: {tipo_funcion} {nombre_funcion}()")
                )

            if re.match(r"^(for|while)\s*\(", linea):
                loops.append(profundidad + linea.count("{"))
                self.aprobados.append(
                    (num, "Estructura de repetición registrada.")
                )

            if re.match(r"^switch\s*\(", linea):
                switches.append(profundidad + linea.count("{"))
                self.aprobados.append(
                    (num, "Estructura switch registrada.")
                )

            m_return = re.search(r"\breturn\b\s*(.*?);", linea)

            if m_return:
                expr = m_return.group(1).strip()

                if not funciones:
                    self.errores.append(
                        (num, "Error semántico [Retorno de función]: la instrucción return solo puede utilizarse dentro de una función.")
                    )
                else:
                    funcion_actual = funciones[-1]
                    tipo_esperado = funcion_actual["tipo"]
                    nombre_funcion = funcion_actual["nombre"]

                    if tipo_esperado == "void":
                        if expr:
                            self.errores.append(
                                (num, f"Error semántico [Retorno de función]: la función void '{nombre_funcion}' no debe retornar un valor.")
                            )
                        else:
                            self.aprobados.append(
                                (num, f"Return válido en función void '{nombre_funcion}'.")
                            )
                    else:
                        if not expr:
                            self.errores.append(
                                (num, f"Error semántico [Retorno de función]: la función '{nombre_funcion}' debe retornar un valor de tipo {tipo_esperado}.")
                            )
                        else:
                            tipo_recibido = self.inferir_tipo(expr)

                            if tipo_recibido is None:
                                self.errores.append(
                                    (num, f"Error semántico [Retorno de función]: no se puede determinar el tipo retornado por '{nombre_funcion}'.")
                                )
                            elif tipo_recibido != tipo_esperado:
                                self.errores.append(
                                    (num, f"Error semántico [Retorno de función]: se esperaba un valor de tipo {tipo_esperado} y se recibió un valor de tipo {tipo_recibido}.")
                                )
                            else:
                                self.aprobados.append(
                                    (num, f"Return válido en función '{nombre_funcion}': tipo {tipo_recibido}.")
                                )

            if re.search(r"\bbreak\s*;", linea):
                if not loops and not switches:
                    self.errores.append(
                        (num, "Error semántico [Estructuras de control]: la instrucción break solo puede utilizarse dentro de un bucle o switch.")
                    )
                else:
                    self.aprobados.append(
                        (num, "Uso válido de break dentro de estructura de control.")
                    )

            if re.search(r"\bcontinue\s*;", linea):
                if not loops:
                    self.errores.append(
                        (num, "Error semántico [Estructuras de control]: la instrucción continue solo puede utilizarse dentro de un bucle.")
                    )
                else:
                    self.aprobados.append(
                        (num, "Uso válido de continue dentro de un bucle.")
                    )

            profundidad += linea.count("{") - linea.count("}")

            while funciones and profundidad < funciones[-1]["profundidad"]:
                funciones.pop()

            while loops and profundidad < loops[-1]:
                loops.pop()

            while switches and profundidad < switches[-1]:
                switches.pop()

        ahora = datetime.now().strftime("%d%m%Y-%Hh%M")
        nombre_log = f"semantico-{nombre_desarrollador}-{ahora}.txt"
        ruta_log = os.path.join("logs", nombre_log)
        os.makedirs("logs", exist_ok=True)

        with open(ruta_log, "w", encoding="utf-8") as log:
            log.write("=" * 60 + "\n")
            log.write("ANÁLISIS SEMÁNTICO - ANALIZADOR DART\n")
            log.write(f"Desarrollador: {nombre_desarrollador}\n")
            log.write(f"Archivo analizado: {ruta_codigo}\n")
            log.write(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            log.write("=" * 60 + "\n\n")

            log.write("REGLAS IMPLEMENTADAS POR ENRIQUE ROSADO:\n")
            log.write("  1. Rango de calificación válido entre 0 y 10.\n")
            log.write("  2. Géneros permitidos en la plataforma.\n")
            log.write("  3. Retorno de funciones compatible con el tipo declarado.\n")
            log.write("  4. break y continue usados dentro de estructuras válidas.\n\n")

            log.write("ERRORES SEMÁNTICOS:\n")

            if not self.errores:
                log.write("  - No se detectaron errores semánticos.\n")
            else:
                for l, msg in self.errores:
                    log.write(f"  Línea {l}: {msg}\n")

            log.write("\nPRUEBAS APROBADAS:\n")

            if not self.aprobados:
                log.write("  - Ninguna prueba aprobada.\n")
            else:
                for l, msg in self.aprobados:
                    log.write(f"  Línea {l}: {msg}\n")

            estado = "CON ERRORES" if self.errores else "COMPLETADO"
            log.write(f"\nEstado del análisis: {estado}\n")
            log.write("=" * 60 + "\n")

        print(f"Log generado: {nombre_log}")
        return ruta_log

# ==========================================
# APORTE ENRIQUE ROSADO - FIN
# ==========================================