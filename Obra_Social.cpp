#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <fstream>
#include <algorithm>
#include <map>

using namespace std;

struct DatosCliente {
    int id;
    char nombre[200];
    char tipo;// b Basico, m Medio, p Premiun
    int cantidad; // cantidad de veces que utilizo el servicio
};

class cliente {
    private:
    int id;
    string nombre;
    char tipo;
    int cantidad;

    public:
    cliente(DatosCliente datos) {
        this->id = datos.id;
        this->nombre = datos.nombre;
        this->tipo = datos.tipo;
        this->cantidad = datos.cantidad;
    }
    int get_id(){
        return this->id;
    }
    char get_tipo(){
        return this->tipo;
    }
    string get_nombre(){
        return this->nombre;
    }
    int get_cant(){
        return this->cantidad;
    }

};

class ObraSocial {
    private:
    vector<cliente> clientes;

    public:
    void leer_archivoBinario(const char* direccion){
        ifstream archivo(direccion, ios::binary);
        if(archivo.is_open()){
            while(!archivo.eof()){
                DatosCliente datos;
                archivo.read(reinterpret_cast<char*>(&datos),sizeof(DatosCliente));

                cliente nuevoCliente(datos);
                clientes.push_back(nuevoCliente);
            }
        }else{
            cout << "Error al abrir el archivo" <<endl;
        }
    }

    bool BuscarPrestacion_archivoTexto(const char* direccion,string prestacion){
        ifstream archivoPlan(direccion);
        if(archivoPlan.is_open()){
            string linea;
            while(getline(archivoPlan,linea)){
                if(linea ==prestacion){
                    archivoPlan.close();
                    return true;
                }
            }
        }
    }
    }
    
    bool verificarPrestacion(int id_Usuario,string prestacionB){
        auto it =find_if(clientes.begin(),clientes.end(),[id_Usuario](cliente &client){return id_Usuario==client.get_id();});

        if(it==clientes.end|()){
            return false;
        }

        string basica="basica.txt";
        string media="media.txt";
        string premiun="premiun.txt";
        char tipo=it.get_tipo();

        switch (tipo){
            case 'b':
            return BuscarPrestacion_archivoTexto(basica, prestacionB);
            break;
            case 'm':
            return BuscarPrestacion_archivoTexto(media, prestacionB);
            break;
            case 'p':
            return BuscarPrestacion_archivoTexto(premiun, prestacionB);
            break;
        
            default:
            return false;
            break;
        }
    }

    void usuarios_que_mas_usaron_el_servicio(){
        sort(clientes.begin(),clientes.end(),[](cliente &a,cliente &b){return a.get_cant()>b.get_cant();});

        for(int i =0; i<5;i++){
            cout<<clientes[i].get_nombre()<<" "<<clientes[i].get_cant()<<endl;
        }
    }

    void prestaciones(){
        vector <string>Prestaciones;
        ofstream archivoB("basico.txt");
        ofstream archivoM("medio.txt");
        ofstream archivoP("premiun.txt");

        if(archivoB.fail()||archivoM.fail()||archivoP.fail()){
            exit -1;
        }

        string linea;
       
        
        while(getline(archivoB,linea){
            Prestaciones.push_back(linea);
        }
        
        while(getline(archivoM,linea){
            Prestaciones.push_back(linea);
        }
        
        while(getline(archivoP,linea){
            Prestaciones.push_back(linea);
        }

        cout<<"listado de todas las prestaciones"<<endl;

        for(int i=0; i<Prestaciones.size();i++){
            cout<<Prestaciones[i]<<endl;
        }
    }

    void Cantidad_de_veces_que_se_utilizo_el_servicio(){
        map<char,int>Uso_Servicio;
        for (const auto& cliente : clientes){
            Uso_Servicio[cliente.get_tipo()]+=cliente.get_cant();
        }

        //mostrar resultados
        for(const auto& UsoServ:Uso_Servicio){
            cout<<"tipo"<<UsoServ.first<<" "<<"cantidad"<<UsoServ.second<<endl;
        }
    }

      //Mapa como contador
    void Prestaciones_repetidas(){
    
    map<string,int>contador;
    for(const auto& Pres: Prestaciones){
    contador[Pres]++}

    for(const auto& cont:contador){
        if(cont.second>1){
            cout<<"Prestacion"<<cont.first<<endl;
        }
    }
}
    
    //Esto recorre el vector de clientes y va aumentado el contador del mapa (contador.second)
    
};     

