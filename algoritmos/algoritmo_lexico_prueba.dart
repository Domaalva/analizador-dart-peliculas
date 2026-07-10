// Algoritmo de prueba léxico - Domenika Arboleda
// Incluye tokens válidos y errores léxicos intencionales

void main() {
  // Declaraciones válidas
  int calificacion = 8;
  double promedio = 8.5;
  String titulo = "Inception";
  bool esRecomendada = true;
  var director = "Nolan";
  const double calificacionMaxima = 10.0;
  final String plataforma = "Netflix";

  // Operadores válidos
  double total = promedio + 1.5;
  calificacion += 1;
  promedio -= 0.5;

  // ERROR 1: carácter @ no válido en Dart
  @titulo = "Tenet";

  // ERROR 2: carácter # no válido en Dart
  #calificacion = 9;

  // ERROR 3: carácter $ suelto (fuera de string)
  $promedio = 7.5;

  // Más tokens válidos después del error
  int anio = 2010;
  bool activo = false;
}