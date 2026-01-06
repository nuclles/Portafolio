#ifndef INGREDIENTE_H
#define INGREDIENTE_H
#include <iostream>
#include <cstring>
#include <memory>
#include <fstream>

using namespace std;

class ingrediente
{

public:

    string nombre;
    double costo;
    int id;

    ingrediente();
    virtual double Costo()=0;
    virtual void guardar(const char* direccion)=0;
    virtual int GetID();

};

#endif // INGREDIENTE_H

#include "ingrediente.h"

ingrediente::ingrediente() {}

int ingrediente::GetID(){
    return this->id;
}

//--------------------------------------------------------------------------------------------------//

#ifndef INGREDIENTEBASE_H
#define INGREDIENTEBASE_H
#include "ingrediente.h"

struct S_IngredienteBase{
    char nombre[200];
    double costo;
    int id;
};



class IngredienteBase:public ingrediente
{

public:
    IngredienteBase();
    IngredienteBase(string &nombre, double costo, int id);
    double Costo();
    S_IngredienteBase GetIngrediente();
    void guardar(const char* direccion);

};

#endif // INGREDIENTEBASE_H

#include "ingredientebase.h"

IngredienteBase::IngredienteBase() {}

IngredienteBase::IngredienteBase(string &nombre, double costo, int id){
    this->nombre=nombre;
    this->costo=costo;
    this->id=id;
}

double IngredienteBase::Costo(){
    return costo;
}

S_IngredienteBase IngredienteBase::GetIngrediente(){
    S_IngredienteBase aux;
    strcpy(aux.nombre,nombre.c_str());
    aux.costo =costo;
    aux.id=id;
    return aux;
}

void IngredienteBase::guardar(const char *direccion){
    S_IngredienteBase nuevoIngrediente =GetIngrediente();

    //verificar si el ingrediente ya existe en el archivo
    ifstream archivoIngredientes (direccion,ios::binary);
    bool existe = false;
    if(archivoIngredientes.is_open()){
        S_IngredienteBase ingredienteExistente;


        //leer todos los ingredientes del archivo
        while(archivoIngredientes.read(reinterpret_cast<char*>(&ingredienteExistente),sizeof(S_IngredienteBase))){
            if(strcmp(ingredienteExistente.nombre,nuevoIngrediente.nombre)==0){
                existe=true;
                break;
            }
        }
        archivoIngredientes.close();
    }
    if(!existe){
        ofstream archivoIngredientes(direccion,ios::binary);
        if(archivoIngredientes.fail())return;

        archivoIngredientes.write(reinterpret_cast<char*>(&nuevoIngrediente),sizeof(S_IngredienteBase));
         archivoIngredientes.close();
    }

}


//--------------------------------------------------------------------------------------------------//

#ifndef PLATO_H
#define PLATO_H

#include "ingrediente.h"
#include "vector"
struct S_Relacion{
    int id_Plato;
    vector <int>id_ingredientes;
};

struct S_plato{
    char nombre[200];
    double costo;
    int id;
};

class plato: public ingrediente
{
    vector<ingrediente*> ingredientes;

public:
    plato();
    plato(string nombre, int id);

    void addIngrediente(ingrediente *ingrediente);
    double Costo();
    S_plato GetPlato();
    S_Relacion GetRelacion();
    void guardar(const char*direccion);
    void guardar_relacion(const char *direccion);

};

#endif // PLATO_H

#include "plato.h"

plato::plato() {}

plato::plato(string nombre,int id)
{
    this->nombre=nombre;
    this->id=id;
}

void plato::addIngrediente(ingrediente *ingrediente){
    ingredientes.push_back(ingrediente);
}

double plato::Costo(){

    for(auto& ingrediente:ingredientes){
        this->costo += ingrediente->Costo();
    }
    return this->costo;
}

S_plato plato::GetPlato(){
    S_plato aux;
    strcpy_s(aux.nombre,nombre.c_str());
    aux.costo=Costo();
    aux.id=id;
    return aux;
}

S_Relacion plato::GetRelacion(){
    S_Relacion aux;
    aux.id_Plato=id;
    for (auto& ingrediente:ingredientes){
        aux.id_ingredientes.push_back(ingrediente->GetID());
        }

    return aux;
}

void plato::guardar(const char *direccion){
    S_plato nuevoPlato = GetPlato();

    //verifica si el plato ya existe en el archivo
    ifstream archivoPlatos(direccion,ios::binary);
    bool existe =false;
    if(archivoPlatos.is_open()){
        S_plato platoExistente;

        //leer todos los platos del archivo
        while (archivoPlatos.read(reinterpret_cast<char*>(&platoExistente),sizeof(S_plato))){
            if(strcmp(platoExistente.nombre,nuevoPlato.nombre)==0){
                existe=true;
            }
        }
        archivoPlatos.close();
    }
    if(!existe){

        ofstream archivoPlatos(direccion,ios::binary);
        if(archivoPlatos.fail())return;

        archivoPlatos.write(reinterpret_cast<char *>(&nuevoPlato),sizeof(S_plato));
        archivoPlatos.close();
    }

}


void plato::guardar_relacion(const char* direccion){
    ofstream archivoRelacion(direccion,ios::binary);
    if(archivoRelacion.fail())return;

    S_Relacion aux=GetRelacion();
    archivoRelacion.write(reinterpret_cast<char*>(&aux),sizeof(S_Relacion));
}

//--------------------------------------------------------------------------------------------------//

