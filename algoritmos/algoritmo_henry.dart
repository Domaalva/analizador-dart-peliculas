// Algoritmo de prueba - Henry Olvera
void main() {
  int edad = 20;
  bool activo = true;
  int contador = 0;
  int opcion = 1;

  print('Inicio - edad: $edad, activo: $activo, contador: $contador, opcion: $opcion');

  // Ejemplo: if con operadores relacionales y lógicos (>=, &&, ==)
  if (edad >= 18 && activo == true) {
    print('Acceso permitido');
  } else {
    print('Acceso denegado');
  }

  // Ejemplo: while con ++ (incremento)
  while (contador < 3) {
    contador++;
    print('Dentro while, contador: $contador');
    if (contador == 2) {
      // continue para saltar al siguiente ciclo
      contador++;
      continue;
    }
  }

  print('Después del while, contador: $contador');

  // Ejemplo: decremento --
  contador--;
  print('Después de --, contador: $contador');

  // Ejemplo: for, break y operadores <, >
  for (int i = 0; i < 5; i++) {
    print('for i = $i');
    if (i > 2) {
      print('i mayor que 2, rompo el for');
      break;
    }
  }

  // Ejemplo: switch, case y default
  switch (opcion) {
    case 0:
      print('Opción 0');
      break;
    case 1:
      print('Opción 1');
      break;
    default:
      print('Opción por defecto');
      break;
  }

  // Ejemplo: operadores relacionales y lógicos adicionales
  int a = 5;
  int b = 10;
  if (a < b || a == b) {
    print('a < b o a == b');
  }

  if (!(a != b)) {
    print('a es igual a b (negado)');
  } else {
    print('a es distinto de b');
  }

  print('Fin del algoritmo de prueba');
}
