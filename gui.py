import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog, messagebox
import io
import sys
import os
from datetime import datetime

# ==========================================
# INTERFAZ GRÁFICA - Domenika Arboleda
# Analizador Dart — Plataforma de Películas
# ==========================================

class AnalizadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Dart — Plataforma de Películas")
        self.root.geometry("1200x750")
        self.root.configure(bg="#F9F9F7")
        self.root.resizable(True, True)

        self._build_header()
        self._build_stats()
        self._build_main()
        self._build_toolbar()
        self._build_statusbar()

    # ── HEADER ──────────────────────────────────────
    def _build_header(self):
        header = tk.Frame(self.root, bg="#FFFFFF", pady=12)
        header.pack(fill="x", padx=0)

        tk.Label(header, text="Analizador Dart", font=("Helvetica", 16, "bold"),
                 fg="#630ED4", bg="#FFFFFF").pack(side="left", padx=20)
        self.subtitulo_var = tk.StringVar(value="Plataforma de Películas")

        tk.Label( header, textvariable=self.subtitulo_var, font=("Helvetica", 11),
            fg="#7B7487", bg="#FFFFFF" ).pack(side="left")
        
        # Tabs
        # Tabs
        tab_frame = tk.Frame(header, bg="#FFFFFF")
        tab_frame.pack(side="right", padx=20)

        self.tab_var = tk.StringVar(value="Léxico")
        self.tab_buttons = {}

        for tab in ["Léxico", "Sintáctico", "Semántico", "Todos"]:
            btn = tk.Button(
                tab_frame,
                text=tab,
                command=lambda t=tab: self._set_tab(t),
                font=("Helvetica", 10),
                relief="solid",
                bd=1,
                padx=12,
                pady=5,
                bg="#FFFFFF",
                fg="#4A4455",
                activebackground="#EDE9FE",
                activeforeground="#630ED4",
                cursor="hand2"
            )
            btn.pack(side="left", padx=4)

            self.tab_buttons[tab] = btn

        # Mostrar Léxico seleccionado al iniciar
        self._actualizar_tabs()

    def _set_tab(self, tab):
        self.tab_var.set(tab)
        self._actualizar_tabs()
        self._update_status(f"Vista: {tab}")

    def _actualizar_tabs(self):
        for nombre, boton in self.tab_buttons.items():
            if nombre == self.tab_var.get():
                boton.config(
                    bg="#EDE9FE",      # fondo morado claro
                    fg="#630ED4",      # texto morado
                    relief="solid",
                    bd=2,
                    highlightbackground="#630ED4"
                )
            else:
                boton.config(
                    bg="#FFFFFF",
                    fg="#4A4455",
                    relief="solid",
                    bd=1,
                    highlightbackground="#D1D5DB"
                )

    # ── STATS ────────────────────────────────────────
    def _build_stats(self):
        stats_frame = tk.Frame(self.root, bg="#F9F9F7", pady=10)
        stats_frame.pack(fill="x", padx=20)

        self.stat_tokens  = self._stat_card(stats_frame, "Tokens / Variables", "0", "#630ED4")
        self.stat_errores = self._stat_card(stats_frame, "Errores Detectados",  "0", "#A43073")
        self.stat_estado  = self._stat_card(stats_frame, "Estado", "Listo",          "#005B3D")

    def _stat_card(self, parent, label, value, color):
        frame = tk.Frame(parent, bg="#FFFFFF", bd=0,
                         highlightbackground=color,
                         highlightthickness=2,
                         padx=16, pady=10)
        frame.pack(side="left", fill="x", expand=True, padx=6)
        tk.Label(frame, text=label, font=("Helvetica", 9),
                 fg="#7B7487", bg="#FFFFFF").pack(anchor="w")
        lbl = tk.Label(frame, text=value, font=("Helvetica", 22, "bold"),
                       fg=color, bg="#FFFFFF")
        lbl.pack(anchor="w")
        return lbl

    # ── MAIN (editor + resultados) ───────────────────
    def _build_main(self):
        main = tk.Frame(self.root, bg="#F9F9F7")
        main.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        # Editor izquierdo
        left = tk.Frame(main, bg="#1E1B2E", bd=0)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(left, text="<> editor.dart", font=("Courier", 10),
                 fg="#9CA3AF", bg="#1E1B2E").pack(anchor="w", padx=10, pady=6)

        self.editor = scrolledtext.ScrolledText(
            left, font=("Courier New", 12), bg="#1E1B2E", fg="#E9D5FF",
            insertbackground="white", wrap="none",
            relief="flat", padx=10, pady=10)
        self.editor.pack(fill="both", expand=True)

        # Panel derecho de resultados
        right = tk.Frame(main, bg="#FFFFFF", bd=0,
                         highlightbackground="#E2E3E1", highlightthickness=1)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, text="Resultados del análisis",
                 font=("Helvetica", 12, "bold"),
                 fg="#1A1C1B", bg="#FFFFFF").pack(anchor="w", padx=14, pady=(10, 4))

        self.resultado = scrolledtext.ScrolledText(
            right, font=("Courier New", 10), bg="#FFFFFF", fg="#1A1C1B",
            relief="flat", padx=12, pady=8, state="disabled")
        self.resultado.pack(fill="both", expand=True)

        # Colores para tags
        self.resultado.tag_config("ok",    foreground="#10B981", font=("Courier New", 10))
        self.resultado.tag_config("error", foreground="#FB7185", font=("Courier New", 10, "bold"))
        self.resultado.tag_config("info",  foreground="#7C3AED", font=("Courier New", 10))
        self.resultado.tag_config("titulo",foreground="#1A1C1B", font=("Courier New", 11, "bold"))

    # ── TOOLBAR ──────────────────────────────────────
    def _build_toolbar(self):
        bar = tk.Frame(self.root, bg="#F9F9F7", pady=8)
        bar.pack(fill="x", padx=20)

        btn_style = dict(font=("Helvetica", 11), relief="flat",
                         padx=18, pady=8, cursor="hand2")

        tk.Button(bar, text="▶  Analizar", bg="#7C3AED", fg="white",
                  command=self._analizar, **btn_style).pack(side="left", padx=4)
        tk.Button(bar, text="🗑  Limpiar", bg="#FFFFFF", fg="#7C3AED",
                  command=self._limpiar, **btn_style).pack(side="left", padx=4)
        tk.Button(bar, text="📂  Cargar .dart", bg="#FFFFFF", fg="#7C3AED",
                  command=self._cargar, **btn_style).pack(side="left", padx=4)
        tk.Button(bar, text="💾  Exportar", bg="#FFFFFF", fg="#7C3AED",
                  command=self._exportar, **btn_style).pack(side="left", padx=4)

    # ── STATUS BAR ───────────────────────────────────
    def _build_statusbar(self):
        self.status_var = tk.StringVar(value="● Motor de análisis activo  |  Versión 1.0.4 - Dart Stable")
        bar = tk.Label(self.root, textvariable=self.status_var,
                       font=("Helvetica", 9), fg="#7B7487", bg="#E8E8E6",
                       anchor="w", padx=12, pady=4)
        bar.pack(fill="x", side="bottom")

    def _update_status(self, msg):
        ahora = datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"● {msg}  |  {ahora}")

    # ── ACCIONES ─────────────────────────────────────
    def _limpiar(self):
        self.editor.delete("1.0", "end")
        self._write_resultado([])
        self.stat_tokens.config(text="0")
        self.stat_errores.config(text="0")
        self.stat_estado.config(text="Listo", fg="#005B3D")
        self._update_status("Editor limpiado")

    def _cargar(self):
        path = filedialog.askopenfilename(
            filetypes=[("Archivos Dart", "*.dart"), ("Todos", "*.*")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                contenido = f.read()
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", contenido)
            nombre = os.path.basename(path)
            self.subtitulo_var.set(f"Plataforma de Películas — {nombre}")
            self._update_status(f"Archivo cargado: {os.path.basename(path)}")

    def _exportar(self):
        contenido = self.resultado.get("1.0", "end")
        if not contenido.strip():
            messagebox.showinfo("Exportar", "No hay resultados para exportar.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(contenido)
            self._update_status(f"Exportado: {os.path.basename(path)}")

    def _analizar(self):
        codigo = self.editor.get("1.0", "end").strip()
        if not codigo:
            messagebox.showwarning("Sin código", "Escribe o carga un archivo .dart primero.")
            return

        tab = self.tab_var.get()
        lineas = []
        total_errores = 0
        total_tokens = 0

        # ── ANÁLISIS LÉXICO ──────────────────────────
        if tab in ("Léxico", "Todos"):
            lineas.append(("titulo", "═══ ANÁLISIS LÉXICO ═══\n"))
            try:
                from lexer.lexer import lexer, errores_lexicos
                errores_lexicos.clear()

                lexer.lineno = 1
                lexer.input(codigo)

                toks = []

                for tok in lexer:
                    toks.append(tok)

                # Mostrar errores léxicos encontrados
                for err in errores_lexicos:
                    lineas.append(("error", f"{err}\n"))

                total_errores += len(errores_lexicos)
                
                total_tokens += len(toks)
                lineas.append(("info", f"Tokens encontrados: {len(toks)}\n\n"))
                for tok in toks:
                    lineas.append(("ok", f"[Línea {tok.lineno}] {tok.type:20} → {tok.value}\n"))

                if not toks:
                    lineas.append(("error", "No se encontraron tokens.\n"))
            except Exception as e:
                lineas.append(("error", f"Error en análisis léxico: {e}\n"))
                total_errores += 1
            lineas.append(("info", "\n"))

        # ── ANÁLISIS SINTÁCTICO ──────────────────────
        if tab in ("Sintáctico", "Todos"):
            lineas.append(("titulo", "═══ ANÁLISIS SINTÁCTICO ═══\n"))
            try:
                import sys, io
                from parser.parser import parser as yacc_parser

                buffer = io.StringIO()
                old_stdout = sys.stdout
                sys.stdout = buffer
                try:
                    yacc_parser.parse(codigo)
                finally:
                    sys.stdout = old_stdout

                salida = buffer.getvalue()
                errores_sint = [l for l in salida.splitlines() if "Error" in l]
                aprobados_sint = [l for l in salida.splitlines() if "Error" not in l and l.strip()]

                total_errores += len(errores_sint)
                for l in aprobados_sint:
                    lineas.append(("ok", f"✓ {l}\n"))
                for l in errores_sint:
                    lineas.append(("error", f"✗ {l}\n"))

                if not salida.strip():
                    lineas.append(("error", "No se reconoció ninguna estructura.\n"))

            except Exception as e:
                lineas.append(("error", f"Error en análisis sintáctico: {e}\n"))
                total_errores += 1
            lineas.append(("info", "\n"))

        # ── ANÁLISIS SEMÁNTICO ───────────────────────
                # ── ANÁLISIS SEMÁNTICO ───────────────────────
        if tab in ("Semántico", "Todos"):
            lineas.append(("titulo", "═══ ANÁLISIS SEMÁNTICO ═══\n"))

            ruta_temp = os.path.join("algoritmos", "_temp_gui.dart")

            try:
                # Guardar temporalmente el código escrito en el editor
                with open(ruta_temp, "w", encoding="utf-8") as f:
                    f.write(codigo)

                # Importar los analizadores semánticos de los tres integrantes
                from semantic.semantico import (
                    SemanticAnalyzer,
                    SemanticAnalyzerDome,
                    SemanticAnalyzerEnrique
                )

                analizadores = [
                    (
                        "Henry Olvera",
                        SemanticAnalyzer(),
                        "analizar_archivo",
                        "GUI-Henry"
                    ),
                    (
                        "Domenika Arboleda",
                        SemanticAnalyzerDome(),
                        "analizar",
                        "GUI-Domenika"
                    ),
                    (
                        "Enrique Rosado",
                        SemanticAnalyzerEnrique(),
                        "analizar",
                        "GUI-Enrique"
                    )
                ]

                resultados_semanticos = []
                total_validaciones = 0

                # Ejecutar cada analizador
                for integrante, analizador, metodo, nombre_log in analizadores:

                    funcion_analisis = getattr(analizador, metodo)
                    funcion_analisis(ruta_temp, nombre_log)

                    aprobados = list(analizador.aprobados)
                    errores = list(analizador.errores)

                    total_validaciones += len(aprobados) + len(errores)
                    total_errores += len(errores)

                    resultados_semanticos.append(
                        (integrante, aprobados, errores)
                    )

                lineas.append((
                    "info",
                    f"Validaciones realizadas: {total_validaciones}\n\n"
                ))

                # Mostrar los resultados separados por integrante
                for integrante, aprobados, errores in resultados_semanticos:

                    lineas.append((
                        "info",
                        f"── Reglas de {integrante} ──\n"
                    ))

                    for num, mensaje in aprobados:
                        lineas.append((
                            "ok",
                            f"[Línea {num}] ✓ {mensaje}\n"
                        ))

                    for num, mensaje in errores:
                        lineas.append((
                            "error",
                            f"[Línea {num}] ✗ {mensaje}\n"
                        ))

                    if not aprobados and not errores:
                        lineas.append((
                            "info",
                            "No se encontraron casos para estas reglas.\n"
                        ))

                    lineas.append(("info", "\n"))

                if tab == "Semántico":
                    total_principal += total_validaciones

            except Exception as e:
                lineas.append((
                    "error",
                    f"Error en análisis semántico: {e}\n"
                ))
                total_errores += 1

            finally:
                if os.path.exists(ruta_temp):
                    os.remove(ruta_temp)

        # ── ACTUALIZAR UI ────────────────────────────
        self._write_resultado(lineas)
        self.stat_tokens.config(text=str(total_tokens))
        self.stat_errores.config(text=str(total_errores))

        if total_errores == 0:
            self.stat_estado.config(text="Completado ✓", fg="#005B3D")
            self._update_status("Análisis completado sin errores")
        else:
            self.stat_estado.config(text="Con errores ✗", fg="#A43073")
            self._update_status(f"Análisis completado — {total_errores} error(es) encontrado(s)")

    def _write_resultado(self, lineas):
        self.resultado.config(state="normal")
        self.resultado.delete("1.0", "end")
        for tag, texto in lineas:
            self.resultado.insert("end", texto, tag)
        self.resultado.config(state="disabled")


# ── MAIN ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = AnalizadorGUI(root)
    root.mainloop()
