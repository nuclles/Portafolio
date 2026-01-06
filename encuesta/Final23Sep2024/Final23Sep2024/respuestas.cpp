#include "respuestas.h"

Respuestas::Respuestas() {}

Respuestas::Respuestas(string &textoRespuesta, Pregunta *subPreguntaRespuesta):texto(textoRespuesta),subPregunta(subPreguntaRespuesta){}

string Respuestas::getTexto()
{
    return texto;
}

Pregunta *Respuestas::getSubpregunta()
{
    return subPregunta;
}

void Respuestas::guardar(ofstream &archivo)
{
    size_t longitudTexto = texto.size();
    archivo.write(reinterpret_cast<const char*>(&longitudTexto),sizeof(longitudTexto));
    archivo.write(texto.c_str(),longitudTexto);

    bool tieneSubpregunta =(subPregunta!=nullptr);
    archivo.write(reinterpret_cast <const char*>(&tieneSubpregunta),sizeof(tieneSubpregunta));

    if(tieneSubpregunta){
        subPregunta->guardar(archivo);
    }
}

void Respuestas::cargar(ifstream &archivo)
{
    size_t longitudTexto;
    archivo.read(reinterpret_cast<char*>(&longitudTexto),sizeof(longitudTexto));

    char* buffer = new char[longitudTexto+1];
    archivo.read(buffer,longitudTexto);
    buffer[longitudTexto]='\0';
    texto=buffer;
    delete[]buffer;

    bool tieneSubpregunta;
    archivo.read(reinterpret_cast<char*>(&tieneSubpregunta), sizeof(tieneSubpregunta));

    if(tieneSubpregunta){
        subPregunta =new Pregunta("");
        subPregunta->cargar(archivo);
    }else{
        subPregunta = nullptr;
    }
}
