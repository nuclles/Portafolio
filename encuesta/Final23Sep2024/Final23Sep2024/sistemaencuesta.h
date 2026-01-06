#ifndef SISTEMAENCUESTA_H
#define SISTEMAENCUESTA_H
#include "encuesta.h"
#include "respuestas.h"
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include "pregunta.h"

class SistemaEncuesta {
private:
    Encuesta encuesta;

public:
    SistemaEncuesta();
    void cargarEncuesta();

    void guardarEncuesta(string& nombreArchivo);

    void cargarEncuestaDesdeArchivo(string& nombreArchivo);

    void mostrarEncuesta();
};
#endif // SISTEMAENCUESTA_H
