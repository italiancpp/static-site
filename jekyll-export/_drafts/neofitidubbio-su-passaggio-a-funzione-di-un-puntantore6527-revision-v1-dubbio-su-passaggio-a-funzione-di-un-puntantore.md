---
id: 6528
title: dubbio su passaggio a funzione di un puntantore
date: 2016-08-08T20:13:03+02:00
author: ma
layout: revision
guid: http://www.italiancpp.org/2016/08/08/6527-revision-v1/
permalink: /2016/08/08/6527-revision-v1/
---
Ciao a tutti,  
spiego il mio problema:  
sto effettuando la lettura di un file binario(un assembly .net per intenderci), di cui ho il puntatore al primo byte del file e conosco gli offset dei dati che devo leggere, per la lettura sto utilizzando il seguente metodo  
[cce_cpp]  
std::string ReadString(char *pStart)  
{  
std::string str;  
while (*pStart != 0)  
{  
str.append(1, ((char)*pStart++));  
}

return str;  
}  
[/cce_cpp]  
che chiamo così:  
[cce_cpp]  
int offset = 100;  
string x = ReadString(fileLoaded->pStringsStream + offset);  
[/cce_cpp]  
Dove pStringStream è un puntatore (un char *) al primo byte del file.

Il tutto funge, ma&#8230; volevo provare a crearmi una classe che mi aiuti nella lettura, ed ho scritto la seguente classe:  
header  
[cce_cpp]  
class ByteReader  
{  
private:  
unsigned long long byteReadedCount;  
char * pByteStream;  
char * pBaseStream;

public:  
ByteReader(char * pBStream);  
~ByteReader();

//unsigned char GetCharAt(int i);  
std::string ReadStringFromByteIndex(int i);

};  
[/cce_cpp]

e la classe:  
[cce_cpp]

ByteReader::ByteReader(char * pBStream)  
{  
pByteStream = pBStream;  
// clono il puntantore per mantenere la posizione iniziale  
pBaseStream = new char(*pBStream);  
}

ByteReader::~ByteReader()  
{  
delete pBaseStream;  
}

std::string ByteReader::ReadStringFromByteIndex(int i)  
{  
char \* pStream = \*(pBaseStream + i);

std::string str;  
while (*pStream != 0)  
{  
str.append(1, ((char)*pStream++));  
}

return str;  
}  
[/cce_cpp]

esempio di chiamata  
[cce_cpp]  
ByteReader typeDefReader = ByteReader(fileLoaded->pStringsStream);  
string x = typeDefReader.ReadStringFromByteIndex(offset);

Ovviamente non funziona, e non capisco il perché.  
Il dubbio è che il pBaseStream non sia in realtà una copia del puntatore che inizialmente passo al costruttore. Oppure di sbagliare qualcosa nell&#8217;aritmetica dei puntatori.  
Qualche idea a riguardo?

Grazie  
Sergio