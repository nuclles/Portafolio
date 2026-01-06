//emanuelpeg@yahoo.com.ar
#include <iostream>
#include <fstream>
#include <vector>
#include <map> //al final no se uso.
#include <cstring>

using namespace std;

/*1)respuesta teorica: no es necesario utilizar polimorfismo dado que el metodo que utilizamos para ahorrar codigo es Composicion*/



struct DatosEmpleado{
    char nombre[200];
    int id;
    double sueldoNeto;
    int aniosAntiguedad;
    int empleadosACargo;
}

class item{
    protected:
    //int id;
    //char nombre[200];
    int antiguedad;
    int empleadosACargo;
    double sueldoNeto;
    double montoItem;

    public:

    virtual double calcularMontoItem()=0;
    double getSueldoNeto(){
        return this->sueldoNeto;
    }
};

class Antiguedad : public item{
    public:
    Antiguedad(DatosEmpleado dat){
        this->sueldoNeto=dat.sueldoNeto;
        this->antiguedad=dat.aniosAntiguedad;
    }

    double calcularMontoItem(){
        this->montoItem=this->sueldoNeto*(this->antiguedad/100);
        return this->montoItem;
    }
};

class EmpleadosACargo : public item{
    public:
    EmpleadosACargo(DatosEmpleado dat){
        this->sueldoNeto=dat.sueldoNeto;
        this->empleadosACargo=dat.empleadosACargo;
    }
    double calcularMontoItem(){
        this->montoItem=this->empleadosACargo+1000;
        return this->montoItem;
    }
};




class empleado{
    private:
    DatosEmpleado recibo;
    vector<item*>items;

    public:
    empleado(DatosEmpleado dat){
        this->recibo=dat;
        items.push_back(new Antiguedad(dat));
        items.push_back(new EmpleadosACargo(dat));
    }
    double getMontoAntiguedad(){
        return items[0]->calcularMontoItem();
    }
    double getMontoEmpleadosACargo(){
        return items[1]->calcularMontoItem();
    }
    double get_MontoTotal(){
        double total=0;
        for(auto &it:items){
            total+=it->calcularMontoItem();
        }
        return total;
    }
    double get_SueldoNeto(){
        return recibo.sueldoNeto;
    }
    string get_nombre(){
        string aux;
        strcpy (aux, recibo.nombre);
        return aux;
    }
}



class gestora{
    private:
    vector<empleado>empleados;

    public:

    //2)
    void leerArcBinario(const char*direccion){
        ifstream ArchDatos(direccion,ios::binary);
        if(ArchDatos.fail()){
            exit -1;
        }
        DatosEmpleado aux;
        while(!ArchDatos.eof()){
            ArchDatos.read(reinterpret_cast <char*>(&aux),sizeof(DatosEmpleado));
            empleados.push_back(new empleado(aux));
        }

        ArchDatos.close();
    }

    //3)
     void imprimirRecibo(int id){
            auto it=find_if(empleados.begin(),empleados.end(),[id](empleado &a){
                return a.get_id()==id;
            });
            it.calcularCostoDe_TodosLosEmpleados();
            it.calcularAntiguedad();
            it.MontoTotal()

            ifstream ArcRecibo("Recibo.txt");
            if(ArcRecibo.fail())exit -1;

            ArcRecibo<<
            "nombre"<<it.get_nombre()<<endl<<
            "Sueldo Neto"<<in.get_SueldoNeto()<<endl<<
            "Monto por empleados"<<it.getMontoEmpleadosACargo()<<endl<<
            "Monto por antiguedad"<<it.getMontoAntiguedad()<<endl;

            ArchDatos.close();
        }


        //4)
        //a.
        void empleadoConMasAntiguedad(){
            sort(empleados.begin(),empleados.end(),[](empleados &a,empleado &b){
                return a.getMontoEmpleadosACargo()>b.getMontoEmpleadosACargo();
            })

            cout<<"empleado con mas antiguedad"<<empleados[0].get_nombre()<<"id"<<empleados[0].get_id()<<endl;
        }

        //b.
        void calcularCostoDe_TodosLosEmpleados(){
            double costoTotal=0;
            for_each(auto &vec:empleados){
                costoTotal+=vec.get_MontoTotal();
            }
            cout<<"el costo Total por todos los empleados es: "<<costoTotal;
        }

        //c.
        void LosMasantiguosPorSalario(){
            sort(empleados.begin(),empleados.end(),[](empleado &a,empleado &b){
                return a.getMontoAntiguedad()>b.getMontoAntiguedad();
            })

            //obtenemos los de mas antiguedad
            vector<empleado>aux;
            aux.push_back(empleados[0])
            aux.push_back(empleados[1])
            aux.push_back(empleados[2])
            aux.push_back(empleados[3])
            aux.push_back(empleados[4])

              sort(aux.begin(),aux.end(),[](empleado &a,empleado &b){
                return a.get_MontoTotal()>b.get_MontoTotal();
            })

            cout<<"los mas antiguos ordenados por sueldos"<<endl;
            for(int i=0;i<5;i++){
                cout<<aux[i].get_nombre()<<endl;
            }
        };




    


    
}