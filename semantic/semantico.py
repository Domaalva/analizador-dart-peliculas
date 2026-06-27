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
# ==========================================

class SemanticAnalyzerDome:
    def __init__(self):
        self.tabla_simbolos = {}  # nombre -> {'tipo': str, 'es_const': bool, 'linea': int}
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
            # Detectar declaración const
            m = re.match(r'^const\s+(int|double|String|bool)\s+([A-Za-z_]\w*)\s*=\s*(.+);$', linea)
            if m:
                tipo, nombre, expr = m.group(1), m.group(2), m.group(3).strip()
                self.tabla_simbolos[nombre] = {'tipo': tipo, 'es_const': True, 'linea': num}

                # --- REGLA 1: verificar compatibilidad de tipo ---
                tipo_valor = self.inferir_tipo(expr)
                if tipo_valor is None:
                    self.errores.append((num, f"Error semántico [Asignación de tipo]: no se puede determinar el tipo de '{expr}' para la constante '{nombre}'."))
                elif tipo_valor != tipo:
                    self.errores.append((num, f"Error semántico [Asignación de tipo]: no se puede asignar un valor de tipo {tipo_valor} a una constante de tipo {tipo} ('{nombre}')."))
                else:
                    self.aprobados.append((num, f"Declaración const válida: {tipo} {nombre} = {expr}"))
                continue

            # Detectar declaración final (también inmutable)
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

                # --- REGLA 1: verificar compatibilidad de tipo ---
                tipo_valor = self.inferir_tipo(expr)
                if tipo_valor is None:
                    self.errores.append((num, f"Error semántico [Asignación de tipo]: no se puede determinar el tipo de '{expr}' para '{nombre}'."))
                elif tipo_valor != tipo:
                    self.errores.append((num, f"Error semántico [Asignación de tipo]: no se puede asignar un valor de tipo {tipo_valor} a una variable de tipo {tipo} ('{nombre}')."))
                else:
                    self.aprobados.append((num, f"Declaración válida: {tipo} {nombre} = {expr}"))
                continue

            # Detectar reasignación a variable ya declarada
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