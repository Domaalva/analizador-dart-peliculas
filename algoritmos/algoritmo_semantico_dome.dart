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