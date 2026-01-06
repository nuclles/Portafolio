#include <iostream>
#include <vector>
#include <cstring>
#include <fstream>
#include <map>
#include <algorithm>

using namespace std;
//1
struct S_producto {
    int numero;
    char desc[200];
    float precio;
    char tipo; // 'P' para parte, 'B' para bicicleta
    int id_bicicleta; // nuevo campo para relacionar partes con bicicletas
};


class producto{
    public:
    int numero;
    char desc[200];
    float precio;
    char tipo;

   S_producto getDatos() {
    S_producto aux;
    aux.numero = this->numero;
    strcpy(aux.desc, this->desc);
    aux.precio = this->precio;
    aux.tipo = this->tipo;
    aux.id_bicicleta = 0; // valor por defecto, solo para partes será relevante
    return aux;
}
    char getTipo(){return tipo;}


    virtual float calcularPrecio()=0;
    float getPrecio(){ return precio; }
};

//*************************************************************************//

 class parte:public producto{
    private:
    char tipo ='P';

    public:

    parte(int numero, const char* desc, float precio){
        this->numero=numero;
        strcpy(this->desc,desc);
        this->precio=precio;
}

    float  calcularPrecio(){
        return this->precio;
    }
 };

 class bicicleta:public producto{
    private:
    char tipo ='B';
    vector<parte>partes;
    public:

    bicicleta(int numero, const char* desc, float precio, vector<parte> partes_){
        this->numero=numero;
        strcpy(this->desc,desc);
        this->precio=precio;
        this->partes.reserve(partes_.size());
        // Copiamos las partes al vector de la bicicleta
        std::copy(partes_.begin(), partes_.end(), std::back_inserter(partes));
    }


    int getComponentes(){
        int a=sizeof(partes);
        return a;
    }

    vector<parte>getPartes(){
        return partes;
                    }


    float calcularPrecio(){
        
        for (auto &part:partes){
            this->precio+=part.getPrecio();
        }
    }
 };

 class oferta{
    private:
    vector<producto*>productos_ofertas;
    float precio;
    int numero;
    char desc[200];
    friend ostream& operador<<(ofstream& os, const oferta& O);

    public:
    oferta(int numero, const char* desc,vector<producto>productos_ofertas_){
        this->numero = numero;
        strcpy(this->desc, desc);
        this->productos_ofertas.reserve(productos_ofertas_.size());
        // Copiamos los productos de la oferta al vector de la oferta
        std::copy(productos_ofertas_.begin(), productos_ofertas_.end(), std::back_inserter(productos_ofertas));
        this->precio = 0.0f; // Inicializamos el precio a 0
        }

        //sobrecarga del operador "<<"
        ostream& operador<<(ostream& os, /*const*/ oferta& O){// si hago "const oferta& O" no puedo precalcular el precio total con "calcularPrecio()" 
            calcularPrecio();
            os<<"productos: ";
            for(auto &prod:o.getProductos_ofertas()){// puedo hacer "for(auto &prod:o.Productos_ofertas)" solo si el << es "friend" de la clase
                os<<prod.getNombre()", "// importante mostrar por pantalla usando "OS" no "cout"
            }
            os<<"precio total: "<<getPrecio();
            return os;
        }

        float getPrecio(){return this->precio;}

        void calcularPrecio(){
            for (auto &prod:productos_ofertas){
            this ->precio += prod->calcularPrecio();
            }
        }
    };
 

 //1) Si se puede utilizar polimorfismo ya que todas las clases van a compartir atributos en comun que son el precio la descripcion y el numero de identificacion
 // El polimorfismo nos ayuda a ahorrar codigo al momento de calcular los precios y devolver a informacion de cada producto.


 class bicicleteria{

    private:
    vector<producto*>productos;
    vector<bicicleta>bicis;
    vector<oferta>ofertas;

    // Estructura para almacenar los datos de los productos



    public:


    bicicleteria(){}
    //1Agregar productos
    void agregarProducto(){
        S_producto aux;
        cout << "Ingrese el numero del producto: ";
        cin >> aux.numero;
        cout << "Ingrese la descripcion del producto: ";
        cin.ignore();
        cin.getline(aux.desc, 200);
        cout << "Ingrese el precio del producto: ";
        cin >> aux.precio;
        cout << "Ingrese el tipo de producto (P para parte, B para bicicleta): ";
        cin >> aux.tipo;
        switch(aux.tipo){
            case 'P':{
                parte* nuevaParte = new parte(aux.numero, aux.desc, aux.precio);
                productos.push_back(nuevaParte);
                break;
            }
            case 'B':{
                vector<parte> partesAux;
                int numPartes;
                cout << "Ingrese el numero de partes de la bicicleta: ";
                cin >> numPartes;
                for(int i = 0; i < numPartes; i++){ 
                    S_producto parteAux;
                    cout << "Ingrese el numero de la parte: ";
                    cin >> parteAux.numero;
                    cout << "Ingrese la descripcion de la parte: ";
                    cin.ignore();
                    cin.getline(parteAux.desc, 200);
                    cout << "Ingrese el precio de la parte: ";
                    cin >> parteAux.precio;
                    partesAux.push_back(parte(parteAux.numero, parteAux.desc, parteAux.precio));
                }
                bicicleta* nuevaBici = new bicicleta(aux.numero, aux.desc, aux.precio, partesAux);
                productos.push_back(nuevaBici);
                break;
            }
            default:
                cout << "Tipo de producto no valido." << endl;
                return;
        }
        cout << "Producto agregado correctamente." << endl;
    }

    //2Guardar en binario
    //cada producto tiene su metodo para guardarce en un archivo aparte
    void guardarBinario(const char* direccionPartes, const char* direccionBicis){
        ofstream archivoPartes(direccionPartes, ios::binary);
        if(archivoPartes.fail()){
            cout << "Error al abrir el archivo de partes." << endl;
            exit(-1);
        }
        ofstream archivoBicis(direccionBicis, ios::binary);
        if(archivoBicis.fail()){
            cout << "Error al abrir el archivo de bicicletas." << endl;
            exit(-1);
        }
            for(auto &prod:productos){ 
                S_producto aux = prod->getDatos();

                if(prod->tipo == 'P'){
                    archivoPartes.write(reinterpret_cast<const char*>(&aux), sizeof(S_producto));
                }
                else if(prod->tipo == 'B'){
                    archivoBicis.write(reinterpret_cast<const char*>(&aux), sizeof(S_producto));

                    // Guardar las partes de la bicicleta en el archivo de partes
                    bicicleta* bici = dynamic_cast<bicicleta*>(prod);
                    if (bici) {
                        int idBici = bici->numero; // usa el numero como identificador
                        vector<parte> partesBici = bici->getPartes();
                        for (auto& parteBici : partesBici) {
                        S_producto parteAux = parteBici.getDatos();
                        parteAux.tipo = 'P'; // aseguramos el tipo
                        parteAux.id_bicicleta = idBici; // asigna ID a cada parte
                        archivoPartes.write(reinterpret_cast<const char*>(&parteAux), sizeof(S_producto));
                        }
                    }
                }
            }
    }
/*
    //leemos el archivo para generar el vector de bicis
     void leerArcBinario(const char*direccion){
        ifstream archivoBici(direccion,ios::binary);
        if(archivoBici.fail()){
            exit -1;
        }
        S_producto aux;
        while(!ArchDatos.eof()){
            ArchDatos.read(reinterpret_cast <char*>(&aux),sizeof(S_producto));
            this->bicis.push_back(new bicicleta(aux));
        }

        ArchDatos.close();
}*/

void generar_vec_bicis(){
    for(auto &prod:productos){
        if(prod.getTipo()=='B')
        bicis.push_back(prod);
    }
}



//3) Guardar en un archivo de texto
void guardarTXT(const string& dir) { // Usar string en lugar de const char*
    ofstream archivo(dir);
    if (!archivo) {
        cerr << "Error al abrir: " << dir << endl;
        return;
    }
    
    for(auto& ofer : ofertas) {
        archivo << ofer << '\n'; // '\n' en lugar de endl (más eficiente)
    }
    archivo.close();
}

    //4 STL
    //a
    void ordenarBici(){
           for(auto &bic:bicis){
            bic.calcularPrecio();
        }
        sort(bicis.begin(),bicis.end(),[](bicicleta &a,bicicleta &b){return a.getPrecio()>b.getPrecio();});

        for(int i=1;i<5;i++){
            cout << bicis[i].getNombre();
        }
    }

    //b
    void parteMasUtilizada(){
    map<string,int>contadorPartes;

    for(auto&bic :bicis){
        vector<bicicleta>bicisAux = bic.getPartes();
        for(auto& part :biciAux){
            contadorPermisos[part.getNombre()]++;
        }
    }

    vector<parte>partes_mas_usadas;
    for(auto& par:contadorPartes){
        if(par.second>1){
           partes_mas_usadas.push_back(par.first);
        }
    }
    cout << partes_mas_usadas[0].getNombre();}
    

    //c
    void bicicletaConMasComponentes(){
        sort(bicis.begin(),bicis.end(),[](bicicleta &a,bicicleta &b){return a.getComponentes()>b.getComponentes();});

        cout <<bicis[0].getNombre()<<endl;
    }

 }
