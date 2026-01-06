#ifndef PREGUNTA_H
#define PREGUNTA_H

#include "respuestas.h"
#include <iostream>
#include <string>
#include <vector>
#include <fstream>


using namespace std;

class Pregunta
{
private:
    string texto;
    vector<Respuestas>respuestas;

public:
    Pregunta();
    Pregunta(string &textoPregunta);

    vector<Respuestas>&getRespuestas();
    string getTexto();
    void guardar(ofstream &archivo);
    void cargar(ifstream &archivo);
    void responder();

};

#endif // PREGUNTA_H
