---
id: 6600
title: 'Problema con un esercizio. Errore di compilazione&#8230;'
date: 2016-08-24T18:31:35+02:00
author: Kevin De Donato
layout: revision
guid: http://www.italiancpp.org/2016/08/24/6593-revision-v1/
permalink: /2016/08/24/6593-revision-v1/
---
Salve come mai questo codice mi da il seguente errore di compilazione:  
La variabile y non è stata dichiarata.  
si riscontra l&#8217;errore nella prima riga della seconda definizione della funzione membro.  
Come mai? la variabile y non è stata gia dichiarata all&#8217;interno della classe? Perchè per la prima definizione di funzione non da problemi e per la seconda si?  
[cce_cpp]#include <iostream>

using namespace std;  
class dayType  
{  
public:  
int Getday();  
void Get\_Prox\_and\_Prec\_Day();  
dayType();  
private:  
string x;  
int y;

};  
int main()  
{  
dayType Day;  
Day.Getday();  
Day.Get\_Prox\_and\_Prec\_Day();  
return 0;  
}

dayType::dayType()  
{  
x = &#8221; &#8220;;  
y = 0;  
}  
int dayType::Getday()  
{  
cin >> x;  
if (x == &#8220;Lun&#8221;)  
{  
y = 1;  
cout << &#8220;Lunedi&#8221;;  
return y;  
}  
else  
if (x == &#8220;Mar&#8221;)  
{  
y = 2;  
cout << &#8220;Martedi&#8221;;  
return y;  
}  
else  
if (x == &#8220;Mer&#8221;)  
{  
y = 3;  
cout << &#8220;Mercoledi&#8221;;  
return y;  
}  
else  
if(x == &#8220;Gio&#8221;)  
{  
y = 4;  
cout << &#8220;Giovedi&#8221;;  
return y;  
}  
else  
if (x == &#8220;Ven&#8221;)  
{  
y = 5;  
cout << &#8220;Venerdi&#8221;;  
return y;  
}  
else  
if (x == &#8220;Sab&#8221;)  
{  
y = 6;  
cout << &#8220;Sabato&#8221;;  
return y;  
}  
else  
{  
y = 7;  
cout << &#8220;Domenica&#8221;;  
return y;  
}  
}  
void Get\_Prox\_and\_Prec\_Day()  
{

y = y + 1;  
if (y > 7)  
y = 1;  
switch (y)  
case 1:  
cout << &#8220;Il giorno successivo e&#8217; Lunedi&#8221;;  
case 2:  
cout << &#8220;Il giorno successivo e&#8217; Martedi&#8221;;  
case 3:  
cout << &#8220;Il giorno successivo e&#8217; Mercoledi&#8221;;  
case 4:  
cout << &#8220;Il giorno successivo e&#8217; Giovedi&#8221;;  
case 5:  
cout << &#8220;Il giorno successivo e&#8217; Venerdi&#8221;;  
case 6:  
cout << &#8220;Il giorno successivo e&#8217; Sabato&#8221;;

case 7:  
cout << &#8220;Il giorno successivo e&#8217; Domenica&#8221;;  
y = y &#8211; 2  
if (y < 1)  
y == 7;  
switch (y)  
case 1:  
cout << &#8220;Il giorno Precedente e&#8217; Lunedi&#8221;;

case 2:  
cout << &#8220;Il giorno Precedente e&#8217; Martedi&#8221;;  
case 3:  
cout << &#8220;Il giorno Precedente e&#8217; Mercoledi&#8221;;  
case 4:  
cout << &#8220;Il giorno Precedente e&#8217; Giovedi&#8221;;  
case 5:  
cout << &#8220;Il giorno Precedente e&#8217; Venerdi&#8221;;  
case 6:  
cout << &#8220;Il giorno Precedente e&#8217; Sabato&#8221;;  
case 7:  
cout << &#8220;Il giorno Precedente e&#8217; Domenica&#8221;;

}  
}[/cce_cpp]