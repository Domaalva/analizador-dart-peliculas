// Algoritmo de prueba semántico - Enrique Rosado
// Reglas: rangos de calificación, géneros permitidos, retorno de funciones, break/continue.

// Casos válidos de dominio
String genero = "Acción";
double calificacion = 8.8;
int rating = 10;
var promedio = 7.5;

// Casos inválidos de dominio
String generoInvalido = "Western";
double calificacionInvalida = 11.5;
int ratingInvalido = -1;

// Casos válidos con estructuras tipo Map
Map<String, dynamic> peliculaValida = {
  "titulo": "Inception",
  "genero": "Ciencia ficción",
  "calificacion": 9.0
};

// Casos válidos con estructuras tipo List
List<String> generosValidos = [
  "Acción",
  "Drama",
  "Comedia"
];

// Casos válidos con estructuras tipo Set
Set<String> generosPermitidos = {
  "Acción",
  "Drama",
  "Comedia"
};

// Casos inválidos con estructuras tipo Map
Map<String, dynamic> peliculaInvalida = {
  "titulo": "Pelicula X",
  "genero": "Gore",
  "calificacion": 15.0
};

// Casos inválidos con estructuras tipo List
List<int> numerosInvalidos = [
  1,
  2.5,
  "tres"
];

// Casos inválidos con estructuras tipo Set
Set<int> generosInvalidos = {
  1,
  2,
  "tres"
};

// Retornos válidos
String obtenerGenero() {
  return "Drama";
}

double obtenerPromedio() {
  return 8.5;
}

bool esPopular() {
  return true;
}

// Retornos inválidos
String obtenerTituloIncorrecto() {
  return 5;
}

double obtenerPromedioIncorrecto() {
  return "alto";
}

bool esPopularIncorrecto() {
  return "si";
}

void mostrarMensajeIncorrecto() {
  return "No deberia retornar texto";
}

// break y continue válidos
while (true) {
  break;
}

for (int i = 0; i < 3; i++) {
  continue;
}

// break y continue inválidos
break;
continue;