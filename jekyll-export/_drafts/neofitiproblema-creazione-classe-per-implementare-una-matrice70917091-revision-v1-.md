---
id: 7092
date: 2016-11-23T12:52:38+01:00
author: Lorenzo
layout: revision
guid: http://www.italiancpp.org/2016/11/23/7091-revision-v1/
permalink: /2016/11/23/7091-revision-v1/
---
Ok, ho risolto e ora funziona! Ho anche aggiunto gli operatori di accesso al singolo elemento della matrice, così da renderla un po più bella e completa come classe.

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

///ACCESS OPERATORS  
int operator()(int,int) const;  
int& operator()(int,int);

///DESTRUCTOR  
virtual ~MyMatrix();

private:  
int _rows;  
int _columns;  
int _initValue;  
int *_matrixData;

};

#endif // MYMATRIX_H  
[/cce_cpp]

MyMatrix.cpp

[cce_cpp]  
#include &#8220;MyMatrix.h&#8221;

#include <iostream>

using namespace std;

///CONSTRUCTOR  
MyMatrix::MyMatrix(int r,int c):  
\_rows(r),\_columns(c)  
{  
_matrixData= new int[r*c];  
}

///DESTRUCTOR  
MyMatrix::~MyMatrix()  
{  
delete [] _matrixData;  
}

///SETTERS  
void MyMatrix::setRow(int r)  
{  
if(r>0)  
_rows=r;  
else  
cerr<<&#8220;ERROR: negative value&#8221;<<endl;  
}

void MyMatrix::setColumn(int c)  
{  
if(c>0)  
_columns=c;  
else  
cerr<<&#8220;ERROR: negative value&#8221;<<endl;  
}

void MyMatrix::setInitValue(int init)  
{  
_initValue=init;  
}

///GETTERS  
int MyMatrix::getRow()  
{  
return _rows;  
}

int MyMatrix::getColumn()  
{  
return _columns;  
}

int MyMatrix::getInitValue()  
{  
return _initValue;  
}

///MEMBER FUNCTIONS  
void MyMatrix::initializeMatrix()  
{  
for(int i=0;i<getRow();i++)  
{  
for(int j=0;j<getColumn();j++)  
_matrixData[i*getColumn()+j]=getInitValue();  
}  
}

void MyMatrix::printMatrix()  
{  
for(int i=0;i<getRow();i++)  
{  
cout<<&#8216;\n&#8217;;  
for(int j=0;j<getColumn();j++)  
cout<<_matrixData[i*getColumn()+j]<<&#8216; &#8216;;  
}  
}

///ACCESS OPERATORS  
int MyMatrix::operator()(int r,int c) const  
{  
return \_matrixData[r*\_columns+c];  
}

int& MyMatrix::operator()(int r,int c)  
{  
return \_matrixData[r*\_columns+c];  
}  
[/cce_cpp]

main.cpp

[cce_cpp]  
#include <iostream>  
#include <fstream>  
#include <stdlib.h>  
#include <string>  
#include &#8220;MyMatrix.h&#8221;

using namespace std;

int main()  
{  
int row=0;  
int column=0;  
ifstream inputFile;  
string fileName;  
string line;

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
MyMatrix m(row,column);  
m.setInitValue(2);  
m.initializeMatrix();

cout<<&#8220;\nColonne : &#8220;<<m.getColumn()<<&#8220;\nRighe : &#8220;<<m.getRow()<<&#8220;\nValore di inizializzazione : &#8220;<<m.getInitValue();  
m(1,2)=4;  
cout<<&#8220;\nm(2,3) = &#8220;<<m(1,2);  
cout<<&#8220;\n\n\n&#8221;;  
m.printMatrix();  
return 0;  
}  
[/cce_cpp]