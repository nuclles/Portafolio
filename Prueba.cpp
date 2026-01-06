#include <iostream>
#include <ctime>

#include <vector>
#include <fstream>
#include <string>

struct Alumno {
    std::string nombre;
    int edad;
    float promedio;
};

void guardarAlumnosEnArchivo(const std::vector<Alumno>& alumnos, const std::string& nombreArchivo) {
    std::ofstream archivo(nombreArchivo, std::ios::binary);
    if (!archivo) {
        std::cerr << "Error al abrir el archivo para escritura." << std::endl;
        return;
    }

    for (const auto& alumno : alumnos) {
        size_t nombreSize = alumno.nombre.size();
        archivo.write(reinterpret_cast<const char*>(&nombreSize), sizeof(nombreSize));
        archivo.write(alumno.nombre.c_str(), nombreSize);
        archivo.write(reinterpret_cast<const char*>(&alumno.edad), sizeof(alumno.edad));
        archivo.write(reinterpret_cast<const char*>(&alumno.promedio), sizeof(alumno.promedio));
    }

    archivo.close();
}

void leerAlumnosDeArchivoYGuardarEnTxt(const std::string& archivoBinario, const std::string& archivoTxt) {
    std::ifstream archivoBin(archivoBinario, std::ios::binary);
    if (!archivoBin) {
        std::cerr << "Error al abrir el archivo binario para lectura." << std::endl;
        return;
    }

    std::ofstream archivoTexto(archivoTxt);
    if (!archivoTexto) {
        std::cerr << "Error al abrir el archivo de texto para escritura." << std::endl;
        return;
    }

    while (archivoBin.peek() != EOF) {
        size_t nombreSize;
        archivoBin.read(reinterpret_cast<char*>(&nombreSize), sizeof(nombreSize));

        std::string nombre(nombreSize, '\0');
        archivoBin.read(&nombre[0], nombreSize);

        int edad;
        archivoBin.read(reinterpret_cast<char*>(&edad), sizeof(edad));

        float promedio;
        archivoBin.read(reinterpret_cast<char*>(&promedio), sizeof(promedio));

        archivoTexto << "Nombre: " << nombre << "\n";
        archivoTexto << "Edad: " << edad << "\n";
        archivoTexto << "Promedio: " << promedio << "\n";
        archivoTexto << "--------------------------\n";
    }

    archivoBin.close();
    archivoTexto.close();
}

int main() {
    // Crear un vector de alumnos
    std::vector<Alumno> alumnos = {
        {"Juan Perez", 20, 8.5},
        {"Maria Lopez", 22, 9.0},
        {"Carlos Sanchez", 19, 7.8}
    };

    // Guardar los alumnos en un archivo binario en el escritorio
    guardarAlumnosEnArchivo(alumnos, "C:/Users/nicov/OneDrive/Escritorio/alumnos.bin");

    // Leer los alumnos del archivo binario y guardarlos en un archivo de texto
    leerAlumnosDeArchivoYGuardarEnTxt("C:/Users/nicov/OneDrive/Escritorio/alumnos.bin", 
                                      "C:/Users/nicov/OneDrive/Escritorio/alumnos.txt");

    std::cout << "Alumnos guardados en el archivo binario y exportados al archivo de texto." << std::endl;

    return 0;
}