// Algoritmo de prueba - Enrique Rosado
// Prueba de funciones, clases, delimitadores y comentarios

class Pelicula {

  String titulo;
  double calificacion;

  Pelicula(this.titulo, this.calificacion);

  void mostrarInformacion() {
    print("Título: $titulo");
    print("Calificación: $calificacion");
  }

  String obtenerCategoria() {
    return "Recomendada";
  }
}

void mostrarGeneros(List<String> generos) {

  for (var genero in generos) {
    print(genero);
  }

}

void main() {

  // Comentario de una línea

  /*
     Comentario
     multilínea
     para probar el lexer
  */

  Pelicula pelicula = Pelicula(
    "Inception",
    8.8
  );

  pelicula.mostrarInformacion();

  String categoria =
      pelicula.obtenerCategoria();

  print(categoria);

  List<String> generos = [
    "Acción",
    "Drama",
    "Ciencia ficción"
  ];

  mostrarGeneros(generos);

  Map<String, dynamic> datos = {
    "titulo": "Interstellar",
    "anio": 2014
  };

  print(datos);

}