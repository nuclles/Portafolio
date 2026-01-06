#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

const string ARCHIVO_BINARIO = "arbol_genealogico.dat";
const string ARCHIVO_TEXTO = "arbol_genealogico.txt";

class Persona {
public:
    string dni;
    string nombre;
    string apellido;
    string nacionalidad;
    Persona* padre;
    Persona* madre;

    Persona() : dni(""), nombre(""), apellido(""), nacionalidad(""), padre(nullptr), madre(nullptr) {}

    Persona(string d, string n, string a, string nac) 
        : dni(d), nombre(n), apellido(a), nacionalidad(nac), padre(nullptr), madre(nullptr) {}

    ~Persona() {
        if (padre) delete padre;
        if (madre) delete madre;
    }

    bool esItaliano() const {
        return nacionalidad == "italiana" || nacionalidad == "italiano"; // devuelve true si se cumple una de las dos comparaciones.
    }

    void cargarArbolGenealogico() {
        cout << "\nCargando datos para " << nombre << " " << apellido << endl;
        
        // Cargar padre
        cout << "\n¿Desea cargar datos del padre? (s/n): ";
        if (confirmarEntrada()) {
            padre = new Persona();
            padre->ingresarDatos();
            padre->cargarArbolGenealogico();
        }

        // Cargar madre
        cout << "\n¿Desea cargar datos de la madre? (s/n): ";
        if (confirmarEntrada()) {
            madre = new Persona();
            madre->ingresarDatos();
            madre->cargarArbolGenealogico();
        }
    }

    void ingresarDatos() {
        cout << "DNI: ";
        cin >> dni;
        cout << "Nombre: ";
        cin.ignore();
        getline(cin, nombre);
        cout << "Apellido: ";
        getline(cin, apellido);
        cout << "Nacionalidad: ";
        getline(cin, nacionalidad);
    }

    bool esAptaParaCiudadania() const {
        // Verificar si la persona misma es italiana
        if (esItaliano()) return true;

        // Verificar antepasados por nivel
        vector<Persona*> nivelActual = {this};
        int nivel = 0;

        while (!nivelActual.empty()) {
            int italianosEnNivel = 0;
            int totalEnNivel = 0;
            vector<Persona*> siguienteNivel;

            for (Persona* persona : nivelActual) {
                if (persona->padre) {
                    siguienteNivel.push_back(persona->padre);
                    if (persona->padre->esItaliano()) italianosEnNivel++;
                    totalEnNivel++;
                }
                if (persona->madre) {
                    siguienteNivel.push_back(persona->madre);
                    if (persona->madre->esItaliano()) italianosEnNivel++;
                    totalEnNivel++;
                }
            }

            if (totalEnNivel > 0 && italianosEnNivel * 2 >= totalEnNivel) {
                return true;
            }

            nivelActual = siguienteNivel;
            nivel++;
        }

        return false;
    }

    int contarAntepasadosItalianos() const {
        int contador = 0;
        if (padre) {
            if (padre->esItaliano()) contador++;
            contador += padre->contarAntepasadosItalianos();
        }
        if (madre) {
            if (madre->esItaliano()) contador++;
            contador += madre->contarAntepasadosItalianos();
        }
        return contador;
    }

    bool tieneAntepasadoConNombre(const string& nombreBuscado) const {
        if (nombre == nombreBuscado) return true;
        if (padre && padre->tieneAntepasadoConNombre(nombreBuscado)) return true;
        if (madre && madre->tieneAntepasadoConNombre(nombreBuscado)) return true;
        return false;
    }

bool tieneAntepasadoConMismoNombre() const {
    // Verificar si algún padre tiene el mismo nombre
    if (padre) {
        if (padre->nombre == nombre && padre->apellido == apellido) return true;
        if (padre->tieneAntepasadoConMismoNombre()) return true;
    }
    
    // Verificar si alguna madre tiene el mismo nombre
    if (madre) {
        if (madre->nombre == nombre && madre->apellido == apellido) return true;
        if (madre->tieneAntepasadoConMismoNombre()) return true;
    }
    
    // Si no encontró coincidencias
    return false;
}


    void guardarEnArchivo(ofstream& archivo) const {
        archivo << dni << " " << nombre << " " << apellido << " " << nacionalidad << " ";
        archivo << (padre ? padre->dni : "NULL") << " ";
        archivo << (madre ? madre->dni : "NULL") << "\n";

        if (padre) padre->guardarEnArchivo(archivo);
        if (madre) madre->guardarEnArchivo(archivo);
    }

    void guardarEnArchivoBinario(ofstream& archivo) const {
        size_t size;

        // Guardar datos de la persona
        size = dni.size();
        archivo.write(reinterpret_cast<const char*>(&size), sizeof(size));
        archivo.write(dni.c_str(), size);

        size = nombre.size();
        archivo.write(reinterpret_cast<const char*>(&size), sizeof(size));
        archivo.write(nombre.c_str(), size);

        size = apellido.size();
        archivo.write(reinterpret_cast<const char*>(&size), sizeof(size));
        archivo.write(apellido.c_str(), size);

        size = nacionalidad.size();
        archivo.write(reinterpret_cast<const char*>(&size), sizeof(size));
        archivo.write(nacionalidad.c_str(), size);

        // Guardar referencias a padres
        bool tienePadre = (padre != nullptr);
        archivo.write(reinterpret_cast<const char*>(&tienePadre), sizeof(tienePadre));
        if (tienePadre) {
            padre->guardarEnArchivoBinario(archivo);
        }

        bool tieneMadre = (madre != nullptr);
        archivo.write(reinterpret_cast<const char*>(&tieneMadre), sizeof(tieneMadre));
        if (tieneMadre) {
            madre->guardarEnArchivoBinario(archivo);
        }
    }

    void imprimirArbol(int nivel = 0) const {
        string indent(nivel * 2, ' ');
        cout << indent << nombre << " " << apellido << " (" << nacionalidad << ")" << endl;
        if (padre) padre->imprimirArbol(nivel + 1);
        if (madre) madre->imprimirArbol(nivel + 1);
    }

private:
    bool confirmarEntrada() {
        char opcion;
        cin >> opcion;
        return (opcion == 's' || opcion == 'S');
    }
};

// Funciones auxiliares
void guardarArbolEnArchivoTexto(const Persona* persona) {
    ofstream archivo(ARCHIVO_TEXTO);
    if (!archivo) {
        cerr << "Error al abrir el archivo de texto" << endl;
        return;
    }

    archivo << "Árbol Genealógico:\n";
    archivo << "=================\n";
    persona->guardarEnArchivo(archivo);
    archivo.close();
    cout << "Árbol genealógico guardado en " << ARCHIVO_TEXTO << endl;
}

void guardarArbolEnArchivoBinario(const Persona* persona) {
    ofstream archivo(ARCHIVO_BINARIO, ios::binary);
    if (!archivo) {
        cerr << "Error al abrir el archivo binario" << endl;
        return;
    }

    persona->guardarEnArchivoBinario(archivo);
    archivo.close();
    cout << "Árbol genealógico guardado en " << ARCHIVO_BINARIO << endl;
}

Persona* cargarDesdeArchivoBinario(ifstream& archivo) {
    if (!archivo) return nullptr;

    Persona* persona = new Persona();
    size_t size;

    // Leer DNI
    archivo.read(reinterpret_cast<char*>(&size), sizeof(size));
    persona->dni.resize(size);
    archivo.read(&persona->dni[0], size);

    // Leer nombre
    archivo.read(reinterpret_cast<char*>(&size), sizeof(size));
    persona->nombre.resize(size);
    archivo.read(&persona->nombre[0], size);

    // Leer apellido
    archivo.read(reinterpret_cast<char*>(&size), sizeof(size));
    persona->apellido.resize(size);
    archivo.read(&persona->apellido[0], size);

    // Leer nacionalidad
    archivo.read(reinterpret_cast<char*>(&size), sizeof(size));
    persona->nacionalidad.resize(size);
    archivo.read(&persona->nacionalidad[0], size);

    // Leer padre
    bool tienePadre;
    archivo.read(reinterpret_cast<char*>(&tienePadre), sizeof(tienePadre));
    if (tienePadre) {
        persona->padre = cargarDesdeArchivoBinario(archivo);
    }

    // Leer madre
    bool tieneMadre;
    archivo.read(reinterpret_cast<char*>(&tieneMadre), sizeof(tieneMadre));
    if (tieneMadre) {
        persona->madre = cargarDesdeArchivoBinario(archivo);
    }

    return persona;
}

int main() {
    // Crear persona principal
    Persona* persona = new Persona();
    cout << "Ingrese datos de la persona principal:" << endl;
    persona->ingresarDatos();

    // Cargar árbol genealógico
    persona->cargarArbolGenealogico();

    // Mostrar árbol
    cout << "\nÁrbol Genealógico:" << endl;
    persona->imprimirArbol();

    // Verificar elegibilidad para ciudadanía
    if (persona->esAptaParaCiudadania()) {
        cout << "\nRESULTADO: La persona ES apta para la ciudadanía italiana." << endl;
    } else {
        cout << "\nRESULTADO: La persona NO es apta para la ciudadanía italiana." << endl;
    }

    // Contar antepasados italianos
    cout << "\nLa persona tiene " << persona->contarAntepasadosItalianos() 
         << " antepasados italianos." << endl;

    // Buscar antepasado por nombre
    string nombreBuscado;
    cout << "\nIngrese un nombre para buscar en los antepasados: ";
    cin.ignore();
    getline(cin, nombreBuscado);
    if (persona->tieneAntepasadoConNombre(nombreBuscado)) {
        cout << "El nombre '" << nombreBuscado << "' aparece en el árbol genealógico." << endl;
    } else {
        cout << "El nombre '" << nombreBuscado << "' NO aparece en el árbol genealógico." << endl;
    }

    // Guardar en archivos
    guardarArbolEnArchivoBinario(persona);
    guardarArbolEnArchivoTexto(persona);

    // Liberar memoria
    delete persona;

    return 0;
}