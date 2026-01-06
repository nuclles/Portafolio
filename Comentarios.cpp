#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <fstream>
#include <algorithm>

using namespace std;

struct S_producto{
    char nombre[200];
    int puntaje;
    int cantComentarios;
}

class producto{
    private:
    string nombre;
    int puntaje;
    int cantComentarios;
    vector<comentario>comentarios;
    public:
    producto(string n){
        this->nombre =n;
        this->puntaje=0;
    }

    S_producto getDatos(){
        S_producto aux;
        aux.puntaje=this->puntaje;
        aux.cantComentarios=this->cantComentarios;
        strcpy(nombre,this->nombre.c_str());
    }


    void agregarComentario(comentario c){
        comentarios.push_back(c);
    }
    
    void calcularPuntaje(){
        for(auto &c : comentarios){
            this->puntaje += c.getPuntaje();
            this->puntaje += c.calcularPuntajeSubComentarios();
        }
    }

    void Cantidad_de_Comentarios(){
        this->cantComentarios=size_t(comentarios);
        for(auto &com:comentarios){
           this->cantComentarios+=com.cantidadSubordinados();
        }
    }
    vector<comentario>VecComentarios(){
        return comentarios;
    }
    int getPuntaje(){
        return this->puntaje;
    }
    string getNombre(){
        return this->nombre;
    }
};
class subComentario{
    private:
    string texto;
    int puntaje;
    public:
    subComentario(string t, int p){
        this->texto =t;
        this->puntaje =p;
    }
    string getNombre(){
        return this->nombre;
    }
    int getPuntaje(){
        return this->puntaje;
    }
};

class comentario{
    private:
    string texto;
    int puntaje;
    int cantSubComentarios;
    vector<subComentario>respuestas;
    public:
    comentario(string t, int p){
        this->texto =t;
        this->puntaje =p;
    }

    int Cant_de_SubComentarios(){
        int aux = size_t(respuestas);
        return aux;
    }

    void agregarRespuesta(subComentario c){
        respuestas.push_back(c);
    }
    string getTexto(){
        return this->texto;
    }
    int getPuntaje(){
        return this->puntaje;
    }
    int calcularPuntajeSubComentarios(){
        int SC_total; 
        for(auto &SC:respuestas){
            SC_total += SC.getPuntaje();
        }
        return SC_total;
    }
};

class gestora{
    private:
    vector<producto>productos;
    public:
    gestora(){}
    void agrgarProducto(producto p){
        productos.push_back(p);
    }
     void gestora::comentariosMayorPuntaje(){
        for(auto &prod:productos){
            prod.calcularPuntaje();
        }
        sort(productos.begin(),productos.end(),[](producto &a,producto &b){return a.getPuntaje()>b.getPuntaje();});

        for(int i=1;i<5;i++){
           cout<<"los puntajes mas altos: " productos[i].getNombre()<<endl;
        }
    }

    void gestora::ProductosConMasComentariosNegativos(){
        for(auto &prod:productos){
            prdo.calcularPuntaje();
            if(prod.getPuntaje()<=2){
                cout<<" producto"<< prod.getNombre()<<"puntaje"<<prdo.getPuntaje()<<endl;
            }
        }
    }

    void gestora::ProductoConMasComentarios(){
        for(auto &prdo:productos){
            prod.Cantidad_de_Comentarios();
        }
        sort(productos.begin(),productos.end(),[](producto &a,producto &b){return a.getcantComentarios()>b.getcantComentarios();});

        for(int i=1;i<5;i++){
           cout<<"los productos con mas comentarios son: " productos[i].getNombre()<<endl;
        }
    }

    void guardarBinario(const char* dir1,const char* dir2,const char* dir3)
    ofstream archivo1(dir1,ios::binary)
    for(auto &prod:productos){
            prod.calcularPuntaje();
        }
    if(archivo1.is_open()){
        //guardamos los productos con mayor puntaje
        sort(productos.begin(),productos.end(),[](producto &a,producto &b){return a.getPuntaje()>b.getPuntaje();});

        for(int i =1;i<5;i++){
            S_producto aux1 =productos[i].getDatos()
            archivo1.write(reinterpret_cast<const char*>(&aux1),size_t(S_producto)); 
        }}

        ofstream archivo2(dir2,ios::binary)
        if(archivo2.is_open()){
        //guardamaos los productos con mas comentarios negativos
          for(auto &prod:productos){
            if(prod.getPuntaje()<=2){
            S_producto aux2 =prod.getDatos()
            archivo2.write(reinterpret_cast<const char*>(&aux),size_t(S_producto)); 
            }
        }
        }
        ofstream archivo3(dir3,ios::binary)
        if(archivo3.is_open()){
        //guardamos los productos con mas comentarios
             for(auto &prdo:productos){
            prod.Cantidad_de_Comentarios();
        }
        sort(productos.begin(),productos.end(),[](producto &a,producto &b){return a.getcantComentarios()>b.getcantComentarios();});
            for(int i =1;i<5;i++){
                        S_producto aux3 =productos[i].getDatos()
                        archivo1.write(reinterpret_cast<const char*>(&aux1),size_t(S_producto)); 
                    }}

                    archivo1.close();
                    archivo2.close();
                    archivo3.close();
    }

    void gestora:: leerArchivo(const char* DieraccionArchivo){
        ofstream archivo(DieraccionArchivo);
        string linea;
        producto *productoActual=nullptr;
        comentario *comentarioActual=nullptr;

        if(archivo.is_open()){

            while(getline(archivo,linea)){
                linea.erase(0,linea.find_first_not_of("\t\r\n")); //no lee los espacios en blanco de cada renglon
                if (linea.empty()) continue;

                if(linea.substr(0,2)=="--"){// extraemos el subComentario
                    size_t pos = linea.find(':');//busca la posicion del primer caracter ":" y la almacena en pos
                    if(pos != std :: string:: npos && comentarioActual){ //cuando la funcion find no encuentra nada devuelve "npos"
                        string texto = linea.substr(2,pos-2);
                        int puntuacion = stoi(linea.substr(pos+1));
                        subComentario c(texto,puntuacion);
                        comentarioActual->agregarRespuesta(c);
                    }
                } else if(linea[0]=='-'){// extraemos el comentario
                    size_t pos = linea.find(':');
                    if(pos != std :: string :: npos && productoActual){
                        string texto = linea.substr(1,pos-1);
                        int puntuacion = stoi(linea.substr(pos+1));
                        comentario c(texto,puntuacion);
                        productoActual->agregarComentario(c);
                        comentarioActual = &productoActual->VecComentarios().back();//referencia al elemento que acabo de agrgar para poder agregar subcomentarios mas adelante
                    }
                } else {
                    producto p(linea);
                    agrgarProducto(p);
                    productoActual =&productos.back();//referencia al ultimo elemento del vector.
                    comentarioActual=nullptr;
                    }
                }

            }
            archivo.close();
        } 
    }
};
