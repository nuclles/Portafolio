#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <stack>
#include <queue>

//1. Diseño de la solución e implementación de clases
/*Respuesta sobre polimorfismo:
En este diseño no es necesario usar polimorfismo ya que todos los empleados son del mismo tipo y no hay comportamientos diferentes según el tipo de empleado.
 La ventaja de usar polimorfismo sería si tuviéramos diferentes tipos de empleados con comportamientos específicos.
 La desventaja sería la complejidad adicional cuando no es necesaria.*/

class Empleado {
private:
    int numero;
    std::string nombre;
    std::vector<Empleado*> subordinados;

public:
    Empleado(int num, const std::string& nom) : numero(num), nombre(nom) {}

    void agregarSubordinado(Empleado* subordinado) {
        subordinados.push_back(subordinado);
    }

    int getNumero() const { return numero; }
    const std::string& getNombre() const { return nombre; }
    const std::vector<Empleado*>& getSubordinados() const { return subordinados; }
    int getCantidadSubordinados() const { return subordinados.size(); }

    // Para liberar memoria
    ~Empleado() {
        for (auto sub : subordinados) {
            delete sub;
        }
    }
};

class SistemaRRHH {
private:
    Empleado* raiz;
    std::map<int, Empleado*> empleadosMap;

    void limpiar() {
        if (raiz) {
            delete raiz;
            raiz = nullptr;
        }
        empleadosMap.clear();
    }

public:
    SistemaRRHH() : raiz(nullptr) {}
    ~SistemaRRHH() { limpiar(); }

    // Métodos que implementaremos más adelante
    void leerArchivoTexto(const std::string& nombreArchivo);
    Empleado* obtenerResponsable(int numEmpleado) const;
    void guardarArchivoBinario(const std::string& nombreArchivo) const;
    Empleado* obtenerEmpleadoMasSubordinados() const;
    std::vector<int> obtenerEmpleadosConNumeroRepetido() const;
};


//2. Procedimiento para leer el archivo de texto
void SistemaRRHH::leerArchivoTexto(const std::string& nombreArchivo) {
    limpiar();
    std::ifstream archivo(nombreArchivo);
    if (!archivo.is_open()) {
        throw std::runtime_error("No se pudo abrir el archivo");
    }

    std::stack<Empleado*> pilaJerarquia;
    std::string linea;

    while (std::getline(archivo, linea)) {
        if (linea.empty()) continue;

        // Contar guiones para determinar nivel de jerarquía
        size_t pos = linea.find_first_not_of('-');
        int nivel = pos;
        int num = std::stoi(linea.substr(pos, linea.find('-', pos) - pos));
        std::string nombre = linea.substr(linea.find('-', pos) + 1);

        Empleado* nuevoEmp = new Empleado(num, nombre);
        empleadosMap[num] = nuevoEmp;

        if (nivel == 0) {
            raiz = nuevoEmp;
            pilaJerarquia.push(nuevoEmp);
        } else {
            // Retroceder en la pila hasta encontrar el nivel superior
            while (pilaJerarquia.size() > nivel) {
                pilaJerarquia.pop();
            }
            pilaJerarquia.top()->agregarSubordinado(nuevoEmp);
            pilaJerarquia.push(nuevoEmp);
        }
    }
    archivo.close();
}


//3. Método para obtener el responsable de un empleado
Empleado* SistemaRRHH::obtenerResponsable(int numEmpleado) const {
    if (!raiz || empleadosMap.find(numEmpleado) == empleadosMap.end()) {
        return nullptr;
    }

    // Usamos BFS para buscar al responsable
    std::queue<Empleado*> cola;
    cola.push(raiz);

    while (!cola.empty()) {
        Empleado* actual = cola.front();
        cola.pop();

        for (Empleado* sub : actual->getSubordinados()) {
            if (sub->getNumero() == numEmpleado) {
                return actual;
            }
            cola.push(sub);
        }
    }

    return nullptr; // No tiene responsable (es la raíz)
}

//4. Método para guardar en archivo binario
void SistemaRRHH::guardarArchivoBinario(const std::string& nombreArchivo) const {
    std::ofstream archivo(nombreArchivo, std::ios::binary);
    if (!archivo.is_open()) {
        throw std::runtime_error("No se pudo crear el archivo binario");
    }

    for (const auto& par : empleadosMap) {
        Empleado* emp = par.second;
        // Escribir número de empleado
        archivo.write(reinterpret_cast<const char*>(&emp->getNumero()), sizeof(int));
        // Escribir nombre (primero la longitud)
        size_t nombreLen = emp->getNombre().size();
        archivo.write(reinterpret_cast<const char*>(&nombreLen), sizeof(size_t));
        archivo.write(emp->getNombre().c_str(), nombreLen);
        // Escribir cantidad de subordinados
        int cantSub = emp->getCantidadSubordinados();
        archivo.write(reinterpret_cast<const char*>(&cantSub), sizeof(int));
    }

    archivo.close();
}

//5. Métodos adicionales
//a. Obtener el empleado con más subordinados
Empleado* SistemaRRHH::obtenerEmpleadoMasSubordinados() const {
    if (empleadosMap.empty()) return nullptr;

    Empleado* maxEmp = nullptr;
    int maxSub = -1;

    for (const auto& par : empleadosMap) {
        Empleado* emp = par.second;
        int cantSub = emp->getCantidadSubordinados();
        if (cantSub > maxSub) {
            maxSub = cantSub;
            maxEmp = emp;
        }
    }

    return maxEmp;
}

//b. Obtener empleados con número repetido
std::vector<int> SistemaRRHH::obtenerEmpleadosConNumeroRepetido() const {
    std::map<int, int> conteoNumeros;
    std::vector<int> repetidos;

    // Contar ocurrencias de cada número
    for (const auto& par : empleadosMap) {
        conteoNumeros[par.first]++;
    }

    // Encontrar los que tienen más de una ocurrencia
    for (const auto& par : conteoNumeros) {
        if (par.second > 1) {
            repetidos.push_back(par.first);
        }
    }

    return repetidos;
}

//Programa principal de ejemplo
int main() {
    SistemaRRHH sistema;

    try {
        // 2. Leer archivo de texto
        sistema.leerArchivoTexto("jerarquia.txt");

        // 3. Obtener responsable
        int numBuscar = 78;
        Empleado* responsable = sistema.obtenerResponsable(numBuscar);
        if (responsable) {
            std::cout << "El responsable del empleado " << numBuscar 
                      << " es: " << responsable->getNombre() << std::endl;
        } else {
            std::cout << "El empleado " << numBuscar 
                      << " no tiene responsable o no existe." << std::endl;
        }

        // 4. Guardar archivo binario
        sistema.guardarArchivoBinario("empleados.dat");

        // 5a. Empleado con más subordinados
        Empleado* empMasSub = sistema.obtenerEmpleadoMasSubordinados();
        if (empMasSub) {
            std::cout << "El empleado con más subordinados es: " 
                      << empMasSub->getNombre() 
                      << " con " << empMasSub->getCantidadSubordinados() 
                      << " subordinados." << std::endl;
        }

        // 5b. Números de empleado repetidos
        std::vector<int> repetidos = sistema.obtenerEmpleadosConNumeroRepetido();
        if (!repetidos.empty()) {
            std::cout << "Números de empleado repetidos: ";
            for (int num : repetidos) {
                std::cout << num << " ";
            }
            std::cout << std::endl;
        } else {
            std::cout << "No hay números de empleado repetidos." << std::endl;
        }

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}