"""
Aporte de Henry Olvera
Script para ejecutar el log.
"""
from semantic.semantico import SemanticAnalyzer
import os

def main():
    ruta_test = os.path.join('algoritmos', 'algoritmo_semantico_henry.dart')
    sa = SemanticAnalyzer()
    log = sa.analizar_archivo(ruta_test, 'HenryOlvera')
    print(f'Analizador semántico ejecutado. Log: {log}')

if __name__ == '__main__':
    main()
