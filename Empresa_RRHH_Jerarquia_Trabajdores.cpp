//1. Diseño

#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <stack>
#include <algorithm>
#include <climits>

using namespace std;

class Empleado {
private:
    int numeroEmpleado;
    string nombre;
    int numeroResponsable;  // Ahora guardamos solo el número del jefe
    vector<int> subordinados;  // Números de empleados a cargo

public:
    Empleado(int num, const string& nom, int resp = -1) 
        : numeroEmpleado(num), nombre(nom), numeroResponsable(resp) {}

    // Getters
    int getNumero() const { return numeroEmpleado; }
    string getNombre() const { return nombre; }
    int getResponsable() const { return numeroResponsable; }
    const vector<int>& getSubordinados() const { return subordinados; }

    // Setters
    void setResponsable(int resp) { numeroResponsable = resp; }

    void agregarSubordinado(int numEmp) {
        subordinados.push_back(numEmp);
    }

    int cantidadSubordinados() const {
        return subordinados.size();
    }
};

class GestorJerarquia {
private:
    vector<Empleado> empleados;
    vector<Empleado> jefes;  // Empleados con subordinados

    // Mapa para búsqueda rápida (número -> índice en vector empleados)
    map<int, size_t> indiceEmpleados;

    // Helpers
    int obtenerNivel(const string& linea);
    tuple<int, string, int> parsearLinea(const string& linea, int nivel);

public:
    void leerArchivo(const string& ruta);
    Empleado* obtenerResponsable(int numEmpleado);
    void guardarEnBinario(const string& ruta) const;
    Empleado* empleadoMasSubordinados() const;
    vector<int> empleadosConNumeroRepetido() const;
};

//1. Helpers para Procesar Archivo  
int GestorJerarquia::obtenerNivel(const string& linea) {
    int nivel = 0;
    while (nivel < linea.size() && linea[nivel] == '-') {
        nivel++;
    }
    return nivel;
}

tuple<int, string, int> GestorJerarquia::parsearLinea(const string& linea, int nivel) {
    string contenido = linea.substr(nivel);
    size_t guion = contenido.find('-');
    int numero = stoi(contenido.substr(0, guion));
    string nombre = contenido.substr(guion + 1);
    return make_tuple(numero, nombre, nivel);
}

//2. Leer Archivo y Construir Estructura
void GestorJerarquia::leerArchivo(const string& ruta) {
    ifstream archivo(ruta);
    if (!archivo.is_open()) {
        cerr << "Error al abrir el archivo: " << ruta << endl;
        return;
    }

    string linea;
    stack<int> pilaResponsables;  // Guarda números de empleado

    while (getline(archivo, linea)) {
        if (linea.empty()) continue;

        int nivel = obtenerNivel(linea);
        auto [num, nombre, niv] = parsearLinea(linea, nivel);
        
        // Determinar responsable
        int responsable = -1;  // -1 indica que no tiene responsable
        if (nivel > 0) {
            while (pilaResponsables.size() > nivel) {
                pilaResponsables.pop();
            }
            if (!pilaResponsables.empty()) {
                responsable = pilaResponsables.top();
            }
        }

        // Crear empleado
        Empleado nuevo(num, nombre, responsable);
        size_t indice = empleados.size();
        empleados.push_back(nuevo);
        indiceEmpleados[num] = indice;

        // Si tiene responsable, actualizar su lista de subordinados
        if (responsable != -1) {
            auto it = indiceEmpleados.find(responsable);
            if (it != indiceEmpleados.end()) {
                empleados[it->second].agregarSubordinado(num);
                
                // Si es el primer subordinado, añadir a jefes
                if (empleados[it->second].cantidadSubordinados() == 1) {
                    jefes.push_back(empleados[it->second]);
                }
            }
        }

        // Actualizar pila
        if (pilaResponsables.size() <= nivel) {
            pilaResponsables.push(num);
        } else {
            pilaResponsables.top() = num;
        }
    }
    archivo.close();
}

//3. Obtener Responsable

Empleado* GestorJerarquia::obtenerResponsable(int numEmpleado) {
    auto it = indiceEmpleados.find(numEmpleado);
    if (it == indiceEmpleados.end()) return nullptr;

    int numResponsable = empleados[it->second].getResponsable();
    if (numResponsable == -1) return nullptr;

    auto itResp = indiceEmpleados.find(numResponsable);
    if (itResp == indiceEmpleados.end()) return nullptr;

    return &empleados[itResp->second];
}

//4. Guardar en Archivo Binario

void GestorJerarquia::guardarEnBinario(const string& ruta) const {
    ofstream archivo(ruta, ios::binary);
    if (!archivo.is_open()) {
        cerr << "Error al crear archivo binario" << endl;
        return;
    }

    for (const auto& emp : empleados) {
        int num = emp.getNumero();
        int cantSub = emp.cantidadSubordinados();
        size_t nombreLen = emp.getNombre().size();
        int responsable = emp.getResponsable();

        archivo.write(reinterpret_cast<const char*>(&num), sizeof(num));
        archivo.write(reinterpret_cast<const char*>(&responsable), sizeof(responsable));
        archivo.write(reinterpret_cast<const char*>(&nombreLen), sizeof(nombreLen));
        archivo.write(emp.getNombre().c_str(), nombreLen);
        archivo.write(reinterpret_cast<const char*>(&cantSub), sizeof(cantSub));
        
        // Guardar subordinados si los tiene
        if (cantSub > 0) {
            const auto& subs = emp.getSubordinados();
            archivo.write(reinterpret_cast<const char*>(subs.data()), cantSub * sizeof(int));
        }
    }
    archivo.close();
}

//5. Métodos Adicionales

Empleado* GestorJerarquia::empleadoMasSubordinados() const {
    if (jefes.empty()) return nullptr;

    const Empleado* maxEmp = &jefes[0];
    for (const auto& jefe : jefes) {
        if (jefe.cantidadSubordinados() > maxEmp->cantidadSubordinados()) {
            maxEmp = &jefe;
        }
    }
    return const_cast<Empleado*>(maxEmp);
}

vector<int> GestorJerarquia::empleadosConNumeroRepetido() const {
    map<int, int> contadorNumeros;
    vector<int> repetidos;

    for (const auto& emp : empleados) {
        contadorNumeros[emp.getNumero()]++;
    }

    for (const auto& [num, count] : contadorNumeros) {
        if (count > 1) {
            repetidos.push_back(num);
        }
    }
    return repetidos;
}