#include <iostream>
#include <fstream>


using namespace std:

struct DatosViaje{//estructura para cargar los datos y para guardar en los archivos
    char nombre[200];
    char tipo;
    float costo;
    int tiempo;
    float precio =0;
    int km;
}

class viaje{
    public:
    string nombre;
    char tipo;
    float costo;
    int tiempo;
    float precio;
    int km;

    DatosViaje dat;

    virtual float calcular_precio()=0;
    DatosViaje get_datos(){
        dat.tipo=this tipo;
    }
}
class EnAvion:public viaje{
    public:
    EnAvion(DatosViaje datos){
        this->nombre=datos.nombre;
        this->tipo=datos.tipo;
        this->costo=datos.costo;
        this->tiempo=(datos.tiempo+2);
        this->km=datos.km;
    }
    float calcular_precio(){
        this->precio = (this->costo*1.2);
    }
}

class EnColectivo:public viaje{
    public:
    EnColectivo(DatosViaje datos){
        this->nombre=datos.nombre;
        this->tipo=datos.tipo;
        this->costo=datos.costo;
        this->tiempo=datos.tiempo;
        this->km=datos.km;
    }

    float calcular_precio(){
        this->precio=(this->km*8);
    }
}

class Compuesto_AyC:public viaje{
    private:
    EnAvion vuelo;
    EnColectivo Colectivo;
    public:    Compuesto_AyC(DatosViaje datos){
        this->nombre=datos.nombre;
        this->tipo=datos.tipo;
        this->costo=datos.costo;
        this->tiempo=datos.tiempo;
        this->km=datos.km;
    }

}
