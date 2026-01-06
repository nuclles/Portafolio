#ifndef RESPUESTAS_H
#define RESPUESTAS_H
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include "pregunta.h"

using namespace std;


class Respuestas
{
private:
    string texto;
    Pregunta* subPregunta;
public:
    Respuestas();
    Respuestas(string& textoRespuesta, Pregunta* subPreguntaRespuesta = nullptr);

    string getTexto();
    Pregunta* getSubpregunta();

    void guardar(ofstream& archivo);
    void cargar (ifstream& archivo);

};

#endif // RESPUESTAS_H
