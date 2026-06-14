// Algoritmo de prueba - Domenika Arboleda
// Plataforma de recomendación de películas

void mostrarPelicula(String titulo, [double calificacion = 0.0, String genero = "Sin género"]) {
  print("Título: $titulo");
  print("Calificación: $calificacion");
  print("Género: $genero");
}

void main() {
  // Declaración de variables con tipos primitivos
  int anio = 2010;
  double promedio = 8.5;
  String nombrePelicula = "Inception";
  bool esRecomendada = true;
  var director = "Christopher Nolan";

  // Constantes
  const double calificacionMaxima = 10.0;
  const int calificacionMinima = 0;
  final String plataforma = "Netflix";

  // Operadores aritméticos
  double total = promedio + 1.5;
  double resultado = calificacionMaxima - promedio;
  double multiplicacion = promedio * 2;
  double division = total / 2;
  int modulo = anio % 2;

  // Operadores de asignación
  promedio += 0.5;
  total -= 1.0;

  // Map de película
  Map<String, dynamic> pelicula = {
    "titulo": "Inception",
    "calificacion": 8.5,
    "genero": "Ciencia ficción",
    "esRecomendada": true
  };

  // Set de géneros
  Set<String> generosPermitidos = {
    "Acción",
    "Drama",
    "Comedia",
    "Terror"
  };

  // Estructura while
  int indice = 0;
  while (indice < 5) {
    print("Índice: $indice");
    indice++;
  }

  // Estructura switch
  switch (nombrePelicula) {
    case "Inception":
      print("Película de ciencia ficción");
      break;

    case "Drama":
      print("Película de drama");
      break;

    default:
      print("Género no reconocido");
  }

  // Llamada a función
  mostrarPelicula("Interstellar", 9.0, "Ciencia ficción");
  mostrarPelicula("Tenet");
}