# Script de ejecución semántico - Enrique Rosado
from semantic.semantico import SemanticAnalyzerEnrique
import os


def main():
    ruta_test = os.path.join("algoritmos", "algoritmo_semantico_enrique.dart")
    sa = SemanticAnalyzerEnrique()
    log = sa.analizar(ruta_test, "EnriqueRosado")
    print(f"Analizador semántico ejecutado. Log: {log}")


if __name__ == "__main__":
    main()