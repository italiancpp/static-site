---
id: 7089
date: 2016-11-22T16:56:09+01:00
author: Lorenzo
layout: revision
guid: http://www.italiancpp.org/2016/11/22/7088-revision-v1/
permalink: /2016/11/22/7088-revision-v1/
---
Io la condivido ma non è programmazione super avanzata quindi non so quanto possa servire, ma sono pro alla condivisione &#x1f642;  
MyMatrix.h  
[cce_cpp]  
#ifndef MYMATRIX_H  
#define MYMATRIX_H

#include <string>

using namespace std;

class MyMatrix  
{  
public:  
///CONSTRUCTOR  
MyMatrix(int,int);

///SETTERS  
void setRow(int);  
void setColumn(int);  
void setInitValue(int);

///GETTERS  
int getRow();  
int getColumn();  
int getInitValue();

///MEMBER FUNCTIONS  
void initializeMatrix();  
void printMatrix();

///DESTRUCTOR  
virtual ~MyMatrix();

private:  
int _row;  
int _column;  
int _initValue;  
int *_matrix;  
};

#endif // MYMATRIX_H  
[/cce_cpp]  
MyMatrix.cpp  
[cce_cpp]  
#include &#8220;MyMatrix.h&#8221;  
#include <iostream>

using namespace std;

MyMatrix::MyMatrix(int r,int c)  
{  
_matrix= new int[r*c];  
this->_row=r;  
this->_column=c;

}

MyMatrix::~MyMatrix()  
{  
//dtor  
}

void MyMatrix::setRow(int r)  
{  
if(r>0)  
_row=r;  
else  
cerr<<&#8220;ERROR: negative value&#8221;<<endl;  
}  
int MyMatrix::getRow()  
{  
return _row;  
}

void MyMatrix::setColumn(int c)  
{  
if(c>0)  
_column=c;  
else  
cerr<<&#8220;ERROR: negative value&#8221;<<endl;  
}

int MyMatrix::getColumn()  
{  
return _column;  
}

void MyMatrix::setInitValue(int init)  
{  
_initValue=init;  
}

int MyMatrix::getInitValue()  
{  
return _initValue;  
}

void MyMatrix::initializeMatrix()  
{  
for(int i=0;i<getRow();i++)  
{  
for(int j=0;j<getColumn();j++)  
_matrix[i*getColumn()+j]=getInitValue();  
}  
}

void MyMatrix::printMatrix()  
{  
for(int i=0;i<getRow();i++)  
{  
cout<<&#8216;\n&#8217;;  
for(int j=0;j<getColumn();j++)  
cout<<_matrix[i*getColumn()+j]<<&#8216; &#8216;;  
}  
}  
[/cce_cpp]

Ora avrei anche una piccola domanda da porvi, ho provato a scrivere nel main una serie di istruzioni per creare una matrice a partire da dei dati in un file di testo e dopo avergli inserito il nome del file l&#8217;esecuzione si interrompe dicendomi che l&#8217;eseguibile ha smesso di funzionare.  
Vi posto il mio main  
main.cpp  
[cce_cpp]  
#include <iostream>  
#include <vector>  
#include <fstream>  
#include <stdlib.h>  
#include <string>  
#include &#8220;MyMatrix.h&#8221;

using namespace std;

int main()  
{  
int row=0;  
int column=0;  
MyMatrix m(1,1);  
m.setInitValue(0);  
ifstream inputFile;  
string fileName;  
string line;  
vector<string>::iterator it;

cout<<&#8220;Enter file name :&#8221;<<endl;  
cin>>fileName;

inputFile.open(fileName.c_str());  
while(inputFile.good())  
{  
getline(inputFile,line);  
if(line.compare(0,6,&#8221;INPUTS&#8221;)==0)  
{  
column=atoi(line.substr(7,&#8217;\n&#8217;).c_str());  
}  
if(line.compare(0,7,&#8221;OUTPUTS&#8221;)==0)  
{  
row=atoi(line.substr(8,&#8217;\n&#8217;).c_str());  
}  
if(line.compare(0,4,&#8221;NETS&#8221;)==0)  
{  
row+=atoi(line.substr(5,&#8217;\n&#8217;).c_str());  
column+=atoi(line.substr(5,&#8217;\n&#8217;).c_str());  
}  
}

m.setRow(row);  
m.setColumn(column);  
//m.initializeMatrix();

cout<<&#8220;\nColonne : &#8220;<<m.getColumn()<<&#8220;\nRighe : &#8220;<<m.getRow()<<&#8220;\nValore di inizializzazione : &#8220;<<m.getInitValue();  
m.printMatrix();

return 0;  
}  
[/cce_cpp]  
Nel codice del main ho commentato la funzione initializeMatrix perchè ho scoperto che quando viene invocata il programma si arresta con un errore ma non ho capito di che errore si tratta&#8230;.penso che sto provando ad accedere in modo sbagliato allo spazio di memoria riservato alla matrice e quindi non mi fa salvare il dato di inizializzazione in tutti gli elementi della matrice&#8230;.quindi come posso fare?