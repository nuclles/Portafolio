#ifndef COMERCIO_H
#define COMERCIO_H
#include <algorithm>
#include <map>
#include <vector>
#include<iostream>
#include "producto.h"
#include "productoi.h"
#include "productoj.h"
#include "producton.h"
#include <fstream>


using namespace std;


class comercio
{
private:
    vector<Producto*>Productos;

public:
    comercio();

    void ActualizarPrecios(){
        for(auto &prod:Productos){
            prod->ActualizarPrecio();
        }
    }

    void cargar_productos(const char* diereccionLectura,const char*direccionGuardado){
        ifstream archivoLectura(diereccionLectura,ios::binary);
        S_producto aux;
        while (archivoLectura.read((char*)&aux,sizeof(S_producto))) {
            if(archivoLectura.is_open()){

                switch(aux.tipo){

                case 'N': Productos.push_back(new ProductoN(aux));
                    break;
                case 'I': Productos.push_back(new ProductoI(aux));
                    break;
                case 'J': Productos.push_back(new ProductoJ(aux));
                    break;
                }
            }
        }archivoLectura.close();
            ofstream archivoGuardado(direccionGuardado,ios::binary);
        if(archivoGuardado.is_open()){
                for(auto &prod:Productos){
                prod->ActualizarPrecio();
                S_producto aux = prod->GetProducto();
                    archivoGuardado.write(reinterpret_cast <char*>(&aux),sizeof(S_producto));

            }

        }
    }

    void mostrarProductos(const char* direccionLectura, const char* direccionMostrar){
        ifstream archivoGuardado (direccionLectura,ios::binary);
        S_producto aux;
        vector<Producto*>Prod;
        while (archivoGuardado.read((char*)(&aux),sizeof(S_producto))) {
            if(archivoGuardado.is_open()){


                switch (aux.tipo){

                case 'N': Prod.push_back(new ProductoN (aux));
                    break;
                case 'I': Prod.push_back(new ProductoI (aux));
                    break;
                case 'J': Prod.push_back(new ProductoJ (aux));
                    break;
                }
            }
        }
        sort(Prod.begin(),Prod.end(),[](Producto& a, Producto& b){
            return a.getnombre() < b.getnombre();
        });

        ofstream archivoMostrar(direccionMostrar);
        if(archivoMostrar.is_open()){
            for(auto &producto:Prod){
                archivoMostrar<<producto->getnombre()<<", "<<producto->getmarca()<<"..........$"<<producto->getprecio();
            }
        }

    }

    void ProductosPorMarca(){
        map<string,int>Prod;

        for_each(Productos.begin(),Productos.end(),[&Prod](Producto &aux){
            Prod[aux.getmarca()]++;
        });

        sort(Productos.begin(),Productos.end(),[](Producto &a,Producto &b){
            return a.getprecio() < b.getprecio();
        });

            for(auto & producto:Prod){
            cout<<producto.first <<" "<<producto.second<< endl;
        }

            size_t a=Productos.size();
            cout<<"Producto con maryor precio:  "<<Productos[0]->getnombre()<<"  "<<Productos[0]->getprecio()<<endl;
            cout<<"Producto con menor precio:  "<<Productos[a]->getnombre()<<"  "<<Productos[a]->getprecio()<<endl;
    }

    /*
STL (Standard Template Library):

Es una biblioteca estándar de C++ que proporciona plantillas (templates) para estructuras de datos (como vectores,
 listas, mapas) y algoritmos (como ordenación y búsqueda). Es una herramienta fundamental para la programación genérica.

Polimorfismo:

Es la capacidad de un objeto de tomar múltiples formas. En C++, se logra mediante funciones virtuales y herencia.
 Permite que una función se comporte de manera diferente según el tipo del objeto que la invoca.

Programación Genérica:

Es un paradigma que permite escribir código independiente del tipo de datos.
 En C++, se implementa mediante plantillas (templates),
 que permiten crear funciones y clases que funcionan con cualquier tipo de dato.

*/
};

#endif // COMERCIO_H

//-----------------------------------------------------------------------------------------//

#ifndef PRODUCTO_H
#define PRODUCTO_H
#include <iostream>
#include <cstring>
#include <fstream>

using namespace std;

struct S_producto {
    int codigo;
    char nombre [200];
    char marca[200];
    char tipo;
    double precio;
};

class Producto
{ 
public:
    string nombre;
    string marca;
    int codigo;
    char tipo;
    double precio;
    float IncrementoDolar;

    Producto();

    virtual void ActualizarPrecio()=0;
    char GetTipo();
    string  getnombre(){return nombre;}
    string getmarca(){return marca;}
    double getprecio(){return precio;}

    S_producto GetProducto(){
        S_producto aux;
        strcpy(aux.nombre,nombre.c_str());
        strcpy(aux.marca,marca.c_str());
        aux.codigo=codigo;
        aux.tipo=tipo;
        aux.precio=precio;
        return aux;
    }


};

#endif // PRODUCTO_H

//----------------------------------------------------------------------------------------------//

#ifndef PRODUCTOI_H
#define PRODUCTOI_H

#include <Producto.h>


class ProductoI:public Producto
{
public:
    ProductoI();
    ProductoI(S_producto aux);
    void ActualizarPrecio();
};

#endif // PRODUCTOI_H

//----------------------------------------------------------------------------------------------//

#ifndef PRODUCTOJ_H
#define PRODUCTOJ_H

#include <Producto.h>


class ProductoJ:public Producto
{
public:
    ProductoJ();
    ProductoJ(S_producto aux);
    void ActualizarPrecio();
};

#endif // PRODUCTOJ_H


//----------------------------------------------------------------------------------------------//

#ifndef PRODUCTON_H
#define PRODUCTON_H

#include <Producto.h>


class ProductoN: public Producto
{
public:
    ProductoN();
    ProductoN(S_producto aux);
    void ActualizarPrecio();
};

#endif // PRODUCTON_H
