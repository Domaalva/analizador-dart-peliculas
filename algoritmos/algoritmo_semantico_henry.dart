// Aporte de Henry Olvera
// Archivo de prueba para el analizador semántico

// Constantes (válidas e inválidas)
const double calificacionMaxima = 10.0;
calificacionMaxima = 9.0; // debería generar error: no modificar const

const String plataforma = "Netflix";
plataforma = "HBO"; // error

const int minimoCalificacion = 0;
minimoCalificacion = 1; // error

// Declaraciones con tipos (válidas e inválidas)
int calificacion = 8;
int calificacion_wrong = "ocho"; // error: String a int

double promedio = 8.5;
double promedio_wrong = "alto"; // error

bool esRecomendada = true;
esRecomendada_wrong = 1; // error: int a bool

String titulo = "Inception";
titulo_wrong = 42; // error: int a String

// Var y asignaciones entre identificadores
var x = 5;
var y = "hola";
int a = 2;
int b = a; // válido: asignación desde otro identificador declarado

// Asignación a variable no declarada
nuevaVar = 5; // error: no declarada

// final (tratado similar a const en este analizador simple)
final int fijo = 3;
fijo = 4; // error: no puede reasignarse
