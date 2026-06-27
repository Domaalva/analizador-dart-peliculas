# Script de ejecución semántico - Domenika Arboleda
from semantic.semantico import SemanticAnalyzerDome
import os

def main():
    ruta_test = os.path.join('algoritmos', 'algoritmo_semantico_dome.dart')
    sa = SemanticAnalyzerDome()
    log = sa.analizar(ruta_test, 'DomenikaArboleda')
    print(f'Analizador semántico ejecutado. Log: {log}')

if __name__ == '__main__':
    main()