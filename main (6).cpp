#include <iostream>
#include <fstream>
#include <string>
using namespace std;

//Funcion creacion del archivo con nombre de los integrantes
void crear(){
    ofstream archi;
    archi.open("C:/Users/angel/Documents/tp1.txt");//desp habria que sacar la ubi de todos
    if (archi.fail()){
        cout<<"error";
        exit(1);
    }
    archi<<"angela garcia verdier. santino pross. santino ricle. nicolas varrone.";
    archi.close();
}

//Funcion ejercicio 1
int contarfilas(int cont){
    ifstream archi;
    string linea;
    archi.open("C:/Users/angel/Documents/tp1.txt");
    if (archi.fail()){
        cout<<"error";
        exit(1);
    }
    while (getline(archi,linea)){
        cont++;
    }
    archi.close();
    return cont;
}

//Funcion ejercicio 2
int caracterrepetido(char caracter,string linea,int &contador){
    contador=0;
    for (char c : linea) {
        if (c == caracter) {
            contador++;
        }
    }
    return 1;
}

//Funcion ejercicio 3
void modificararchi(){
    fstream archi;
    archi.open("C:/Users/angel/Documents/tp1.txt", ios::in | ios::out);
    if (archi.fail()) {
        cout << "Error" << endl;
        }
    int i=0;
    char caracter;
    while (archi.get(caracter)){
        if(caracter == '.'){
            i=archi.tellg();
            archi.seekp(i-1);
            archi<<endl;
            archi.seekp(i-1);
            archi<<".";
        }
    }
    archi.close();
}

//Funcion ejercicio 4
int buscaryreemplazar(char buscar,char reemplazar,string linea,int &contador){
    fstream archi;
    contador=0;
    archi.open("C:/Users/angel/Documents/tp1.txt", ios::in | ios::out);
    if (archi.fail()) {
        cout << "Error" << endl;
    }
    int i=0;
    bool r;
    char caracter;
    while (archi.get(caracter)){
        if(caracter== buscar){
            i=archi.tellg();
            archi.seekp(i-1);
            archi<<reemplazar;
            r=true;
        }
    if ((caracter=='\n')&&(r==true)) {
            contador++;
            r=false;
    }
    }
    archi.close();
    return contador;
    }
int main()
{
    crear(); //crea archivo con nombre de integrantes

    //Ejercicio 1
    cout<<"numero de filas del archivo: "<<contarfilas(0)<<endl;
    char caracter;
    cout<<"ingrese caracter a buscar en el archivo: ";
    cin>>caracter;

    //Ejercicio 2
    ifstream archi;
    string linea;
    int i=0;
    archi.open("C:/Users/angel/Documents/tp1.txt");
    if (archi.fail()){
        cout<<"error";
        exit(1);
    }
    int contador,acumulador=0;
    while (getline(archi, linea)) {
        caracterrepetido (caracter,linea,contador);
        cout<<"linea "<<(i+1)<<" "<<contador<<endl;
        acumulador+=contador;
    }
    cout<<"total de "<<caracter<<": "<<acumulador<<endl;
    archi.close();

    //Ejercicio 3
    modificararchi();

    //Ejercicio 4
    char buscar,reemplazar;
    cout<<"ingrese caracter a buscar:";
    cin>>buscar;
    cout<<"ingrese caracter a reemplazar:";
    cin>>reemplazar;
    int cont2;
    cout<<"lineas en las que se reemplazo: "<<buscaryreemplazar(buscar,reemplazar,linea,cont2)<<endl;
    return 0;
}

