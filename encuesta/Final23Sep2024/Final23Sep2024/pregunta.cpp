#include "pregunta.h"

Pregunta::Pregunta() {}

Pregunta::Pregunta(string &textoPregunta):texto(textoPregunta){}

vector<Respuestas> &Pregunta::getRespuestas()
{
    return respuestas;
}

string Pregunta::getTexto()
{
    return texto;
}

void Pregunta::guardar(ofstream &archivo)
{
    size_t longitudTexto = texto.size();
    archivo.write(reinterpret_cast<const char*>(&longitudTexto),sizeof(longitudTexto));
    archivo.write(texto.c_str(),longitudTexto);

    size_t numRespuestas = respuestas.size();
    archivo.write(reinterpret_cast<const char*>(&numRespuestas),sizeof(numRespuestas));

    for(auto &respuesta : respuestas){
        respuesta.guardar(archivo);
    }

}

void Pregunta::cargar(ifstream &archivo)
{
    size_t longitudTexto;
    archivo.read(reinterpret_cast<char*>(&longitudTexto),sizeof(longitudTexto));

    char* buffer = new char[longitudTexto+1];
    archivo.read(buffer, longitudTexto);
    buffer[longitudTexto]='\0';
    texto=buffer;
    delete[]buffer;

    size_t numRespuestas;
    archivo.read(reinterpret_cast<char*>(&numRespuestas),sizeof(numRespuestas));

    respuestas.clear();
    for(size_t i=0;i<numRespuestas; i++){
        Respuestas respuesta("",nullptr);
        respuesta.cargar(archivo);
        respuestas.push_back(respuesta);

    }

}

void Pregunta::responder()
{
    cout<<"Pregunta: "<< texto <<endl;

    //mostrar las respuestas disponibles
    for(size_t i=0;i<respuestas.size();i++){
        cout<<" "<<(i+1)<<". "<<respuestas[i].getTexto()<<endl;
    }

    //solicitar al usuario que seleccione una respuesta
    int seleccion;
    cout<<"seleccione una respuesta (1-"<< respuestas.size()<<"):";
    cin>>seleccion;

    //validar la seleccion del ususario
    if(seleccion < 1 || seleccion > respuestas.size()){
        cout<<"Seleccion invalida. Intente de nuevo."<<endl;
        return;
    }

    //obtener la respuesta seleccionada
    Respuestas& respuestaSeleccionada = respuestas[seleccion -1];

    if(respuestaSeleccionada.getSubpregunta()){
        cout<<"\n Subpregunta: \n";
        respuestaSeleccionada.getSubpregunta()->responder();
    }

}


