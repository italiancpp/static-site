---
id: 7080
title: Problema creazione classe per implementare una matrice
date: 2016-11-19T15:51:05+01:00
author: Lorenzo
layout: revision
guid: http://www.italiancpp.org/2016/11/19/7079-revision-v1/
permalink: /2016/11/19/7079-revision-v1/
---
Salve a tutti, ho provato a tirare giù del codice per produrre una classe che mi crei una matrice.  
Quando compilo non mi da nessun tipo di errore e warning, ma quando eseguo mi appare la finestra in cui mi dice che l&#8217;eseguibile ha smesso di funzionare.  
vi posto il codice:  
MyMatrix.h  
[cce_cpp]  
#ifndef MYMATRIX_H  
#define MYMATRIX_H

#include <string>  
#include <vector>

using namespace std;

class MyMatrix  
{  
public:  
///CONSTRUCTOR  
MyMatrix(int,int,int);

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
void printMatrix() const;

///DESTRUCTOR  
virtual ~MyMatrix();

private:  
int _row;  
int _column;  
int _initValue;  
vector< vector<int> > _matrix;  
};

#endif // MYMATRIX_H  
[/cce_cpp]

MyMatrix.cpp  
[cce_cpp]  
#include &#8220;MyMatrix.h&#8221;

#include <iostream>

using namespace std;

MyMatrix::MyMatrix(int r,int c,int init):  
\_row(r),\_column(c),_initValue(init)  
{  
initializeMatrix();  
}

MyMatrix::~MyMatrix()  
{  
//dtor  
}

void MyMatrix::setRow(int r)  
{  
_row=r;  
}  
int MyMatrix::getRow()  
{  
return _row;  
}

void MyMatrix::setColumn(int c)  
{  
_column=c;  
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
_matrix\[i\]\[j\]=getInitValue();  
}  
}

void MyMatrix::printMatrix() const  
{  
for(int i=0;i<_row;i++)  
{  
cout<<&#8216;\n&#8217;;  
for(int j=0;j<_column;j++)  
cout<<_matrix\[i\]\[j\]<<&#8216; &#8216;;  
}  
}  
[/cce_cpp]

main.cpp  
[cce_cpp]  
#include <iostream>  
#include &#8220;MyMatrix.h&#8221;  
#include <string>

using namespace std;

int main()  
{  
MyMatrix m(2,3,1);  
cout<<&#8220;Colonne matrice :&#8221;<<m.getColumn()<<&#8220;\n&#8221;;  
cout<<&#8220;Righe matrice :&#8221;<<m.getRow();  
m.printMatrix();  
return 0;  
}  
[/cce_cpp]

Non capisco dove stanno gli errori!  
Grazie &#x1f642;