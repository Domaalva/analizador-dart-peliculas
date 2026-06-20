// Algoritmo de prueba sintáctico - Domenika Arboleda
// Asignación de variables, switch, Map, función con parámetros opcionales

var genero = "Acción";
const double calificacionMaxima = 10.0;
final String director = "Nolan";
int calificacion = 8;

switch (genero) {
  case "Acción":
    print("Película de acción");
    break;
  case "Drama":
    print("Película de drama");
    break;
  default:
    print("Género no reconocido");
}

Map<String, dynamic> pelicula = {
  "titulo": "Inception",
  "calificacion": 8.5
};

void mostrarPelicula(String titulo, [double calificacion = 0.0]) {}