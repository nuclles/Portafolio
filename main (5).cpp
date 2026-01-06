#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>

using namespace std;
struct personas{
    int orden;
    int anio;
    string NyA;
}dato;
int contarfilas(int cont){
    ifstream archi;
    string linea;
    archi.open("C:/Users/angel/Documents/E7.txt");
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
int main()
{
    int n=contarfilas(0);
    //cout<<n<<endl;
    ifstream archi;
    archi.open("C:/Users/angel/Documents/E7.txt");
    if(archi.fail()){
        cout<<"error";
        exit(1);
    }
    int *ord,*ani,i=0;
    string *Nom;
    /*ord=new int[n];
    ani=new int [n];
    Nom=new string[n];*/
    personas *m;
    m= new personas[n];
    while(i<n){
        archi>>dato.orden>>dato.anio;
        getline(archi,dato.NyA);
        m[i].orden=dato.orden;
        m[i].anio=dato.anio;
        m[i].NyA=dato.NyA;
        i++;
        /*
        archi>>dato.orden>>dato.anio;
        getline(archi,dato.NyA);
        //cout<<dato.orden<<endl;
        ord[i]=dato.orden;
        ani[i]=dato.anio;
        Nom[i]=dato.NyA;
        //cout<<"vector dinamico: "<<Nom[i]<<endl;
        i++;*/
    }
    archi.close();
    cout<<"orden   anio   nombre y apellido"<<endl;
    for(int j=0;j<n;j++){
        cout<<m[j].orden<<" "<<m[j].anio<<" "<<m[j].NyA<<" "<<endl;
    }
    delete[] m;

}
