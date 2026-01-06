#include "encuesta.h"

Encuesta::Encuesta() {}

void Encuesta::agregarPregunta(Pregunta &pregunta){
    preguntas.push_back(pregunta);
}

vector<Pregunta> &Encuesta::getPreguntas(){
    return preguntas;

}

void Encuesta::guardar(string &nombreArchivo){
    ofstream archivo(nombreArchivo,ios::binary);
    if(archivo.fail()){
        cout<<"Error al abrir el archivo"<<endl;
        return;
    }

    size_t numPreguntas = preguntas.size();
    archivo.write(reinterpret_cast<const char*>(&numPreguntas),sizeof(numPreguntas));

    for(auto &pregunta: preguntas){
        pregunta.guardar(archivo);
    }
}

void Encuesta::cargar(string &nombreArchivo){
    ifstream archivo(nombreArchivo, ios::binary);
    if(archivo.fail()){
        cout<<"Error al abrir el archivo para lectura. "<<endl;
        return;

        size_t numPreguntas;
        archivo.read(reinterpret_cast<char*>(&numPreguntas),sizeof(numPreguntas));

        preguntas.clear();
        for(size_t i=0; i < numPreguntas;i++){
            Pregunta pregunta("");
            pregunta.cargar(archivo);
            preguntas.push_back(pregunta);

        }
    }
}
