#include "sistemaencuesta.h"

SistemaEncuesta::SistemaEncuesta() {}

void SistemaEncuesta::cargarEncuesta() {
    // Ejemplo de carga manual de una encuesta
    Pregunta pregunta1("¿Tiene teléfono móvil?");
    pregunta1.agregarRespuesta(Respuesta("Sí", new Pregunta("¿Cuál marca?")));
    pregunta1.agregarRespuesta(Respuestas("No"));

    encuesta.agregarPregunta(pregunta1);
}

void SistemaEncuesta::guardarEncuesta(string &nombreArchivo){
    encuesta.guardar(nombreArchivo);
}

void SistemaEncuesta::cargarEncuestaDesdeArchivo(string &nombreArchivo) {
    encuesta.cargar(nombreArchivo);
}

void SistemaEncuesta::mostrarEncuesta(){
    for (auto& pregunta : encuesta.getPreguntas()) {
        std::cout << "Pregunta: " << pregunta.getTexto() << std::endl;
        for (auto& respuesta : pregunta.getRespuestas()) {
            std::cout << "  Respuesta: " << respuesta.getTexto() << std::endl;
            if (respuesta.getSubpregunta()) {
                std::cout << "    Subpregunta: " << respuesta.getSubpregunta()->getTexto() << std::endl;
            }
        }
    }
}
