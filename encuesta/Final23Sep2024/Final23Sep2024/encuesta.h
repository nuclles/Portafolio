#ifndef ENCUESTA_H
#define ENCUESTA_H
#include "respuestas.h"
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include "pregunta.h"


class Encuesta
{
private:
    vector<Pregunta>preguntas;

public:
    Encuesta();
    void agregarPregunta(Pregunta& pregunta);
    vector<Pregunta>&getPreguntas();

    void guardar(string& nombreArchivo);

    void cargar(string& nombreArchivo);
};

#endif // ENCUESTA_H
