#include <iostream>
#include <fstream>
#include <string>

using namespace std;

string def(string palabra,string caracter,string definicion){
	
	fstream archi;
	archi.open("./Datos.txt", ios::in | ios::out);
	if(archi.fail()){
		cout<<"Error";
		exit(1);
	}
	
	while(getline(archi,caracter)){
		int j=palabra.size();
		if(caracter.substr(0,j)==palabra){
			definicion=caracter.substr(j+1);
		}
	}
	archi.close();
	return definicion;
}
	

int main(){
	string palabra,caracter,resultado;
	
	cout<<"palabra: ";
	getline(cin,palabra);
	
	string definicion="Error";
	
	resultado=def(palabra,caracter,definicion);
	
	cout<<endl<<"La definicion es: "<< resultado;
	
	return 0;
}
	
