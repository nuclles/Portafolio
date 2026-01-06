#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <algorithm>
using namespace std;


struct informacion
{
    private:
    int dni;
    char nombre[200];
    char apellido[200];
    char nacionalidad[200];
};



class persona{
    private:
    informacion datos;
    vector<persona>padres;
    vector<persona>Antepasados;
    

    public:
    // Constructor
    persona(informacion d) {
       this->datos =d;
    }
    void agregarAntepasado(persona P);{
        Antepasado.push_back(p);
    }

    // Método para mostrar información
    void mostrar(){
        cout << "DNI: " << getDNI() << endl;
        cout << "Nombre: " << getNombre() << endl;
        cout << "Apellido: " << getApellido() << endl;
        cout << "Nacionalidad: " << getNacionalidad() << endl;
    }

     void cargarPadres(){
        int i=0;


          informacion P;
          informacion M;

          //padre

        cout <<"DNI"<<endl;
        cin >> P.dni;
         cin.get();
        cout<<"nombre"
        cin.getline(P.nombre);
         cin.get();
        cout<<"apellido"
        cin.getline(P.apellido);
         cin.get();
        cout<<"nacionalidad"
        cin.getline(P.nacionalidad);
        
        //madre

          cout <<"DNI"<<endl;
        cin >> M.dni;
         cin.get();
        cout<<"nombre"
        cin.getline(M.nombre);
         cin.get();
        cout<<"apellido"
        cin.getline(M.apellido);
         cin.get();
        cout<<"nacionalidad"
        cin.getline(M.nacionalidad);

        if(P.nacionalidad == "iatliano" && M.nacionalidad == "italiano"){

            persona padre(P);
            persona madre(M);

        padres.push_back(padre);
        padres.push_back (madre);

        padres[i].cargarPadres();
        padres[i+1].cargarPadres();

        //para stl. asi puedo contar los antepasados;
        agregarAntepasado(padre);
        agregarAntepasado(madre);

        i++;
        } else exit-1;
      }
};

class gestora(){
    public:

    void agrgarPersona(){
        informacion aux;

        cout <<"DNI"<<endl;
        cin >> aux.dni;
         cin.get();
        cout<<"nombre"
        cin.getline(aux.nombre);
         cin.get();
        cout<<"apellido"
        cin.getline(aux.apellido);
         cin.get();
        cout<<"nacionalidad"
        cin.getline(aux.nacionalidad);

        persona p(aux);
        p.cargarPadres();
    }

    //guardar en un archiv TXT
    void guardarEnTexto(persona p, ofstream &archivo) {
        // Guardar datos de la persona
        archivo << "DNI: " << p.getDNI() << endl;
        archivo << "Nombre: " << p.getNombre() << endl;
        archivo << "Apellido: " << p.getApellido() << endl;
        archivo << "Nacionalidad: " << p.getNacionalidad() << endl;
        archivo << "------------------------" << endl;

        // Guardar recursivamente los padres
        for (auto &padre : p.getPadres()) {
            guardarEnTexto(padre, archivo);
        } 
    }



    //funcion para verificar si damos la nacionalidad.
    bool VerificarSiOtorgamosNacionalidad(persona P){
        if(P.getNacionalidad == "italiano"){
            return true;
        }else if(P.getPadre().getNacionalidad == "italiano" || P.getMadre().getNacionalidad() == "italiano"){
            return true;
        }else {
            VerificarSiOtorgamosNacionalidad(P.getPadre());
             VerificarSiOtorgamosNacionalidad(P.getMadre());
        }

        return false;
    }

    //tiene antepasado con nombre igual.
    bool tieneAntepasadoConMismoNombre(persona &P) {
        string nombreActual = P.getNombre();
        for (auto &antepasado : P.getAntepasados()) {
            if (antepasado.getNombre() == nombreActual) {
                return true;
            }
            if (tieneAntepasadoConMismoNombre(antepasado)) {
                return true;
            }
        }
        return false;
    }

    //guardamos en el archivo de forma recursiva.

    void guardarEnBinario(persona p,const char *Dir){
        informacion aux = P.getDato();
        informacion aux2= p.getPadre().getDato();
        informacion aux3= p.getMadre().getDato();

        ofstream archivo(Dir,ios::binary)
        if(archivo.fail()){
            exit -1;
        }
        archivo.write(reinterpret_cast <char*>(&aux),sizaof(informacion));//persona
        archivo.write(reinterpret_cast <char*>(&aux2),sizaof(informacion));//padre
        archivo.write(reinterpret_cast <char*>(&aux3),sizaof(informacion));//madre

        archivo.close();

        guerdarEnBinario(p.getPadre,const char* Dir);//paddres del padre
        guerdarEnBinario(p.getMadre,const char* Dir);// padres de la Madre
    }

    //3. funcion para contar antepasados.
    int contarAntepasados(persona P){
        int i=0;
        for_each(auto &P:P.getAntepasados()){
            i++;
        }
        return i;
    }

};

//4.
//TEROIA
/*
1) En los lenguajes de de tipado estatico son importatens las clases template porque nos perminte programar de forma generica. Nos permite escribir código independiente del tipo de datos.
 Permiten crear funciones y clases que funcionan con cualquier tipo de dato.*/

 /*
 2) En C++, los punteros son necesarios para implementar el polimorfismo debido a cómo el lenguaje maneja la memoria y las funciones en tiempo de ejecución*/
