#include <iostream>
#include <climits>
const int PMAX = 20;   //tamaño area datos
const int OVER = PMAX + 1; //inicio del overflow
const int OMAX = 30;  //fin del overflow
const int n = 4;    //cantidad de datos por bloque
const int TAM_TAB_IND =5;   //tamaño tabla indices
using namespace std;


//estructura para datos
struct dato {
	int clave;
	int valor;
	dato* dir;  
};

//estructura para indices
struct indice {
	int clave;
	dato* dir;  
};

//variables para todo
dato TablaDatos[OMAX];      
indice TablaIndices[TAM_TAB_IND];   

//funciones
int EspacioOcupado(int num_bloque); //devuelve el espacio ocupado en un bloque
int EspacioLibre(int num_bloque); //devuelve el espacio libre en un bloque
int BlokeLibre(); //encuentra el primer bloque libre
bool Blokes_no_libres(); //verifica si no hay bloques disponibles
bool buscar_rango(int num_bloque, int clave); //verifica rango en un bloque
void enviar_al_overflow(int clave, int valor); //manda al overflow
void ordenar(int num_bloque); //ordena tabla datos
void Ordenar_Tabla_Indice(); //ordena tabla indices
int determinar_bloque_destino(int clave); //determina en que bloque debe ir cada clave
bool debe_generar_bloque_nuevo(int bloque, int clave); //verifica si hay que generar un bloque nuevo
bool debe_enviar_overflow(int bloque); //verifica si hay que enviar al overflow
void mostrarEstado(); //muestra las tablas con los datos
int calcularProximidad(int bloque, int clave); //devuelve cual es la clave mas proxima para ayudar a determinar donde hacer la insercion
bool seriaClaveIntermedia(int num_bloque,int clave); //verifica si la clave es intermedia
int consultarClave(int clave); //permite buscar el valor ingresando una clave
void insertar (dato a); //para insertar los datos en las tablas
//----------------------------------------------//

void insertar(dato a) {
	int pos_bloque;
	int espacio_ocupado;
	int espacio_libre;
	bool rango_valido;
	
	// primer insercion
	if (TablaIndices[0].clave == 0) {
		TablaDatos[0].clave = a.clave;
		TablaDatos[0].valor = a.valor;
		TablaDatos[0].dir = nullptr;
		TablaIndices[0].clave = TablaDatos[0].clave;
		TablaIndices[0].dir = &TablaDatos[0];
		return;
	}
	
	int bloque_destino = determinar_bloque_destino(a.clave); //a donde va la clave
	
	// si genera nuevo bloque entra aca
	if (debe_generar_bloque_nuevo(bloque_destino, a.clave)) {
		if (!Blokes_no_libres()) {
			pos_bloque = BlokeLibre();
			
			//insertar en nuevo bloke, actualizar tabla indices y ordenar
			TablaDatos[pos_bloque*n].clave = a.clave;
			TablaDatos[pos_bloque*n].valor = a.valor;
			TablaDatos[pos_bloque*n].dir = nullptr;
			TablaIndices[pos_bloque].clave = TablaDatos[pos_bloque*n].clave;
			TablaIndices[pos_bloque].dir = &TablaDatos[pos_bloque*n];
			Ordenar_Tabla_Indice();
			return;
		} else {
			cout <<endl<< "No se puede generar un bloque nuevo" << endl;
			return;
		}
	}
	
	//verificar si hay espacio, si hay insertar y ordenar
	espacio_ocupado = EspacioOcupado(bloque_destino);
	espacio_libre = EspacioLibre(bloque_destino);
	rango_valido = buscar_rango(bloque_destino, a.clave);
	if (espacio_libre > 0 && rango_valido) {
		int pos_insert = bloque_destino * n + espacio_ocupado;
		TablaDatos[pos_insert].clave = a.clave;
		TablaDatos[pos_insert].valor = a.valor;
		TablaDatos[pos_insert].dir = nullptr;
		ordenar(bloque_destino);

		// actualizar, si corresponde, tabla de indices
		if (a.clave < TablaIndices[bloque_destino].clave) {
			TablaIndices[bloque_destino].clave = TablaDatos[bloque_destino*n].clave;
			TablaIndices[bloque_destino].dir = &TablaDatos[bloque_destino*n];
		}
		Ordenar_Tabla_Indice();
		return;
	}
	
	// No hay lugar en el bloque, no se puede generar bloque nuevo, mandar overflow
	if (debe_enviar_overflow(bloque_destino)) {
		enviar_al_overflow(a.clave, a.valor);
		if (espacio_libre == 0) {
			TablaDatos[bloque_destino*n + 3].dir = &TablaDatos[PMAX];
		}
	} else {
		int inicio_bloque = bloque_destino * n;
		int pos_insert = inicio_bloque;
		while ((pos_insert > inicio_bloque + n &&
			   TablaDatos[pos_insert].clave > a.clave &&
			   TablaDatos[pos_insert].clave != 0)) {
			pos_insert++;
		}

		for (int i = inicio_bloque + n - 1; i > pos_insert; i--) {
			TablaDatos[i] = TablaDatos[i-1];
		}
		
		enviar_al_overflow(a.clave, a.valor);
		
		TablaDatos[inicio_bloque + n - 1].dir = &TablaDatos[PMAX];
		
		if (pos_insert == inicio_bloque) {
			TablaIndices[bloque_destino].clave = TablaDatos[inicio_bloque].clave;
			TablaIndices[bloque_destino].dir = &TablaDatos[inicio_bloque];
		}

		Ordenar_Tabla_Indice();
	}
}

//------------------------------//
bool debe_enviar_overflow(int bloque) {
	int ocupados = EspacioOcupado(bloque);
	return (ocupados < n / 2);
}
//-----------------------------//
bool seriaClaveIntermedia(int num_bloque, int clave) {
	if (num_bloque < 0 || num_bloque >= TAM_TAB_IND || TablaIndices[num_bloque].clave == 0) {
		return false;
	}
	
	int primera_clave = TablaIndices[num_bloque].clave;
	int ultima_clave = primera_clave;
	int inicio_bloque = num_bloque * n;
	
	for (int i = 0; i < n; i++) {
		if (TablaDatos[inicio_bloque + i].clave > ultima_clave) {
			ultima_clave = TablaDatos[inicio_bloque + i].clave;
		}
	}
	
	return (clave > primera_clave) && (clave < ultima_clave);
}
// -------------------//hasta aca angela
bool debe_generar_bloque_nuevo(int bloque, int clave) {
	int primera_clave = TablaIndices[bloque].clave;
	int ultima_clave;
	for (int i=0;i<4;i++){
		if(TablaDatos[i].clave!=0){
			ultima_clave=TablaDatos[i].clave;
		}
	}
	
	if ((clave < primera_clave)||(clave > ultima_clave)) {
		int ocupados = EspacioOcupado(bloque);
		if ((ocupados >= n / 2)&&(!seriaClaveIntermedia(bloque,clave))) {
			return true;
		}
	}
	return false;
}

// --------------------------//
int calcularProximidad(int bloque, int clave) {
	if (TablaIndices[bloque].clave == 0) return INT_MAX; 
	
	int inicio = bloque * n;
	int primera = TablaIndices[bloque].clave;
	int ultima = primera;
	
	for (int i = 0; i < n; i++) {
		if (TablaDatos[inicio+i].clave > ultima) {
			ultima = TablaDatos[inicio+i].clave;
		}
	}
	
	if (clave >= primera && clave <= ultima) {
		return 0; 
	} else if (clave < primera) {
		return primera - clave;
	} else {
		return clave - ultima;
	}
}

int determinar_bloque_destino(int clave) {
	// un bloque con datos
	if (TablaIndices[1].clave == 0) {
		return 0;
	}
	
	int bloque_cercano = 0;
	int menor_distancia = INT_MAX;
	for (int i = 0; i < TAM_TAB_IND && TablaIndices[i].clave != 0; i++) {
		int distancia = calcularProximidad(i, clave);
		if (distancia < menor_distancia) {
			menor_distancia = distancia;
			bloque_cercano = i;
		}
	}
	
	// esta dentro del rango
	if (menor_distancia == 0) {
		return bloque_cercano;
	}
	
	// menor que el primero
	if (bloque_cercano == 0 && clave < TablaIndices[0].clave) {
		return 0;
	}
	
	//mayor que el ultimo
	int ultimo_bloque = 0;
	while (ultimo_bloque < TAM_TAB_IND-1 && TablaIndices[ultimo_bloque+1].clave != 0) {
		ultimo_bloque++;
	}
	
	if (bloque_cercano == ultimo_bloque && clave > TablaDatos[ultimo_bloque*n + n-1].clave) {
		return ultimo_bloque;
	}
	
	// si genera nuevo bloque
	if (menor_distancia > 0 && debe_generar_bloque_nuevo(bloque_cercano, clave) && !Blokes_no_libres()) {
		return -1; 
	}
	return bloque_cercano;
}
//------------------------//
int EspacioOcupado(int num_bloque) {
	int inicio_bloque = num_bloque * n;
	int contador = 0;
	
	for (int i = 0; i < n; i++) {
		if (TablaDatos[inicio_bloque+i].clave != 0) {
			contador++;
		}
	}
	return contador;
}
//--------------------------//
int EspacioLibre(int num_bloque) {
	return n - EspacioOcupado(num_bloque);
}
//--------------------------//
int BlokeLibre() {
	for (int i = 0; i < TAM_TAB_IND; i++) {
		if (EspacioOcupado(i) == 0) { 
			return i;
		}
	}
	return -1; 
}
//-------------------//
bool Blokes_no_libres() {
	return (BlokeLibre() == -1);
}
//-------------------//
bool buscar_rango(int num_bloque, int clave) {
	if (TablaIndices[num_bloque].clave == 0){
		return true;
	}
	int primera_clave = TablaIndices[num_bloque].clave;
	int ultima_clave = primera_clave;
	
	// busca ultima clave
	int inicio_bloque = num_bloque * n;
	for (int i = 0; i < n; i++) {
		if (TablaDatos[inicio_bloque + i].clave != 0 &&
			TablaDatos[inicio_bloque + i].clave > ultima_clave) {
			ultima_clave = TablaDatos[inicio_bloque + i].clave;
		}
	}
	
	// dentro del rango
	if ((clave >= primera_clave)||(clave <= ultima_clave)) {
		return true;
	}
	
	// mayor que el ultimo y hay lugar
	if (clave > ultima_clave) {
		return (EspacioLibre(num_bloque) > 0);
	}
	
	return false;
}
//-------------------------------// hasta aca nico
void enviar_al_overflow(int clave, int valor) {
	for (int i = PMAX; i < OMAX; i++) {
		if (TablaDatos[i].clave == 0) { 
			TablaDatos[i].clave = clave;
			TablaDatos[i].valor = valor;
			TablaDatos[i].dir = nullptr;
			cout << "Dato enviado a overflow: [" << clave << "," << valor << "]" << endl;
			return;
		}
	}
	// no hay lugar en el overflow
	cout << "Overflow lleno. No se pudo insertar: [" << clave << "," << valor << "]" << endl;
}
//------------------------//
void ordenar(int num_bloque) {
	int inicio_bloque = num_bloque * n;
	bool intercambio;
	
	do {
		intercambio = false;
		for (int i = inicio_bloque; i < inicio_bloque + n - 1; i++) {
			if (TablaDatos[i].clave == 0) continue; 
			
			if (TablaDatos[i+1].clave != 0 && TablaDatos[i].clave > TablaDatos[i+1].clave) {
				// Intercambiar registros
				dato temp = TablaDatos[i];
				TablaDatos[i] = TablaDatos[i+1];
				TablaDatos[i+1] = temp;
				intercambio = true;
			}
		}
	} while (intercambio);
}
//----------------//
void Ordenar_Tabla_Indice() {
	bool intercambio;
	
	do {
		intercambio = false;
		for (int i = 0; i < TAM_TAB_IND - 1; i++) {
			if (TablaIndices[i].clave == 0) continue; 
			
			if (TablaIndices[i+1].clave != 0 && TablaIndices[i].clave > TablaIndices[i+1].clave) {
				// Intercambiar índices
				indice temp = TablaIndices[i];
				TablaIndices[i] = TablaIndices[i+1];
				TablaIndices[i+1] = temp;
				intercambio = true;
			}
		}
	} while (intercambio);
}
//--------------//
void mostrarEstado() {
	cout << "\n=== TABLA DE INDICES ===" << endl;
	for (int i = 0; i < TAM_TAB_IND; i++) {
		cout << "Indice " << i << ": ";
		if (TablaIndices[i].clave != 0) {
			cout << "Clave=" << TablaIndices[i].clave
				<< ", Dir=" << TablaIndices[i].dir;
		} else {
			cout << "Vacio";
		}
		cout << endl;
	}
	
	cout << "\n=== AREA PRIMARIA ===" << endl;
	for (int i = 0; i < TAM_TAB_IND * n; i++) {
		if (i % n == 0) {
			cout << "\nBloque " << i/n << ": ";
		}
		if (TablaDatos[i].clave != 0) {
			cout << "[" << TablaDatos[i].clave << "," << TablaDatos[i].valor << "] ";
			if (TablaDatos[i].dir != nullptr) {
				cout << "->overflow posición: 20";
			}
		} else {
			cout << "[Vacio] ";
		}
	}
	
	cout << "\n\n=== AREA DE OVERFLOW ===" << endl;
	for (int i = PMAX; i < OMAX; i++) {
		if (i % 5 == 0) cout << "\n"; 
		if (TablaDatos[i].clave != 0) {
			cout << "[" << TablaDatos[i].clave << "," << TablaDatos[i].valor << "] ";
		} else {
			cout << "[Vacio] ";
		}
	}
	cout << endl;
}
//-------------------------//
int consultarClave(int clave) {
	for (int bloque = 0; bloque < TAM_TAB_IND; bloque++) {
		if (TablaIndices[bloque].clave == 0) continue; 
		
		int inicio_bloque = bloque * n;
		for (int i = 0; i < n; i++) {
			int pos = inicio_bloque + i;
			if (TablaDatos[pos].clave == clave) {
				return TablaDatos[pos].valor; 
			}
			if (TablaDatos[pos].clave == 0) break; 
		}
		int ultima_pos = inicio_bloque + n - 1;
		if (TablaDatos[ultima_pos].dir != nullptr) {
			dato* overflow_ptr = TablaDatos[ultima_pos].dir;
			int overflow_index = overflow_ptr - TablaDatos; 
			for (int i = overflow_index; i < OMAX; i++) {
				if (TablaDatos[i].clave == clave) {
					cout<<"encontrado en el overflow"<<endl;
					return TablaDatos[i].valor;
				}
				if (TablaDatos[i].clave == 0) break;
			}
		}
	}
	for (int i = PMAX; i < OMAX; i++) {
		if (TablaDatos[i].clave == clave) {
			return TablaDatos[i].valor;
		}
	}
	cout << "Dato no encontrado" << endl;
	return -1; 
}
//----------MAIN------//
int main() {
//inicializacion
	for (int i = 0; i < OMAX; i++) {
		TablaDatos[i].clave = 0;
		TablaDatos[i].valor = 0;
		TablaDatos[i].dir = nullptr;
	}
	for (int i = 0; i < TAM_TAB_IND; i++) {
		TablaIndices[i].clave = 0;
		TablaIndices[i].dir = nullptr;
	}
//valores de prueba
	dato d1 = {10, 100, nullptr};
	insertar(d1);
	mostrarEstado();

	dato d2 = {5, 50, nullptr};
	insertar(d2);
	mostrarEstado();

	dato d3 = {15, 150, nullptr};
	insertar(d3);
	mostrarEstado();
	
	dato d6 = {12, 120, nullptr};
	insertar(d6);
	mostrarEstado();
	
	dato d7 = {17, 121, nullptr};
	insertar(d7);
	mostrarEstado();
	
	dato d8 = {3, 122, nullptr};
	insertar(d8);
	mostrarEstado();
	
	dato d82 = {13, 122, nullptr};
	insertar(d82);
	mostrarEstado();
	
	dato d9 = {29, 123, nullptr};
	insertar(d9);
	mostrarEstado();
	
	dato d10 = {120, 124, nullptr};
	insertar(d10);
	mostrarEstado();
	
	dato d11 = {40, 125, nullptr};
	insertar(d11);
	mostrarEstado();
	
	dato d12 = {50, 126, nullptr};
	insertar(d12);
	mostrarEstado();
	
	dato d13 = {119, 127, nullptr};
	insertar(d13);
	mostrarEstado();
	
	int buscado;
	cout<<"Buscar valor de clave: (si desea salir ingrese 0)"<<endl;
	cin>>buscado;
	while(buscado!=0){
	int valor = consultarClave(buscado);
	if (valor != -1) {
		cout << "Valor encontrado: " << valor << endl;
	}
	cout<<"Buscar valor de clave: (si desea salir ingrese 0)"<<endl;
	cin>>buscado;
	}
	return 0;

}
