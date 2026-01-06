#include <iostream>
#include <vector>
#include <string>

using namespace std;

//---------------------------------//
//Estructuras para leer los archivos
struct S_paquetes{
    char codigo[100];
    char nombre [100];
    int version;
};

struct S_dependencias{
char codigoPaquete[100];
char PaqueteDependencia[100];
};

class dependencia{
    private:
    string codPack;
    string codPackDepen;

    public:
    dependencia(S_dependencias);
};

class paquete{
    private:
    string cod;
    string nombre;
    int version;
    vector<paquete>Vec_Dependencias;

    public:
    paquete(S_paquetes aux){
        strcpy(this->cod, aux.codigo);
        strcpy(this->nombre, aux.nombre);
        this->version = aux.version;
    }
    void AgregarDependencia(dependencia dep){
        Vec_Dependencias.push_back(dep);
    }
    string gettnombre(){
        return nombre;
    }
    int getVersion(){
        return version;
    }
    vector<paquete>getVectorDependencias(){
        return Vec_Dependencias;
    }

};

class gestor{
    private:
    vector<paquete>Vec_paquetes;
    vector<dependencia>Vec_dependencias;

    public:

// Función recursiva para mostrar dependencias de un paquete
void MostrarDependenciasRecursivo(const paquete& pack, int nivel = 0) {
    // Imprime el nombre del paquete con indentación según el nivel
    for (int i = 0; i < nivel; ++i) std::cout << "  ";
    cout << pack.nombre << " (v" << pack.version << ")" << std::endl;

    // Recorre las dependencias del paquete y llama recursivamente
    vector<paquete> dependencias = pack.getVectorDependencias();
    for (const auto& dep : dependencias) {
        MostrarDependenciasRecursivo(dep, nivel + 1);
    }
}

// Función para recorrer todos los paquetes y mostrar sus dependencias
void MostrarTodasLasDependencias() {
    for (const auto& pack : Vec_paquetes) {
        MostrarDependenciasRecursivo(pack);
    }
}



};

void MostrarDependenciasPorCodigo(const string& codigo) {
    for (const auto& pack : Vec_paquetes) {
        if (pack.cod == codigo) {
            MostrarDependenciasRecursivo(pack);
            return;
        }
    }
    cout << "Paquete no encontrado." << endl;
}