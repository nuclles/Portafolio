#include <iostream>


class nodo{
    private:
    string dato;
    nodo *link;

    public:
    nodo(string d) {
        this->dato=d;
        this->link =nullptr;
    }

    string getDato(){return dato;}
    nodo* getLink(){return link;}
    void setSiguiente(nodo* sig){link = sig;}
};

//---------------------------------------------------//-------------------------------------------------------//
//lista enlazada

class listaEnlazada{
    private:
    nodo* cabeza;

    public:
    listaEnlazada(){this->cabeza =nullptr;}
    
    void agregarAlInicio(string dato){
        nodo *nuevo = new nodo(dato);
        nuevo->setSiguiente(cabeza);
        cabeza =nuevo;
    }

    void imprimirLista(){
        nodo* actual = cabeza;
        while (actual != nullptr){
            cout<< actual->getDato()<<"->";
            actual = actual->getLink();
        }
        cout<< "null"<<endl;
    }

    ~listaEnlazada(){
        nodo* actual = cabeza;
        while (actual != nullptr){
            nodo* link = actual->getLink();
            delete actual;
            actual =link;
        }
    }

    vod agregarAlFinal(string dato){
        nodo* nuevo = new nodo(dato);
        if (cabeza == nullptr){
            cabeza = nuevo;
            return;
        }

        nodo* actual = cabeza;
        while (actual->getLink()!=nullptr){
            actual = actual->getLink();
        }
        actual->getLink(nuevo);
    }
};


//--------------------------------------------//------------------------------------------------//
//COLA
#include <iostream>
#include <string>
using namespace std;

class Cola {
private:
    nodo* frente;  // Primer elemento de la cola
    nodo* final;   // Último elemento de la cola

public:
    Cola() {
        frente = nullptr;
        final = nullptr;
    }

    // Verifica si la cola está vacía
    bool estaVacia() {
        return (frente == nullptr);
    }

    // Método para encolar (añadir al final)
    void encolar(string dato) {
        nodo* nuevoNodo = new nodo(dato);

        if (estaVacia()) {
            // Si la cola está vacía, el nuevo nodo es el frente y el final
            frente = nuevoNodo;
            final = nuevoNodo;
        } else {
            // Enlaza el nuevo nodo al final y actualiza el puntero 'final'
            final->setSiguiente(nuevoNodo);
            final = nuevoNodo;
        }
    }

    // Método para desencolar (eliminar el frente)
    string desencolar() {
        if (estaVacia()) {
            throw runtime_error("La cola está vacía");
        }

        nodo* temp = frente;
        string datoEliminado = temp->getDato();

        // Mueve 'frente' al siguiente nodo
        frente = frente->getLink();

        // Si la cola queda vacía, actualiza 'final' a nullptr
        if (frente == nullptr) {
            final = nullptr;
        }

        delete temp;  // Libera memoria del nodo eliminado
        return datoEliminado;
    }

    // Método para ver el dato del frente (sin eliminarlo)
    string verFrente() {
        if (estaVacia()) {
            throw runtime_error("La cola está vacía");
        }
        return frente->getDato();
    }

    // Destructor para liberar memoria
    ~Cola() {
        while (!estaVacia()) {
            desencolar();
        }
    }
};

//--------------------------------------------------//-----------------------------------------------------//
//PILA

#include <iostream>
#include <string>
#include <stdexcept>  // Para std::runtime_error
using namespace std;

class Pila {
private:
    nodo* tope;  // Puntero al nodo superior (último en entrar)

public:
    // Constructor
    Pila() : tope(nullptr) {}

    // Verifica si la pila está vacía
    bool estaVacia() {
        return (tope == nullptr);
    }

    // Apilar (push): Añade un elemento al tope
    void apilar(string dato) {
        nodo* nuevoNodo = new nodo(dato);
        nuevoNodo->setSiguiente(tope);  // El nuevo nodo apunta al tope actual
        tope = nuevoNodo;               // Actualiza el tope
    }

    // Desapilar (pop): Elimina y devuelve el elemento del tope
    string desapilar() {
        if (estaVacia()) {
            throw runtime_error("La pila está vacía");
        }
        nodo* temp = tope;
        string dato = temp->getDato();
        tope = tope->getLink();  // Mueve el tope al siguiente nodo
        delete temp;             // Libera memoria
        return dato;
    }

    // Ver tope (peek): Devuelve el elemento del tope sin eliminarlo
    string verTope() {
        if (estaVacia()) {
            throw runtime_error("La pila está vacía");
        }
        return tope->getDato();
    }

    // Destructor (libera toda la memoria al destruir la pila)
    ~Pila() {
        while (!estaVacia()) {
            desapilar();
        }
    }
};

//--------------------------------------------------//-----------------------------------------------------//
//ARBOL

//Primero, definamos la estructura del nodo:
#include <iostream>
using namespace std;

struct Nodo {
    int dato;
    Nodo* izquierdo;
    Nodo* derecho;
    
    // Constructor
    Nodo(int valor) : dato(valor), izquierdo(nullptr), derecho(nullptr) {}
};

//1. Insertar Elementos en el Árbol
Nodo* insertar(Nodo* raiz, int valor) {
    // Si el árbol está vacío, crea un nuevo nodo
    if (raiz == nullptr) {
        return new Nodo(valor);
    }
    
    // Si el valor es menor, inserta en el subárbol izquierdo
    if (valor < raiz->dato) {
        raiz->izquierdo = insertar(raiz->izquierdo, valor);
    }
    // Si el valor es mayor, inserta en el subárbol derecho
    else if (valor > raiz->dato) {
        raiz->derecho = insertar(raiz->derecho, valor);
    }
    
    // Si el valor ya existe, no hacemos nada
    return raiz;
}

//2. Para buscar un elemento:
bool buscar(Nodo* raiz, int valor) {
    // Si el árbol está vacío, el elemento no existe
    if (raiz == nullptr) {
        return false;
    }
    
    // Si encontramos el valor
    if (raiz->dato == valor) {
        return true;
    }
    
    // Si el valor es menor, buscamos en el subárbol izquierdo
    if (valor < raiz->dato) {
        return buscar(raiz->izquierdo, valor);
    }
    // Si el valor es mayor, buscamos en el subárbol derecho
    else {
        return buscar(raiz->derecho, valor);
    }
}

//3. La eliminación es más compleja porque hay varios casos:
Nodo* eliminar(Nodo* raiz, int valor) {
    // Caso base: árbol vacío
    if (raiz == nullptr) {
        return raiz;
    }
    
    // Buscar el valor a eliminar
    if (valor < raiz->dato) {
        raiz->izquierdo = eliminar(raiz->izquierdo, valor);
    } 
    else if (valor > raiz->dato) {
        raiz->derecho = eliminar(raiz->derecho, valor);
    }
    // Si encontramos el nodo a eliminar
    else {
        // Caso 1: Nodo con un solo hijo o sin hijos
        if (raiz->izquierdo == nullptr) {
            Nodo* temp = raiz->derecho;
            delete raiz;
            return temp;
        } 
        else if (raiz->derecho == nullptr) {
            Nodo* temp = raiz->izquierdo;
            delete raiz;
            return temp;
        }
        
        // Caso 2: Nodo con dos hijos
        // Encontrar el sucesor in-order (mínimo en el subárbol derecho)
        Nodo* temp = encontrarMinimo(raiz->derecho);
        
        // Copiar el dato del sucesor
        raiz->dato = temp->dato;
        
        // Eliminar el sucesor
        raiz->derecho = eliminar(raiz->derecho, temp->dato);
    }
    return raiz;
}

// Función auxiliar para encontrar el nodo con el valor mínimo
Nodo* encontrarMinimo(Nodo* nodo) {
    Nodo* actual = nodo;
    while (actual && actual->izquierdo != nullptr) {
        actual = actual->izquierdo;
    }
    return actual;
}

//4. Puedes cargar elementos de varias formas:
// Cargar elementos manualmente
Nodo* raiz = nullptr;
raiz = insertar(raiz, 50);
insertar(raiz, 30);
insertar(raiz, 20);
insertar(raiz, 40);
insertar(raiz, 70);
insertar(raiz, 60);
insertar(raiz, 80);

// O cargar desde un arreglo
int valores[] = {50, 30, 20, 40, 70, 60, 80};
int n = sizeof(valores) / sizeof(valores[0]);
Nodo* raiz = nullptr;
for (int i = 0; i < n; i++) {
    raiz = insertar(raiz, valores[i]);
}

//5. Función para Mostrar el Árbol (In-Order)
void inOrder(Nodo* raiz) {
    if (raiz != nullptr) {
        inOrder(raiz->izquierdo);
        cout << raiz->dato << " ";
        inOrder(raiz->derecho);
    }
}

// Uso:
inOrder(raiz);  // Mostrará los valores ordenados

