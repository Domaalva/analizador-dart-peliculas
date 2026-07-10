# analizador-dart-peliculas

# Analizador Dart — Plataforma de Películas

Implementación de un analizador léxico, sintáctico y semántico para un subconjunto del lenguaje Dart, aplicado al contexto de una plataforma de recomendación de películas.

## Integrantes
- Domenika Arboleda (domaalva)
- Henry Olvera (HenryOlvera28)
- Enrique Rosado (Enrique2305-gif)

## Requisitos

Python 3.10 o superior.

Instalar las dependencias con:

```bash
pip install ply
```

No se requieren más librerías externas. `tkinter` ya viene incluido con Python.

## Estructura del proyecto
analizador-dart-peliculas/
├── lexer/
│   └── lexer.py              # Analizador léxico
├── parser/
│   └── parser.py             # Analizador sintáctico
├── semantic/
│   └── semantico.py          # Analizador semántico
├── algoritmos/
│   ├── algoritmo_dome.dart
│   ├── algoritmo_dome_sintactico.dart
│   ├── algoritmo_semantico_dome.dart
│   ├── algoritmo_henry.dart
│   ├── algoritmo_semantico_henry.dart
│   └── algoritmo_enrique.dart
├── logs/                     # Logs generados por cada análisis
├── gui.py                    # Interfaz gráfica
├── run_lexer.py              # Ejecutar análisis léxico
├── run_semantico_dome.py     # Ejecutar análisis semántico Dome
├── run_semantico.py          # Ejecutar análisis semántico Henry
├── run_semantico_enrique.py  # Ejecutar análisis semántico Enrique
└── README.md

## Cómo ejecutar

### Interfaz gráfica
```bash
python gui.py
```

### Análisis léxico
```bash
python lexer/lexer.py
```

### Análisis sintáctico
```bash
python -m parser.parser
```

### Análisis semántico
```bash
python run_semantico_dome.py
python run_semantico.py
python run_semantico_enrique.py
```

## Logs

Los logs se generan automáticamente en la carpeta `logs/` con el formato:
- `lexico-NombreApellido-fecha-hora.txt`
- `sintactico-NombreApellido-fecha-hora.txt`
- `semantico-NombreApellido-fecha-hora.txt`

- 
