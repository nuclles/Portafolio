#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <fstream>
#include <limits>

using namespace std;

// Constantes para los tipos de viaje
const int AVION = 1;
const int COLECTIVO = 2;
const int AVION_COLECTIVO = 3;

string tipoToString(int tipo) {
    switch(tipo) {
        case AVION: return "Avión";
        case COLECTIVO: return "Colectivo";
        case AVION_COLECTIVO: return "Avión y Colectivo";
        default: return "Desconocido";
    }
}

class Viaje {
protected:
    string nombre;
    int tipo;
    double precio;
    double horasViaje;

public:
    Viaje(const string& nombre, int tipo) : nombre(nombre), tipo(tipo), precio(0), horasViaje(0) {}
    virtual ~Viaje() {}

    virtual void calcularPrecio() = 0;
    virtual void calcularHorasViaje() = 0;

    string getNombre() const { return nombre; }
    int getTipo() const { return tipo; }
    double getPrecio() const { return precio; }
    double getHorasViaje() const { return horasViaje; }

    virtual void guardar(ofstream& archivo) const {
        archivo << nombre << "|" << tipo << "|" << precio << "|" << horasViaje;
    }
};

class ViajeAvion : public Viaje {
private:
    double costoAerolinea;
    double horasVuelo;

public:
    ViajeAvion(const string& nombre, double costoAerolinea, double horasVuelo)
        : Viaje(nombre, AVION), costoAerolinea(costoAerolinea), horasVuelo(horasVuelo) {
        calcularPrecio();
        calcularHorasViaje();
    }

    void calcularPrecio() override {
        precio = costoAerolinea * 1.20;
    }

    void calcularHorasViaje() override {
        horasViaje = horasVuelo + 2;
    }

    void guardar(ofstream& archivo) const override {
        archivo << "A|";
        Viaje::guardar(archivo);
        archivo << "|" << costoAerolinea << "|" << horasVuelo << "\n";
    }
};

class ViajeColectivo : public Viaje {
private:
    double kilometros;
    double horasIngresadas;

public:
    ViajeColectivo(const string& nombre, double kilometros, double horasIngresadas)
        : Viaje(nombre, COLECTIVO), kilometros(kilometros), horasIngresadas(horasIngresadas) {
        calcularPrecio();
        calcularHorasViaje();
    }

    void calcularPrecio() override {
        precio = kilometros * 8;
    }

    void calcularHorasViaje() override {
        horasViaje = horasIngresadas;
    }

    void guardar(ofstream& archivo) const override {
        archivo << "C|";
        Viaje::guardar(archivo);
        archivo << "|" << kilometros << "|" << horasIngresadas << "\n";
    }
};

class ViajeAvionColectivo : public Viaje {
private:
    double costoAerolinea;
    double horasVuelo;
    double kilometros;
    double horasColectivo;

public:
    ViajeAvionColectivo(const string& nombre, double costoAerolinea, double horasVuelo, double kilometros, double horasColectivo)
        : Viaje(nombre, AVION_COLECTIVO), costoAerolinea(costoAerolinea), horasVuelo(horasVuelo),
          kilometros(kilometros), horasColectivo(horasColectivo) {
        calcularPrecio();
        calcularHorasViaje();
    }

    void calcularPrecio() override {
        precio = (costoAerolinea * 1.20) + (kilometros * 8);
    }

    void calcularHorasViaje() override {
        horasViaje = horasVuelo + 2 + horasColectivo;
    }

    void guardar(ofstream& archivo) const override {
        archivo << "AC|";
        Viaje::guardar(archivo);
        archivo << "|" << costoAerolinea << "|" << horasVuelo << "|" << kilometros << "|" << horasColectivo << "\n";
    }
};

vector<Viaje*> cargarViajes() {
    vector<Viaje*> viajes;
    int opcion;
    string nombre;
    double costo, horas, km;

    cout << "Carga de viajes (0 para terminar):\n";
    while(true) {
        cout << "Tipo de viaje (1-Avion, 2-Colectivo, 3-Avion+Colectivo, 0-Terminar): ";
        cin >> opcion;
        if(opcion == 0) break;

        cout << "Nombre del viaje: ";
        cin.ignore();
        getline(cin, nombre);

        try {
            switch(opcion) {
                case AVION: {
                    cout << "Costo aerolínea: ";
                    cin >> costo;
                    cout << "Horas de vuelo: ";
                    cin >> horas;
                    viajes.push_back(new ViajeAvion(nombre, costo, horas));
                    break;
                }
                case COLECTIVO: {
                    cout << "Kilómetros: ";
                    cin >> km;
                    cout << "Horas de viaje: ";
                    cin >> horas;
                    viajes.push_back(new ViajeColectivo(nombre, km, horas));
                    break;
                }
                case AVION_COLECTIVO: {
                    cout << "Costo aerolínea: ";
                    cin >> costo;
                    cout << "Horas de vuelo: ";
                    cin >> horas;
                    cout << "Kilómetros en colectivo: ";
                    cin >> km;
                    double horasColectivo;
                    cout << "Horas en colectivo: ";
                    cin >> horasColectivo;
                    viajes.push_back(new ViajeAvionColectivo(nombre, costo, horas, km, horasColectivo));
                    break;
                }
                default:
                    cout << "Opción no válida.\n";
            }
        } catch(...) {
            cout << "Error en los datos ingresados. Intente nuevamente.\n";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }
    }

    return viajes;
}

void guardarViajes(const vector<Viaje*>& viajes, const string& archivoNombre) {
    ofstream archivo(archivoNombre);
    if(!archivo) {
        cerr << "Error al abrir el archivo para escritura.\n";
        return;
    }

    for(const auto& viaje : viajes) {
        viaje->guardar(archivo);
    }

    cout << "Viajes guardados correctamente en " << archivoNombre << endl;
}

void mostrarViajesMasBaratos(const vector<Viaje*>& viajes) {
    if(viajes.empty()) {
        cout << "No hay viajes para mostrar.\n";
        return;
    }

    vector<Viaje*> copiaViajes = viajes;
    sort(copiaViajes.begin(), copiaViajes.end(), [](Viaje* a, Viaje* b) {
        return a->getPrecio() < b->getPrecio();
    });

    cout << "\n--- 5 viajes más baratos ---\n";
    int limite = min(5, static_cast<int>(copiaViajes.size()));
    for(int i = 0; i < limite; ++i) {
        cout << i+1 << ". " << copiaViajes[i]->getNombre() 
             << " (" << tipoToString(copiaViajes[i]->getTipo()) 
             << ") - Precio: $" << copiaViajes[i]->getPrecio() 
             << " - Horas: " << copiaViajes[i]->getHorasViaje() << endl;
    }
}

void mostrarViajeMasLargo(const vector<Viaje*>& viajes) {
    if(viajes.empty()) {
        cout << "No hay viajes para mostrar.\n";
        return;
    }

    auto maxElement = max_element(viajes.begin(), viajes.end(), [](Viaje* a, Viaje* b) {
        return a->getHorasViaje() < b->getHorasViaje();
    });

    cout << "\n--- Viaje más largo ---\n";
    cout << "Nombre: " << (*maxElement)->getNombre() 
         << " (" << tipoToString((*maxElement)->getTipo()) 
         << ") - Horas: " << (*maxElement)->getHorasViaje() 
         << " - Precio: $" << (*maxElement)->getPrecio() << endl;
}

void mostrarViajesPorTiempo(const vector<Viaje*>& viajes, double horasMaximas) {
    vector<Viaje*> viajesFiltrados;
    copy_if(viajes.begin(), viajes.end(), back_inserter(viajesFiltrados), [horasMaximas](Viaje* v) {
        return v->getHorasViaje() <= horasMaximas;
    });

    if(viajesFiltrados.empty()) {
        cout << "No hay viajes que se puedan realizar en " << horasMaximas << " horas o menos.\n";
        return;
    }

    cout << "\n--- Viajes que se pueden realizar en " << horasMaximas << " horas o menos ---\n";
    for(size_t i = 0; i < viajesFiltrados.size(); ++i) {
        cout << i+1 << ". " << viajesFiltrados[i]->getNombre() 
             << " (" << tipoToString(viajesFiltrados[i]->getTipo()) 
             << ") - Horas: " << viajesFiltrados[i]->getHorasViaje() 
             << " - Precio: $" << viajesFiltrados[i]->getPrecio() << endl;
    }
}

void liberarViajes(vector<Viaje*>& viajes) {
    for(auto viaje : viajes) {
        delete viaje;
    }
    viajes.clear();
}

int main() {
    vector<Viaje*> viajes;
    int opcion;
    double horas;

    do {
        cout << "\nMENU PRINCIPAL\n";
        cout << "1. Cargar viajes\n";
        cout << "2. Guardar viajes\n";
        cout << "3. Mostrar 5 viajes más baratos\n";
        cout << "4. Mostrar viaje más largo\n";
        cout << "5. Buscar viajes por tiempo máximo\n";
        cout << "0. Salir\n";
        cout << "Opción: ";
        cin >> opcion;

        switch(opcion) {
            case 1:
                liberarViajes(viajes);
                viajes = cargarViajes();
                break;
            case 2:
                guardarViajes(viajes, "viajes.txt");
                break;
            case 3:
                mostrarViajesMasBaratos(viajes);
                break;
            case 4:
                mostrarViajeMasLargo(viajes);
                break;
            case 5:
                cout << "Ingrese el tiempo máximo en horas: ";
                cin >> horas;
                mostrarViajesPorTiempo(viajes, horas);
                break;
            case 0:
                cout << "Saliendo...\n";
                break;
            default:
                cout << "Opción no válida.\n";
        }
    } while(opcion != 0);

    liberarViajes(viajes);
    return 0;
}

//-------------------------------------------------------------------------------------//


1. Estructura Básica
cpp
template <typename K, typename V>
class Diccionario {
private:
    struct Nodo {
        K clave;
        V valor;
        Nodo* siguiente;
        
        Nodo(const K& k, const V& v) : clave(k), valor(v), siguiente(nullptr) {}
    };
    
    Nodo* primero;
    int cantidad;
Template: La clase es genérica (template <typename K, typename V>) permitiendo cualquier tipo de clave y valor.

Nodo: Cada elemento se almacena en un nodo que contiene:

clave: Identificador único

valor: Dato asociado

siguiente: Puntero al siguiente nodo (lista enlazada)

Estructura: Lista enlazada simple con:

primero: Puntero al primer nodo

cantidad: Contador de elementos

2. Gestión de Memoria
cpp
public:
    Diccionario() : primero(nullptr), cantidad(0) {}
    ~Diccionario() {
        limpiar();
    }
    
    void limpiar() {
        while (primero != nullptr) {
            Nodo* aEliminar = primero;
            primero = primero->siguiente;
            delete aEliminar;
        }
        cantidad = 0;
    }
Constructor: Inicializa la lista vacía

Destructor: Llama a limpiar() para liberar toda la memoria

Limpiar: Recorre toda la lista eliminando nodos uno por uno

3. Operaciones Principales
Agregar Elementos
cpp
bool agregar(const K& clave, const V& valor) {
    if (existe(clave)) {
        return false; // Evita duplicados
    }
    
    Nodo* nuevo = new Nodo(clave, valor);
    nuevo->siguiente = primero; // Insertar al inicio
    primero = nuevo;
    cantidad++;
    return true;
}
Verifica que la clave no exista

Crea un nuevo nodo

Inserta al inicio de la lista (operación O(1))

Incrementa el contador

Obtener Elementos
cpp
// Versión con excepción
V& obtener(const K& clave) {
    Nodo* actual = primero;
    while (actual != nullptr) {
        if (actual->clave == clave) {
            return actual->valor;
        }
        actual = actual->siguiente;
    }
    throw runtime_error("Clave no encontrada");
}

// Versión segura
bool obtener(const K& clave, V& valor) {
    Nodo* actual = primero;
    while (actual != nullptr) {
        if (actual->clave == clave) {
            valor = actual->valor;
            return true;
        }
        actual = actual->siguiente;
    }
    return false;
}
Dos versiones para diferentes casos de uso:

Lanza excepción si no encuentra la clave

Versión segura que retorna un booleano

Búsqueda lineal O(n) (recorre la lista)

Eliminar Elementos
cpp
bool eliminar(const K& clave) {
    if (primero == nullptr) return false;
    
    // Caso especial: eliminar el primero
    if (primero->clave == clave) {
        Nodo* aEliminar = primero;
        primero = primero->siguiente;
        delete aEliminar;
        cantidad--;
        return true;
    }
    
    // Buscar el nodo a eliminar
    Nodo* anterior = primero;
    Nodo* actual = primero->siguiente;
    
    while (actual != nullptr) {
        if (actual->clave == clave) {
            anterior->siguiente = actual->siguiente;
            delete actual;
            cantidad--;
            return true;
        }
        anterior = actual;
        actual = actual->siguiente;
    }
    
    return false;
}
Maneja dos casos:

Eliminar el primer elemento (caso especial)

Eliminar un elemento intermedio

Mantiene la integridad de los punteros

Libera la memoria correctamente

4. Funciones Auxiliares
cpp
bool existe(const K& clave) const {
    Nodo* actual = primero;
    while (actual != nullptr) {
        if (actual->clave == clave) {
            return true;
        }
        actual = actual->siguiente;
    }
    return false;
}

int tamanio() const {
    return cantidad;
}
existe(): Verifica si una clave está presente

tamanio(): Retorna la cantidad de elementos (O(1) gracias al contador)