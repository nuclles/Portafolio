#include <iostream>
#include <vector>
#include <string>

using namespace std;

struct Datos_persona{
    int dni;
    char nombre[200];
    char apellido[200];
    char nacionalidad[200];
};

class persona{
    private:
    Datos_persona datos;

    persona* padre=nullptr;
    persona* madre=nullptr;

    public:
    persona(){}; 
//--------------------------------------------------------------------------------
    persona(const Datos_persona& dts) {                                         // Si AMBAS estructuras, 
    datos.dni = dts.dni;                                                        // la de la clase y 
    strncpy(datos.nombre, dts.nombre, sizeof(datos.nombre));                    // la estructura de datos
    strncpy(datos.apellido, dts.apellido, sizeof(datos.apellido));              // usan "arrays de char" 
    strncpy(datos.nacionalidad, dts.nacionalidad, sizeof(datos.nacionalidad));  // se hace de esta forma
                                                                                //
    // Asegurar terminación nula                                                //
    datos.nombre[sizeof(datos.nombre) - 1] = '\0';                              //
    datos.apellido[sizeof(datos.apellido) - 1] = '\0';                          //
    datos.nacionalidad[sizeof(datos.nacionalidad) - 1] = '\0';                  //
    }                                                                           // 
//--------------------------------------------------------------------------------
    /*Si la fuente es std::string y el destino es array de char:
        persona(const Datos_persona& dts){
        datos.dni = dts.dni;
        strncpy(datos.nombre, dts.nombre.c_str(), sizeof(datos.nombre));
        strncpy(datos.apellido, dts.apellido.c_str(), sizeof(datos.apellido));
        strncpy(datos.nacionalidad, dts.nacionalidad.c_str(), sizeof(datos.nacionalidad));
        
        // Asegurar terminación nula
        datos.nombre[sizeof(datos.nombre) - 1] = '\0';
        datos.apellido[sizeof(datos.apellido) - 1] = '\0';
        datos.nacionalidad[sizeof(datos.nacionalidad) - 1] = '\0';
    }*/

//--------------------------------------
    const char* get_nombre() const {  // con los const solo permitimos lectura
    return datos.nombre;              //
}                                     //
//--------------------------------------


    // Método simplificado para cargar padres recursivamente
    void cargarPadres() {
        char respuesta;
        
        cout << "\n¿Desea cargar el PADRE de " << datos.nombre << "? (s/n): ";
        cin >> respuesta;
        if (respuesta == 's' || respuesta == 'S') {
            padre = nuevaPersona("el padre de " + string(datos.nombre));
            padre->cargarPadres(); // ¡Recursividad automática!
        }

        cout << "¿Desea cargar la MADRE de " << datos.nombre << "? (s/n): ";
        cin >> respuesta;
        if (respuesta == 's' || respuesta == 'S') {
            madre = nuevaPersona("la madre de " + string(datos.nombre));
            madre->cargarPadres(); // ¡Recursividad automática!
        }
    }

    // Método auxiliar para crear nueva persona
    static persona* nuevaPersona(const string& relacion) {
        Datos_persona datos;
        
        cout << "\n=== Cargando " << relacion << " ===\n";
        cout << "DNI: ";
        cin >> datos.dni;
        cout << "Nombre: ";
        cin >> datos.nombre;
        cout << "Apellido: ";
        cin >> datos.apellido;
        cout << "Nacionalidad: ";
        cin >> datos.nacionalidad;
        
        return new persona(datos);
    }
};

class arbolGen{
    private:
    persona* raiz==nullptr;


    void contarEnNivel(persona* p, int nivelDeseado, int nivelActual, 
                      int& italianos, int& total) const {
        if (p == nullptr) return;
        
        if (nivelActual == nivelDeseado) {
            total++;
            if (p->esItaliana()) {
                italianos++;
            }
            return;
        }
        
        contarEnNivel(p->padre, nivelDeseado, nivelActual + 1, italianos, total);
        contarEnNivel(p->madre, nivelDeseado, nivelActual + 1, italianos, total);
    }

    public:
    arbolGen();

    void cargarArbol() {
        cout << "=== CARGANDO PERSONA PRINCIPAL ===\n";
        raiz = persona::nuevaPersona("la persona principal");
        raiz->cargarPadres(); // ¡Esto carga toda la genealogía automáticamente!
    }

    
    
     // Método simple: verifica ciudadanía hasta cierto nivel
    bool puedeObtenerCiudadania(int nivelesMaximos = 3) const {
        if (raiz == nullptr) return false;
        
        for (int nivel = 0; nivel <= nivelesMaximos; nivel++) {
            int italianos = 0;
            int total = 0;
            contarEnNivel(raiz, nivel, 0, italianos, total);
            
            if (total > 0 && italianos * 2 >= total) {
                return true;
            }
        }
        return false;
    }

        // Métodos para guardar en archivo
    void guardarEnArchivo(ofstream& archivo) const {
        // Guardar datos de esta persona
        archivo.write(reinterpret_cast<const char*>(&datos), sizeof(Datos_persona));
        
        // Guardar si tiene padre (1) o no (0)
        bool tienePadre = (padre != nullptr);
        archivo.write(reinterpret_cast<const char*>(&tienePadre), sizeof(bool));
        if (tienePadre) {
            padre->guardarEnArchivo(archivo);
        }
        
        // Guardar si tiene madre (1) o no (0)
        bool tieneMadre = (madre != nullptr);
        archivo.write(reinterpret_cast<const char*>(&tieneMadre), sizeof(bool));
        if (tieneMadre) {
            madre->guardarEnArchivo(archivo);
        }
    }

     // Método para cargar desde archivo
    void cargarDesdeArchivo(ifstream& archivo) {
        // Cargar datos de esta persona
        archivo.read(reinterpret_cast<char*>(&datos), sizeof(Datos_persona));
        
        // Cargar información del padre
        bool tienePadre;
        archivo.read(reinterpret_cast<char*>(&tienePadre), sizeof(bool));
        if (tienePadre) {
            padre = new persona();
            padre->cargarDesdeArchivo(archivo);
        }
        
        // Cargar información de la madre
        bool tieneMadre;
        archivo.read(reinterpret_cast<char*>(&tieneMadre), sizeof(bool));
        if (tieneMadre) {
            madre = new persona();
            madre->cargarDesdeArchivo(archivo);
        }
    }

    //3)Saber cuantos antepasados Italianos tiene una persona.
    // MÉTODO 1: Contar todos los antepasados italianos (BFS con queue)
    int contarAntepasadosItalianosBFS() const {
        if (padre == nullptr && madre == nullptr) {
            return 0; // No tiene antepasados
        }
        
        int contador = 0;
        queue<const persona*> cola;
        
        // Agregar padres a la cola
        if (padre != nullptr) cola.push(padre);
        if (madre != nullptr) cola.push(madre);
        
        while (!cola.empty()) {
            const persona* actual = cola.front();
            cola.pop();
            
            // Contar si es italiano
            if (actual->esItaliana()) {
                contador++;
            }
            
            // Agregar sus padres a la cola
            if (actual->padre != nullptr) cola.push(actual->padre);
            if (actual->madre != nullptr) cola.push(actual->madre);
        }
        
        return contador;
    }

    //3)
    //Guardar en un archivo de texto los datos de la persona con todo su árbol genealógico.

    // MÉTODO 3: Guardar solo los datos básicos usando ostream
    friend ostream& operator<<(ostream& os, const persona& p) {
        os << "Nombre: " << p.datos.nombre << " " << p.datos.apellido << endl;
        os << "DNI: " << p.datos.dni << endl;
        os << "Nacionalidad: " << p.datos.nacionalidad;
        if (p.esItaliana()) {
            os << " (Italiana)";
        }
        return os;
    }

     void guardarRecursivo(ofstream& archivo, const persona* p, int nivel) const {
        if (p == nullptr) return;
        
        // Sangría según el nivel
        string sangria(nivel * 4, ' ');
        
        // Guardar persona actual
        archivo << sangria;
        archivo << *p << endl;  // Usa nuestro operador <<
        
        // Llamar recursivamente para padres
        guardarRecursivo(archivo, p->padre, nivel + 1);
        guardarRecursivo(archivo, p->madre, nivel + 1);
    }

      void guardarArbolCompleto(const string& nombreArchivo) const {
        ofstream archivo(nombreArchivo);
        if (raiz != nullptr) {
            archivo << "=== ÁRBOL GENEALÓGICO COMPLETO ===" << endl << endl;
            guardarRecursivo(archivo, raiz, 0);
        }
        archivo.close();
    }

     //3 Realice las siguientes métodos utilizando stl :
   // Función auxiliar para comparar nombres (case-insensitive)
    static bool compararNombres(const char* nombre1, const char* nombre2) {
        string n1 = nombre1, n2 = nombre2;
        
        // Convertir a minúsculas
        transform(n1.begin(), n1.end(), n1.begin(), ::tolower);
        transform(n2.begin(), n2.end(), n2.begin(), ::tolower);
        
        return n1 == n2;
    }

     // MÉTODO 3: Búsqueda por nombre y apellido exactos
    bool tieneAntepasadoConNombreCompleto(const char* nombreBuscado, const char* apellidoBuscado) const {
        if (padre == nullptr && madre == nullptr) {
            return false;
        }
        
        queue<const persona*> cola;
        if (padre != nullptr) cola.push(padre);
        if (madre != nullptr) cola.push(madre);
        
        while (!cola.empty()) {
            const persona* actual = cola.front();
            cola.pop();
            
            if (compararNombres(actual->datos.nombre, nombreBuscado) &&
                compararNombres(actual->datos.apellido, apellidoBuscado)) {
                return true;
            }
            
            if (actual->padre != nullptr) cola.push(actual->padre);
            if (actual->madre != nullptr) cola.push(actual->madre);
        }
        
        return false;
    }
}
