#include <iostream>
#include "respuestas.h"
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include "pregunta.h"
#include "sistemaencuesta.h"

using namespace std;

int main() {
    SistemaEncuesta sistema;
    sistema.cargarEncuesta();
    sistema.guardarEncuesta("encuesta.bin");

    SistemaEncuesta sistema2;
    sistema2.cargarEncuestaDesdeArchivo("encuesta.bin");
    sistema2.mostrarEncuesta();

    return 0;
}
