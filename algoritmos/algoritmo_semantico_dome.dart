// Algoritmo de prueba semántico - Domenika Arboleda
// Prueba de reglas: asignación de tipo y constantes

// Declaraciones válidas
int calificacion = 8;
double promedio = 8.5;
String titulo = "Inception";
bool esRecomendada = true;
const double calificacionMaxima = 10.0;
const String plataforma = "Netflix";
final String director = "Nolan";

// Errores de asignación de tipo
int calificacionMal = "ocho";
double promedioMal = "alto";
bool esRecomendadaMal = 1;
String tituloMal = 42;

// Errores de modificación de constante
calificacionMaxima = 9.0;
plataforma = "HBO";
director = "Spielberg";

// Prueba de operaciones permitidas
int totalValido = 5 + 3;
double promedioValido = 8.5 + 1.5;
String concatenacion = "Inception" + " Movie";
int operacionInvalida = 5 + "Accion";
String restaInvalida = "Drama" - "Comedia";
bool operacionBool = true + 1;