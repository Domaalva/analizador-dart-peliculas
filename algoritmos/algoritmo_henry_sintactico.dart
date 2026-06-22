// Archivo de prueba creado por HenryOlvera

// 1. Expresiones aritméticas
int totalPeliculas = 5 + 3;
double promedio = 85 / 10;
int resultado = (5 + 3) * 2;

// 2. Expresiones booleanas (AND / OR)
bool esPopular = totalPeliculas > 8;
bool esValida = promedio >= 0 && promedio <= 10;
bool recomendada = "Acción" == "Acción" || "Drama" == "Terror";

// 3. Estructura for
List<String> peliculas = ["Inception", "Interstellar", "Tenet"];
for (int indice = 0; indice < peliculas.length; indice++) {
  print(peliculas[indice]);
}

// 4. Declaraciones List y Set
List<String> peliculasFavoritas = ["Inception", "Interstellar", "Tenet"];
Set<String> generosPermitidos = {"Acción", "Drama", "Comedia", "Terror"};

// 5. Función con parámetros opcionales por nombre
void mostrarPelicula({String titulo = "", double calificacion = 0.0, String genero = "Sin género"}) {
  print(titulo);
  print(calificacion);
  print(genero);
}

// 6. Lambda (forma simplificada)
double calcularPromedio = (double suma, double cantidad) => suma / cantidad;
print(calcularPromedio(42.5, 5));
