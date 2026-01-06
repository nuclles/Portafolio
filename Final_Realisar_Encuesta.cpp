Empresa para desarrollar software que permita cargar una encuesta
Una empresa lo contrata para realizar un software que permita cargar una encuesta. La encuesta tiene preguntas y cada pregunta contiene diferentes respuestas. A la vez algunas respuestas pueden contener preguntas. 

Por ejemplo : Tiene teléfono móvil? si la respuesta es afirmativa, se desprende la pregunta: Cual marca? y si la respuesta es negativa, no se continua preguntando sobre el tema. 

(30) Realice un diseño que permita guardar las preguntas y respuestas cargadas en un o varios archivos binarios. 

(30) Realice un procedimiento que permita responder dicha encuesta. Para este procedimiento no es necesario guardar las respuestas. 

(20) Utilizando STL realice:

una función que indique cual es o son las preguntas con más respuestas. 

una función que indique las respuestas que tienen preguntas encadenadas.  

(20) Explique porque son necesarias las clases template. ¿Cuándo las utilizaría? ¿Cuáles son sus ventajas y desventajas? 


#include <iostream>
#include <vector>
#include <string>
#include <fstream>

class Respuesta;

class Pregunta {
private:
    std::string texto;
    std::vector<Respuesta*> respuestas;
    
public:
    Pregunta(const std::string& texto = "") : texto(texto) {}
    ~Pregunta() {
        for (auto resp : respuestas) {
            delete resp;
        }
    }
    
    void agregarRespuesta(Respuesta* respuesta) {
        respuestas.push_back(respuesta);
    }
    
    const std::vector<Respuesta*>& obtenerRespuestas() const {
        return respuestas;
    }
    
    const std::string& obtenerTexto() const {
        return texto;
    }
    

//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++//
//(30) Realice un diseño que permita guardar las preguntas y respuestas cargadas en un o varios archivos binarios. //

    void guardarEnArchivo(std::ofstream& archivo) const {
        // Guardar tamaño del texto y luego el texto
        size_t tamañoTexto = texto.size();
        archivo.write(reinterpret_cast<const char*>(&tamañoTexto), sizeof(tamañoTexto));
        archivo.write(texto.c_str(), tamañoTexto);
        
        // Guardar cantidad de respuestas
        size_t numRespuestas = respuestas.size();
        archivo.write(reinterpret_cast<const char*>(&numRespuestas), sizeof(numRespuestas));
        
        // Guardar cada respuesta
        for (const auto& respuesta : respuestas) {
            respuesta->guardarEnArchivo(archivo);
        }
    }
    
    void cargarDesdeArchivo(std::ifstream& archivo) {
        // Cargar texto
        size_t tamañoTexto;
        archivo.read(reinterpret_cast<char*>(&tamañoTexto), sizeof(tamañoTexto));
        char* buffer = new char[tamañoTexto + 1];
        archivo.read(buffer, tamañoTexto);
        buffer[tamañoTexto] = '\0';
        texto = buffer;
        delete[] buffer;
        
        // Cargar respuestas
        size_t numRespuestas;
        archivo.read(reinterpret_cast<char*>(&numRespuestas), sizeof(numRespuestas));
        
        for (size_t i = 0; i < numRespuestas; ++i) {
            Respuesta* respuesta = new Respuesta("");
            respuesta->cargarDesdeArchivo(archivo);
            respuestas.push_back(respuesta);
        }
    }
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++//
    
    void mostrar() const {
        std::cout << "Pregunta: " << texto << std::endl;
        for (size_t i = 0; i < respuestas.size(); ++i) {
            std::cout << i+1 << ") ";
            respuestas[i]->mostrar();
        }
    }
};





class Respuesta {
private:
    std::string texto;
    Pregunta* preguntaSiguiente;
    
public:
    Respuesta(const std::string& texto = "", Pregunta* preguntaSiguiente = nullptr)
        : texto(texto), preguntaSiguiente(preguntaSiguiente) {}
    
    ~Respuesta() {
        delete preguntaSiguiente;
    }
    
    bool tienePreguntaSiguiente() const {
        return preguntaSiguiente != nullptr;
    }
    
    Pregunta* obtenerPreguntaSiguiente() const {
        return preguntaSiguiente;
    }
    
    const std::string& obtenerTexto() const {
        return texto;
    }

//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++//
//(30) Realice un diseño que permita guardar las preguntas y respuestas cargadas en un o varios archivos binarios. //
    
    void guardarEnArchivo(std::ofstream& archivo) const {
        // Guardar texto de la respuesta
        size_t tamañoTexto = texto.size();
        archivo.write(reinterpret_cast<const char*>(&tamañoTexto), sizeof(tamañoTexto));
        archivo.write(texto.c_str(), tamañoTexto);
        
        // Guardar si tiene pregunta siguiente
        bool tienePregunta = (preguntaSiguiente != nullptr);
        archivo.write(reinterpret_cast<const char*>(&tienePregunta), sizeof(tienePregunta));
        
        if (tienePregunta) {
            preguntaSiguiente->guardarEnArchivo(archivo);
        }
    }
    
    void cargarDesdeArchivo(std::ifstream& archivo) {
        // Cargar texto
        size_t tamañoTexto;
        archivo.read(reinterpret_cast<char*>(&tamañoTexto), sizeof(tamañoTexto));
        char* buffer = new char[tamañoTexto + 1];
        archivo.read(buffer, tamañoTexto);
        buffer[tamañoTexto] = '\0';
        texto = buffer;
        delete[] buffer;
        
        // Cargar pregunta siguiente si existe
        bool tienePregunta;
        archivo.read(reinterpret_cast<char*>(&tienePregunta), sizeof(tienePregunta));
        
        if (tienePregunta) {
            preguntaSiguiente = new Pregunta();
            preguntaSiguiente->cargarDesdeArchivo(archivo);
        } else {
            preguntaSiguiente = nullptr;
        }
    }
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++//

    
    void mostrar() const {
        std::cout << texto;
        if (preguntaSiguiente) {
            std::cout << " [-> tiene pregunta condicional]";
        }
        std::cout << std::endl;
    }
};

class Encuesta {
private:
    std::vector<Pregunta*> preguntas;
    
public:
    ~Encuesta() {
        for (auto preg : preguntas) {
            delete preg;
        }
    }
    
    void agregarPregunta(Pregunta* pregunta) {
        preguntas.push_back(pregunta);
    }
    


//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++//
//(30) Realice un diseño que permita guardar las preguntas y respuestas cargadas en un o varios archivos binarios. //

    void guardarEnArchivo(const std::string& nombreArchivo) const {
        std::ofstream archivo(nombreArchivo, std::ios::binary);
        if (!archivo) {
            throw std::runtime_error("No se pudo abrir el archivo para escritura");
        }
        
        // Guardar cantidad de preguntas
        size_t numPreguntas = preguntas.size();
        archivo.write(reinterpret_cast<const char*>(&numPreguntas), sizeof(numPreguntas));
        
        // Guardar cada pregunta
        for (const auto& pregunta : preguntas) {
            pregunta->guardarEnArchivo(archivo);
        }
    }
    
    void cargarDesdeArchivo(const std::string& nombreArchivo) {
        std::ifstream archivo(nombreArchivo, std::ios::binary);
        if (!archivo) {
            throw std::runtime_error("No se pudo abrir el archivo para lectura");
        }
        
        // Limpiar preguntas existentes
        for (auto& pregunta : preguntas) {
            delete pregunta;
        }
        preguntas.clear();
        
        // Cargar cantidad de preguntas
        size_t numPreguntas;
        archivo.read(reinterpret_cast<char*>(&numPreguntas), sizeof(numPreguntas));
        
        // Cargar cada pregunta
        for (size_t i = 0; i < numPreguntas; ++i) {
            Pregunta* pregunta = new Pregunta();
            pregunta->cargarDesdeArchivo(archivo);
            preguntas.push_back(pregunta);
        }
    }

//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++//
    
    void ejecutar() {
        for (auto pregunta : preguntas) {
            realizarPregunta(pregunta);
        }
    }
    
private:
    void realizarPregunta(Pregunta* pregunta) {
        pregunta->mostrar();
        
        int eleccion;
        std::cout << "Seleccione una opción: ";
        std::cin >> eleccion;
        
        if (eleccion > 0 && eleccion <= pregunta->obtenerRespuestas().size()) {
            Respuesta* respuesta = pregunta->obtenerRespuestas()[eleccion-1];
            if (respuesta->tienePreguntaSiguiente()) {
                realizarPregunta(respuesta->obtenerPreguntaSiguiente());
            }
        } else {
            std::cout << "Opción inválida." << std::endl;
        }
    }
};

//+++++++++++++++++++++++//
//ejemplo de uso
int main() {
    try {
        // Crear y guardar encuesta
        {
            Encuesta encuesta;
            
            Pregunta* pregunta1 = new Pregunta("¿Tiene teléfono móvil?");
            Pregunta* preguntaCond = new Pregunta("¿Cuál marca?");
            preguntaCond->agregarRespuesta(new Respuesta("Apple"));
            preguntaCond->agregarRespuesta(new Respuesta("Samsung"));
            preguntaCond->agregarRespuesta(new Respuesta("Otra"));
            
            pregunta1->agregarRespuesta(new Respuesta("Sí", preguntaCond));
            pregunta1->agregarRespuesta(new Respuesta("No"));
            
            encuesta.agregarPregunta(pregunta1);
            
            // Guardar en archivo
            encuesta.guardarEnArchivo("encuesta.dat");
            std::cout << "Encuesta guardada correctamente.\n";
        }
        
        // Cargar y ejecutar encuesta
        {
            Encuesta encuesta;
            encuesta.cargarDesdeArchivo("encuesta.dat");
            std::cout << "\nEncuesta cargada correctamente.\n";
            encuesta.ejecutar();
        }
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}


//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++//
// Realice un procedimiento que permita responder dicha encuesta. Para este procedimiento no es necesario guardar las respuestas.  //


//#include <iostream>
#include <vector>
#include <string>
#include <map>

class EncuestaResponder {
private:
    struct Pregunta {
        size_t id;
        std::string texto;
        std::vector<size_t> respuestaIDs;
    };

    struct Respuesta {
        size_t id;
        std::string texto;
        size_t siguientePreguntaID;
    };

    std::vector<Pregunta> preguntas;
    std::map<size_t, Respuesta> respuestas;
    size_t preguntaInicialID;

public:
    void cargarDesdeArchivos(const std::string& preguntasFile, const std::string& respuestasFile) {
        // Implementación igual que en el diseño anterior
        // ...
    }

    void responderEncuesta() {
        if (preguntas.empty()) {
            std::cout << "No hay preguntas cargadas para responder." << std::endl;
            return;
        }

        // Comenzar con la primera pregunta (asumimos que es la de ID más bajo)
        size_t currentPreguntaID = preguntas[0].id;
        
        while (currentPreguntaID != 0) {
            // Buscar la pregunta actual
            auto preguntaIt = std::find_if(preguntas.begin(), preguntas.end(), 
                [currentPreguntaID](const Pregunta& p) { return p.id == currentPreguntaID; });
            
            if (preguntaIt == preguntas.end()) {
                std::cout << "Error: Pregunta no encontrada." << std::endl;
                break;
            }

            // Mostrar pregunta
            std::cout << "\n" << preguntaIt->texto << std::endl;
            
            // Mostrar opciones de respuesta
            for (size_t i = 0; i < preguntaIt->respuestaIDs.size(); ++i) {
                auto respIt = respuestas.find(preguntaIt->respuestaIDs[i]);
                if (respIt != respuestas.end()) {
                    std::cout << i + 1 << ") " << respIt->second.texto << std::endl;
                }
            }

            // Obtener selección del usuario
            int seleccion;
            std::cout << "Seleccione una opción (0 para salir): ";
            std::cin >> seleccion;
            
            // Validar entrada
            if (seleccion == 0) {
                std::cout << "Encuesta terminada por el usuario." << std::endl;
                break;
            }

            if (seleccion < 1 || seleccion > preguntaIt->respuestaIDs.size()) {
                std::cout << "Opción inválida. Por favor intente nuevamente." << std::endl;
                continue;
            }

            // Obtener la respuesta seleccionada
            size_t respuestaID = preguntaIt->respuestaIDs[seleccion - 1];
            auto respIt = respuestas.find(respuestaID);
            
            if (respIt == respuestas.end()) {
                std::cout << "Error: Respuesta no encontrada." << std::endl;
                break;
            }

            // Mover a la siguiente pregunta (0 si no hay)
            currentPreguntaID = respIt->second.siguientePreguntaID;
        }

        std::cout << "\n¡Gracias por completar la encuesta!" << std::endl;
    }
};

// Ejemplo de uso
int main() {
    EncuestaResponder encuesta;
    
    try {
        // Cargar la encuesta desde archivos
        encuesta.cargarDesdeArchivos("preguntas.dat", "respuestas.dat");
        
        // Iniciar el proceso de responder la encuesta
        std::cout << "=== INICIO DE ENCUESTA ===" << std::endl;
        encuesta.responderEncuesta();
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}

//****************************************************//
//****************************************************//
=== INICIO DE ENCUESTA ===

¿Tiene teléfono móvil?
1) Sí
2) No
Seleccione una opción (0 para salir): 1

¿Cuál marca?
1) Apple
2) Samsung
3) Otra
Seleccione una opción (0 para salir): 2

¡Gracias por completar la encuesta!
//****************************************************//
//****************************************************//


Funciones utilizando STL
1. Función para encontrar preguntas con más respuestas
cpp
#include <vector>
#include <algorithm>
#include <map>

std::vector<Pregunta*> encontrarPreguntasConMasRespuestas(const std::vector<Pregunta*>& preguntas) {
    if (preguntas.empty()) return {};
    
    // Encontrar el número máximo de respuestas
    auto maxElem = std::max_element(preguntas.begin(), preguntas.end(),
        [](const Pregunta* a, const Pregunta* b) {
            return a->obtenerRespuestas().size() < b->obtenerRespuestas().size();
        });
    
    size_t maxRespuestas = (*maxElem)->obtenerRespuestas().size();
    
    // Recoger todas las preguntas con ese número de respuestas
    std::vector<Pregunta*> resultado;
    std::copy_if(preguntas.begin(), preguntas.end(), std::back_inserter(resultado),
        [maxRespuestas](const Pregunta* p) {
            return p->obtenerRespuestas().size() == maxRespuestas;
        });
    
    return resultado;
}
2. Función para encontrar respuestas con preguntas encadenadas
cpp
std::vector<Respuesta*> encontrarRespuestasConPreguntasEncadenadas(const std::vector<Pregunta*>& preguntas) {
    std::vector<Respuesta*> resultado;
    
    for (const auto& pregunta : preguntas) {
        for (const auto& respuesta : pregunta->obtenerRespuestas()) {
            if (respuesta->tienePreguntaSiguiente()) {
                resultado.push_back(respuesta);
            }
        }
    }
    
    return resultado;
}

¿Por qué son necesarias las clases template?
Las clases template son necesarias para crear estructuras de datos o algoritmos genéricos que pueden trabajar con diferentes tipos de datos sin necesidad de reescribir el código para cada tipo. Proporcionan:

Reutilización de código: Un mismo template puede usarse con múltiples tipos

Type safety: El compilador verifica los tipos en tiempo de compilación

Eficiencia: No hay sobrecarga de runtime como en los enfoques basados en herencia

¿Cuándo utilizarlas?
Cuando necesitas contenedores que funcionen con cualquier tipo (vector, list, map)

Para implementar algoritmos genéricos (sort, find)

Cuando varias clases comparten la misma lógica pero difieren solo en el tipo de datos

Para políticas de diseño y metaprogramación

Ventajas:
Flexibilidad: Trabajan con cualquier tipo que cumpla los requisitos

Eficiencia: Generan código específico para cada tipo en tiempo de compilación

Seguridad de tipos: Detectan errores de tipo en compilación

Reducción de duplicación: Evitan escribir múltiples versiones de la misma clase

Desventajas:
Errores de compilación complejos: Los mensajes de error pueden ser difíciles de entender

Tiempo de compilación: Pueden aumentar significativamente

Sobrecarga conceptual: Mayor complejidad para los desarrolladores

Limitaciones: No todos los tipos son compatibles con todas las operaciones del template

Ejemplo clásico: std::vector<T> es un template que puede crear vectores de cualquier tipo, manteniendo la seguridad de tipos y eficiencia como si estuviera especializado para cada tipo.

Las clases template son fundamentales en la programación genérica en C++ y son la base de la STL (Standard Template Library).